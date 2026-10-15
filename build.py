#!/usr/bin/env python3
"""Build only explicitly public content. No dependencies, no private-folder copies."""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit
import json
import os
import re
import shutil

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
DATA = json.loads((ROOT / 'content.json').read_text())
ORIGIN = os.environ.get('PORTFOLIO_ORIGIN', 'https://vatsal-jain-portfolio.windygoose17.chatgpt.site').rstrip('/')
if urlsplit(ORIGIN).scheme not in ('http', 'https') or not urlsplit(ORIGIN).netloc:
    raise SystemExit('PORTFOLIO_ORIGIN must be an absolute HTTP(S) URL')

def e(value):
    return escape(str(value), quote=True)

def paragraphs(items):
    return ''.join(f'<p>{e(p)}</p>' for p in items)

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
                  origin=e(ORIGIN), canonical=e(ORIGIN+path), schema=json.dumps(schema).replace('<','\\u003c'))
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
    return f'''
    <section class="hero wrap">
      <div class="hero-copy"><p class="eyebrow"><span class="blue-line"></span>Applied AI · Systems · Enablement</p>
      <h1>I turn messy workflows into <em>working AI systems.</em></h1>
      <p class="hero-description">I’m Vatsal — a founder and hands-on builder. I connect client discovery, code, and capability transfer to make AI useful in the work people already do.</p>
      <div class="hero-actions"><a class="button" href="#work">Explore my work <span aria-hidden="true">↓</span></a><a class="text-link" href="mailto:{e(DATA['email'])}">Get in touch ↗</a></div>
      <p class="hero-location"><span class="location-mark" aria-hidden="true">⌖</span> Greater Vancouver, BC <span> / </span> Open to remote & US opportunities</p></div>
      <div class="hero-side"><div class="portrait-frame"><img src="/assets/vatsal.jpg" width="1200" height="1600" alt="Vatsal Jain" fetchpriority="high"><span class="portrait-corner" aria-hidden="true">+</span><div class="portrait-caption"><span>Vatsal Jain</span><span>Founder, Clarity Works</span></div></div><div class="field-note"><span class="eyebrow">The through line</span><p>Understand the work.<br>Build the system.<br>Leave the team capable.</p><span class="field-note-arrow" aria-hidden="true">↙</span></div></div>
    </section>
    <div class="proof-strip wrap"><span>Business context.<br><strong>Technical execution.</strong></span><div><b>7</b><span>stages in the<br>outbound pipeline</span></div><div><b>3</b><span>LLM agents<br>working together</span></div><div><b>60+</b><span>personalized outreach<br>messages per day</span></div></div>
    <section class="work-section wrap" id="work"><div class="section-heading"><div><p class="eyebrow">01 / Selected work</p><h2>From an operational problem<br>to something people can use.</h2></div><span class="section-aside">Built, shipped, and learning.</span></div>
      <div class="work-toolbar"><div class="filters" role="group" aria-label="Filter projects"><button type="button" aria-pressed="true" data-filter="all">All work <span>05</span></button><button type="button" aria-pressed="false" data-filter="systems">AI systems <span>04</span></button><button type="button" aria-pressed="false" data-filter="enablement">Enablement <span>01</span></button></div><span id="project-count" aria-live="polite">5 projects</span></div>{projects}
    </section>
    <section class="approach-section" id="approach"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">02 / How I work</p><h2>The build starts<br>with a better question.</h2></div><p class="section-intro">The software matters. So do the process it fits into and the people who will use it.</p></div><div class="approach-grid"><div><span>01 — Discover</span><h3>Find the real constraint.</h3><p>Talk to the team, map the workflow, and turn an ambiguous request into a problem worth solving.</p></div><div><span>02 — Build</span><h3>Connect reasoning to action.</h3><p>Use Python, APIs, and agent workflows to ship a useful system, with explicit checks around model output.</p></div><div><span>03 — Enable</span><h3>Make it usable without me.</h3><p>Explain the decisions, document the process, and help the team own what happens next.</p></div></div></div></section>
    <section class="about-section wrap" id="about"><div><p class="eyebrow">03 / A little context</p><h2>Economics by training.<br>A builder by practice.</h2></div><div class="about-copy"><p class="lead">I’m interested in the space between what a business needs and what the technology can actually do.</p><p>I studied International Economics at UBC, then built Clarity Works to help non-technical teams develop practical AI capability. My work moves between client conversations, workflow design, Python pipelines, and hands-on teaching.</p><p>I build with Claude Code and Codex, work with Python and SQL, and have foundational TypeScript experience. My focus is understanding the logic, the failure modes, and the operational outcome.</p><div class="timeline"><div><span>2025 — Present</span><strong>Founder · Clarity Works</strong></div><div><span>2022</span><strong>Product Research Fellow · Circonomy</strong></div><div><span>2020 — 2024</span><strong>International Economics · UBC</strong></div></div><a class="text-link" href="{e(DATA['business'])}">More about Clarity Works ↗</a></div></section>
    <section class="notes-section wrap" id="notes"><div class="section-heading"><div><p class="eyebrow">04 / Notes from the work</p><h2>What I’m thinking through.</h2></div><a class="text-link" href="{e(DATA['youtube'])}">Watch on YouTube ↗</a></div><div class="notes-grid">{notes}</div></section>
    <section class="contact-section wrap" id="contact"><div class="contact-top"><p class="eyebrow"><i class="availability-dot"></i>Open to the right opportunity</p><span>Remote preferred · Open to the US</span></div><h2>Have a messy workflow<br>or an ambitious AI team?</h2><div class="contact-bottom"><p>I’m exploring Forward Deployed Engineer, AI Solutions Architect, and AI Enablement roles — as well as B2B engagements.</p><a class="button button-light" href="mailto:{e(DATA['email'])}">Let’s talk <span aria-hidden="true">↗</span></a></div></section>'''

def case_study(p):
    sections=''.join(f'<section class="story-section"><h2>{e(s["title"])}</h2><div>{paragraphs(s["paragraphs"])}</div></section>' for s in p['sections'])
    tags=''.join(f'<span>{e(t)}</span>' for t in p['stack'])
    external = f'<a class="button" href="{e(p["link"]["url"])}">{e(p["link"]["label"])} ↗</a>' if p.get('link') else ''
    body=f'''<div class="wrap story"><a class="back-link" href="/#work">← All selected work</a><header class="story-header"><p class="eyebrow">{e(p['context'])} <span class="status"><i></i>{e(p['status'])}</span></p><h1>{e(p['name'])}</h1><p class="story-deck">{e(p['summary'])}</p></header><dl class="story-facts"><div><dt>Project</dt><dd>{e(p['product'])}</dd></div><div><dt>My role</dt><dd>{e(p['role'])}</dd></div><div><dt>Current outcome</dt><dd>{e(p['outcome'])}</dd></div></dl><div class="story-flow"><p class="eyebrow">The workflow, at a glance</p>{flow(p,True)}<p class="flow-caption">A simplified view of the workflow.</p></div>{sections}<section class="story-tools"><h2>Tools & focus</h2><div class="tags">{tags}</div></section><div class="story-cta">{external}<a class="text-link" href="mailto:{e(DATA['email'])}">Talk about this work ↗</a></div></div>'''
    return shell(p['name']+' — Vatsal Jain',p['summary'],body,'/work/'+p['slug']+'/')

def note_page(n):
    body=f'''<article class="wrap note-page"><a class="back-link" href="/#notes">← Notes from the work</a><header><p class="eyebrow">{e(n['tag'])} / October 2026</p><h1>{e(n['title'])}</h1><p class="story-deck">{e(n['summary'])}</p></header><div class="prose">{paragraphs(n['paragraphs'])}</div><div class="note-signature"><img src="/assets/vatsal.jpg" width="52" height="52" alt=""><div><strong>Vatsal Jain</strong><p>Founder, Clarity Works · Applied AI & systems</p></div></div><a class="text-link" href="mailto:{e(DATA['email'])}">Continue the conversation ↗</a></article>'''
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
    write('robots.txt','User-agent: *\nAllow: /\nSitemap: '+ORIGIN+'/sitemap.xml\n')
    print(f'Built {len(paths)} content pages plus 404 in {OUT}')
