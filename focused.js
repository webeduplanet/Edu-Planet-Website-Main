(function(){'use strict';
const toggle=document.querySelector('.phase-menu-toggle'),menu=document.getElementById('phase-submenu');
function closeMenu(){if(toggle){toggle.setAttribute('aria-expanded','false');menu.hidden=true;}}
if(toggle){toggle.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')==='true';toggle.setAttribute('aria-expanded',String(!open));menu.hidden=open;});document.addEventListener('click',e=>{if(!e.target.closest('.learning-menu'))closeMenu();});document.addEventListener('keydown',e=>{if(e.key==='Escape'&&toggle.getAttribute('aria-expanded')==='true'){closeMenu();toggle.focus();}});}
const page=location.pathname.split('/').pop()||'index.html';
const labels={'early-years':'Grades R–3','intermediate':'Grades 4–6','senior':'Grades 7–9','matric':'Grades 10–12'},phase=new URL(location.href).searchParams.get('phase');if(page==='contact.html'&&labels[phase]){const el=document.createElement('p');el.className='phase-context';el.textContent='Your enquiry: '+labels[phase]+'. Please mention this phase when contacting reception.';document.querySelector('.pagehead .wrap').appendChild(el);}
})();
