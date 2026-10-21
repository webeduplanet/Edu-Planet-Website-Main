const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const script=fs.readFileSync(require('node:path').join(__dirname,'../publish-focused/reviewed-source/enrolment.js'),'utf8');
async function browser(reply,options={}){
 const ids=['fees-dialog','fee-grade-select','fee-inclusions','fee-grade-heading','fee-grade-empty','fee-next-actions','fee-scholarship-offer'];
 const nodes=Object.fromEntries(ids.map(id=>[id,{id,open:false,hidden:false,value:'',listeners:{},addEventListener(t,fn){this.listeners[t]=fn;},showModal(){this.open=true;},close(){this.open=false;this.listeners.close?.();}}]));
 const select=nodes['fee-grade-select'];select.options=[{value:'',textContent:'Select a grade',dataset:{}},{value:'12',textContent:'Grade 12',dataset:{feeGroup:'6'}}];
 Object.defineProperty(select,'selectedIndex',{get(){return this.options.findIndex(option=>option.value===this.value);}});
 const session=new Map(options.savedGrade?[['eduplanet-fee-grade',options.savedGrade]]:[]);
 const nav={classList:{contains(){return Boolean(options.menuOpen);},remove(){options.menuOpen=false;}}};
 const toggle={setAttribute(){},focus(){this.focused=true;}};
 const calls=[],fees={addEventListener(t,fn){this[t]=fn;}};
 await vm.runInNewContext(script,{document:{querySelector:selector=>selector==='.nav-toggle'?toggle:null,getElementById:id=>id==='site-nav'?nav:nodes[id]||null,querySelectorAll:selector=>selector==='[data-open-fees]'?[fees]:[]},location:{href:'http://127.0.0.1:8001/early-years.html'},sessionStorage:{getItem:key=>session.get(key),setItem:(key,value)=>session.set(key,value)},URL,
 fetch:async(url,args)=>{calls.push({url,args});assert.equal(url,'enrolment-config.json');return {ok:!options.offline,json:async()=>({links:{}})};}});
 return {nodes,calls,toggle,session,openFees:()=>fees.click()};
}
test('fees open directly without collecting or transmitting contact details, even if config is unavailable',async()=>{const b=await browser(()=>{throw Error('Unexpected submission');},{offline:true});b.openFees();assert.equal(b.nodes['fees-dialog'].open,true);assert.equal(b.calls.length,1);assert.equal(b.calls[0].url,'enrolment-config.json');});
test('closing and reopening fees retains the chosen grade and collapses inclusions',async()=>{const b=await browser();b.nodes['fee-grade-select'].value='12';b.nodes['fee-grade-select'].listeners.change();b.nodes['fee-inclusions'].open=true;b.openFees();b.nodes['fees-dialog'].close();b.openFees();assert.equal(b.nodes['fee-grade-select'].value,'12');assert.equal(b.nodes['fee-inclusions'].open,false);assert.equal(b.nodes['fee-next-actions'].hidden,false);assert.equal(b.session.get('eduplanet-fee-grade'),'12');});
test('previously selected grade is restored within the browser session',async()=>{const b=await browser(undefined,{savedGrade:'12'});assert.equal(b.nodes['fee-grade-select'].value,'12');assert.equal(b.nodes['fee-next-actions'].hidden,false);});
test('opening fees from mobile navigation closes the menu and restores focus to its toggle',async()=>{const b=await browser(undefined,{menuOpen:true});b.openFees();b.nodes['fees-dialog'].close();assert.equal(b.toggle.focused,true);});
