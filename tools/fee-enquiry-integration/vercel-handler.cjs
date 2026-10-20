// Copy this file to api/fee-enquiry.js, with lib/fee-enquiry-core.cjs at the project root.
const {createHandler} = require('../lib/fee-enquiry-core.cjs');
const handle = createHandler();
module.exports = async (req,res) => {
  const result = await handle({method:req.method,headers:req.headers,body:req.body,
    ip:req.headers['x-forwarded-for']?.split(',')[0]?.trim() || 'unknown'});
  for (const [key,value] of Object.entries(result.headers)) res.setHeader(key,value);
  res.statusCode=result.status;
  res.end(result.body===null ? '' : JSON.stringify(result.body));
};
