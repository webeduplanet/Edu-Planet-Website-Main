(async function(){'use strict';
const dialog=document.getElementById('fees-dialog'),gradeSelect=document.getElementById('fee-grade-select'),inclusions=document.getElementById('fee-inclusions');
let config;
const ready=fetch('enrolment-config.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error();return r.json();}).then(data=>config=data).catch(()=>null);
function updateFeeGrade(){
 const option=gradeSelect.options[gradeSelect.selectedIndex],group=option?.dataset.feeGroup;
 for(const panel of document.querySelectorAll('[data-fee-group-panel]'))panel.hidden=panel.dataset.feeGroupPanel!==group;
 const heading=document.getElementById('fee-grade-heading');heading.hidden=!group;heading.textContent=group?'Fees for '+option.textContent:'';
 document.getElementById('fee-grade-empty').hidden=Boolean(group);document.getElementById('fee-next-actions').hidden=!group;
 document.getElementById('fee-scholarship-offer').hidden=!group;
}
gradeSelect.addEventListener('change',()=>{updateFeeGrade();try{sessionStorage.setItem('eduplanet-fee-grade',gradeSelect.value);}catch{}});
try{const saved=sessionStorage.getItem('eduplanet-fee-grade');if(saved&&['R',...Array.from({length:12},(_,i)=>String(i+1))].includes(saved))gradeSelect.value=saved;}catch{}
updateFeeGrade();
let feesFromMenu=false;
function openFees(event){
 event?.preventDefault();
 const nav=document.getElementById('site-nav'),toggle=document.querySelector('.nav-toggle');
 feesFromMenu=Boolean(nav?.classList.contains('is-open'));
 if(feesFromMenu){nav.classList.remove('is-open');toggle?.setAttribute('aria-expanded','false');}
 if(!dialog.open)dialog.showModal();
}
for(const button of document.querySelectorAll('[data-open-fees]'))button.addEventListener('click',openFees);
if(new URL(location.href).searchParams.get('view')==='fees')openFees();
for(const link of document.querySelectorAll('[data-fees-apply]'))link.addEventListener('click',()=>dialog.close());
dialog.addEventListener('close',()=>{inclusions.open=false;if(feesFromMenu){document.querySelector('.nav-toggle')?.focus();feesFromMenu=false;}});
await ready;if(!config)return;
const deadline=document.getElementById('deadline-notice'),late=document.getElementById('late-application-notice');if(deadline)deadline.textContent=config.deadlineNotice;if(late)late.textContent=config.lateApplicationNotice;
// Every action has a usable HTML fallback; only replace it when an approved URL exists.
for(const [key,selector,label] of [['VISIT_CALENDAR_URL','[data-appointment]','Make an appointment'],['APPLICATION_PDF_URL','[data-application-pdf]','Download the PDF form'],['SCHOLARSHIP_FORM_URL','[data-scholarship-form]','Register scholarship interest']]){
 let destination;try{const parsed=new URL(config.links?.[key]);if(parsed.protocol==='https:')destination=parsed.href;}catch{}
 if(destination)for(const control of document.querySelectorAll(selector)){
  let link=control;
  if(control.tagName==='BUTTON'){link=document.createElement('a');link.className=control.className;link.textContent=label;control.replaceWith(link);}
  link.href=destination;if(link.textContent==='Request an appointment'||key==='APPLICATION_PDF_URL')link.textContent=label;
 }
}
})();
