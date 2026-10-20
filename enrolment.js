(async function(){'use strict';
const titles={FAQ_URL:'Full FAQ',APPLICATION_PDF_URL:'PDF application form',VISIT_CALENDAR_URL:'School visit booking'};
const dialog=document.getElementById('fees-dialog'),gradeSelect=document.getElementById('fee-grade-select'),inclusions=document.getElementById('fee-inclusions');
let config;
const ready=fetch('enrolment-config.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error();return r.json();}).then(data=>config=data).catch(()=>null);
function updateFeeGrade(){
 const option=gradeSelect.options[gradeSelect.selectedIndex],group=option?.dataset.feeGroup;
 for(const panel of document.querySelectorAll('[data-fee-group-panel]'))panel.hidden=panel.dataset.feeGroupPanel!==group;
 const heading=document.getElementById('fee-grade-heading');heading.hidden=!group;heading.textContent=group?'Fees for '+option.textContent:'';
 document.getElementById('fee-grade-empty').hidden=Boolean(group);document.getElementById('fee-next-actions').hidden=!group;
}
gradeSelect.addEventListener('change',updateFeeGrade);
function openFees(){if(!dialog.open)dialog.showModal();}
for(const button of document.querySelectorAll('[data-open-fees]'))button.addEventListener('click',openFees);
if(new URL(location.href).searchParams.get('view')==='fees')openFees();
for(const link of document.querySelectorAll('[data-fees-apply]'))link.addEventListener('click',()=>dialog.close());
dialog.addEventListener('close',()=>{gradeSelect.value='';updateFeeGrade();inclusions.open=false;});
const scholarshipDialog=document.getElementById('scholarship-dialog'),form=document.getElementById('scholarship-interest-form'),phone=document.getElementById('scholarship-contact-number'),email=document.getElementById('scholarship-email'),name=document.getElementById('scholarship-parent-name'),grade=document.getElementById('scholarship-grade'),status=document.getElementById('scholarship-status'),confirmation=document.getElementById('scholarship-confirmation'),submit=form.querySelector('[type="submit"]');
let pending=false,controller,generation=0;
const message=text=>{status.textContent=text;status.hidden=!text;};
for(const button of document.querySelectorAll('[data-open-scholarship]'))button.addEventListener('click',async()=>{
 await ready;const enabled=config?.feeEnquiryMode==='email'&&config.emailForms?.activated;
 form.hidden=!enabled;document.getElementById('scholarship-email-option').hidden=Boolean(enabled);grade.value=gradeSelect.value;scholarshipDialog.showModal();
});
phone.addEventListener('input',()=>phone.setCustomValidity(''));email.addEventListener('input',()=>email.setCustomValidity(''));
form.addEventListener('submit',async event=>{
 event.preventDefault();if(pending)return;
 const parentName=name.value.trim(),contactNumber=phone.value.trim(),emailAddress=email.value.trim(),selectedGrade=grade.value;
 if(!parentName||parentName.length>100||/[\x00-\x1f\x7f]/.test(parentName))return;
 const digits=contactNumber.replace(/\D/g,'');
 if(digits.length<7||digits.length>15||!/^[+()\d\s.-]+$/.test(contactNumber)||/[\x00-\x1f\x7f]/.test(contactNumber)){phone.setCustomValidity('Enter a valid contact number with 7 to 15 digits.');phone.reportValidity();return;}
 if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailAddress)){email.setCustomValidity('Enter a valid email address.');email.reportValidity();return;}
 if(!['R',...Array.from({length:12},(_,i)=>String(i+1))].includes(selectedGrade))return;
 const attempt=++generation;pending=true;submit.disabled=true;submit.textContent='Sending…';form.setAttribute('aria-busy','true');message('');controller=new AbortController();const timer=setTimeout(()=>controller.abort(),30000);
 try{
  await ready;const recipient=config?.emailForms?.recipient;
  if(config?.feeEnquiryMode!=='email'||!config.emailForms?.activated||!recipient||!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(recipient))throw new Error('Please email info@eduplanet.co.za for assistance.');
  const website=form.elements.website.value;if(website)throw new Error('Please check the form and try again.');
  const payload={name:parentName,email:emailAddress,'Contact number':contactNumber,'Enquiry type':'Scholarship interest','Grade of interest':'Grade '+selectedGrade,_subject:'EduPlanet — scholarship interest',_replyto:emailAddress,_template:'table',_honey:website,_captcha:'false',_url:'https://www.eduplanet.co.za/admissions.html'};
  let response,result;
  try{response=await fetch('https://formsubmit.co/ajax/'+encodeURIComponent(recipient),{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},credentials:'omit',signal:controller.signal,body:JSON.stringify(payload)});result=await response.json();}catch(error){if(error.name==='AbortError')throw error;throw new Error('We could not confirm your enquiry was sent. Please try again or contact the accounts office.');}
  if(!response.ok||!(result.success===true||result.success==='true'))throw new Error(response.status===429?'Please wait a few minutes before trying again.':'We could not confirm your enquiry was sent. Please try again or contact the accounts office.');
  if(!scholarshipDialog.open||generation!==attempt)return;
  form.reset();form.hidden=true;confirmation.hidden=false;document.getElementById('scholarship-confirmation-title').focus();
 }catch(error){if(scholarshipDialog.open&&generation===attempt)message(error.name==='AbortError'?'We could not confirm your enquiry was sent. Please try again or contact the accounts office.':error.message);}
 finally{clearTimeout(timer);pending=false;submit.disabled=false;submit.textContent='Submit scholarship interest';form.removeAttribute('aria-busy');controller=null;}
});
scholarshipDialog.addEventListener('close',()=>{generation++;controller?.abort();form.reset();phone.setCustomValidity('');email.setCustomValidity('');form.hidden=false;confirmation.hidden=true;message('');});
await ready;if(!config)return;
const deadline=document.getElementById('deadline-notice'),late=document.getElementById('late-application-notice');if(deadline)deadline.textContent=config.deadlineNotice;if(late)late.textContent=config.lateApplicationNotice;
for(const button of document.querySelectorAll('[data-enrolment-link]')){
 const key=button.dataset.enrolmentLink,url=config.links[key];let destination;try{const parsed=new URL(url);if(['https:','http:'].includes(parsed.protocol))destination=parsed.href;}catch{}
 if(destination){const link=document.createElement('a');link.className=button.className;link.innerHTML=button.innerHTML;link.href=destination;button.replaceWith(link);}
 else button.addEventListener('click',()=>{document.getElementById('missing-link-title').textContent=titles[key]+' link';document.getElementById('missing-link-token').textContent='['+key+']';document.getElementById('missing-link-dialog').showModal();});
}
})();
