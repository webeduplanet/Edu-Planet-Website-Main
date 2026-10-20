'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const {generateKeyPairSync,verify}=require('node:crypto');
const {createHandler,HEADER}=require('./handler.cjs');
const pair=generateKeyPairSync('rsa',{modulusLength:2048});
const privateKey=pair.privateKey.export({type:'pkcs8',format:'pem'});
const env={FEE_ENQUIRY_ALLOWED_ORIGINS:'http://127.0.0.1:8000',GOOGLE_SHEET_ID:'test-sheet-12345',GOOGLE_SERVICE_ACCOUNT_JSON:JSON.stringify({type:'service_account',client_email:'test@example.iam.gserviceaccount.com',private_key:privateKey})};
const input={parentName:'Preview Parent',contactNumber:'0123456789',email:'preview@example.com',website:''};
const req=body=>({method:'POST',headers:{origin:'http://127.0.0.1:8000','content-type':'application/json'},body:JSON.stringify(body),ip:'test-client'});
function fixture({failAppend=false,badHeaders=false,brokenAuth=false}={}){
 const calls=[];
 return {calls,handle:createHandler({env,now:()=>1800000000000,fetchImpl:async(url,options)=>{
  calls.push({url,options});
  if(url.includes('oauth2')){
   const jwt=options.body.get('assertion').split('.');
   assert.equal(verify('RSA-SHA256',Buffer.from(jwt.slice(0,2).join('.')),pair.publicKey,Buffer.from(jwt[2],'base64url')),true);
   assert.equal(JSON.parse(Buffer.from(jwt[1],'base64url')).scope,'https://www.googleapis.com/auth/spreadsheets');
   return {ok:!brokenAuth,json:async()=>brokenAuth?{}:{access_token:'mock-token',expires_in:3600}};
  }
  if(options.method==='POST')return {ok:!failAppend,json:async()=>failAppend?{}:{updates:{updatedRows:1,updatedCells:5}}};
  return {ok:true,json:async()=>({values:[badHeaders?['Wrong headers']:HEADER]})};
 }})};
}
test('only acknowledges a confirmed five-cell append; strings use RAW',async()=>{
 const {handle,calls}=fixture();const result=await handle(req(input));assert.equal(result.status,200);assert.deepEqual(result.body,{ok:true});
 const saved=calls.find(c=>c.url.includes(':append'));assert.match(saved.url,/valueInputOption=RAW/);
 assert.deepEqual(JSON.parse(saved.options.body).values[0],['2027-01-15T08:00:00.000Z','Preview Parent','0123456789','preview@example.com','2027 fees enquiry']);
 assert.equal(result.headers['Access-Control-Allow-Origin'],'http://127.0.0.1:8000');
});
test('untrusted origin is rejected without contacting Google',async()=>{const {handle,calls}=fixture();const r=req(input);r.headers.origin='https://other.example';assert.equal((await handle(r)).status,403);assert.equal(calls.length,0);});
test('preflight carries exact origin and never writes',async()=>{const {handle,calls}=fixture();assert.equal((await handle({...req(input),method:'OPTIONS'})).status,204);assert.equal(calls.length,0);});
test('rejects missing fields, invalid contact/email, honeypot and large requests',async()=>{const {handle,calls}=fixture();for(const invalid of [{...input,parentName:''},{...input,contactNumber:'123'},{...input,email:'not-email'},{...input,website:'spam'}])assert.equal((await handle(req(invalid))).status,400);assert.equal((await handle(req({...input,parentName:'x'.repeat(5000)}))).status,413);assert.equal(calls.length,0);});
test('missing configuration cannot falsely succeed',async()=>{const handle=createHandler({env:{FEE_ENQUIRY_ALLOWED_ORIGINS:env.FEE_ENQUIRY_ALLOWED_ORIGINS}});assert.equal((await handle(req(input))).status,503);});
test('auth and save failures never produce success',async()=>{for(const variant of [{brokenAuth:true},{failAppend:true},{badHeaders:true}]){const {handle}=fixture(variant);const r=await handle(req(input));assert.equal(r.status,502);assert.equal(r.body.ok,false);}});
test('RAW preserves formula-like names as strings',async()=>{const {handle,calls}=fixture();assert.equal((await handle(req({...input,parentName:'=1+1'}))).status,200);assert.equal(JSON.parse(calls.find(c=>c.url.includes(':append')).options.body).values[0][1],'=1+1');});
test('per-instance throttling limits repeated submissions',async()=>{const {handle}=fixture();for(let i=0;i<10;i++)assert.equal((await handle(req(input))).status,200);assert.equal((await handle(req(input))).status,429);});
