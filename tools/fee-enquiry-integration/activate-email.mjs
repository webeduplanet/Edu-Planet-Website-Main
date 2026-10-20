// Sends one setup/activation test to the explicitly chosen school inbox.
// No parent or learner information is used. The owner approves activation in email.
const recipient=process.argv[2];
if(!recipient||!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(recipient))throw new Error('Provide the chosen receiving email address.');
const response=await fetch('https://formsubmit.co/ajax/'+encodeURIComponent(recipient),{
 // The setup script identifies the school page; browser submissions supply their own referrer.
 method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json','Referer':'https://www.eduplanet.co.za/admissions.html'},signal:AbortSignal.timeout(25000),
 body:JSON.stringify({name:'EduPlanet website setup test',email:recipient,message:'This is an authorised setup test for the EduPlanet fee-enquiry and scholarship-interest email forms. No parent or learner details are included.',_subject:'EduPlanet website — email form activation test',_captcha:'false',_url:'https://www.eduplanet.co.za/admissions.html'})
});
let result;try{result=await response.json();}catch{throw new Error('The service did not return a readable response. Delivery is not confirmed.');}
if(response.ok&&/needs activation/i.test(String(result.message||''))){
 console.log('The service reports sending its activation email. The owner of '+recipient+' must click Activate Form. Submission delivery is still inactive and unverified.');
 process.exit(0);
}
if(!response.ok||!(result.success===true||result.success==='true'))throw new Error('The service did not accept the setup test (HTTP '+response.status+'). '+String(result.message||'No service explanation was supplied.').slice(0,350)+' Delivery is not confirmed.');
console.log('The service accepted the setup request. Check the receiving inbox (and spam) for its activation email. Inbox delivery and activation still need the owner’s confirmation.');
