#!/usr/bin/env python3
"""Build only explicitly public content. No dependencies, no private-folder copies."""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit
import json
import hashlib
import os
import re
import shutil

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
DATA = json.loads((ROOT / 'content.json').read_text())
MEDIA = json.loads((ROOT / 'media.json').read_text())
STYLES = (ROOT / 'static/style.css').read_text()
APP_VERSION = hashlib.sha256((ROOT / 'static/app.js').read_bytes()).hexdigest()[:12]
ORIGIN = os.environ.get('PORTFOLIO_ORIGIN', DATA['production_origin']).rstrip('/')
PREVIEW = os.environ.get('VERCEL_ENV') in ('preview', 'development')
ANALYTICS = '''  <script>
    window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };
  </script>
  <script defer src="/_vercel/insights/script.js"></script>''' if os.environ.get('VERCEL_ENV') == 'production' else ''
if urlsplit(ORIGIN).scheme not in ('http', 'https') or not urlsplit(ORIGIN).netloc:
    raise SystemExit('PORTFOLIO_ORIGIN must be an absolute HTTP(S) URL')

def e(value):
    return escape(str(value), quote=True)

def paragraphs(items):
    return ''.join(f'<p>{e(p)}</p>' for p in items)

def responsive_image(src, alt, lazy=False, priority=False):
    media = MEDIA['images'][src]
    def srcset(fmt):
        return ', '.join(f'{item["src"]} {item["width"]}w' for item in media[fmt])
    loading = ' loading="lazy"' if lazy else ''
    fetch = ' fetchpriority="high"' if priority else ''
    return (f'<picture><source type="image/avif" srcset="{e(srcset("avif"))}" sizes="{e(media["sizes"])}">'
            f'<img src="{e(media["fallback"])}" srcset="{e(srcset("webp"))}" sizes="{e(media["sizes"])}" '
            f'width="{media["width"]}" height="{media["height"]}" alt="{e(alt)}" decoding="async"{loading}{fetch}></picture>')

def flow(project, large=False):
    nodes = ''.join(f'<span class="flow-node"><i aria-hidden="true">{i+1:02d}</i>{e(label)}</span>'
                    for i, label in enumerate(project['flow']))
    return f'<div class="flow {"flow-large" if large else ""}" aria-label="Workflow overview">{nodes}</div>'

def shell(title, description, body, path='/'):
    template = (ROOT / 'templates/shell.html').read_text()
    schema = {'@context':'https://schema.org', '@type':'Person', 'name':DATA['name'],
              'url':ORIGIN, 'sameAs':[DATA['linkedin'], DATA['youtube'], DATA['business']],
              'alumniOf':{'@type':'CollegeOrUniversity','name':'University of British Columbia'},
              'knowsAbout':['Applied AI','Workflow design','AI enablement','Python']}
    values = dict(DATA, title=e(title), description=e(description), body=body,
                  origin=e(ORIGIN), canonical=e(ORIGIN+path),
                  robots='<meta name="robots" content="noindex, nofollow">' if PREVIEW else '',
                  analytics=ANALYTICS,
                  styles=STYLES, app_version=APP_VERSION,
                  dm_sans_font=MEDIA['fonts']['dm-sans']['src'],
                  manrope_font=MEDIA['fonts']['manrope']['src'],
                  schema=json.dumps(schema).replace('<','\\u003c'))
    return re.sub(r'\{\{([a-z_]+)\}\}', lambda m:str(values[m.group(1)]), template)

def write(path, content):
    target = OUT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)

def project_card(p, i):
    return f'''<article class="project" data-category="{e(p['category'])}">
      <div class="project-index">{i:02d}</div>
      <div class="project-main"><div class="project-meta"><span>{e(p['context'])}</span><span class="status"><i></i>{e(p['status'])}</span></div>
      <h3><a href="/work/{e(p['slug'])}/">{e(p['name'])}<span class="project-arrow" aria-hidden="true">↗</span></a></h3>
      <p>{e(p['summary'])}</p><div class="project-bottom"><span>{e(p['product'])}</span><a href="/work/{e(p['slug'])}/">Read the case study <span aria-hidden="true">→</span></a></div></div>
      {flow(p)}</article>'''

def home():
    projects=''.join(project_card(p,i+1) for i,p in enumerate(DATA['projects']))
    notes=''.join(f'''<a class="note" href="/notes/{e(n['slug'])}/"><span class="eyebrow">{e(n['tag'])}</span><h3>{e(n['title'])}<span aria-hidden="true">↗</span></h3><p>{e(n['summary'])}</p><span class="note-read">Read note →</span></a>''' for n in DATA['notes'])
    method=''.join(f'''<div><span>{i+1:02d} — {e(item['label'])}</span><h3>{e(item['heading'])}</h3><p>{e(item['description'])}</p></div>''' for i,item in enumerate(DATA['method']))
    videos=''.join(f'''<a class="video-link" href="{e(v['url'])}"><div class="video-image">{responsive_image(v['thumbnail'], "", lazy=True)}<span class="play-mark" aria-hidden="true">↗</span></div><div><span class="eyebrow">{e(v['tag'])}</span><h3>{e(v['title'])}</h3><p>{e(v['description'])}</p><span class="note-read">Watch on YouTube ↗</span></div></a>''' for v in DATA['videos'])
    filters=''.join(f'<button type="button" aria-pressed="{str(category=="all").lower()}" data-filter="{category}">{label} <span>{sum(category=="all" or p["category"]==category for p in DATA["projects"]):02d}</span></button>' for category,label in [('all','All work'),('systems','AI systems'),('enablement','Enablement')])
    return f'''
    <section class="hero wrap">
      <div class="hero-copy"><p class="eyebrow"><span class="accent-line"></span>Applied AI · Systems · Enablement</p>
      <h1>I turn messy workflows into <em>working AI systems.</em></h1>
      <p class="hero-description">{e(DATA['hero_description'])}</p>
      <div class="hero-actions"><a class="button" href="#work">Explore my work <span aria-hidden="true">↓</span></a><a class="text-link" href="mailto:{e(DATA['email'])}">Get in touch ↗</a></div>
      <p class="hero-location"><span class="location-mark" aria-hidden="true">⌖</span> Greater Vancouver, BC <span> / </span> Open to remote & US opportunities</p></div>
      <div class="hero-side"><div class="portrait-frame">{responsive_image("/assets/vatsal.jpg", "Vatsal Jain", priority=True)}<span class="portrait-corner" aria-hidden="true">+</span><div class="portrait-caption"><span>Vatsal Jain</span><span>Founder, Clarity Works</span></div></div><div class="field-note"><span class="eyebrow">The through line</span><p>Understand the work.<br>Build the system.<br>Leave the team capable.</p><span class="field-note-arrow" aria-hidden="true">↙</span></div></div>
    </section>
    <div class="proof-strip wrap"><span>Business context.<br><strong>Technical execution.</strong></span><div><b>7</b><span>stages in the<br>outbound pipeline</span></div><div><b>3</b><span>LLM agents<br>working together</span></div><div><b>150</b><span>personalized outreach<br>messages per day</span></div></div>
    <section class="work-section wrap" id="work"><div class="section-heading"><div><p class="eyebrow">01 / Selected work</p><h2>From an operational problem<br>to something people can use.</h2></div><span class="section-aside">Built, shipped, and learning.</span></div>
      <div class="work-toolbar"><div class="filters" role="group" aria-label="Filter projects">{filters}</div><span id="project-count" aria-live="polite">{len(DATA['projects'])} projects</span></div>{projects}
    </section>
    <section class="approach-section" id="approach"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">02 / How I work</p><h2>Context. Process.<br>Then the build.</h2></div><p class="section-intro">My operating method at Clarity Works. Each step makes the next one more useful.</p></div><div class="approach-grid">{method}</div><a class="method-source text-link" href="https://www.tryclarityworks.com/philosophy">The philosophy behind the method ↗</a></div></section>
    <section class="about-section wrap" id="about"><div><p class="eyebrow">03 / A little context</p><h2>Economics by training.<br>A builder by practice.</h2><figure class="about-photo">{responsive_image(DATA['about']['photo'], DATA['about']['photo_alt'], lazy=True)}<figcaption>{e(DATA['about']['photo_caption'])}</figcaption></figure></div><div class="about-copy"><p class="lead">{e(DATA['about']['lead'])}</p>{paragraphs(DATA['about']['paragraphs'])}<div class="timeline"><div><span>2025 — Present</span><strong>Founder · Clarity Works</strong></div><div><span>2022</span><strong>Product Research Fellow · Circonomy</strong></div><div><span>2020 — 2024</span><strong>International Economics · UBC</strong></div></div><a class="text-link" href="{e(DATA['business'])}">More about Clarity Works ↗</a></div></section>
    <section class="video-section wrap" id="teaching"><div class="section-heading"><div><p class="eyebrow">04 / Teaching in the open</p><h2>See how I explain the work.</h2></div><a class="text-link" href="{e(DATA['youtube'])}">The full YouTube library ↗</a></div><div class="video-grid">{videos}</div></section>
    <section class="notes-section wrap" id="notes"><div class="section-heading"><div><p class="eyebrow">05 / Notes from the work</p><h2>What I’m thinking through.</h2></div></div><div class="notes-grid">{notes}</div></section>
    <section class="contact-section wrap" id="contact"><div class="contact-top"><p class="eyebrow"><i class="availability-dot"></i>Open to the right opportunity</p><span>Remote preferred · Open to the US</span></div><h2>Have a messy workflow<br>or an ambitious AI team?</h2><div class="contact-bottom"><p>I’m exploring Forward Deployed Engineer, AI Solutions Architect, and AI Enablement roles — as well as B2B engagements.</p><a class="button button-light" href="mailto:{e(DATA['email'])}">Let’s talk <span aria-hidden="true">↗</span></a></div></section>'''

def case_study(p):
    sections=''.join(f'<section class="story-section"><h2>{e(s["title"])}</h2><div>{paragraphs(s["paragraphs"])}</div></section>' for s in p['sections'])
    tags=''.join(f'<span>{e(t)}</span>' for t in p['stack'])
    external = f'<a class="button" href="{e(p["link"]["url"])}">{e(p["link"]["label"])} ↗</a>' if p.get('link') else ''
    metrics=''
    if p.get('metrics'):
        metric_items=''.join(f'<div><strong>{e(m["value"])}</strong><span>{e(m["label"])}</span></div>' for m in p['metrics'])
        metrics=f'<aside class="case-metrics" aria-label="Reported project results"><div>{metric_items}</div><p>{e(p["metrics_note"])}</p></aside>'
    stages=''
    if p.get('stages'):
        stage_items=''.join(f'<li><span>{i+1:02d}</span>{e(stage)}</li>' for i,stage in enumerate(p['stages']))
        stages=f'<section class="stage-section"><h2>The stages</h2><ol>{stage_items}</ol></section>'
    sources=''
    if p.get('sources'):
        source_items=''.join(f'<a href="{e(s["url"])}">{e(s["label"])} ↗</a>' for s in p['sources'])
        sources=f'<aside class="story-sources"><h2>More detail</h2><div>{source_items}</div></aside>'
    body=f'''<div class="wrap story"><a class="back-link" href="/#work">← All selected work</a><header class="story-header"><p class="eyebrow">{e(p['context'])} <span class="status"><i></i>{e(p['status'])}</span></p><h1>{e(p['name'])}</h1><p class="story-deck">{e(p['summary'])}</p></header><dl class="story-facts"><div><dt>Project</dt><dd>{e(p['product'])}</dd></div><div><dt>My role</dt><dd>{e(p['role'])}</dd></div><div><dt>Current outcome</dt><dd>{e(p['outcome'])}</dd></div></dl>{metrics}<div class="story-flow"><p class="eyebrow">The workflow, at a glance</p>{flow(p,True)}<p class="flow-caption">A simplified view of the workflow.</p></div>{stages}{sections}<section class="story-tools"><h2>Tools & focus</h2><div class="tags">{tags}</div></section>{sources}<div class="story-cta">{external}<a class="text-link" href="mailto:{e(DATA['email'])}">Talk about this work ↗</a></div></div>'''
    return shell(p['name']+' — Vatsal Jain',p['summary'],body,'/work/'+p['slug']+'/')

def note_page(n):
    body=f'''<article class="wrap note-page"><a class="back-link" href="/#notes">← Notes from the work</a><header><p class="eyebrow">{e(n['tag'])} / October 2026</p><h1>{e(n['title'])}</h1><p class="story-deck">{e(n['summary'])}</p></header><div class="prose">{paragraphs(n['paragraphs'])}</div><div class="note-signature"><img src="{e(MEDIA['images']['/assets/vatsal.jpg']['webp'][0]['src'])}" width="52" height="52" alt="" loading="lazy" decoding="async"><div><strong>Vatsal Jain</strong><p>Founder, Clarity Works · Applied AI & systems</p></div></div><a class="text-link" href="mailto:{e(DATA['email'])}">Continue the conversation ↗</a></article>'''
    return shell(n['title']+' — Vatsal Jain',n['summary'],body,'/notes/'+n['slug']+'/')

if __name__ == '__main__':
    slugs=[p['slug'] for p in DATA['projects']]+[n['slug'] for n in DATA['notes']]
    if len(slugs)!=len(set(slugs)) or any(not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',s) for s in slugs):
        raise SystemExit('Content slugs must be unique URL-safe strings')
    if OUT.exists(): shutil.rmtree(OUT)
    shutil.copytree(ROOT / 'static', OUT)
    write('index.html',shell('Vatsal Jain — '+DATA['title'],DATA['description'],home()))
    for p in DATA['projects']: write('work/'+p['slug']+'/index.html',case_study(p))
    for n in DATA['notes']: write('notes/'+n['slug']+'/index.html',note_page(n))
    write('404.html',shell('Page not found — Vatsal Jain','Return to Vatsal Jain’s portfolio.','<section class="wrap not-found"><p class="eyebrow">404 / A loose end</p><h1>This page has moved<br>or doesn’t exist.</h1><a class="button" href="/">Back to the portfolio →</a></section>'))
    paths=['/']+['/work/'+p['slug']+'/' for p in DATA['projects']]+['/notes/'+n['slug']+'/' for n in DATA['notes']]
    write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+e(ORIGIN+p)+'</loc></url>' for p in paths)+'</urlset>')
    write('robots.txt','User-agent: *\n'+('Disallow: /\n' if PREVIEW else 'Allow: /\nSitemap: '+ORIGIN+'/sitemap.xml\n'))
    print(f'Built {len(paths)} content pages plus 404 in {OUT}')
