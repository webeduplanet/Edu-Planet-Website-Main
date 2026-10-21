"""Check the generated public release without a browser or network submission."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import argparse
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).resolve().parent / 'reviewed-source'


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links, self.nodes = [], [], []
        self.feed(text)

    def handle_starttag(self, tag, items):
        attrs = dict(items)
        self.nodes.append((tag, attrs))
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for attr in ('href', 'src'):
            if attr in attrs:
                self.links.append(attrs[attr])


def check(preview=False):
    paths = sorted(ROOT.glob('*.html'))
    texts = {path.name: path.read_text() for path in paths}
    pages = {name: Page(text) for name, text in texts.items()}
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    def target_exists(origin, link):
        target = urlsplit(link)
        if target.scheme or target.netloc:
            return
        name = ('index.html' if target.path == '/' else unquote(target.path).lstrip('/')) or origin
        require((ROOT / name).exists(), f'{origin}: missing target {link}')
        if target.fragment and name in pages:
            require(target.fragment in pages[name].ids, f'{origin}: missing anchor {link}')

    fee_schedule = json.loads((SOURCE / 'enrolment-source/fee-schedule-2027.json').read_text())
    expected_fees = [f'R{row["amounts"][group]:,}' for group in range(7) for row in fee_schedule['rows']]
    links = json.loads((SOURCE / 'enrolment-config.json').read_text())['links']
    application = links['APPLICATION_FORM_URL']
    identity = json.loads((SOURCE / 'site-identity.json').read_text())
    footers = []
    descriptions = []
    for name, page in pages.items():
        text = texts[name]
        duplicate = [key for key, count in Counter(page.ids).items() if count > 1]
        require(not duplicate, f'{name}: duplicate IDs {duplicate}')
        require(sum(tag == 'h1' for tag, attrs in page.nodes) == 1, f'{name}: requires one h1')
        for link in page.links:
            target_exists(name, link)
        require(not re.search(r'\bRR\b|\[[A-Z_]+_URL\]|/focused/', text), f'{name}: stale grade, token or preview URL')
        require('fees-dialog' in page.ids and 'scholarship-dialog' in page.ids, f'{name}: shared dialogs missing')
        require(not any('data-enrolment-link' in attrs for tag, attrs in page.nodes), f'{name}: unresolved action control')
        for tag, attrs in page.nodes:
            if tag == 'img':
                require(bool(attrs.get('alt')), f'{name}: image alternative missing')
                require('width' in attrs and 'height' in attrs, f'{name}: image dimensions missing')
        for match in re.finditer(r'<a\b([^>]*)>(.*?)</a>', text, re.S):
            label = re.sub(r'<[^>]+>', '', match[2]).strip()
            if label == 'Apply now':
                require(f'href="{application}"' in match[1], f'{name}: Apply now must open the Google Form directly')
        panels = re.findall(r'<dl class="selected-grade-fees".*?</dl>', text, re.S)
        amounts = [amount for panel in panels for amount in re.findall(r'<dd>(.*?)</dd>', panel)]
        require(amounts == expected_fees, f'{name}: supplied fee amounts changed')
        if name != '404.html':
            robots = [attrs.get('content', '') for tag, attrs in page.nodes if tag == 'meta' and attrs.get('name') == 'robots']
            require(any('noindex' in value for value in robots) == preview, f'{name}: indexing mode incorrect')
            canonicals = [attrs['href'] for tag, attrs in page.nodes if tag == 'link' and attrs.get('rel') == 'canonical']
            expected = 'https://www.eduplanet.co.za' + ('/' if name == 'index.html' else '/' + name)
            require(canonicals == [expected], f'{name}: canonical missing or incorrect')
            require(not re.search(r'href="/?index\.html(?:[?#"]|$)', text), f'{name}: navigation should use the canonical home address')
            graphs = re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', text, re.S)
            require(len(graphs) == 1, f'{name}: requires one structured-data graph')
            try:
                graph = json.loads(graphs[0])['@graph']
                types = {node['@type']: node for node in graph}
                school, web_page = types['School'], types['WebPage']
                require(school['name'] == identity['name'] and school['address'] == identity['address'], f'{name}: school identity mismatch')
                require(school['telephone'] == identity['telephone'] and school['email'] == identity['email'], f'{name}: school contacts mismatch')
                require(school['logo'] == identity['url'] + identity['logo'], f'{name}: school logo mismatch')
                require((ROOT / identity['logo'].lstrip('/')).is_file(), f'{name}: school logo missing')
                require(web_page['url'] == expected and web_page['@id'] == expected + '#webpage', f'{name}: structured page URL mismatch')
                require(web_page['description'] in [attrs.get('content') for tag, attrs in page.nodes if tag == 'meta' and attrs.get('name') == 'description'], f'{name}: structured description mismatch')
                if name != 'index.html':
                    crumbs = types['BreadcrumbList']['itemListElement']
                    require(crumbs[0]['item'] == identity['url'] + '/' and crumbs[-1]['item'] == expected, f'{name}: breadcrumb URLs mismatch')
            except (ValueError, KeyError, IndexError, TypeError) as error:
                require(False, f'{name}: invalid structured data ({error})')
            descriptions += [attrs.get('content') for tag, attrs in page.nodes if tag == 'meta' and attrs.get('name') == 'description']
            require('class="nav-fees"' in text, f'{name}: shared fee action missing')
            footers.append(re.search(r'<footer\b.*?</footer>', text, re.S)[0])
    require(len(set(descriptions)) == 10, 'Page descriptions must be distinct')
    require(len(set(footers)) == 1, 'Footer must be consistent across all pages')
    sitemap = ET.fromstring((ROOT / 'sitemap.xml').read_text())
    require(len(sitemap) == 10, 'Sitemap must list the ten public pages')
    sitemap_urls = {node.text for node in sitemap.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
    canonical_urls = {identity['url'] + ('/' if name == 'index.html' else '/' + name) for name in pages if name != '404.html'}
    require(sitemap_urls == canonical_urls, 'Sitemap must match the public canonical URLs')
    require('Sitemap: ' + identity['url'] + '/sitemap.xml' in (ROOT / 'robots.txt').read_text(), 'robots.txt must identify the sitemap')
    require('Disallow: /\n' in (ROOT / 'robots.txt').read_text() if preview else 'Disallow: /\n' not in (ROOT / 'robots.txt').read_text(), 'robots.txt indexing mode incorrect')
    routes = json.loads((ROOT / 'vercel.json').read_text()).get('redirects', [])
    require(len({route['source'] for route in routes}) == len(routes), 'Duplicate redirect sources')
    for route in routes:
        target_exists('vercel.json', route['destination'])
        require(route['source'] != route['destination'], f'Redirect loop: {route}')
        require(route.get('permanent') is True, f'Legacy redirect must be permanent: {route["source"]}')
        require(urlsplit(route['destination']).path not in {r['source'] for r in routes}, f'Avoid a redirect chain: {route["source"]}')
    route_map = {route['source']: route['destination'] for route in routes}
    # Every recovered old school page needs a destination, except the unapproved testimonials.
    # This inventory comes from the archived school's navigation, not generated route guesses.
    legacy = json.loads((SOURCE / 'legacy-pages.json').read_text())
    legacy_paths = set(legacy['paths'])
    require(legacy_paths - {'/parent-testimonials'} <= route_map.keys(), 'Known old school pages are missing redirects')
    require('/parent-testimonials' not in route_map, 'Parent testimonials need approved content before a redirect is added')
    require(route_map.get('/index.html') == '/', 'Old index.html URL must redirect to the canonical homepage')
    old_pdf = '/wp-content/uploads/2023/08/Eduplanet-Application-Form-2024.pdf'
    require(route_map.get(old_pdf) == links['APPLICATION_PDF_URL'], 'Old application PDF must lead to the supplied current PDF')
    require(route_map.get('/get') == '/senior.html', 'Old Grade 8-9 GET page must lead to Senior Phase')
    for source, fragment in [('/facilities', '#facilities'), ('/important-documents', '#downloads'), ('/uniform', '#uniform')]:
        require(route_map.get(source, '').endswith(fragment), f'{source}: relevant replacement section missing')
    pdf_controls = [attrs for tag, attrs in pages['admissions.html'].nodes if 'data-application-pdf' in attrs]
    require(len(pdf_controls) == 1 and pdf_controls[0].get('href') == links['APPLICATION_PDF_URL'], 'Application PDF link must use the supplied Drive file')
    require('noindex' in texts['404.html'] and 'application/ld+json' not in texts['404.html'], '404 must remain unindexed with no copied Contact schema')
    for private in ('output', 'tmp', 'reports', 'tools'):
        require(private + '/' in (ROOT / '.vercelignore').read_text(), f'Vercel must exclude {private}')
        require("--exclude '" + private + "'" in (ROOT / '.github/workflows/pages.yml').read_text(), f'Pages must exclude {private}')
    require('Select your child’s phase.' in texts['academics.html'], 'Owner Academics edit must be preserved')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--preview', action='store_true')
    errors = check(parser.parse_args().preview)
    if errors:
        raise SystemExit('\n'.join(errors))
    print('PASS: page links, fees, application actions, indexing, canonical URLs, structured data, sitemap, legacy redirects and draft exclusions.')
