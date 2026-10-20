"""Place the reviewed website in the repository for a non-production review branch."""
from pathlib import Path
import shutil,re,json
REPO=Path(__file__).resolve().parents[2]
SOURCE=Path(__file__).resolve().parent/'reviewed-source'
PAGES=['index.html','about.html','academics.html','admissions.html','school-life.html','contact.html','early-years.html','intermediate.html','senior.html','matric.html']
for file in PAGES:
 text=(SOURCE/file).read_text()
 text=text.replace('/focused/','/').replace('Local only · Draft for review','Draft for review · Forms not connected')
 text=re.sub(r'<a href="/selected/[^\"]*">Previous draft</a>','',text)
 (REPO/file).write_text(text)
for file in ['focused.css','focused.js','preview.css','preview.js','enrolment.css','enrolment.js','enrolment-config.json','page-manifest.json']:
 shutil.copy2(SOURCE/file,REPO/file)
shutil.copytree(SOURCE/'photos',REPO/'photos',dirs_exist_ok=True)
assert all('noindex, nofollow' in (REPO/p).read_text() for p in PAGES)
assert all(not re.search(r'\bRR\b',(REPO/p).read_text()) for p in PAGES)
print('Prepared all 10 reviewed pages at the repository root. Review notices remain; no live forms or production deployment enabled.')
