"""Build the public website, or an explicitly non-indexable review, from source."""
from pathlib import Path
import shutil,re,json,hashlib,html,argparse
from PIL import Image
REPO=Path(__file__).resolve().parents[2]
SOURCE=Path(__file__).resolve().parent/'reviewed-source'
PAGES=['index.html','about.html','academics.html','admissions.html','school-life.html','contact.html','early-years.html','intermediate.html','senior.html','matric.html']
parser=argparse.ArgumentParser()
parser.add_argument('--preview',action='store_true',help='Exclude review pages from search indexing')
args=parser.parse_args()
ORIGIN='https://www.eduplanet.co.za'
IDENTITY=json.loads((SOURCE/'site-identity.json').read_text())
assert IDENTITY['url']==ORIGIN
META={
 'index.html':('EduPlanet Independent School | Grade R–12 in Gqeberha','A Christian independent school in Struandale, Gqeberha. Explore small classes, learner support, Grade R–12 phases, 2027 fees and applications.'),
 'about.html':('Our Christian Vision, Mission & Values | EduPlanet','Discover EduPlanet’s Christian vision, mission and values, and how faith, character and service shape our school community.'),
 'academics.html':('Academics & Learner Support | EduPlanet','Explore EduPlanet’s CAPS curriculum, small classes, free extra classes, learner support and technology education from Grade R to Grade 12.'),
 'admissions.html':('Admissions & 2027 School Fees | EduPlanet','View EduPlanet’s 2027 fees and included benefits. Apply online, request a school visit and understand the three steps to enrolment.'),
 'school-life.html':('Sport, Activities & School Life | EduPlanet','Discover soccer, netball, creative learning and Christian service at EduPlanet Independent School in Gqeberha.'),
 'contact.html':('Contact & Appointment Requests | EduPlanet','Contact EduPlanet about applications or a school visit. Find our phone, WhatsApp, office hours and directions to Struandale, Gqeberha.'),
 'early-years.html':('Foundation Phase, Grades R–3 | EduPlanet','A caring start to school through stories, play, early literacy and numeracy. Explore EduPlanet’s Foundation Phase, support and 2027 fees.'),
 'intermediate.html':('Intermediate Phase, Grades 4–6 | EduPlanet','Explore broader subjects, growing independence and academic support in EduPlanet’s Intermediate Phase. View 2027 fees and apply online.'),
 'senior.html':('Senior Phase, Grades 7–9 | EduPlanet','Explore EduPlanet’s Senior Phase: a broad curriculum, healthy discipline, learner support and guidance towards Grade 10 subject choices.'),
 'matric.html':('FET Phase, Grades 10–12 | EduPlanet','Explore EduPlanet’s FET subjects, free extra classes, practical technology and career guidance. View 2027 fees and apply for Grades 10–12.'),
}
def structured_data(file,title,description,url):
 school={
  '@type':'School','@id':ORIGIN+'/#school',
  'name':IDENTITY['name'],'url':ORIGIN+'/',
  'description':IDENTITY['description'],
  'logo':ORIGIN+IDENTITY['logo'],
  'telephone':IDENTITY['telephone'],'email':IDENTITY['email'],
  'address':IDENTITY['address'],'foundingDate':IDENTITY['foundingDate'],
  'identifier':{'@type':'PropertyValue','propertyID':'DBE EMIS','value':IDENTITY['emis']},
  'contactPoint':{'@type':'ContactPoint','contactType':'Admissions and accounts',
                  'telephone':IDENTITY['telephone'],'email':IDENTITY['admissionsEmail']}
 }
 website={'@type':'WebSite','@id':ORIGIN+'/#website','url':ORIGIN+'/',
          'name':IDENTITY['name'],'publisher':{'@id':school['@id']},'inLanguage':'en-ZA'}
 page={'@type':'WebPage','@id':url+'#webpage','url':url,'name':title,
       'description':description,'inLanguage':'en-ZA',
       'isPartOf':{'@id':website['@id']},'about':{'@id':school['@id']}}
 graph=[school,website,page]
 if file!='index.html':
  label={'early-years.html':'Foundation Phase','intermediate.html':'Intermediate Phase',
         'senior.html':'Senior Phase','matric.html':'FET Phase'}.get(file,title.split(' | ')[0])
  breadcrumb={'@type':'BreadcrumbList','@id':url+'#breadcrumb','itemListElement':[
   {'@type':'ListItem','position':1,'name':'Home','item':ORIGIN+'/'},
   {'@type':'ListItem','position':2,'name':label,'item':url}]}
  page['breadcrumb']={'@id':breadcrumb['@id']};graph.append(breadcrumb)
 return json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')
dialogs=(SOURCE/'enrolment-source/fee-dialogs.html').read_text().strip()
footer=(SOURCE/'shared-footer.html').read_text().strip()
cache_files=['focused.css','focused.js','preview.css','preview.js','enrolment.css','enrolment.js']
for file in PAGES:
 text=(SOURCE/file).read_text()
 text=re.sub(r'<dialog\b[^>]*\bid="(?:fees-dialog|scholarship-dialog)".*?</dialog>','',text,flags=re.S)
 text=text.replace('</main>',dialogs+'\n</main>',1)
 text=text.replace('/focused/','/')
 text=re.sub(r'<a href="/selected/[^\"]*">Previous draft</a>','',text)
 text=re.sub(r'<footer\b.*?</footer>',lambda _:footer,text,flags=re.S)
 text=re.sub(r'<dialog\b[^>]*\bid="(?:application-preview|missing-link-dialog)".*?</dialog>','',text,flags=re.S)
 title,description=META[file]
 for name,value in [('description',description),('og:title',title),('og:description',description)]:
  attr='property' if name.startswith('og:') else 'name'
  text=re.sub(r'<meta '+attr+'="'+re.escape(name)+r'"[^>]*>',lambda _:f'<meta {attr}="{name}" content="{html.escape(value,quote=True)}">',text)
 text=re.sub(r'<title>.*?</title>',lambda _:f'<title>{html.escape(title)}</title>',text)
 text=re.sub(r'<meta name="robots"[^>]*>|<link rel="canonical"[^>]*>|<meta property="og:(?:url|image)"[^>]*>','',text)
 text=re.sub(r'<script\b[^>]*type="application/ld\+json"[^>]*>.*?</script>','',text,flags=re.S)
 url=ORIGIN+('/' if file=='index.html' else '/'+file)
 tags=f'<link rel="canonical" href="{url}">\n<meta property="og:url" content="{url}">\n<meta property="og:image" content="{ORIGIN}/assets/img/hero-poster.jpg">'
 if args.preview:tags+='\n<meta name="robots" content="noindex, nofollow">'
 tags+='\n<script type="application/ld+json">'+structured_data(file,title,description,url)+'</script>'
 text=text.replace('</head>',tags+'\n</head>')
 text=text.replace('<!-- DEPLOY STEP: replace with the live absolute URLs once the domain is live -->','')
 # Use the preferred home address in navigation, keeping /index.html as an old URL only.
 text=re.sub(r'\bhref="/?index\.html([?#][^"]*)?"',lambda m:'href="/'+(m[1] or '')+'"',text)
 for asset in cache_files:
  digest=hashlib.sha256((SOURCE/asset).read_bytes()).hexdigest()[:10]
  text=re.sub(re.escape(asset)+r'(?:\?v=[a-z0-9]+)?(?=")',asset+'?v='+digest,text)
 for asset in ['assets/js/main.js','assets/css/styles.css']:
  digest=hashlib.sha256((REPO/asset).read_bytes()).hexdigest()[:10]
  text=re.sub(re.escape(asset)+r'(?:\?v=[a-z0-9]+)?(?=")',asset+'?v='+digest,text)
 # Reserve image space without changing the approved crops.
 def dimensions(match):
  tag=match.group(0)
  src=re.search(r'\bsrc="([^"]+)"',tag)
  if src and not re.search(r'\bwidth=',tag):
   image_path=REPO/src[1].lstrip('/')
   if image_path.exists():
    with Image.open(image_path) as image:
     tag=tag[:-1]+f' width="{image.width}" height="{image.height}">'
  return tag
 text=re.sub(r'<img\b[^>]*>',dimensions,text)
 (REPO/file).write_text(text)
for file in ['focused.css','focused.js','preview.css','preview.js','enrolment.css','enrolment.js','enrolment-config.json','page-manifest.json']:
 shutil.copy2(SOURCE/file,REPO/file)
shutil.copytree(SOURCE/'photos',REPO/'photos',dirs_exist_ok=True)
assert all(('noindex, nofollow' in (REPO/p).read_text())==args.preview for p in PAGES)
assert all(not re.search(r'\bRR\b',(REPO/p).read_text()) for p in PAGES)
urls=[ORIGIN+('/' if p=='index.html' else '/'+p) for p in PAGES]
(REPO/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{url}</loc></url>\n' for url in urls)+'</urlset>\n')
(REPO/'robots.txt').write_text('User-agent: *\n'+('Disallow: /\n' if args.preview else 'Allow: /\nDisallow: /tools/\nDisallow: /reports/\nDisallow: /output/\nDisallow: /tmp/\n')+'\nSitemap: '+ORIGIN+'/sitemap.xml\n')
not_found=(REPO/'contact.html').read_text()
not_found=re.sub(r'<main\b.*?</main>',lambda _:'<main id="main" tabindex="-1"><section class="pagehead focused-pagehead"><div class="wrap"><p class="eyebrow">Page not found</p><h1>Let’s help you find your way.</h1><p class="lede">This address may have changed. Explore the school, find your child’s phase or contact us for help.</p><div class="btn-row"><a class="btn btn--primary" href="/">Go to Home</a><a class="btn btn--ghost" href="/academics.html#learning-phases">Explore the phases</a><a href="/admissions.html">Fees and admissions</a><a href="/contact.html">Contact us</a></div></div></section>'+dialogs+'</main>',not_found,flags=re.S)
not_found=re.sub(r'<title>.*?</title>','<title>Page not found | EduPlanet</title>',not_found)
not_found=re.sub(r'<meta property="og:title"[^>]*>','<meta property="og:title" content="Page not found | EduPlanet">',not_found)
not_found=re.sub(r'<script\b[^>]*type="application/ld\+json"[^>]*>.*?</script>','',not_found,flags=re.S)
not_found=re.sub(r'<meta (name="description"|property="og:description")[^>]*>',lambda m:'<meta '+m[1]+' content="Find your way to EduPlanet’s school phases, fees, admissions or contact information.">',not_found)
not_found=not_found.replace(' aria-current="page"','')
not_found=re.sub(r'<link rel="canonical"[^>]*>|<meta property="og:url"[^>]*>|<meta name="robots"[^>]*>','',not_found).replace('</head>','<meta name="robots" content="noindex, follow"></head>')
# A missing page can be served at a nested URL; its recovery links/assets must stay at the site root.
not_found=re.sub(r'\b(href|src)="(?![a-zA-Z][a-zA-Z0-9+.-]*:|/|#)([^"]+)"',lambda m:f'{m[1]}="/{m[2]}"',not_found)
(REPO/'404.html').write_text(not_found)
print('Prepared 10 pages, a helpful 404 page and search files. Mode: '+('private review' if args.preview else 'production-ready local files')+'. Nothing has been deployed.')
