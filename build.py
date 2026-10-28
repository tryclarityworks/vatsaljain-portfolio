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
    label_html = '<span>Book<span class="nav-call-suffix"> a call</span></span>' if placement == 'nav' and booking else e(label)
    name = ' aria-label="Book a call"' if placement == 'nav' and booking else ''
    return f'<a class="{classes[placement]}" href="{e(href)}"{name}>{label_html} {arrow()}</a>'


def flow(project, large=False):
    nodes = ''.join(f'<li class="flow-node">{e(label)}{arrow("down") if i < len(project["flow"])-1 else ""}</li>'
                    for i, label in enumerate(project['flow']))
    return f'<ol class="flow {"flow-large" if large else ""}" aria-label="Workflow overview">{nodes}</ol>'

def banner():
    note = DATA.get('announcement')
    if not note or datetime.fromisoformat(note['until']) <= datetime.now(timezone.utc):
        return ''
    subject = quote(note['subject'])
    return (f'  <div class="announce" data-until="{e(note["until"])}"><p><strong>{e(note["lead"])}</strong> {e(note["text"])} '
            f'<a href="mailto:{e(DATA["email"])}?subject={subject}">{e(note["link_label"])} {arrow()}</a></p></div>')

def shell(title, description, body, path='/'):
    template = (ROOT / 'templates/shell.html').read_text()
    sections = [('/work/', 'Work'), ('/about/', 'About'), ('/notes/', 'Notes'), ('/contact/', 'Contact')]
    def nav_link(href, label):
        current = ' aria-current="page"' if path == href else (' aria-current="location"' if path.startswith(href) else '')
        return f'<a href="{href}"{current}>{label}</a>'
    nav_links = ''.join(nav_link(href, label) for href, label in sections)
    schema = {'@context':'https://schema.org', '@type':'Person', 'name':DATA['name'],
              'url':ORIGIN, 'sameAs':[DATA['linkedin'], DATA['youtube'], DATA['business']],
              'alumniOf':{'@type':'CollegeOrUniversity','name':'University of British Columbia'},
              'knowsAbout':['Applied AI','Workflow design','AI enablement','Python']}
    values = dict(DATA, title=e(title), description=e(description), body=body,
                  origin=e(ORIGIN), canonical=e(ORIGIN+path),
                  robots='<meta name="robots" content="noindex, nofollow">' if PREVIEW else '',
                  analytics=ANALYTICS, banner=banner(), arrow_diagonal=arrow(), nav_contact=contact_action('nav'), nav_links=nav_links,
                  styles=STYLES, app_version=APP_VERSION,
                  dm_sans_font=MEDIA['fonts']['dm-sans']['src'],
                  manrope_font=MEDIA['fonts']['manrope']['src'],
                  schema=json.dumps(schema).replace('<','\\u003c'))
    return re.sub(r'\{\{([a-z_]+)\}\}', lambda m:str(values[m.group(1)]), template)

def write(path, content):
    target = OUT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)

def project_art(p):
    """A labeled visual representation of supported project facts."""
    if p['visual'] == 'signals':
        return f'''<div class="artifact artifact-signals"><div class="signal-flow"><div class="signal-source"><strong data-reveal>Newsletter &<br>website signals</strong><span data-reveal>Checked every 15 minutes</span></div>{arrow('right')}<div class="signal-result"><strong data-reveal>Contact record<br>+ AI draft</strong><span data-reveal>For advisor review</span></div></div></div>'''
    if p['visual'] == 'newsletter':
        return '''<div class="artifact artifact-newsletter"><div class="newsletter-sheet"><div class="newsletter-brand" data-reveal>Infnty <span>AI for your work</span></div><div class="newsletter-body"><span data-reveal>Personal AI briefing</span><strong data-reveal>One useful workflow.<br>Made relevant to you.</strong><p data-reveal>Practical application and the news behind it.</p></div><div class="newsletter-foot">Illustrative newsletter format</div></div></div>'''
    return '''<div class="artifact artifact-outbound"><div class="outbound-process"><span data-reveal>Research</span><span data-reveal>Enrich · Route · Draft</span><strong data-reveal>Human approval</strong><p data-reveal>150 personalized messages a day, up from about 10.</p></div></div>'''


def featured_projects(projects, context='work'):
    by_slug={p['slug']:p for p in DATA['projects']}
    names={'intent-signals':'Follow-up, with context.','infnty':'Infnty: AI for your work.','outbound-engine':'The outbound engine.'}
    return ''.join(f'''<article class="folio-entry project project-{e(p['visual'])}" data-category="{e(by_slug[p['slug']]['category'])}">
      <a class="project-cover" href="/work/{e(p['slug'])}/">{project_art(p)}</a>
      <div class="project-main"><h3><a href="/work/{e(p['slug'])}/">{e(names[p['slug']])} {arrow()}</a></h3>
      <p class="project-status">{e(p['detail'])}</p><p>{e(p['description'])}</p>
      <div class="project-bottom"><span>{e(p['contribution'])}</span><a class="text-link" href="/work/{e(p['slug'])}/">Explore project {arrow('right')}</a></div></div></article>''' for p in projects)


def compact_projects():
    by_slug={p['slug']:p for p in DATA['projects']}
    return ''.join(f'''<article class="project project-compact" data-category="{e(by_slug[p['slug']]['category'])}"><a href="/work/{e(p['slug'])}/"><h3>{e(p['title'])} {arrow()}</h3><p>{e(p['description'])}</p><span class="project-status">{e(p['status'])}</span></a></article>''' for p in DATA['home']['other_projects'])


def video_links():
    return ''.join(f'''<a class="video-link" href="{e(v['url'])}"><div class="video-image">{responsive_image(v['thumbnail'], "", lazy=True)}<span class="play-mark">{arrow()}</span></div><div class="video-caption"><h3>{e(v['title'])}</h3><span>Watch on YouTube {arrow()}</span></div></a>''' for v in DATA['videos'])


def note_links():
    return ''.join(f'''<a class="note" href="/notes/{e(n['slug'])}/"><div><h3>{e(n.get('home_title', n['title']))}</h3><p>{e(n['tag'])}</p></div>{arrow()}</a>''' for n in DATA['notes'])


def home():
    copy=DATA['home']
    return f'''
    <section class="home-stage"><div class="wrap stage-grid">
      <div class="stage-intro"><h1>Hi, I’m Vatsal.<br>I build useful AI.</h1><p>I turn real business problems into systems that people can actually use.</p>
        <div class="hero-actions"><a class="button" href="/work/">Explore my work {arrow('right')}</a><a class="text-link" href="/about/">About me {arrow('right')}</a></div>
        <p class="hero-location">{e(copy['availability'])}</p></div>
      <figure class="stage-portrait">{responsive_image('/assets/vatsal.jpg', 'Vatsal Jain', priority=True)}<figcaption><span>Vatsal Jain</span><span>Vancouver, BC</span></figcaption></figure>
      <section class="home-work" id="work"><div class="section-heading"><h2>Selected work.</h2><a class="text-link" href="/work/">All projects {arrow('right')}</a></div><div class="home-projects">{featured_projects(copy['projects'][:2])}</div></section>
    </div></section>
    <section class="home-more wrap" id="about"><div><h2>Curious about how the work gets done?</h2><p>My background is in economics. These days I work across the business problem, the workflow, and the build.</p><a class="text-link" href="/about/">More about me {arrow('right')}</a></div><a class="home-media" href="/notes/" id="notes">{responsive_image(DATA['videos'][0]['thumbnail'], '', lazy=True)}<div id="teaching"><strong>Ideas from the work.</strong><span>Notes & videos</span>{arrow()}</div></a></section>
    <section class="contact-section home-contact wrap" id="contact"><div class="contact-heading"><h2>Let’s work<br>together.</h2><p>{e(copy['contact_description'])}</p><div class="contact-actions">{contact_action('contact')}<a class="text-link" href="/contact/">Contact details {arrow('right')}</a></div></div><div class="contact-copy"><p>Based in Canada.<br>Remote preferred. Open to the US.</p></div></section>'''


def work_page():
    categories=[('all','All work'),('systems','AI systems'),('enablement','Enablement')]
    filters=''.join(f'<button type="button" aria-pressed="{str(category=="all").lower()}" data-filter="{category}">{label} <span>{sum(category=="all" or p["category"]==category for p in DATA["projects"])}</span></button>' for category,label in categories)
    body=f'''<header class="page-masthead wrap"><h1>Work in the<br>real world.</h1><p>Practical AI systems, from an early idea to work in use.</p></header>
    <section class="work-section wrap" id="projects"><div class="section-heading"><h2>Selected projects.</h2><div class="work-toolbar"><div class="filters" role="group" aria-label="Filter projects" hidden>{filters}</div><span id="project-count" role="status" aria-live="polite" aria-atomic="true">{len(DATA['projects'])} projects</span></div></div>
    <div class="project-list">{featured_projects(DATA['home']['projects'])}<div class="work-index">{compact_projects()}</div></div></section>
    <section class="page-next wrap"><h2>Have a problem<br>worth solving?</h2><a class="button" href="/contact/">Let’s connect {arrow('right')}</a></section>'''
    return shell('Work — Vatsal Jain','Explore Vatsal Jain’s applied AI systems, products and workflow projects.',body,'/work/')


def about_page():
    about=DATA['about']
    method=''.join(f'''<div><dt>{e(item['heading'])}</dt><dd>{e(item['description'])}</dd></div>''' for item in DATA['method'])
    stack=''.join(f'''<div><dt>{e(group['label'])}</dt><dd>{e(' · '.join(group['items']))}</dd></div>''' for group in DATA['stack'])
    body=f'''<section class="about-opening wrap"><div class="about-intro"><h1>People first.<br>Then AI.</h1><p>{e(DATA['home']['about_paragraphs'][0])}</p><a class="text-link" href="{e(DATA['business'])}">Meet Clarity Works {arrow()}</a></div><figure class="about-portrait">{responsive_image(about['photo'], about['photo_alt'], priority=True)}<figcaption>Founder, builder, and advisor · Greater Vancouver</figcaption></figure></section>
    <section class="about-story wrap"><h2>How I got here.</h2><div><p>{e(about['lead'])}</p>{paragraphs(about['paragraphs'][1:])}</div></section>
    <section class="journey-section wrap"><h2>A little background.</h2><div class="journey-list"><div><span>2025 — Present</span><strong>Founder, Clarity Works</strong></div><div><span>2022</span><strong>Product Research Fellow, Circonomy</strong></div><div><span>2020 — 2024</span><strong>International Economics, UBC</strong></div></div></section>
    <section class="method-section wrap"><div class="section-heading"><h2>How I work.</h2><a class="text-link" href="https://www.tryclarityworks.com/philosophy">The philosophy {arrow()}</a></div><dl class="method-list">{method}</dl></section>
    <section class="skills-section wrap"><div class="section-heading"><h2>Tools & focus.</h2></div><dl class="skills-list">{stack}</dl></section>
    <section class="page-next wrap"><h2>See the work<br>in practice.</h2><a class="button" href="/work/">Explore projects {arrow('right')}</a></section>'''
    return shell('About — Vatsal Jain','Learn about Vatsal Jain’s background, approach and practical AI skills.',body,'/about/')


def notes_index():
    body=f'''<header class="page-masthead wrap"><h1>Ideas from<br>the work.</h1><p>Videos and notes about building AI systems with people in the loop.</p></header>
    <section class="video-section wrap" id="videos"><div class="section-heading"><h2>Watch.</h2><a class="text-link" href="{e(DATA['youtube'])}">More on YouTube {arrow()}</a></div><div class="video-grid">{video_links()}</div></section>
    <section class="notes-section wrap" id="writing"><div class="section-heading"><h2>Read.</h2></div><div class="notes-grid">{note_links()}</div></section>
    <section class="page-next wrap"><h2>See what<br>I’m building.</h2><a class="button" href="/work/">Explore projects {arrow('right')}</a></section>'''
    return shell('Notes & videos — Vatsal Jain','Notes and video walkthroughs on applied AI, workflow design and reliability.',body,'/notes/')


def contact_page():
    copy=DATA['home']
    body=f'''<section class="contact-section contact-page wrap" id="contact"><div class="contact-heading"><h1>Let’s work<br>together.</h1><p>{e(copy['contact_description'])}</p><div class="contact-actions">{contact_action('contact')}<a class="text-link" href="mailto:{e(DATA['email'])}">Send an email {arrow()}</a></div></div><div class="contact-copy"><p>Based in Canada.<br>Remote preferred. Open to the US.</p><details><summary>Working together</summary><p>I’m exploring Forward Deployed Engineer, AI Solutions Architect, and AI Enablement roles, plus scoped B2B builds.</p><p>I can work with US teams from Canada as an employee, or as a contractor through Clarity Works LLP, registered in British Columbia. Work performed in Canada doesn’t need US visa sponsorship. For US relocation, work authorization would be settled per role.</p></details></div></section>'''
    return shell('Contact — Vatsal Jain','Book a conversation with Vatsal Jain about applied AI work and opportunities.',body,'/contact/')

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
    body=f'''<div class="wrap story"><a class="back-link" href="/work/">{arrow('left')} All selected work</a><header class="story-header"><div class="story-heading"><h1>{e(p['name'])}</h1><p class="content-meta">{e(p['context'])} <span class="status">{e(p['status'])}</span></p><p class="story-deck">{e(p['summary'])}</p></div><dl class="story-facts"><div><dt>Project</dt><dd>{e(p['product'])}</dd></div><div><dt>My role</dt><dd>{e(p['role'])}</dd></div><div><dt>Current outcome</dt><dd>{e(p['outcome'])}</dd></div></dl></header>{metrics}<div class="story-flow"><p class="content-meta">The workflow, at a glance</p>{flow(p,True)}<p class="flow-caption">A simplified view of the workflow.</p></div>{stages}{sections}<section class="story-tools"><h2>Tools & focus</h2><div class="tags">{tags}</div></section>{sources}<div class="story-cta">{external}<a class="text-link" href="mailto:{e(DATA['email'])}">Talk about this work {arrow()}</a></div></div>'''
    return shell(p['name']+' — Vatsal Jain',p['summary'],body,'/work/'+p['slug']+'/')

def note_page(n):
    body=f'''<article class="wrap note-page"><a class="back-link" href="/notes/">{arrow('left')} Notes from the work</a><header><h1>{e(n['title'])}</h1><p class="content-meta">{e(n['tag'])} / October 2026</p><p class="story-deck">{e(n['summary'])}</p></header><div class="prose">{paragraphs(n['paragraphs'])}</div><div class="note-signature"><img src="{e(MEDIA['images']['/assets/vatsal.jpg']['webp'][0]['src'])}" width="52" height="52" alt="" loading="lazy" decoding="async"><div><strong>Vatsal Jain</strong><p>Founder, Clarity Works · Applied AI & systems</p></div></div><a class="text-link" href="mailto:{e(DATA['email'])}">Continue the conversation {arrow()}</a></article>'''
    return shell(n['title']+' — Vatsal Jain',n['summary'],body,'/notes/'+n['slug']+'/')

if __name__ == '__main__':
    slugs=[p['slug'] for p in DATA['projects']]+[n['slug'] for n in DATA['notes']]
    if len(slugs)!=len(set(slugs)) or any(not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',s) for s in slugs):
        raise SystemExit('Content slugs must be unique URL-safe strings')
    if OUT.exists(): shutil.rmtree(OUT)
    shutil.copytree(ROOT / 'static', OUT)
    write('index.html',shell('Vatsal Jain — '+DATA['title'],DATA['description'],home()))
    write('work/index.html',work_page())
    write('about/index.html',about_page())
    write('notes/index.html',notes_index())
    write('contact/index.html',contact_page())
    for p in DATA['projects']: write('work/'+p['slug']+'/index.html',case_study(p))
    for n in DATA['notes']: write('notes/'+n['slug']+'/index.html',note_page(n))
    write('404.html',shell('Page not found — Vatsal Jain','Return to Vatsal Jain’s portfolio.',f'<section class="wrap not-found"><p class="content-meta">404 / A loose end</p><h1>This page has moved<br>or doesn’t exist.</h1><a class="button" href="/">Back to the portfolio {arrow("right")}</a></section>'))
    paths=['/','/work/','/about/','/notes/','/contact/']+['/work/'+p['slug']+'/' for p in DATA['projects']]+['/notes/'+n['slug']+'/' for n in DATA['notes']]
    write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+e(ORIGIN+p)+'</loc></url>' for p in paths)+'</urlset>')
    write('robots.txt','User-agent: *\n'+('Disallow: /\n' if PREVIEW else 'Allow: /\nSitemap: '+ORIGIN+'/sitemap.xml\n'))
    print(f'Built {len(paths)} content pages plus 404 in {OUT}')
