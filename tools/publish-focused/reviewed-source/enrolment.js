(async function(){'use strict';
const titles={FAQ_URL:'Full FAQ',APPLICATION_FORM_URL:'Application form',APPLICATION_PDF_URL:'PDF application form',VISIT_CALENDAR_URL:'School visit booking'};
const dialog=document.getElementById('fees-dialog'),form=document.getElementById('fees-access-form'),reveal=document.getElementById('fees-reveal'),phone=document.getElementById('fees-contact-number'),email=document.getElementById('fees-email'),status=document.getElementById('fee-enquiry-status'),submit=form.querySelector('[type="submit"]');
let config,pending=false,controller,generation=0,lastContact=null;
const gradeSelect=document.getElementById('fee-grade-select');
function updateFeeGrade(){
 if(!gradeSelect)return;
 const option=gradeSelect.options[gradeSelect.selectedIndex],group=option?.dataset.feeGroup;
 for(const panel of document.querySelectorAll('[data-fee-group-panel]'))panel.hidden=panel.dataset.feeGroupPanel!==group;
 const heading=document.getElementById('fee-grade-heading');heading.hidden=!group;heading.textContent=group?'Fees for '+option.textContent:'';
 document.getElementById('fee-grade-empty').hidden=Boolean(group);document.getElementById('fee-next-actions').hidden=!group;
}
gradeSelect?.addEventListener('change',updateFeeGrade);
for(const link of document.querySelectorAll('[data-fees-apply]'))link.addEventListener('click',()=>dialog.close());
const ready=fetch('enrolment-config.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error();return r.json();}).then(data=>config=data).catch(()=>null);
const setMessage=(node,message)=>{node.textContent=message;node.hidden=!message;};
function validateContact(name,phoneField,emailField){
 if(!name.trim()||name.trim().length>100||/[\x00-\x1f\x7f]/.test(name))return false;
 const digits=phoneField.value.replace(/\D/g,'');
 if(digits.length<7||digits.length>15||!/^[+()\d\s.-]+$/.test(phoneField.value)||/[\x00-\x1f\x7f]/.test(phoneField.value)){phoneField.setCustomValidity('Enter a valid contact number with 7 to 15 digits.');phoneField.reportValidity();return false;}
 if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailField.value.trim())){emailField.setCustomValidity('Enter a valid email address.');emailField.reportValidity();return false;}
 return true;
}
async function deliver(kind,data,signal){
 await ready;
 if(!config)throw new Error('The enquiry connection is unavailable. Please try again shortly.');
 if(data.website)throw new Error('Please check the form and try again.');
 if(config.feeEnquiryMode==='local-preview')return {preview:true};
 let endpoint,payload,emailMode=config.feeEnquiryMode==='email';
 if(emailMode){
  const recipient=config.emailForms?.recipient;
  if(!recipient||!config.emailForms.activated||!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(recipient))throw new Error('Email enquiries are being connected. Please contact the accounts office for assistance.');
  endpoint='https://formsubmit.co/ajax/'+encodeURIComponent(recipient);
  payload={name:data.parentName,email:data.email,'Contact number':data.contactNumber,'Enquiry type':kind==='scholarship'?'Scholarship interest':'2027 school fees enquiry',...(data.grade?{'Grade of interest':'Grade '+data.grade}:{}),_subject:kind==='scholarship'?'EduPlanet — scholarship interest':'EduPlanet — 2027 school fees enquiry',_replyto:data.email,_template:'table',_honey:data.website,_captcha:'false',_url:'https://www.eduplanet.co.za/admissions.html'};
 }else if(config.feeEnquiryMode==='connected'&&kind==='fees'){
  if(!config.feeEnquiryEndpoint)throw new Error('The enquiry connection is not set up yet. Please contact the accounts office.');
  const url=new URL(config.feeEnquiryEndpoint,location.href);
  if(url.protocol!=='https:'&&!(url.protocol==='http:'&&['127.0.0.1','localhost'].includes(url.hostname)))throw new Error('The enquiry connection is not set up yet.');
  endpoint=url.href;payload=data;
 }else throw new Error('Email enquiries are being connected. Please contact the accounts office for assistance.');
 let response;
 try{response=await fetch(endpoint,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},credentials:'omit',signal,body:JSON.stringify(payload)});}catch(error){if(error.name==='AbortError')throw error;throw new Error('We could not confirm your enquiry was sent. Please try again or contact the accounts office.');}
 let result;try{result=await response.json();}catch{throw new Error('We could not confirm your enquiry was sent. Please try again or contact the accounts office.');}
 const accepted=emailMode?(result.success===true||result.success==='true'):result.ok===true;
 if(!response.ok||!accepted)throw new Error(response.status===429?'Please wait a few minutes before trying again.':'We could not confirm your enquiry was sent. Please try again or contact the accounts office.');
 return {preview:false};
}
for(const button of document.querySelectorAll('[data-open-fees]'))button.addEventListener('click',()=>dialog.showModal());
if(new URL(location.href).searchParams.get('view')==='fees')dialog.showModal();
phone.addEventListener('input',()=>phone.setCustomValidity(''));email.addEventListener('input',()=>email.setCustomValidity(''));
form.addEventListener('submit',async event=>{
 event.preventDefault();if(pending)return;
 const data={parentName:document.getElementById('fees-parent-name').value.trim(),contactNumber:phone.value.trim(),email:email.value.trim(),website:form.elements.website.value};
 if(!validateContact(data.parentName,phone,email))return;
 const attempt=++generation;pending=true;submit.disabled=true;form.setAttribute('aria-busy','true');setMessage(status,'');controller=new AbortController();
 const timer=setTimeout(()=>controller.abort(),30000);
 try{
  submit.textContent='Sending…';
  await deliver('fees',data,controller.signal);
  if(!dialog.open||attempt!==generation)return;
  lastContact=data;form.reset();setMessage(status,'');dialog.classList.add('fees-dialog--schedule');form.hidden=true;reveal.hidden=false;document.getElementById('fees-reveal-title').focus();
 }catch(error){if(dialog.open&&attempt===generation)setMessage(status,error.name==='AbortError'?'We could not confirm your enquiry was sent. Please try again or contact the accounts office.':error.message);}
 finally{clearTimeout(timer);pending=false;submit.disabled=false;submit.textContent='Show fees';form.removeAttribute('aria-busy');controller=null;}
});
dialog.addEventListener('cancel',event=>{if(pending)event.preventDefault();});
dialog.addEventListener('close',()=>{generation++;controller?.abort();lastContact=null;form.reset();if(gradeSelect){gradeSelect.value='';updateFeeGrade();}dialog.classList.remove('fees-dialog--schedule');phone.setCustomValidity('');email.setCustomValidity('');form.hidden=false;reveal.hidden=true;setMessage(status,'');});
const scholarshipDialog=document.getElementById('scholarship-dialog');
if(scholarshipDialog){
 const sf=document.getElementById('scholarship-interest-form'),sp=document.getElementById('scholarship-contact-number'),se=document.getElementById('scholarship-email'),sn=document.getElementById('scholarship-parent-name'),sg=document.getElementById('scholarship-grade'),ss=document.getElementById('scholarship-status'),confirmation=document.getElementById('scholarship-confirmation'),sb=sf.querySelector('[type="submit"]');
 let sending=false,abort,sequence=0;
 for(const button of document.querySelectorAll('[data-open-scholarship]'))button.addEventListener('click',()=>{if(lastContact){sn.value=lastContact.parentName;sp.value=lastContact.contactNumber;se.value=lastContact.email;}sg.value=gradeSelect?.value||'';scholarshipDialog.showModal();});
 sp.addEventListener('input',()=>sp.setCustomValidity(''));se.addEventListener('input',()=>se.setCustomValidity(''));
 sf.addEventListener('submit',async event=>{
  event.preventDefault();if(sending||!validateContact(sn.value,sp,se))return;
  const grade=sg.value;if(!['R',...Array.from({length:12},(_,i)=>String(i+1))].includes(grade))return;
  const attempt=++sequence;sending=true;sb.disabled=true;sb.textContent='Sending…';sf.setAttribute('aria-busy','true');setMessage(ss,'');abort=new AbortController();const timer=setTimeout(()=>abort.abort(),30000);
  try{
   const result=await deliver('scholarship',{parentName:sn.value.trim(),contactNumber:sp.value.trim(),email:se.value.trim(),grade,website:sf.elements.website.value},abort.signal);
   if(!scholarshipDialog.open||sequence!==attempt)return;
   sf.reset();sf.hidden=true;confirmation.hidden=false;document.getElementById('scholarship-confirmation-copy').textContent=result.preview?'Local demonstration complete. No email has been sent.':'Your scholarship-interest enquiry has been submitted.';document.getElementById('scholarship-confirmation-title').focus();
  }catch(error){if(scholarshipDialog.open&&sequence===attempt)setMessage(ss,error.name==='AbortError'?'We could not confirm your enquiry was sent. Please try again or contact the accounts office.':error.message);}
  finally{clearTimeout(timer);sending=false;sb.disabled=false;sb.textContent='Submit scholarship interest';sf.removeAttribute('aria-busy');abort=null;}
 });
 scholarshipDialog.addEventListener('cancel',event=>{if(sending)event.preventDefault();});
 scholarshipDialog.addEventListener('close',()=>{sequence++;abort?.abort();sf.reset();sp.setCustomValidity('');se.setCustomValidity('');sf.hidden=false;confirmation.hidden=true;setMessage(ss,'');});
}
await ready;if(!config)return;
if(config.feeEnquiryMode==='email'){
 const message='Your details are processed by FormSubmit and emailed to '+config.emailForms.recipient+' for follow-up.';
 for(const id of ['fees-preview-note','scholarship-privacy-note']){const node=document.getElementById(id);if(node)node.textContent=message;}
}else if(config.feeEnquiryMode==='connected')document.getElementById('fees-preview-note').textContent='Your name, contact number and email will be sent to EduPlanet’s enquiries spreadsheet so our accounts office can follow up.';
document.getElementById('deadline-notice').textContent=config.deadlineNotice;document.getElementById('late-application-notice').textContent=config.lateApplicationNotice;
for(const button of document.querySelectorAll('[data-enrolment-link]')){const key=button.dataset.enrolmentLink,url=config.links[key];let destination;try{const parsed=new URL(url);if(['https:','http:'].includes(parsed.protocol))destination=parsed.href;}catch{}
 if(destination){const a=document.createElement('a');a.className=button.className;a.innerHTML=button.innerHTML;a.href=destination;button.replaceWith(a);}
 else button.addEventListener('click',()=>{document.getElementById('missing-link-title').textContent=titles[key]+' link';document.getElementById('missing-link-token').textContent='['+key+']';document.getElementById('missing-link-dialog').showModal();});
}
})();
