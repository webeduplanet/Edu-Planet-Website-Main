'use strict';
// Server-only. Credentials must be supplied through the hosting provider's secrets.
const {createSign, createHash} = require('node:crypto');
const MAX_BYTES = 4096;
const SCOPE = 'https://www.googleapis.com/auth/spreadsheets';
const TOKEN_URL = 'https://oauth2.googleapis.com/token';
const HEADER = ['Received at (UTC)', 'Name', 'Contact number', 'Email', 'Enquiry'];
function createHandler({env = process.env, fetchImpl = global.fetch, now = Date.now} = {}) {
  let token;
  const limits = new Map();
  const response = (status, body, origin) => ({status, headers: {
    'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff', 'Vary': 'Origin',
    ...(origin ? {'Access-Control-Allow-Origin': origin} : {})
  }, body});
  async function google(url, options) {
    return fetchImpl(url, {...options, signal: AbortSignal.timeout(7000)});
  }
  async function accessToken() {
    if (token && token.expiry > now() + 60000) return token.value;
    const credentials = JSON.parse(env.GOOGLE_SERVICE_ACCOUNT_JSON || '{}');
    if (credentials.type !== 'service_account' || !credentials.client_email || !credentials.private_key) throw new Error('configuration');
    const issued = Math.floor(now()/1000);
    const encode = value => Buffer.from(JSON.stringify(value)).toString('base64url');
    const unsigned = encode({alg: 'RS256', typ: 'JWT'}) + '.' + encode({
      iss: credentials.client_email, scope: SCOPE, aud: TOKEN_URL, iat: issued, exp: issued + 3600
    });
    const signature = createSign('RSA-SHA256').update(unsigned).sign(credentials.private_key, 'base64url');
    const result = await google(TOKEN_URL, {method: 'POST', headers: {'Content-Type':'application/x-www-form-urlencoded'},
      body: new URLSearchParams({grant_type:'urn:ietf:params:oauth:grant-type:jwt-bearer', assertion: unsigned+'.'+signature})});
    const data = await result.json();
    if (!result.ok || typeof data.access_token !== 'string' || !data.access_token) throw new Error('google');
    token = {value: data.access_token, expiry: now() + Math.min(Number(data.expires_in)||3600,3600)*1000};
    return token.value;
  }
  return async function handle({method, headers = {}, body, ip = 'unknown'}) {
    const origin = headers.origin;
    const allowed = (env.FEE_ENQUIRY_ALLOWED_ORIGINS || '').split(',').map(s=>s.trim()).filter(Boolean);
    if (!allowed.length) return response(503, {ok:false, error:'The enquiry connection is not configured yet.'});
    if (typeof origin !== 'string' || !allowed.includes(origin)) return response(403, {ok:false, error:'This website is not allowed.'});
    if (method === 'OPTIONS') {
      const result = response(204, null, origin);
      Object.assign(result.headers, {'Access-Control-Allow-Methods':'POST, OPTIONS', 'Access-Control-Allow-Headers':'Content-Type', 'Access-Control-Max-Age':'600'});
      return result;
    }
    if (method !== 'POST') return response(405, {ok:false, error:'Use the enquiry form.'}, origin);
    if (!String(headers['content-type'] || '').toLowerCase().startsWith('application/json')) return response(415, {ok:false, error:'Expected a JSON submission.'}, origin);
    let input;
    try {
      const raw = typeof body === 'string' ? body : JSON.stringify(body);
      if (!raw || Buffer.byteLength(raw) > MAX_BYTES) return response(413, {ok:false,error:'The submission is too large.'}, origin);
      input = JSON.parse(raw);
    } catch { return response(400, {ok:false,error:'Please check the form and try again.'}, origin); }
    if (!input || typeof input !== 'object' || Array.isArray(input)) return response(400, {ok:false,error:'Please check the form and try again.'}, origin);
    if (input.website) return response(400, {ok:false,error:'Please check the form and try again.'}, origin);
    const text = value => typeof value === 'string' ? value.trim() : '';
    const name = text(input.parentName), phone = text(input.contactNumber), email = text(input.email);
    const digits = phone.replace(/\D/g,'');
    if (!name || name.length>100 || /[\x00-\x1f\x7f]/.test(name) || phone.length>30 || /[\x00-\x1f\x7f]/.test(phone) || !/^[+()\d\s.-]+$/.test(phone) || digits.length<7 || digits.length>15 || email.length>254 || !/^[^\s@\x00-\x1f]+@[^\s@\x00-\x1f]+\.[^\s@\x00-\x1f]+$/.test(email)) {
      return response(400, {ok:false,error:'Enter your name, a valid contact number and email address.'}, origin);
    }
    const key = createHash('sha256').update(String(ip)).digest('hex');
    if (limits.size > 2000) for (const [k,v] of limits) if (v.until<=now()) limits.delete(k);
    const count = limits.get(key);
    if (count && count.until>now() && count.count>=10) return response(429, {ok:false,error:'Please wait a few minutes before trying again.'}, origin);
    limits.set(key, count && count.until>now() ? {...count,count:count.count+1} : {count:1,until:now()+600000});
    if (!/^[a-zA-Z0-9_-]{10,}$/.test(env.GOOGLE_SHEET_ID || '') || !env.GOOGLE_SERVICE_ACCOUNT_JSON) return response(503,{ok:false,error:'The enquiry connection is not configured yet.'},origin);
    try {
      const sheet = env.GOOGLE_SHEET_TAB || 'Fee enquiries';
      const range = "'" + sheet.replace(/'/g,"''") + "'!A:E";
      const base = 'https://sheets.googleapis.com/v4/spreadsheets/' + encodeURIComponent(env.GOOGLE_SHEET_ID) + '/values/' + encodeURIComponent(range);
      const bearer = await accessToken();
      const auth = {'Authorization':'Bearer '+bearer, 'Content-Type':'application/json'};
      // Fail before writing if the destination has the wrong columns.
      const check = await google(base.replace(encodeURIComponent(range),encodeURIComponent("'"+sheet.replace(/'/g,"''")+"'!A1:E1")), {headers:auth});
      const current = await check.json();
      if (!check.ok || JSON.stringify(current.values?.[0]) !== JSON.stringify(HEADER)) throw new Error('columns');
      const saved = await google(base+':append?valueInputOption=RAW&insertDataOption=INSERT_ROWS', {method:'POST',headers:auth, body:JSON.stringify({majorDimension:'ROWS', values:[[new Date(now()).toISOString(),name,phone,email,'2027 fees enquiry']]})});
      const data = await saved.json();
      if (!saved.ok || data.updates?.updatedRows !== 1 || data.updates?.updatedCells !== 5) throw new Error('save');
      return response(200, {ok:true}, origin);
    } catch {
      // Never log parent details, tokens, keys or upstream response bodies.
      return response(502, {ok:false,error:'We could not confirm your enquiry was saved. Please try again or contact the accounts office.'}, origin);
    }
  };
}
module.exports = {createHandler, HEADER};
