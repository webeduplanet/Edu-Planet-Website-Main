const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const script=fs.readFileSync(require('node:path').join(__dirname,'enrolment.js'),'utf8');
async function browser(mode, reply) {
 const ids=['fees-dialog','fees-access-form','fees-reveal','fees-contact-number','fees-email','fee-enquiry-status','fees-parent-name','fees-reveal-title','fees-preview-note','deadline-notice','late-application-notice'];
 const nodes=Object.fromEntries(ids.map(id=>[id,{id,hidden:false,value:'',listeners:{},classList:{add(){},remove(){}},addEventListener(type,fn){this.listeners[type]=fn;},setCustomValidity(){},reportValidity(){},focus(){this.focused=true;},setAttribute(){},removeAttribute(){}}]));
 const form=nodes['fees-access-form'],dialog=nodes['fees-dialog'],submit={};dialog.open=true;form.elements={website:{value:''}};form.querySelector=()=>submit;
 form.reset=()=>{form.resets=(form.resets||0)+1;for(const id of ['fees-parent-name','fees-contact-number','fees-email'])nodes[id].value='';};
 nodes['fees-parent-name'].value='Preview Parent';nodes['fees-contact-number'].value='0123456789';nodes['fees-email'].value='preview@example.com';nodes['fees-reveal'].hidden=true;
 const calls=[];
 const context={document:{getElementById:id=>nodes[id],querySelectorAll:()=>[]},location:{href:'http://127.0.0.1:8000/focused/admissions.html'},URL,AbortController,setTimeout,clearTimeout,
  fetch:async(url,options)=>{calls.push({url,options});if(url==='enrolment-config.json')return {ok:true,json:async()=>({feeEnquiryMode:mode,feeEnquiryEndpoint:'https://endpoint.example/api/fee-enquiry',links:{}})};return reply(options);}};
 await vm.runInNewContext(script,context);
 return {nodes,form,submit,calls,send:()=>form.listeners.submit({preventDefault(){}})};
}
test('local preview reveals supplied fees without transmitting details',async()=>{const b=await browser('local-preview',()=>{throw new Error('Unexpected transmission');});await b.send();assert.equal(b.calls.length,1);assert.equal(b.nodes['fees-reveal'].hidden,false);});
test('connected form reveals fees only after acknowledged save',async()=>{let acknowledge;const b=await browser('connected',()=>new Promise(resolve=>acknowledge=resolve));const pending=b.send();await new Promise(resolve=>setImmediate(resolve));assert.equal(b.nodes['fees-reveal'].hidden,true);assert.equal(b.submit.disabled,true);const sent=JSON.parse(b.calls[1].options.body);assert.equal(sent.contactNumber,'0123456789');assert.equal(b.calls[1].options.credentials,'omit');acknowledge({ok:true,json:async()=>({ok:true})});await pending;assert.equal(b.nodes['fees-reveal'].hidden,false);assert.equal(b.form.resets,1);});
test('failed or unconfirmed saves retain details and keep fees hidden',async()=>{for(const reply of [async()=>({ok:false,status:502,json:async()=>({ok:false})}),async()=>({ok:true,json:async()=>({})}),async()=>{throw new Error('Network failure');}]){const b=await browser('connected',reply);await b.send();assert.equal(b.nodes['fees-reveal'].hidden,true);assert.equal(b.nodes['fees-parent-name'].value,'Preview Parent');assert.equal(b.form.hidden,false);assert.equal(b.submit.disabled,false);assert.ok(b.nodes['fee-enquiry-status'].textContent);}});
test('closing a pending submission prevents late fee reveal',async()=>{let acknowledge;const b=await browser('connected',()=>new Promise(resolve=>acknowledge=resolve));const pending=b.send();await new Promise(resolve=>setImmediate(resolve));b.nodes['fees-dialog'].open=false;b.nodes['fees-dialog'].listeners.close();b.nodes['fees-dialog'].open=true;acknowledge({ok:true,json:async()=>({ok:true})});await pending;assert.equal(b.nodes['fees-reveal'].hidden,true);});
