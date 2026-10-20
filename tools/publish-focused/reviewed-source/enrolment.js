(async function(){'use strict';
const titles={FAQ_URL:'Full FAQ',APPLICATION_FORM_URL:'Application form',APPLICATION_PDF_URL:'PDF application form',VISIT_CALENDAR_URL:'School visit booking',SCHOLARSHIP_INTEREST_FORM_URL:'Scholarship interest registration'};
const dialog=document.getElementById('fees-dialog'),form=document.getElementById('fees-access-form'),reveal=document.getElementById('fees-reveal'),phone=document.getElementById('fees-contact-number'),email=document.getElementById('fees-email'),status=document.getElementById('fee-enquiry-status'),submit=form.querySelector('[type="submit"]');
let config, pending=false, controller, generation=0;
const gradeSelect=document.getElementById('fee-grade-select');
const resetFeeGrade=()=>{if(gradeSelect){gradeSelect.value='';updateFeeGrade();}};
function updateFeeGrade(){
 if(!gradeSelect)return;
 const option=gradeSelect.options[gradeSelect.selectedIndex],group=option?.dataset.feeGroup;
 for(const panel of document.querySelectorAll('[data-fee-group-panel]'))panel.hidden=panel.dataset.feeGroupPanel!==group;
 const heading=document.getElementById('fee-grade-heading');heading.hidden=!group;heading.textContent=group?'Fees for '+option.textContent:'';
 document.getElementById('fee-grade-empty').hidden=Boolean(group);
 document.getElementById('fee-next-actions').hidden=!group;
}
gradeSelect?.addEventListener('change',updateFeeGrade);
for(const link of document.querySelectorAll('[data-fees-apply]'))link.addEventListener('click',()=>dialog.close());

const ready=fetch('enrolment-config.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error();return r.json();}).then(data=>config=data).catch(()=>null);
const setStatus=message=>{status.textContent=message;status.hidden=!message;};
for(const button of document.querySelectorAll('[data-open-fees]'))button.addEventListener('click',()=>dialog.showModal());
if(new URL(location.href).searchParams.get('view')==='fees')dialog.showModal();
phone.addEventListener('input',()=>phone.setCustomValidity(''));
email.addEventListener('input',()=>email.setCustomValidity(''));
form.addEventListener('submit',async event=>{
 event.preventDefault();if(pending)return;
 const digits=phone.value.replace(/\D/g,'');
 if(digits.length<7||digits.length>15||!/^[+()\d\s.-]+$/.test(phone.value)||/[\x00-\x1f\x7f]/.test(phone.value)){phone.setCustomValidity('Enter a valid contact number with 7 to 15 digits.');phone.reportValidity();return;}
 if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())){email.setCustomValidity('Enter a valid email address.');email.reportValidity();return;}
 const attempt=++generation;pending=true;submit.disabled=true;form.setAttribute('aria-busy','true');setStatus('');
 try{
  await ready;
  if(!config)throw new Error('The fees connection is unavailable. Please try again shortly.');
  if(config.feeEnquiryMode==='connected'){
   let endpoint;try{endpoint=new URL(config.feeEnquiryEndpoint,location.href);if(endpoint.protocol!=='https:'&&!(endpoint.protocol==='http:'&&['127.0.0.1','localhost'].includes(endpoint.hostname)))throw new Error();}catch{throw new Error('The fees connection is not set up yet. Please contact the accounts office.');}
   if(!config.feeEnquiryEndpoint)throw new Error('The fees connection is not set up yet. Please contact the accounts office.');
   submit.textContent='Sending…';setStatus('Saving your enquiry…');controller=new AbortController();
   const timer=setTimeout(()=>controller.abort(),30000);
   let response;try{response=await fetch(endpoint.href,{method:'POST',headers:{'Content-Type':'application/json'},credentials:'omit',signal:controller.signal,body:JSON.stringify({parentName:document.getElementById('fees-parent-name').value.trim(),contactNumber:phone.value.trim(),email:email.value.trim(),website:form.elements.website.value})});}finally{clearTimeout(timer);}
   let result;try{result=await response.json();}catch{throw new Error('We could not confirm your enquiry was saved. Please try again or contact the accounts office.');}
   if(!response.ok||result.ok!==true)throw new Error(response.status===429?'Please wait a few minutes before trying again.':'We could not confirm your enquiry was saved. Please try again or contact the accounts office.');
  }else if(config.feeEnquiryMode!=='local-preview')throw new Error('The fees connection is not set up yet. Please contact the accounts office.');
  if(!dialog.open||attempt!==generation)return;
  form.reset();setStatus('');dialog.classList.add('fees-dialog--schedule');form.hidden=true;reveal.hidden=false;document.getElementById('fees-reveal-title').focus();
 }catch(error){if(dialog.open&&attempt===generation)setStatus(error.name==='AbortError'?'We could not confirm your enquiry was saved. Please try again or contact the accounts office.':error.message||'Unable to send. Please try again or contact the accounts office.');}
 finally{pending=false;submit.disabled=false;submit.textContent='Show fees';form.removeAttribute('aria-busy');controller=null;}
});
dialog.addEventListener('cancel',event=>{if(pending)event.preventDefault();});
dialog.addEventListener('close',()=>{generation++;controller?.abort();form.reset();resetFeeGrade();dialog.classList.remove('fees-dialog--schedule');phone.setCustomValidity('');email.setCustomValidity('');form.hidden=false;reveal.hidden=true;setStatus('');});
await ready;if(!config)return;
if(config.feeEnquiryMode==='connected')document.getElementById('fees-preview-note').textContent='Your name, contact number and email will be sent to EduPlanet’s enquiries spreadsheet so our accounts office can follow up.';
document.getElementById('deadline-notice').textContent=config.deadlineNotice;document.getElementById('late-application-notice').textContent=config.lateApplicationNotice;
for(const button of document.querySelectorAll('[data-enrolment-link]')){const key=button.dataset.enrolmentLink,url=config.links[key];let destination;try{const parsed=new URL(url);if(['https:','http:'].includes(parsed.protocol))destination=parsed.href;}catch{}
 if(destination){const a=document.createElement('a');a.className=button.className;a.innerHTML=button.innerHTML;a.href=destination;button.replaceWith(a);}
 else button.addEventListener('click',()=>{document.getElementById('missing-link-title').textContent=titles[key]+' link';document.getElementById('missing-link-token').textContent='['+key+']';document.getElementById('missing-link-dialog').showModal();});
}
})();
