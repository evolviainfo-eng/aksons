# Builds every page of the AK & Sons site from data.py.  Run: python3 gen.py
# Edit css/src/*, js/src/* and data.py; never the built css/site.css, js/site.js or the HTML.
import os, json, html
from data import SITE, BIZ, CATS, PROJECTS, HOME_CARDS, SERVICES

ROOT = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.expanduser('~/.claude/skills/signature-web/library/base')
SIZES = json.load(open(os.path.join(ROOT, 'img/sizes.json')))
BY = {p['slug']: p for p in PROJECTS}
CATNAME = dict(CATS)
E = html.escape

def key(pid): return pid.lower().replace('_', '-')

def srcset(k):
    s = SIZES[k]; return ', '.join(f'/img/p/{k}-{w}.webp {w}w' for w in s['widths'])

def img(k, alt, sizes, cls='', lazy=True, extra=''):
    s = SIZES[k]; ws = s['widths']; mid = next((w for w in ws if w >= 800), ws[-1])
    h = round(s['h'] * mid / s['w'])
    c = f' class="{cls}"' if cls else ''
    ld = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    return f'<img{c} src="/img/p/{k}-{mid}.webp" srcset="{srcset(k)}" sizes="{sizes}" width="{mid}" height="{h}" alt="{E(alt)}"{ld} decoding="async"{extra}>'

def alt_of(p, pid):
    for i, a in p['photos']:
        if i == pid: return a
    return p['title'] + ', ' + p['place']

def ar(pid):
    s = SIZES[key(pid)]; return round(s['w'] / s['h'], 4)

# ------------------------------------------------------------------ shell
INTRO = '<div class="intro" aria-hidden="true"><div class="intro__mark"></div></div>'

def nav(solid, current=''):
    cur = lambda h: ' aria-current="page"' if h == current else ''
    quote = '/contact/'
    return f'''<header class="nav{' is-solid' if solid else ''}" data-nav>
  <div class="wrap nav__in">
    <a class="brand" href="/"><img class="brand__mark" src="/img/mark.png" width="155" height="176" alt="AK &amp; Sons logo"><img class="brand__word brand__word--light" src="/img/wordmark-light.png" width="464" height="120" alt="AK &amp; Sons Bespoke Joinery, home"><img class="brand__word brand__word--dark" src="/img/wordmark.png" width="464" height="120" alt="AK &amp; Sons Bespoke Joinery, home"></a>
    <nav class="nav__links" aria-label="Main"><a href="/work/"{cur('/work/')}>Work</a><a href="/#how">How we work</a><a href="/#reviews">Reviews</a><a href="/contact/"{cur('/contact/')}>Contact</a></nav>
    <a class="btn btn--accent nav__cta" href="{quote}">Get a free quote</a>
    <button class="nav__menu" type="button" data-menu-open aria-expanded="false" aria-controls="menu">Menu</button>
  </div>
</header>
<div class="sheet" id="menu" data-menu hidden>
  <div class="sheet__top"><a class="brand" href="/"><img class="brand__mark" src="/img/mark.png" width="155" height="176" alt="AK &amp; Sons logo"><img class="brand__word" src="/img/wordmark-light.png" width="464" height="120" alt="AK &amp; Sons Bespoke Joinery, home"></a><button class="sheet__close" type="button" data-menu-close>Close</button></div>
  <nav class="sheet__links" aria-label="Menu"><a href="/" data-menu-close>Home</a><a href="/work/" data-menu-close>Work</a><a href="/#how" data-menu-close>How we work</a><a href="/#reviews" data-menu-close>Reviews</a><a href="/contact/" data-menu-close>Contact</a></nav>
  <div class="sheet__foot"><a class="btn btn--accent" href="/contact/" data-menu-close>Get a free quote</a><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></div>
</div>'''

PLACES = 'Worksop, Tickhill, Harthill, Harrogate, Carlton in Lindrick, Mansfield, East Markham, Harworth, Kilton, Sheffield, Leicester, Banbury and Crowborough'

def footer():
    return f'''<footer class="foot on-dark">
  <div class="wrap">
    <div class="g12 foot__g">
      <div class="foot__brand"><a class="brand" href="/"><img class="brand__mark" src="/img/mark.png" width="155" height="176" alt="AK &amp; Sons logo" loading="lazy"><img class="brand__word" src="/img/wordmark-light.png" width="464" height="120" alt="AK &amp; Sons Bespoke Joinery, home" loading="lazy"></a><p>Joinery designed, made and fitted by AK &amp; Sons in Worksop. All aspects of joinery undertaken.</p></div>
      <div class="foot__contact"><a class="foot__mail" href="mailto:{BIZ['email']}">{BIZ['email']}</a><p>Based in Worksop, Nottinghamshire, {BIZ['postcode']}</p></div>
      <nav class="foot__links" aria-label="Footer"><a href="/work/">Work</a><a href="/#how">How we work</a><a href="/#reviews">Reviews</a><a href="/contact/">Get a free quote</a><a href="{BIZ['facebook']}" rel="noopener" target="_blank">Facebook</a><a href="{BIZ['instagram']}" rel="noopener" target="_blank">Instagram</a></nav>
      <p class="foot__places">Recent projects in {PLACES}.</p>
    </div>
    <div class="foot__legal"><p>AK &amp; Sons Bespoke Joinery Ltd. Registered in England and Wales, Company No. {BIZ['company_no']}. Registered office: {BIZ['office']}.</p><p>&copy; 2026 AK &amp; Sons Bespoke Joinery Ltd &middot; <a href="/privacy/">Privacy notice</a></p></div>
  </div>
</footer>'''

LB = '''<dialog class="lb" data-lb aria-label="Photo gallery">
  <div class="lb__bar"><p><span data-lb-title></span><span data-lb-count></span></p><button class="lb__btn" type="button" data-lb-close>Close</button></div>
  <figure><img data-lb-img src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" width="1200" height="1600" alt="Enlarged photograph"></figure>
  <button class="lb__nav lb__nav--prev" type="button" data-lb-prev aria-label="Previous photo"><svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M11 3 5 9l6 6" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>
  <button class="lb__nav lb__nav--next" type="button" data-lb-next aria-label="Next photo"><svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="m7 3 6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>
</dialog>'''

def page(path, title, desc, body, solid=True, current='', gallery=None, og='/og.jpg', quote_href='/contact/', extra_head=''):
    canon = SITE + path
    ld = {
        '@context': 'https://schema.org', '@type': 'HomeAndConstructionBusiness', 'name': BIZ['name'], 'legalName': BIZ['legal'],
        'url': SITE + '/', 'email': BIZ['email'], 'image': SITE + '/og.jpg', 'logo': SITE + '/img/logo.png',
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Worksop', 'addressRegion': 'Nottinghamshire', 'postalCode': BIZ['postcode'], 'addressCountry': 'GB'},
        'sameAs': [BIZ['facebook'], BIZ['instagram']],
    }
    g = f'<script>window.GALLERY={json.dumps(gallery[0])};window.GALLERY_TITLES={json.dumps(gallery[1])};</script>' if gallery else ''
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website"><meta property="og:site_name" content="AK &amp; Sons Bespoke Joinery"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{SITE}{og}"><meta property="og:locale" content="en_GB"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#15181B">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png"><link rel="icon" type="image/png" sizes="512x512" href="/favicon-512.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/fonts/jost-latin.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/fonts/albert-latin.woff2" as="font" type="font/woff2" crossorigin>
{extra_head}<script>(function(d){{d.classList.add('js');var r=matchMedia('(prefers-reduced-motion: reduce)').matches,s;try{{s=sessionStorage.getItem('intro-seen')}}catch(e){{}}if(r||s)d.classList.add('no-intro')}})(document.documentElement)</script>
<link rel="stylesheet" href="/css/site.css">
<script type="application/ld+json">{json.dumps(ld)}</script>
</head>
<body>
{INTRO}
<a class="skip" href="#main">Skip to content</a>
{nav(solid, current)}
<main id="main">
{body}
</main>
{footer()}
<a class="qtab" href="{quote_href}" data-qtab>Get a free quote</a>
<div class="actbar" data-actbar><a class="btn" href="mailto:{BIZ['email']}">Email us</a><a class="btn btn--accent" href="{quote_href}">Get a free quote</a></div>
{LB}
{g}<script src="/js/lenis.min.js" defer></script>
<script src="/js/site.js" defer></script>
</body>
</html>
'''

# ------------------------------------------------------------------ shared blocks
def card(p, sizes='(max-width: 759px) 72vw, (max-width: 900px) 46vw, 30vw', lazy=True):
    sec = p['second']; sa = alt_of(p, sec)
    tag = 'Before' if sa.startswith('Before') else 'During' if sa.startswith('During') else 'On the bench' if 'bench' in sa else 'Drawing' if 'CAD' in sa else ''
    t = f'<span class="card__tag">{tag}</span>' if tag else ''
    cats = ' '.join(p['cats'])
    return f'''<a class="card" href="/work/{p['slug']}/" data-cats="{cats}"><div class="card__ph">{img(key(p['cover']), alt_of(p, p['cover']), sizes, lazy=lazy)}{img(key(sec), sa, sizes, 'card__b', lazy=True)}{t}</div><div class="card__cap"><span class="card__t">{E(p['title'])}</span><span class="card__p">{E(p['place'])}</span></div></a>'''

def slider(p, sizes='(max-width: 900px) 92vw, 46vw'):
    b, a, d = 'pair-before', 'pair-after', 'pair-during'
    return f'''<div class="ba" data-ba data-srcset-before="{srcset(b)}" data-srcset-during="{srcset(d)}">
  {img(b, 'Before: the hallway with the open understairs and the old staircase, Worksop', sizes, 'ba__a')}
  {img(a, 'After: panelled understairs storage, new spindles, newel post and handrail', sizes, 'ba__b')}
  <span class="ba__tag ba__tag--a" data-ba-tag>Before</span><span class="ba__tag ba__tag--b">After</span>
  <input class="ba__range" type="range" min="0" max="100" value="50" step="1" aria-label="Compare before and after: drag left or right">
  <span class="ba__line"><span class="ba__knob" aria-hidden="true"><svg width="22" height="12" viewBox="0 0 22 12"><path d="M6 1 1 6l5 5M16 1l5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></span></span>
</div>'''

STAGES = '<div class="stages" role="group" aria-label="Show a stage"><button type="button" data-stage="before" aria-pressed="false">Before</button><button type="button" data-stage="during" aria-pressed="false">During</button><button type="button" data-stage="after" aria-pressed="false">After</button></div>'

JOBTYPES = ['Built-in furniture', 'Kitchen fitting', 'Internal doors', 'Staircase', 'Hallway, panelling or bar', 'Something else']

def quote_section(head_tag='h2', title='Tell us about the job'):
    opts = ''.join(f'<option>{E(o)}</option>' for o in JOBTYPES)
    photo = img(key('P05_06'), alt_of(BY['worksop-hallway-understairs'], 'P05_06'), '(max-width: 900px) 72vw, 26vw')
    return f'''<section class="sec quote" id="quote" data-quote aria-labelledby="quote-h">
  <div class="wrap g12 quote__g">
    <div class="quote__side">
      <{head_tag} class="t-display rv" id="quote-h">{title}</{head_tag}>
      <p class="t-lead rv">Send a few lines and, if you have one, a photo of the space. We will reply by email, answer your questions and arrange a free, no-obligation quote.</p>
      <a class="quote__mail rv" href="mailto:{BIZ['email']}">{BIZ['email']}</a>
      <div class="quote__lines rv"><span>Based in Worksop, Nottinghamshire, {BIZ['postcode']}</span></div>
      <figure class="quote__ph"><div class="ph">{photo}</div><figcaption class="t-caption">One of our team fitting the understairs doors &middot; Worksop</figcaption></figure>
    </div>
    <form class="form" action="https://formsubmit.co/{BIZ['email']}" method="POST" enctype="multipart/form-data" data-form novalidate>
      <input type="hidden" name="_subject" value="New enquiry from the AK &amp; Sons website">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="_captcha" value="false">
      <input type="hidden" name="_next" value="{SITE}/thanks/" data-next>
      <input class="hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
      <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" type="text" autocomplete="name" required><span class="msg" aria-live="polite"></span></div>
      <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required><span class="msg" aria-live="polite"></span></div>
      <div class="field field--full"><label for="f-type">Type of work</label><select id="f-type" name="type_of_work">{opts}</select></div>
      <div class="field field--full"><label for="f-msg">Tell us about the job</label><textarea id="f-msg" name="message" rows="4" placeholder="e.g. built-in shelving either side of the chimney breast, about 2.4 m high" required></textarea><span class="msg" aria-live="polite"></span></div>
      <details class="form__fold" open data-fold><summary>Add your location and a photo</summary><div class="form__more">
        <div class="field field--full"><label for="f-town">Town or postcode</label><input id="f-town" name="location" type="text" autocomplete="postal-code"></div>
        <div class="field field--full"><label for="f-file">Photo of the space (optional)</label><input id="f-file" name="attachment" type="file" accept="image/jpeg,image/png,image/heic,image/webp"><span class="hint">One photo, JPG or PNG, up to 5 MB. More can follow by email.</span><span class="msg" aria-live="polite"></span></div>
      </div></details>
      <p class="form__note">We only use these details to reply to your enquiry. See our <a href="/privacy/">privacy notice</a>.</p>
      <div class="form__end"><button class="btn btn--accent" type="submit">Send enquiry</button><span class="form__free">Free, no-obligation quote.</span></div>
    </form>
  </div>
</section>'''

# ------------------------------------------------------------------ home
def home():
    H = BY['harrogate-display-unit']; W = BY['worksop-hallway-understairs']; M = BY['mansfield-external-door']
    hero = f'''<section class="hero" data-hero aria-labelledby="h1">
  <picture class="hero__ph">
    <source media="(min-width: 760px)" srcset="{srcset('hero-d')}" sizes="100vw">
    {img(key('P00_01'), 'Built-in display and storage unit with LED lighting under every shelf, made and fitted by AK & Sons in Harrogate', '143vw', lazy=False)}
  </picture>
  <div class="wrap g12 hero__in">
    <h1 class="t-display rv" id="h1">Bespoke joinery, designed, made and fitted in Worksop</h1>
    <div class="hero__aside rv" style="--delay: 120ms">
      <p class="hero__lead m-hide">One team from the CAD drawing to the last fitting, for homes and local builders. Recent work in Tickhill, Harthill and Harrogate.</p>
      <div class="hero__act"><a class="btn btn--accent" href="#quote">Get a free quote</a><a class="hero__mail m-hide" href="mailto:{BIZ['email']}">or email us</a></div>
      <p class="hero__cap m-hide">Built-in display and storage unit &middot; Harrogate</p>
    </div>
  </div>
</section>'''
    facts = f'''<section class="facts" aria-label="About us in four facts">
  <div class="wrap facts__row">
    <p class="fact rv"><b>100% recommended</b><span>on Facebook, from 8 reviews</span></p>
    <p class="fact rv" style="--delay: 60ms"><b>Over 35 years&rsquo; experience</b><span>combined between us</span></p>
    <p class="fact rv" style="--delay: 120ms"><b>Based in Worksop</b><span>Nottinghamshire, {BIZ['postcode']}</span></p>
    <p class="fact rv" style="--delay: 180ms"><b>We fit Wren and Howdens</b><span>kitchens and doors</span></p>
  </div>
</section>'''
    rows = ''
    for s in SERVICES:
        th = ''.join(f'<span class="ph">{img(key(x), s["name"], "15vw")}</span>' for x in s['photos'])
        rows += f'<li class="svc__row rv"><a href="/work/?type={s["cat"]}"><span class="svc__name">{E(s["name"])}</span><span class="svc__go" aria-hidden="true">&rarr;</span><span class="svc__data">{E(s["data"])}</span><span class="svc__thumbs" aria-hidden="true"><span>{th}</span></span></a></li>'
    D = BY['tickhill-kitchen-pocket-doors']
    svc = f'''<section class="sec svc" id="services" aria-labelledby="svc-h">
  <div class="wrap g12 svc__g">
    <div class="svc__intro">
      <h2 class="t-display rv" id="svc-h">All aspects of joinery undertaken</h2>
      <p class="t-lead rv">From a single internal door to a whole hallway, kitchen or garage bar.<span class="m-hide"> Recent jobs have also included fire doors for a primary school, a mezzanine, a pergola and a traditional cut roof.</span></p>
      <figure class="svc__plate"><a class="ph ph--link" href="/work/{D['slug']}/"><span data-par="3">{img(key('P02_02'), alt_of(D, 'P02_02'), '(max-width: 900px) 92vw, min(46vw, calc((100vh - 200px) * .86))')}</span></a><figcaption class="t-caption">Wren kitchen and full-height wall units &middot; Tickhill</figcaption></figure>
    </div>
    <div class="svc__list">
      <ul>{rows}</ul>
      <p class="svc__also rv">We fit Wren and Howdens kitchens and doors, and Ironmongery Direct pocket door systems. We work for homeowners and for local builders.</p>
    </div>
  </div>
</section>'''
    dmf = f'''<section class="sec dmf on-dark" id="how" data-signature data-client-only aria-labelledby="how-h">
  <div class="wrap">
    <div class="g12 head">
      <h2 class="t-display rv" id="how-h">Drawn in CAD, made in our workshop, fitted by the same team</h2>
      <div class="head__side rv"><p class="t-body" style="color: var(--c-ink-2)">Before anything is cut, you see a measured drawing of the piece. Then we make it and fit it ourselves, so nothing gets lost between a designer, a workshop and a fitter.</p></div>
    </div>
    <div class="g12 dmf__plates">
      <figure class="dmf__fig dmf__draw"><a class="sheetph" href="/img/p/p00-00-{SIZES['p00-00']['widths'][-1]}.webp" data-open="harrogate" data-index="1" aria-label="Open the CAD drawing full size">{img('p00-00', alt_of(H, 'P00_00'), '(max-width: 900px) 80vw, min(30vw, calc((100vh - 240px) * .75))')}</a><figcaption><b>Drawn</b>The CAD drawing for the Harrogate unit: front elevation, shelf spacing and cupboard doors.</figcaption></figure>
      <figure class="dmf__fig dmf__made"><div class="ph">{img('sig-made', alt_of(M, 'P28_03'), '(max-width: 900px) 60vw, min(26vw, calc((100vh - 200px) * .66))')}</div><figcaption><b>Made</b>An arched door frame glued and clamped on the bench, for a door in Mansfield.</figcaption></figure>
      <figure class="dmf__fig dmf__fit"><a class="ph ph--link" href="/work/{H['slug']}/">{img('sig-fit', alt_of(H, 'P00_04'), '(max-width: 900px) 92vw, min(40vw, calc(100vh - 220px))')}</a><figcaption><b>Fitted</b>The Harrogate unit in place, with LED strips under every shelf. <a class="link link--arrow" href="/work/{H['slug']}/">See the project</a></figcaption></figure>
    </div>
  </div>
</section>'''
    bda = f'''<section class="sec bda bg-2" id="before-after" data-client-only aria-labelledby="bda-h">
  <div class="wrap g12 bda__g">
    <div class="bda__media">{slider(W)}</div>
    <div class="bda__text">
      <h2 class="t-h2 rv" id="bda-h">Before, during and after: an entrance hallway in Worksop</h2>
      <p class="t-body rv">Storage built into the space under the stairs, then a staircase refurb with new spindles, newel posts and handrail. Drag across the photo, or pick a stage.</p>
      <div class="rv">{STAGES}</div>
      <a class="link link--arrow rv" href="/work/{W['slug']}/">See the whole hallway</a>
    </div>
  </div>
</section>'''
    cards = ''.join(card(BY[s]) for s in HOME_CARDS)
    work = f'''<section class="sec work" id="work" aria-labelledby="work-h">
  <div class="wrap">
    <div class="g12 head">
      <h2 class="t-display rv" id="work-h">Recent work, from Tickhill to Harrogate</h2>
      <div class="head__side rv"><p class="t-body m-hide" style="color: var(--c-ink-2)">Every job with the place it was fitted, and where we have them, the before photos.</p><a class="link link--arrow" href="/work/">See all {len(PROJECTS)} projects</a></div>
    </div>
    <div class="g12 cards cards--home">{cards}</div>
  </div>
</section>'''
    rev = f'''<section class="sec rev hair-t" id="reviews" aria-labelledby="rev-h">
  <div class="wrap">
    <div class="g12 head">
      <h2 class="t-h2 rv" id="rev-h">100% recommended on Facebook</h2>
      <div class="head__side rv"><p class="t-body" style="color: var(--c-ink-2)">8 reviews, all recommending us. Three of them below, word for word.</p><a class="link link--arrow" href="{BIZ['fb_reviews']}" rel="noopener" target="_blank">Read all 8 on Facebook</a></div>
    </div>
    <div class="rev__main">
      <blockquote class="rv"><p class="rev__big">&ldquo;We would highly recommend these guys, their communication is fantastic, their time keeping is spot on &amp; their work is outstanding too. They fitted our kitchen &amp; skirting board to perfection.&rdquo;</p><footer class="rev__who">Claire L. &middot; Facebook</footer></blockquote>
      <div class="rev__pair">
        <blockquote class="rv"><p>&ldquo;After being massively let down by another local company these lads really came to our rescue with not much notice at all to make sure we had a room for our new arrival. They worked in minus temperatures and worked right up until Christmas Eve. Always well mannered and polite and kept us informed all the way through the process.&rdquo;</p><footer class="rev__who">Laura B. &middot; Facebook</footer></blockquote>
        <blockquote class="rv" style="--delay: 90ms"><p>&ldquo;I couldn&rsquo;t recommend these guys enough, they have done an absolutely fantastic job fitting our new kitchen.&rdquo;</p><footer class="rev__who">Sherri-Anne B. &middot; Facebook</footer></blockquote>
      </div>
    </div>
  </div>
</section>'''
    body = hero + facts + svc + dmf + bda + work + rev + quote_section()
    gal = ({'harrogate': [gitem(x) for x, _ in H['photos']]}, {'harrogate': 'Built-in display and storage unit · Harrogate'})
    return page('/', 'AK & Sons Bespoke Joinery | Bespoke joinery in Worksop, Nottinghamshire',
                'Bespoke joinery designed, made and fitted by AK & Sons in Worksop: built-in units, kitchen fitting, internal and pocket doors, staircases, hallways and bars. Over 35 years’ experience combined.',
                body, solid=False, gallery=gal, quote_href='#quote',
                extra_head=f'<link rel="preload" as="image" href="/img/p/hero-d-1920.webp" imagesrcset="{srcset("hero-d")}" imagesizes="100vw" media="(min-width: 760px)">\n')

def gitem(pid):
    k = key(pid); s = SIZES[k]; w = s['widths'][-1]
    return {'src': f'/img/p/{k}-{w}.webp', 'w': w, 'h': round(s['h'] * w / s['w'])}

# ------------------------------------------------------------------ work index
def work_index():
    counts = {c: sum(1 for p in PROJECTS if c in p['cats']) for c, _ in CATS}
    btns = f'<button type="button" data-filter="all" aria-pressed="true">All<span class="n">{len(PROJECTS)}</span></button>' + ''.join(
        f'<button type="button" data-filter="{c}" aria-pressed="false">{E(n)}<span class="n">{counts[c]}</span></button>' for c, n in CATS)
    cards = ''.join(card(p, lazy=i > 2) for i, p in enumerate(PROJECTS))
    body = f'''<section class="phead">
  <div class="wrap g12 phead__g">
    <h1 class="t-display rv">Bespoke joinery projects, from Worksop to Harrogate</h1>
    <div class="phead__side rv m-hide"><p class="t-body" style="color: var(--c-ink-2)">Kitchens, built-in units, doors, staircases and bars, each shown with the place it was fitted. Pick a kind of work to narrow the list.</p></div>
  </div>
</section>
<section class="sec" style="--sec-top: 0">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Filter projects" data-filters>{btns}</div>
    <div class="grid3" data-grid>{cards}</div>
  </div>
</section>'''
    return page('/work/', 'Our work | AK & Sons Bespoke Joinery, Worksop',
                'Bespoke joinery projects by AK & Sons: kitchens in Tickhill and Harthill, a built-in unit in Harrogate, staircases and doors in Worksop, a garage bar in Carlton in Lindrick and more.',
                body, current='/work/')

# ------------------------------------------------------------------ project pages
def project(p, nxt):
    rail = ''
    for i, (pid, a) in enumerate(p['photos']):
        k = key(pid); r = ar(pid)
        rail += f'<a href="/img/p/{k}-{SIZES[k]["widths"][-1]}.webp" data-open="p" data-index="{i}" style="--ar: {r}" aria-label="Open photo {i + 1}: {E(a)}">{img(k, a, f"(max-width: 759px) 80vw, calc((100vh - 220px) * {r})", lazy=i > 1)}</a>'
    work = ' &middot; '.join(E(w) for w in p['work'])
    cats = ', '.join(CATNAME[c] for c in p['cats'])
    text = ''.join(f'<p class="rv">{E(t)}</p>' for t in p['text'])
    extra = ''
    if p.get('pair'):
        extra += f'''<section class="sec bda bg-2" data-client-only aria-labelledby="bda-h">
  <div class="wrap g12 bda__g">
    <div class="bda__media">{slider(p)}</div>
    <div class="bda__text"><h2 class="t-h2 rv" id="bda-h">Before, during and after</h2><p class="t-body rv">The same corner of the hall, photographed from the same spot. Drag across the photo, or pick a stage.</p><div class="rv">{STAGES}</div></div>
  </div>
</section>'''
    if p.get('video'):
        v = p['video']; poster = key(v['src'])
        extra += f'''<section class="sec hair-t" aria-labelledby="vid-h">
  <div class="wrap g12 vid__g">
    <figure class="pj-video"><video src="/img/v/{v['src'].lower().replace('_', '-')}.mp4" poster="/img/p/{poster}-800.webp" muted playsinline loop autoplay preload="metadata" aria-label="{E(v['alt'])}"></video></figure>
    <div class="vid__text"><h2 class="t-h2 rv" id="vid-h">{E(v['title'])}</h2><p class="t-body rv" style="color: var(--c-ink-2)">{E(v['text'])}</p></div>
  </div>
</section>'''
    body = f'''<section class="phead">
  <div class="wrap">
    <p class="crumb"><a href="/work/">Work</a><span aria-hidden="true">/</span><span>{E(p['place'])}</span></p>
    <div class="g12 phead__g">
      <h1 class="t-display rv">{E(p['title'])}</h1>
      <div class="phead__side rv"><p class="t-lead">{E(p['place'])}, {E(p['region'])}</p></div>
    </div>
  </div>
</section>
<section aria-label="Photographs">
  <div class="pj-rail" data-rail>{rail}</div>
  <div class="wrap pj-rail__bar"><span class="pj-rail__count">{len(p['photos'])} photographs</span><div class="pj-rail__btns"><button type="button" data-rail-prev aria-label="Previous photographs"><svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M11 3 5 9l6 6" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button><button type="button" data-rail-next aria-label="Next photographs"><svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="m7 3 6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button></div></div>
</section>
<section class="sec sec--tight hair-t" aria-label="About the project">
  <div class="wrap g12 pj-info">
    <dl class="pj-dl rv">
      <div><dt class="t-label">Work</dt><dd>{work}</dd></div>
      <div><dt class="t-label">Location</dt><dd>{E(p['place'])}<br>{E(p['region'])}</dd></div>
      <div><dt class="t-label">Type</dt><dd>{E(cats)}</dd></div>
    </dl>
    <div class="pj-text">{text}<a class="link link--arrow rv" href="https://www.instagram.com/p/{p['ig']}/" rel="noopener" target="_blank">See the post on Instagram</a></div>
    <aside class="pj-aside rv" aria-labelledby="cta-h"><h2 class="t-h3" id="cta-h">Planning something similar?</h2><p class="t-small">Tell us about the job and we will arrange a free, no-obligation quote.</p><a class="btn btn--accent" href="/contact/">Get a free quote</a><a class="link" href="mailto:{BIZ['email']}">Email us</a></aside>
  </div>
</section>
{extra}
<div class="wrap"><a class="pj-next" href="/work/{nxt['slug']}/"><span class="ph">{img(key(nxt['cover']), alt_of(nxt, nxt['cover']), '160px')}</span><span class="pj-next__t"><span>Next project</span><b>{E(nxt['title'])}</b><span class="t-caption">{E(nxt['place'])}</span></span><span class="pj-next__go" aria-hidden="true">&rarr;</span></a></div>'''
    gal = ({'p': [gitem(x) for x, _ in p['photos']]}, {'p': p['title'] + ' · ' + p['place']})
    desc = (p['text'][0][:150].rsplit(' ', 1)[0] + '.') if len(p['text'][0]) > 155 else p['text'][0]
    return page(f'/work/{p["slug"]}/', f'{p["title"]} in {p["place"]} | AK & Sons Bespoke Joinery', desc, body, current='/work/', gallery=gal)

# ------------------------------------------------------------------ contact, privacy, thanks, 404
def contact():
    body = f'''<section class="phead" style="padding-bottom: 0">
  <div class="wrap g12 phead__g"><p class="crumb" style="grid-column: 1 / -1; margin: 0"><a href="/">Home</a><span aria-hidden="true">/</span><span>Contact</span></p></div>
</section>
{quote_section('h1', 'Get a free quote')}'''
    return page('/contact/', 'Get a free joinery quote | AK & Sons Bespoke Joinery, Worksop',
                'Ask AK & Sons for a free, no-obligation joinery quote. Send the details and a photo of the space, or email ak.sonsbespokejoinery@gmail.com. Based in Worksop, Nottinghamshire.',
                body, current='/contact/', quote_href='#quote')

def prose_page(path, title, h1, desc, inner):
    body = f'''<section class="phead"><div class="wrap g12 phead__g"><h1 class="t-display rv">{h1}</h1></div></section>
<section class="sec" style="--sec-top: 0"><div class="wrap"><div class="prose">{inner}</div></div></section>'''
    return page(path, title, desc, body)

PRIVACY = f'''<p>This notice explains what happens to the details you send through this website. It is written by AK &amp; Sons Bespoke Joinery Ltd, Unit 4 Rear Of 38 Church Walk, Worksop, Nottinghamshire, S80 2EJ (Company No. {BIZ['company_no']}). Questions about it: <a href="mailto:{BIZ['email']}">{BIZ['email']}</a>.</p>
<h2>What we collect</h2><p>Only what you type into the enquiry form: your name, email address, town or postcode, the type of work, your message and any photo you attach.</p>
<h2>Why we use it</h2><p>To reply to your enquiry, arrange a visit and prepare a quote. Our lawful basis is that you asked us to, before entering into a contract (UK GDPR Article 6(1)(b)). We do not use it for marketing and we do not sell or share it.</p>
<h2>How it reaches us</h2><p>The form is delivered to our email inbox by FormSubmit (formsubmit.co), a form delivery service. Your message passes through their servers on the way to us.</p>
<h2>How long we keep it</h2><p>For as long as we need it to deal with your enquiry and, if we do the work, for our business records. If we do not go ahead, we delete it once the enquiry is closed.</p>
<h2>Cookies</h2><p>This website sets no cookies and uses no analytics or tracking.</p>
<h2>Your rights</h2><p>You can ask to see, correct or delete the details we hold about you by emailing us. If you are unhappy with how we handle them, you can complain to the Information Commissioner&rsquo;s Office at <a href="https://ico.org.uk" rel="noopener">ico.org.uk</a>.</p>'''

THANKS = f'''<p>Thank you. Your enquiry is on its way to us and we will be in touch.</p><p>If you need to add anything, email <a href="mailto:{BIZ['email']}">{BIZ['email']}</a>.</p><p><a href="/work/">Look through our work</a> &middot; <a href="/">Back to the home page</a></p>'''
NOTFOUND = f'''<p>The page you were looking for is not here. It may have moved.</p><p><a href="/">Home</a> &middot; <a href="/work/">Our work</a> &middot; <a href="/contact/">Get a free quote</a> &middot; <a href="mailto:{BIZ['email']}">Email us</a></p>'''

# ------------------------------------------------------------------ build
def write(path, s):
    full = os.path.join(ROOT, path.lstrip('/'))
    if path.endswith('/'): full = os.path.join(full, 'index.html')
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w').write(s)

def build_assets():
    css = ''.join(open(f).read() + '\n' for f in [os.path.join(ROOT, 'css/src/fonts.css'), os.path.join(LIB, 'tokens.css'), os.path.join(LIB, 'base.css'), os.path.join(LIB, 'motion.css'), os.path.join(ROOT, 'css/src/ak.css')])
    open(os.path.join(ROOT, 'css/site.css'), 'w').write(css)
    js = open(os.path.join(LIB, 'motion.js')).read() + '\n' + open(os.path.join(ROOT, 'js/src/ak.js')).read()
    open(os.path.join(ROOT, 'js/site.js'), 'w').write(js)
    open(os.path.join(ROOT, 'js/lenis.min.js'), 'w').write(open(os.path.join(LIB, 'lenis.min.js')).read())

def main():
    build_assets()
    write('/', home())
    write('/work/', work_index())
    for i, p in enumerate(PROJECTS):
        write(f'/work/{p["slug"]}/', project(p, PROJECTS[(i + 1) % len(PROJECTS)]))
    write('/contact/', contact())
    write('/privacy/', prose_page('/privacy/', 'Privacy notice | AK & Sons Bespoke Joinery', 'Privacy notice', 'How AK & Sons Bespoke Joinery Ltd handles the details you send through the enquiry form.', PRIVACY))
    write('/thanks/', prose_page('/thanks/', 'Thank you | AK & Sons Bespoke Joinery', 'Thank you, your enquiry is on its way', 'Enquiry sent to AK & Sons Bespoke Joinery.', THANKS))
    write('/404.html', prose_page('/404.html', 'Page not found | AK & Sons Bespoke Joinery', 'This page is not here', 'Page not found.', NOTFOUND))
    urls = ['/', '/work/'] + [f'/work/{p["slug"]}/' for p in PROJECTS] + ['/contact/', '/privacy/']
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{SITE}{u}</loc></url>\n' for u in urls) + '</urlset>\n')
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nDisallow: /thanks/\n\nSitemap: {SITE}/sitemap.xml\n')
    print('built', len(urls) + 2, 'pages')

if __name__ == '__main__':
    main()
