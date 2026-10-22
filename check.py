#!/usr/bin/env python3
"""Check generated pages, internal links, metadata, and the publication boundary."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import os
import re

ROOT=Path(__file__).resolve().parent
DIST=ROOT/'dist'

class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.ids=[];self.h1=0;self.description=False;self.canonical=False
        self.canonical_url='';self.robots='';self.og_image=''
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='h1':self.h1+=1
        if 'id' in attrs:self.ids.append(attrs['id'])
        if tag=='meta' and attrs.get('name')=='description':self.description=bool(attrs.get('content'))
        if tag=='link' and attrs.get('rel')=='canonical':self.canonical=True;self.canonical_url=attrs.get('href','')
        if tag=='meta' and attrs.get('name')=='robots':self.robots=attrs.get('content','')
        if tag=='meta' and attrs.get('property')=='og:image':self.og_image=attrs.get('content','')
        for attr in ['href','src']:
            if attrs.get(attr):self.links.append(attrs[attr])
        if tag=='img' and 'alt' not in attrs:raise ValueError('Image missing alt attribute')

def main():
    files=list(DIST.rglob('*'));htmls=list(DIST.rglob('*.html'));pages={}
    data=json.loads((ROOT/'content.json').read_text())
    origin=os.environ.get('PORTFOLIO_ORIGIN',data['production_origin']).rstrip('/')
    preview=os.environ.get('VERCEL_ENV') in ('preview','development')
    assert len(htmls)==len(data['projects'])+len(data['notes'])+2,'Unexpected page count'
    for path in htmls:
        raw=path.read_text();page=Page();page.feed(raw);pages[path.resolve()]=page
        assert page.h1==1,f'{path}: expected one H1'
        assert page.description and page.canonical,f'{path}: missing metadata'
        relative=path.relative_to(DIST).as_posix()
        page_path='/' if relative in ('index.html','404.html') else '/'+relative.removesuffix('index.html')
        assert page.canonical_url==origin+page_path,f'{path}: wrong canonical origin or path'
        assert page.og_image==origin+'/assets/social.png',f'{path}: wrong social image origin'
        assert ('noindex' in page.robots)==preview,f'{path}: wrong indexing policy for build environment'
        assert len(page.ids)==len(set(page.ids)),f'{path}: duplicate IDs'
        assert not re.search(r'\{\{[a-z_]+\}\}',raw),f'{path}: unresolved template'
        for match in re.findall(r'<script type="application/ld\+json">(.*?)</script>',raw,re.S):json.loads(match)
    for path,page in pages.items():
        for href in page.links:
            url=urlsplit(href)
            if url.scheme or url.netloc:continue
            target=(DIST/unquote(url.path.lstrip('/'))) if url.path.startswith('/') else (path.parent/unquote(url.path))
            if not url.path:target=path
            if target.is_dir():target=target/'index.html'
            target=target.resolve()
            assert target.is_relative_to(DIST.resolve()),f'{path}: link escapes output'
            assert target.is_file(),f'{path}: missing local asset or page {href}'
            if url.fragment and target in pages:assert unquote(url.fragment) in pages[target].ids,f'{path}: missing anchor {href}'
    allowed_roots={'assets','work','notes'}
    allowed_files={'index.html','404.html','sitemap.xml','robots.txt','style.css','app.js'}
    for path in files:
        if not path.is_file():continue
        rel=path.relative_to(DIST)
        assert rel.parts[0] in allowed_roots or str(rel) in allowed_files,f'Unexpected public file: {rel}'
        assert path.suffix.lower() not in ['.pdf','.csv','.md','.json','.env'],f'Private/source format in output: {rel}'
        if path.suffix in ['.html','.js','.css','.xml','.txt']:
            text=path.read_text()
            for private in ['opportunities.csv','activity.csv','career/preferences','source_repository_credential','token_expires_at','minimum_annual_compensation']:
                assert private not in text,f'Private field in public output: {rel}'
    print(f'Passed: {len(htmls)} HTML pages, internal links/anchors, image alt attributes, metadata, JSON-LD, and public output boundary.')
    robots=(DIST/'robots.txt').read_text()
    assert ('Disallow: /' in robots)==preview,'Wrong robots.txt policy for build environment'
    print(f'Passed: canonical URLs use {origin}; indexing policy matches the build environment.')

if __name__=='__main__':main()
