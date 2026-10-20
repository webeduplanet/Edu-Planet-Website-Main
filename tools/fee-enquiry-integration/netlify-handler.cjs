// Copy to netlify/functions/fee-enquiry.cjs, with lib/fee-enquiry-core.cjs at the project root.
const {createHandler} = require('../../lib/fee-enquiry-core.cjs');
const handle = createHandler();
exports.handler = async event => {
  const result = await handle({method:event.httpMethod,headers:event.headers,
    body:event.isBase64Encoded?Buffer.from(event.body,'base64').toString('utf8'):event.body,
    ip:event.headers['x-nf-client-connection-ip'] || 'unknown'});
  return {statusCode:result.status,headers:result.headers,body:result.body===null?'':JSON.stringify(result.body)};
};
