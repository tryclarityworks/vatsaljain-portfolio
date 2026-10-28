#!/usr/bin/env python3
"""Build only explicitly public content. No dependencies, no private-folder copies."""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit, quote
from datetime import datetime, timezone
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

def arrow(direction='diagonal'):
    paths = {'diagonal': 'M5 19 19 5M5 5h14v14',
             'right': 'M4 12h16m-7-7 7 7-7 7',
             'left': 'M20 12H4m7-7-7 7 7 7',
             'down': 'M12 4v16m-7-7 7 7 7-7'}
    return f'<svg class="arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true" focusable="false"><path d="{paths[direction]}"/></svg>'


def contact_action(placement):
    booking = DATA.get('booking')
    if booking:
        url = urlsplit(booking['url'])
        if url.scheme != 'https' or url.netloc != 'cal.com' or url.query or url.fragment or not re.fullmatch(r'/[a-z0-9-]+/[a-z0-9-]+', url.path):
            raise ValueError('Booking URL must be a verified public Cal.com event URL')
        label = f'Book a {booking["duration_minutes"]}-min call' if placement == 'contact' else 'Book a call'
        href = booking['url']
    else:
        label = 'Get in touch' if placement == 'hero' else 'Let’s talk'
        href = 'mailto:' + DATA['email']
    classes = {'nav': 'nav-contact', 'hero': 'text-link', 'contact': 'button button-light'}
    return f'<a class="{classes[placement]}" href="{e(href)}">{e(label)} {arrow()}</a>'


def flow(project, large=False):
    nodes = ''.join(f'<li class="flow-node">{e(label)}{arrow("down") if i < len(project["flow"])-1 else ""}</li>'
                    for i, label in enumerate(project['flow']))
    return f'<ol class="flow {"flow-large" if large else ""}" aria-label="Workflow overview">{nodes}</ol>'

def banner():
    note = DATA['announcement']
    if datetime.fromisoformat(note['until']) <= datetime.now(timezone.utc):
        return ''
    subject = quote(note['subject'])
    return (f'  <div class="announce" data-until="{e(note["until"])}"><p><strong>{e(note["lead"])}</strong> {e(note["text"])} '
            f'<a href="mailto:{e(DATA["email"])}?subject={subject}">{e(note["link_label"])} {arrow()}</a></p></div>')

def shell(title, description, body, path='/'):
    template = (ROOT / 'templates/shell.html').read_text()
    schema = {'@context':'https://schema.org', '@type':'Person', 'name':DATA['name'],
              'url':ORIGIN, 'sameAs':[DATA['linkedin'], DATA['youtube'], DATA['business']],
              'alumniOf':{'@type':'CollegeOrUniversity','name':'University of British Columbia'},
              'knowsAbout':['Applied AI','Workflow design','AI enablement','Python']}
    values = dict(DATA, title=e(title), description=e(description), body=body,
                  origin=e(ORIGIN), canonical=e(ORIGIN+path),
                  robots='<meta name="robots" content="noindex, nofollow">' if PREVIEW else '',
                  analytics=ANALYTICS, banner=banner(), arrow_diagonal=arrow(), nav_contact=contact_action('nav'),
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
    proof = '<p class="outbound-proof">7 stages · 3 LLM agents · 150 personalized messages per day</p>' if p['slug'] == 'outbound-engine' else ''
    return f'''<article class="project {'project-featured' if i == 1 else ''}" data-category="{e(p['category'])}">
      <div class="project-main"><h3><a href="/work/{e(p['slug'])}/">{e(p['name'])}</a></h3>
      <div class="project-meta"><span>{e(p['context'])}</span><span class="status">{e(p['status'])}</span></div>
      <p>{e(p['summary'])}</p>{proof}<div class="project-bottom"><span>{e(p['product'])}</span><a class="text-link" href="/work/{e(p['slug'])}/">Read the case study {arrow('right')}</a></div></div>
      {flow(p)}</article>'''


def home():
    email_alternative = f'<a class="text-link contact-email" href="mailto:{e(DATA["email"])}">Or send an email {arrow()}</a>' if DATA.get('booking') else ''
    projects=''.join(project_card(p,i+1) for i,p in enumerate(DATA['projects']))
    notes=''.join(f'''<a class="note" href="/notes/{e(n['slug'])}/"><h3>{e(n['title'])}{arrow()}</h3><p class="content-meta">{e(n['tag'])}</p><p>{e(n['summary'])}</p><span class="note-read">Read note {arrow('right')}</span></a>''' for n in DATA['notes'])
    method=''.join(f'''<li><h3>{e(item['heading'])}</h3><p>{e(item['description'])}</p><span class="method-label">{e(item['label'])}</span></li>''' for item in DATA['method'])
    videos=''.join(f'''<a class="video-link" href="{e(v['url'])}"><div class="video-image">{responsive_image(v['thumbnail'], "", lazy=True)}<span class="play-mark">{arrow()}</span></div><div><h3>{e(v['title'])}</h3><p class="content-meta">{e(v['tag'])}</p><p>{e(v['description'])}</p><span class="note-read">Watch on YouTube {arrow()}</span></div></a>''' for v in DATA['videos'])
    filters=''.join(f'<button type="button" aria-pressed="{str(category=="all").lower()}" data-filter="{category}">{label} <span>{sum(category=="all" or p["category"]==category for p in DATA["projects"])}</span></button>' for category,label in [('all','All work'),('systems','AI systems'),('enablement','Enablement')])
    stack=''.join(f'<div><dt>{e(group["label"])}</dt><dd>{e(" · ".join(group["items"]))}</dd></div>' for group in DATA['stack'])
    return f'''
    <section class="hero wrap" aria-labelledby="hero-title">
      <div class="hero-copy"><h1 id="hero-title">Applied AI,<br>built around real work.</h1>
      <p class="hero-description">{e(DATA['hero_description'])}</p>
      <div class="hero-actions"><a class="button" href="#work">Explore my work {arrow('down')}</a>{contact_action('hero')}</div>
      <p class="hero-location">Greater Vancouver, BC<br>Canadian citizen · Work from Canada, no US visa sponsorship needed</p></div>
      <div class="hero-side"><figure class="portrait-frame">{responsive_image("/assets/vatsal.jpg", "Vatsal Jain", priority=True)}<figcaption><strong>Vatsal Jain</strong><span>Founder, Clarity Works</span></figcaption></figure><p class="field-note">Understand the work. Build the system.<br>Leave the team capable.</p></div>
    </section>
    <section class="work-section wrap" id="work"><div class="section-heading"><h2>Selected work.</h2><p>From an operational problem to something people can use. Built, shipped, and learning.</p></div>
      <div class="work-toolbar"><div class="filters" role="group" aria-label="Filter projects" hidden>{filters}</div><span id="project-count" role="status" aria-live="polite" aria-atomic="true">{len(DATA['projects'])} projects</span></div><div class="project-list">{projects}</div>
      <div class="stack"><h3>What the work is built with</h3><dl>{stack}</dl></div>
    </section>
    <section class="approach-section" id="approach"><div class="wrap"><div class="section-heading"><h2>Context. Process.<br>Then the build.</h2><p>My operating method at Clarity Works. Each step makes the next one more useful.</p></div><ol class="approach-grid">{method}</ol><a class="method-source text-link" href="https://www.tryclarityworks.com/philosophy">The philosophy behind the method {arrow()}</a></div></section>
    <section class="about-section wrap" id="about"><div><h2>Economics by training.<br>A builder by practice.</h2><figure class="about-photo">{responsive_image(DATA['about']['photo'], DATA['about']['photo_alt'], lazy=True)}<figcaption>{e(DATA['about']['photo_caption'])}</figcaption></figure></div><div class="about-copy"><p class="lead">{e(DATA['about']['lead'])}</p>{paragraphs(DATA['about']['paragraphs'])}<div class="timeline"><div><span>2025 — Present</span><strong>Founder · Clarity Works</strong></div><div><span>2022</span><strong>Product Research Fellow · Circonomy</strong></div><div><span>2020 — 2024</span><strong>International Economics · UBC</strong></div></div><a class="text-link" href="{e(DATA['business'])}">More about Clarity Works {arrow()}</a></div></section>
    <section class="video-section wrap" id="teaching"><div class="section-heading"><h2>See how I explain the work.</h2><a class="text-link" href="{e(DATA['youtube'])}">The full YouTube library {arrow()}</a></div><div class="video-grid">{videos}</div></section>
    <section class="notes-section wrap" id="notes"><div class="section-heading"><h2>Notes from the work.</h2></div><div class="notes-grid">{notes}</div></section>
    <section class="contact-section wrap" id="contact"><div class="contact-heading"><h2>Let’s talk about<br>the work.</h2><p>Open to the right opportunity.<br>Remote preferred · Open to the US</p>{contact_action('contact')}{email_alternative}</div><div class="contact-copy"><p>I’m exploring Forward Deployed Engineer, AI Solutions Architect, and AI Enablement roles, plus scoped B2B builds.</p><p><strong>Remote from Canada.</strong> I can work with US teams as an employee, or as a contractor through Clarity Works LLP, registered in British Columbia. Work performed in Canada doesn’t need US visa sponsorship.</p><p><strong>In person in the US.</strong> Open to travel for meetings and to relocating for the right role. Work authorization would be settled per role.</p></div></section>'''

def case_study(p):
    sections=''.join(f'<section class="story-section"><h2>{e(s["title"])}</h2><div>{paragraphs(s["paragraphs"])}</div></section>' for s in p['sections'])
    tags=''.join(f'<span>{e(t)}</span>' for t in p['stack'])
    external = f'<a class="button" href="{e(p["link"]["url"])}">{e(p["link"]["label"])} {arrow()}</a>' if p.get('link') else ''
    metrics=''
    if p.get('metrics'):
        metric_items=''.join(f'<div><strong>{e(m["value"])}</strong><span>{e(m["label"])}</span></div>' for m in p['metrics'])
        metrics=f'<aside class="case-metrics" aria-label="Reported project results"><div>{metric_items}</div><p>{e(p["metrics_note"])}</p></aside>'
    stages=''
    if p.get('stages'):
        stage_items=''.join(f'<li>{e(stage)}</li>' for stage in p['stages'])
        stages=f'<section class="stage-section"><h2>The stages</h2><ol>{stage_items}</ol></section>'
    sources=''
    if p.get('sources'):
        source_items=''.join(f'<a href="{e(s["url"])}">{e(s["label"])} {arrow()}</a>' for s in p['sources'])
        sources=f'<aside class="story-sources"><h2>More detail</h2><div>{source_items}</div></aside>'
    body=f'''<div class="wrap story"><a class="back-link" href="/#work">{arrow('left')} All selected work</a><header class="story-header"><h1>{e(p['name'])}</h1><p class="content-meta">{e(p['context'])} <span class="status">{e(p['status'])}</span></p><p class="story-deck">{e(p['summary'])}</p></header><dl class="story-facts"><div><dt>Project</dt><dd>{e(p['product'])}</dd></div><div><dt>My role</dt><dd>{e(p['role'])}</dd></div><div><dt>Current outcome</dt><dd>{e(p['outcome'])}</dd></div></dl>{metrics}<div class="story-flow"><p class="content-meta">The workflow, at a glance</p>{flow(p,True)}<p class="flow-caption">A simplified view of the workflow.</p></div>{stages}{sections}<section class="story-tools"><h2>Tools & focus</h2><div class="tags">{tags}</div></section>{sources}<div class="story-cta">{external}<a class="text-link" href="mailto:{e(DATA['email'])}">Talk about this work {arrow()}</a></div></div>'''
    return shell(p['name']+' — Vatsal Jain',p['summary'],body,'/work/'+p['slug']+'/')

def note_page(n):
    body=f'''<article class="wrap note-page"><a class="back-link" href="/#notes">{arrow('left')} Notes from the work</a><header><h1>{e(n['title'])}</h1><p class="content-meta">{e(n['tag'])} / October 2026</p><p class="story-deck">{e(n['summary'])}</p></header><div class="prose">{paragraphs(n['paragraphs'])}</div><div class="note-signature"><img src="{e(MEDIA['images']['/assets/vatsal.jpg']['webp'][0]['src'])}" width="52" height="52" alt="" loading="lazy" decoding="async"><div><strong>Vatsal Jain</strong><p>Founder, Clarity Works · Applied AI & systems</p></div></div><a class="text-link" href="mailto:{e(DATA['email'])}">Continue the conversation {arrow()}</a></article>'''
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
    write('404.html',shell('Page not found — Vatsal Jain','Return to Vatsal Jain’s portfolio.',f'<section class="wrap not-found"><p class="content-meta">404 / A loose end</p><h1>This page has moved<br>or doesn’t exist.</h1><a class="button" href="/">Back to the portfolio {arrow("right")}</a></section>'))
    paths=['/']+['/work/'+p['slug']+'/' for p in DATA['projects']]+['/notes/'+n['slug']+'/' for n in DATA['notes']]
    write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+e(ORIGIN+p)+'</loc></url>' for p in paths)+'</urlset>')
    write('robots.txt','User-agent: *\n'+('Disallow: /\n' if PREVIEW else 'Allow: /\nSitemap: '+ORIGIN+'/sitemap.xml\n'))
    print(f'Built {len(paths)} content pages plus 404 in {OUT}')
