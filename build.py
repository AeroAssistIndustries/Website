"""Wraps each page partial in src/ with the shared head, nav and footer; writes the finished site to docs/."""
import os, re, shutil, hashlib, json
import plans, guides, service_pages, industry_pages
from html import escape as esc

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC, DIST = os.path.join(ROOT, "src"), os.path.join(ROOT, "docs")

# Where the site lives. Change both when it moves to its own domain (e.g. https://digitalmondo.com and "/").
SITE_URL = "https://aeroassistindustries.github.io/Website/"
SITE_PATH = "/Website/"
EMAIL = "hello@digitalmondo.com"
SAMPLE_FONTS = "&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Bricolage+Grotesque:opsz,wght@12..96,600..800"
# Where the audit form posts (a form service or Cloudflare Worker URL). Empty: visitors get an email draft instead.
FORM_ENDPOINT = ""

PAGES = {
    "index.html":         ("Digital Mondo · Your Neighborhood, Seen by the World", "Social media, local SEO, reputation management and websites for local businesses, from $250 a month. One person, real attention, month to month.", "home"),
    "services.html":      ("Services · Digital Mondo", "Social media management, local SEO, online reputation management and websites for local businesses, each from $250 a month.", "services"),
    "industries.html":    ("Industries · Digital Mondo", "Marketing for hotels, restaurants, salons, real estate, contractors, dental and wellness practices, retail and local services.", "industries"),
    "pricing.html":       ("Pricing · Digital Mondo", "Plans from $250 a month, all four services from $595 a month, combos up to 20% off, and 2 months free when you pay yearly.", "pricing"),
    "social.html":        ("Social Media Examples · Digital Mondo", "Sample social media posts, Reels and content calendars for local businesses.", "social"),
    "about.html":         ("About · Digital Mondo", "Meet Karla, a well-traveled founder bringing a worldly eye to local marketing.", "about"),
    "faq.html":           ("FAQ · Digital Mondo", "Answers about plans, pricing, contracts, accounts, reporting and how working with Digital Mondo works.", "faq"),
    "resources.html":     ("Guides & Free Tools · Digital Mondo", "Plain-English guides to Google reviews, your Google Business Profile, social media, websites and reaching visitors, plus free marketing tools.", "resources"),
    "checklist.html":     ("Google Business Profile Checklist · Digital Mondo", "A free, interactive checklist to see how complete your Google Business Profile is.", "checklist"),
    "post-planner.html":  ("Free Social Media Post Planner · Digital Mondo", "Pick your type of business and how often you post, and get four weeks of social media post ideas with caption starters. Free.", "resources"),
    "review-cards.html":  ("Free Review QR Card Maker · Digital Mondo", "Make a printable counter card or business card with a QR code that takes customers straight to your Google review form. Free.", "resources"),
    "contact.html":       ("Free Marketing Audit · Digital Mondo", "Request a free marketing audit and website speed check from Digital Mondo.", "contact"),
    "terms.html":         ("Terms of Service · Digital Mondo", "The terms that apply to using this website and to Digital Mondo's marketing services.", "legal"),
    "privacy.html":       ("Privacy Policy · Digital Mondo", "How Digital Mondo collects, uses and protects personal information from website visitors, audit requests and clients.", "legal"),
    "accessibility.html": ("Accessibility · Digital Mondo", "Digital Mondo's commitment to an accessible website, and how to report a barrier.", "legal"),
    "404.html":           ("Page not found · Digital Mondo", "The page you were looking for isn't here.", "404"),
}

NAV = [("services.html", "Services", "services"), ("industries.html", "Industries", "industries"),
       ("pricing.html", "Pricing", "pricing"), ("social.html", "Our work", "social"), ("resources.html", "Guides", "resources"), ("about.html", "About", "about")]

SCHEMA = {
    "@context": "https://schema.org", "@type": "ProfessionalService", "name": "Digital Mondo",
    "url": SITE_URL, "email": EMAIL, "logo": SITE_URL + "assets/logo.svg", "image": SITE_URL + "assets/og-image.png",
    "description": "Social media, local SEO, reputation management and websites for local businesses.",
    "priceRange": "$250–$1,500 per month", "founder": {"@type": "Person", "name": "Karla"},
    "areaServed": "US",
    "makesOffer": [{"@type": "Offer", "name": p["name"], "priceSpecification": {"@type": "UnitPriceSpecification", "price": p["tiers"][0]["price"], "priceCurrency": "USD", "unitText": "MONTH"}} for p in plans.PLANS],
}

def ver(name):
    return hashlib.md5(open(os.path.join(ROOT, name), "rb").read()).hexdigest()[:8]

def ld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj)}</script>\n'


def head(fname, title, desc, style, active, extra_ld=""):
    canon = SITE_URL + ("" if fname == "index.html" else fname)
    base = f'<base href="{SITE_PATH}">\n' if active == "404" else ""
    robots = '<meta name="robots" content="noindex">\n' if active == "404" else ""
    schema = (ld(SCHEMA) if fname == "index.html" else "") + extra_ld
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{base}<title>{title}</title>
<meta name="description" content="{desc}">
{robots}<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#13294b">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="assets/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="manifest" href="assets/site.webmanifest">
<meta property="og:type" content="{"article" if active == "guide" else "website"}">
<meta property="og:site_name" content="Digital Mondo">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE_URL}assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE_URL}assets/og-image.png">
{schema}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&family=Inter:wght@400;500;600;700{SAMPLE_FONTS if fname == "social.html" else ""}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v={ver('style.css')}">
<script>document.documentElement.classList.add('js')</script>
{style}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""

SUBNAV = [("social-media-management.html", "Social media management", "Posts, Reels and replies"),
          ("local-seo.html", "Local SEO", "Google, Maps and AI search"),
          ("reputation-management.html", "Reputation management", "More reviews, every one answered"),
          ("website-design.html", "Websites", "Fast sites that bring in bookings")]

SUBMENUS = {
    "services.html": (SUBNAV, "Show services", "All services and add-ons →", ""),
    "industries.html": ([(ip["file"], ip["name"], ip["tag"]) for ip in industry_pages.PAGES], "Show industries", "All industries →", " sub-ind"),
}

def nav(active, fname=""):
    def item(h, t, k):
        cur = " aria-current=\"page\"" if k == active else ""
        if h not in SUBMENUS:
            return f'<li><a href="{h}"{cur}>{t}</a></li>'
        entries, label, all_text, cls = SUBMENUS[h]
        sub = "".join(f'<li><a href="{sh}"{" aria-current=\"page\"" if sh == fname else ""}><b>{st}</b><small>{sd}</small></a></li>' for sh, st, sd in entries)
        return (f'<li class="has-sub"><a href="{h}"{cur}>{t}</a><button class="sub-btn" type="button" aria-expanded="false" aria-label="{label}">'
                f'<svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true"><path d="M2 4.5l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></button>'
                f'<ul class="sub{cls}">{sub}<li class="sub-all"><a href="{h}">{all_text}</a></li></ul></li>')
    items = "".join(item(h, t, k) for h, t, k in NAV)
    return f"""<nav class="nav" aria-label="Main">
  <div class="wrap">
    <a class="logo" href="index.html"><img src="assets/logo.svg" alt="Digital Mondo" width="207" height="56"></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="navlist"><span class="mb-ic" aria-hidden="true"><i></i><i></i></span><span class="mb-t">Menu</span></button>
    <ul id="navlist">{items}<li class="nav-cta"><a class="btn" href="contact.html">Free audit</a></li><li class="nav-foot"><a href="mailto:{EMAIL}">{EMAIL}</a><span>Your neighborhood, seen by the world.</span></li></ul>
  </div>
</nav>
"""

FOOTER = f"""<footer>
  <div class="wrap">
    <div class="f-brand">
      <a class="logo" href="index.html"><img src="assets/logo-reversed.svg" alt="Digital Mondo" width="196" height="63"></a>
      <p class="f-tag">Your neighborhood, seen by the world. Social media, local SEO, reputation and websites for small businesses, from $250 a month.</p>
      <a class="f-mail" href="mailto:{EMAIL}">{EMAIL}</a>
      <a class="btn f-cta" href="contact.html">Get a free marketing audit</a>
    </div>
    <div>
      <h2 class="fh">Services</h2>
      <ul><li><a href="social-media-management.html">Social media management</a></li><li><a href="local-seo.html">Local SEO</a></li><li><a href="reputation-management.html">Reputation management</a></li><li><a href="website-design.html">Websites</a></li><li><a href="pricing.html">Plans and pricing</a></li></ul>
    </div>
    <div>
      <h2 class="fh">Company</h2>
      <ul><li><a href="about.html">About</a></li><li><a href="industries.html">Industries</a></li><li><a href="social.html">Social media examples</a></li><li><a href="faq.html">FAQ</a></li><li><a href="contact.html">Contact</a></li></ul>
    </div>
    <div>
      <h2 class="fh">Free tools</h2>
      <ul><li><a href="contact.html">Free marketing audit</a></li><li><a href="contact.html#speed">Website speed check</a></li><li><a href="checklist.html">Google profile checklist</a></li><li><a href="pricing.html#value">Customer value calculator</a></li><li><a href="pricing.html#builder">Plan builder</a></li><li><a href="post-planner.html">Post planner</a></li><li><a href="review-cards.html">Review card maker</a></li><li><a href="resources.html">Guides</a></li></ul>
    </div>
    <div class="f-notice">All company names, brands, logos and trademarks shown on this site, including Google, Instagram, Facebook, TikTok, YouTube, LinkedIn, Yelp and others, are the property of their respective owners. They are used for identification and reference purposes only and do not imply any affiliation with, sponsorship by or endorsement from the trademark holders. Businesses shown in social media examples are fictional sample brands. Digital Mondo LLC is an independent marketing agency.</div>
    <div class="legal"><span>© 2026 Digital Mondo LLC. All rights reserved.</span><span class="legal-links"><a href="terms.html">Terms of Service</a><a href="privacy.html">Privacy Policy</a><a href="accessibility.html">Accessibility</a><a href="contact.html">Contact</a></span></div>
  </div>
</footer>
__MCTA__<script src="site.js?v=__JSV__"></script>
</body>
</html>
"""

def img(m):
    """{{img:PHOTO-ID:WIDTH:alt text}} -> responsive Unsplash image"""
    pid, w, alt = m.group(1), int(m.group(2)), m.group(3)
    base = f"https://images.unsplash.com/photo-{pid}?auto=format&fit=crop&q=75"
    return (f'<img src="{base}&w={w}" srcset="{base}&w={w//2} {w//2}w, {base}&w={w} {w}w, {base}&w={int(w*1.6)} {int(w*1.6)}w" '
            f'sizes="(max-width: 700px) 100vw, {w}px" alt="{alt}" loading="lazy" decoding="async">')

def guide_cards(exclude=None, limit=None):
    items = [g for g in guides.GUIDES if g["slug"] != exclude][:limit]
    cls = "g-cards g5" if len(items) == 5 else "g-cards"
    return f'<div class="{cls}">' + "".join(
        f'<a class="g-card" href="{g["slug"]}.html"><div class="ph">{{{{img:{g["photo"][0]}:640:{g["photo"][1]}}}}}</div>'
        f'<div class="g-body"><span class="g-tag">{g["tag"]} · {g["minutes"]} min read</span><h3>{esc(g["title"])}</h3><p>{esc(g["desc"])}</p><span class="g-go">Read the guide →</span></div></a>'
        for g in items) + "</div>"


def guide_page(g):
    body = open(os.path.join(SRC, "guides", g["slug"] + ".html")).read()
    toc = "".join(f'<li><a href="{g["slug"]}.html#{i}">{re.sub("<[^>]+>", "", t)}</a></li>' for i, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body))
    take = "".join(f"<li>{esc(t)}</li>" for t in g["takeaways"])
    from datetime import date
    nice = date.fromisoformat(g["date"]).strftime("%B %-d, %Y")
    return f"""<article class="guide">
<header class="g-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="resources.html">Guides</a><span>/</span><span>{g["tag"]}</span></nav>
    <div class="eyebrow rise">{g["tag"]}</div>
    <h1 class="rise" style="--d:.1s">{esc(g["title"])}</h1>
    <p class="g-meta rise" style="--d:.2s"><img src="assets/mondo-mark.svg" alt="" width="34" height="34"><span>By {guides.AUTHOR}, founder of Digital Mondo · {nice} · {g["minutes"]} min read</span></p>
  </div>
  <div class="wrap"><div class="ph g-cover rise" style="--d:.25s">{{{{img:{g["photo"][0]}:1200:{g["photo"][1]}}}}}</div></div>
</header>
<div class="wrap g-layout">
  <div class="g-side">
    <nav class="toc" aria-label="In this guide"><b>In this guide</b><ol>{toc}</ol></nav>
  </div>
  <div class="g-main">
    <div class="takeaways"><span class="metal-label">Key takeaways</span><ul>{take}</ul></div>
    <div class="prose g-prose">{body}</div>
    <div class="g-author"><img src="assets/mondo-mark.svg" alt="" width="56" height="56"><div><b>Written by Karla</b><p>Karla is the founder of Digital Mondo, a one-person marketing agency for local businesses. She has traveled widely and used social media the way people around the world actually use it. <a href="about.html">More about Karla →</a></p></div></div>
  </div>
</div>
</article>
<section class="alt">
  <div class="wrap">
    <div class="sec-head reveal"><div><div class="eyebrow">Keep reading</div><h2 class="h2">More guides.</h2></div><a class="btn ghost" href="resources.html">All guides and tools →</a></div>
    <div class="reveal">{guide_cards(exclude=g["slug"], limit=3)}</div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="cta-band reveal">
      <div><h2>Want this done for you?</h2><p>Your free marketing audit shows exactly where you stand and the quickest wins, in plain English.</p></div>
      <a class="btn" href="contact.html">Get a free marketing audit</a>
    </div>
  </div>
</section>"""


def guide_ld(g):
    url = SITE_URL + g["slug"] + ".html"
    art = {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"],
           "datePublished": g["date"], "dateModified": g["date"], "mainEntityOfPage": url,
           "image": f'https://images.unsplash.com/photo-{g["photo"][0]}?auto=format&fit=crop&w=1200&q=75',
           "author": {"@type": "Person", "name": guides.AUTHOR, "url": SITE_URL + "about.html"},
           "publisher": {"@type": "Organization", "name": "Digital Mondo", "logo": {"@type": "ImageObject", "url": SITE_URL + "assets/apple-touch-icon.png"}}}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL},
        {"@type": "ListItem", "position": 2, "name": "Guides", "item": SITE_URL + "resources.html"},
        {"@type": "ListItem", "position": 3, "name": g["title"], "item": url}]}
    return ld(art) + ld(crumbs)


def faq_ld(body):
    qa = re.findall(r"<details><summary>(.*?)</summary><p>(.*?)</p></details>", body, re.S)
    if not qa:
        return ""
    strip = lambda t: re.sub("<[^>]+>", "", t).strip()
    return ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in qa]})


def service_page(sp):
    others = [o for o in service_pages.PAGES if o["id"] != sp["id"]]
    inc = "".join(f'<div class="card"><h3>{esc(h)}</h3><ul class="ticks">' + "".join(f"<li>{esc(x)}</li>" for x in items) + "</ul></div>" for h, items in sp["included"])
    steps = "".join(f'<li class="reveal" style="--d:{i*.08:.2f}s"><span class="sp-n">0{i+1}</span><h3>{esc(h)}</h3><p>{esc(t)}</p></li>' for i, (h, t) in enumerate(sp["steps"]))
    faqs = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in sp["faqs"])
    where = "".join(f'<span class="chip">{esc(w)}</span>' for w in sp["where"])
    low = plans.BY_ID[sp["id"]]["tiers"][0]["price"]
    g = guides.BY_SLUG.get(sp["guide"]) if sp["guide"] else None
    guide = (f'<a class="sp-guide reveal" href="{g["slug"]}.html"><div class="ph">{{{{img:{g["photo"][0]}:480:{g["photo"][1]}}}}}</div>'
             f'<div><span class="g-tag">Free guide · {g["minutes"]} min read</span><h3>{esc(g["title"])}</h3><p>{esc(g["desc"])}</p><span class="g-go">Read the guide →</span></div></a>') if g else \
            ('<a class="sp-guide reveal" href="contact.html#speed"><div class="ph">{{img:1460925895917-afdab827c52f:480:A laptop showing website analytics charts}}</div>'
             '<div><span class="g-tag">Free tool</span><h3>Check your website speed</h3><p>See how fast your site loads on a phone, scored by Google, in under a minute.</p><span class="g-go">Run the speed check →</span></div></a>')
    more = "".join(f'<a class="sp-other" href="{o["file"]}"><span class="g-tag">{o["tag"]}</span><b>{esc(o["short"])}</b><span class="g-go">From ${plans.BY_ID[o["id"]]["tiers"][0]["price"]}/mo →</span></a>' for o in others)
    return f"""<header class="page-head split sp-head">
  <div class="wrap">
    <div>
      <nav class="crumbs rise" aria-label="Breadcrumb"><a href="services.html">Services</a><span>/</span><span>{esc(sp["tag"])}</span></nav>
      <div class="eyebrow rise">{esc(sp["short"])}</div>
      <h1 class="rise" style="--d:.1s">{esc(sp["h1"])}</h1>
      <p class="intro rise" style="--d:.2s">{esc(sp["intro"])}</p>
      <div class="hero-cta rise" style="--d:.3s"><a class="btn" href="#plans">See plans from ${low}/mo</a><a class="btn ghost" href="contact.html">Get a free audit</a></div>
      <div class="where rise" style="--d:.35s">{where}</div>
    </div>
    <div class="ph rise" style="--d:.25s">{{{{img:{sp["photo"][0]}:700:{sp["photo"][1]}}}}}</div>
  </div>
</header>

<section class="sp-sec">
  <div class="wrap sp-inc">
    <div class="reveal">
      <div class="eyebrow">What's included</div>
      <h2 class="h2">Everything handled, start to finish.</h2>
      <div class="best"><b>Best for</b>{esc(sp["best"])}</div>
    </div>
    <div class="sp-cards reveal" style="--d:.1s">{inc}</div>
  </div>
</section>

<section class="alt" id="plans">
  <div class="wrap">
    <div class="sec-head reveal"><div><div class="eyebrow">Plans</div><h2 class="h2">Pick your level.</h2></div><p class="intro">Month to month, no setup fees. Pay yearly and get 2 months free, or add another service and save up to 20%. <a href="pricing.html">Compare all plans →</a></p></div>
    <div class="reveal">{plans.service_plans_html(sp["id"])}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="reveal"><div class="eyebrow">How it works</div><h2 class="h2">Four simple steps.</h2></div>
    <ol class="sp-steps">{steps}</ol>
  </div>
</section>

<section class="alt">
  <div class="wrap sp-faq">
    <div class="reveal"><div class="eyebrow">Questions</div><h2 class="h2">Good to know.</h2><p class="intro">More answers on the <a href="faq.html">FAQ page</a>.</p></div>
    <div class="faq reveal" style="--d:.1s">{faqs}</div>
  </div>
</section>

<section>
  <div class="wrap">
    {guide}
    <div class="sp-more reveal"><div class="eyebrow">Other services</div><div class="sp-others">{more}</div></div>
    <div class="cta-band reveal">
      <div><h2>See where you stand, free.</h2><p>Your free marketing audit shows what's working, what's missing and the quickest wins, in plain English.</p></div>
      <a class="btn" href="contact.html">Get a free marketing audit</a>
    </div>
  </div>
</section>"""


def service_ld(sp):
    url = SITE_URL + sp["file"]
    tiers = plans.BY_ID[sp["id"]]["tiers"]
    svc = {"@context": "https://schema.org", "@type": "Service", "name": sp["title"], "description": sp["desc"], "url": url,
           "provider": {"@type": "Organization", "name": "Digital Mondo", "url": SITE_URL},
           "areaServed": "US",
           "offers": [{"@type": "Offer", "name": t, "price": str(tier["price"]), "priceCurrency": "USD",
                       "priceSpecification": {"@type": "UnitPriceSpecification", "price": str(tier["price"]), "priceCurrency": "USD", "unitText": "MONTH"}}
                      for t, tier in zip(plans.TIERS, tiers)]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL},
        {"@type": "ListItem", "position": 2, "name": "Services", "item": SITE_URL + "services.html"},
        {"@type": "ListItem", "position": 3, "name": sp["title"], "item": url}]}
    return ld(svc) + ld(crumbs)


def industry_page(ip):
    combo = [c for c in plans.COMBOS if c["id"] == ip["combo"]][0]
    pr = plans.combo_prices(combo["services"]); pct = plans.pct_for(len(combo["services"]))
    svc_names = " + ".join(plans.BY_ID[s]["name"] for s in combo["services"])
    preset = "pricing.html?plan=" + ",".join(f"{s}-growth" for s in combo["services"]) + "#builder"
    sp_links = "".join(f'<a class="chip" href="{sp["file"]}">{esc(sp["short"])}</a>' for sp in service_pages.PAGES if sp["id"] in combo["services"])
    chall = "".join(f"<li>{esc(x)}</li>" for x in ip["challenges"])
    focus = "".join(f"<li>{esc(x)}</li>" for x in ip["focus"])
    month = "".join(f'<li class="reveal" style="--d:{i*.06:.2f}s"><span class="sp-n">0{i+1}</span><p>{esc(x)}</p></li>' for i, x in enumerate(ip["month"]))
    ideas = "".join(f'<span class="chip">{esc(x)}</span>' for x in ip["ideas"])
    planner = (f'<a class="btn ghost" href="post-planner.html?ind={ip["planner"]}">Get four weeks of post ideas →</a>' if ip["planner"] else "")
    example = (f'<a class="btn ghost" href="{ip["example"][0]}">{esc(ip["example"][1].rstrip(" →"))} →</a>' if ip["example"] else "")
    faqs = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in ip["faqs"])
    g = guides.BY_SLUG[ip["guide"]]
    others = "".join(f'<a class="chip" href="{o["file"]}">{esc(o["name"])}</a>' for o in industry_pages.PAGES if o["id"] != ip["id"])
    return f"""<header class="page-head split sp-head">
  <div class="wrap">
    <div>
      <nav class="crumbs rise" aria-label="Breadcrumb"><a href="industries.html">Industries</a><span>/</span><span>{esc(ip["name"])}</span></nav>
      <div class="eyebrow rise">{esc(ip["tag"])}</div>
      <h1 class="rise" style="--d:.1s">{esc(ip["h1"])}</h1>
      <p class="intro rise" style="--d:.2s">{esc(ip["intro"])}</p>
      <div class="hero-cta rise" style="--d:.3s"><a class="btn" href="contact.html">Get a free audit</a><a class="btn ghost" href="#plan">See the plan I'd suggest</a></div>
    </div>
    <div class="ph rise" style="--d:.25s">{{{{img:{ip["photo"]}:700:{ip["name"]}}}}}</div>
  </div>
</header>

<section class="sp-sec">
  <div class="wrap">
    <div class="reveal"><div class="eyebrow">Where it gets stuck</div><h2 class="h2">What I see most with {esc(ip["noun"])}.</h2></div>
    <div class="in-cmp reveal" style="--d:.1s">
      <div class="card"><h3>Common challenges</h3><ul class="xl">{chall}</ul></div>
      <div class="card in-fix"><h3>What I focus on</h3><ul class="ticks">{focus}</ul></div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="reveal"><div class="eyebrow">A typical month</div><h2 class="h2">What you can expect.</h2></div>
    <ol class="sp-steps in-month">{month}</ol>
    <div class="in-ideas reveal"><b>Content ideas</b>{ideas}</div>
    <div class="in-links reveal">{planner}{example}</div>
  </div>
</section>

<section id="plan">
  <div class="wrap">
    <div class="in-plan reveal">
      <div>
        <div class="eyebrow">Where I'd start</div>
        <h2 class="h2">{esc(combo["name"])}</h2>
        <p class="intro">{esc(combo["pitch"])}</p>
        <div class="in-svcs">{sp_links}</div>
      </div>
      <div class="in-price">
        <span class="lbl">{esc(svc_names)}</span>
        <div class="in-amt">from <b><span class="amt" data-m="{pr[0][1]}">${pr[0][1]:,}</span></b>/month</div>
        <p>Essentials level, {pct}% off for combining. Growth is <span class="amt" data-m="{pr[1][1]}">${pr[1][1]:,}</span>/month. Every plan is month to month, or pay yearly for 2 months free.</p>
        <a class="btn" href="{preset}">Open this plan in the builder</a>
        <a class="in-all" href="pricing.html">Compare every plan →</a>
      </div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap sp-faq">
    <div class="reveal"><div class="eyebrow">Questions</div><h2 class="h2">Good to know.</h2><p class="intro">More answers on the <a href="faq.html">FAQ page</a>.</p></div>
    <div class="faq reveal" style="--d:.1s">{faqs}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <a class="sp-guide reveal" href="{g["slug"]}.html"><div class="ph">{{{{img:{g["photo"][0]}:480:{g["photo"][1]}}}}}</div><div><span class="g-tag">Free guide · {g["minutes"]} min read</span><h3>{esc(g["title"])}</h3><p>{esc(g["desc"])}</p><span class="g-go">Read the guide →</span></div></a>
    <div class="sp-more reveal"><div class="eyebrow">Other industries</div><div class="in-others">{others}</div></div>
    <div class="cta-band reveal">
      <div><h2>See where you stand, free.</h2><p>Your free marketing audit compares you with two or three nearby competitors and lists the quickest wins, in plain English.</p></div>
      <a class="btn" href="contact.html">Get a free marketing audit</a>
    </div>
  </div>
</section>"""


def industry_ld(ip):
    url = SITE_URL + ip["file"]
    svc = {"@context": "https://schema.org", "@type": "Service", "name": ip["title"], "description": ip["desc"], "url": url,
           "serviceType": "Marketing", "audience": {"@type": "BusinessAudience", "name": ip["name"]},
           "provider": {"@type": "Organization", "name": "Digital Mondo", "url": SITE_URL}, "areaServed": "US"}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL},
        {"@type": "ListItem", "position": 2, "name": "Industries", "item": SITE_URL + "industries.html"},
        {"@type": "ListItem", "position": 3, "name": ip["name"], "item": url}]}
    return ld(svc) + ld(crumbs)


for g in guides.GUIDES:
    PAGES[g["slug"] + ".html"] = (g.get("seo_title", g["title"]) + " · Digital Mondo", g["desc"], "guide")
for sp in service_pages.PAGES:
    PAGES[sp["file"]] = (sp["title"] + " · Digital Mondo", sp["desc"], "services")
for ip in industry_pages.PAGES:
    PAGES[ip["file"]] = (ip["title"] + " · Digital Mondo", ip["desc"], "industries")

os.makedirs(DIST, exist_ok=True)
for fname, (title, desc, active) in PAGES.items():
    gd = guides.BY_SLUG.get(fname[:-5])
    sp = service_pages.BY_FILE.get(fname)
    ipg = industry_pages.BY_FILE.get(fname)
    src = guide_page(gd) if gd else service_page(sp) if sp else industry_page(ipg) if ipg else open(os.path.join(SRC, fname)).read()
    styles = "\n".join(re.findall(r"<style>.*?</style>", src, re.S))
    body = re.sub(r"<style>.*?</style>", "", src, flags=re.S).strip()
    body = body.replace("{{packages}}", plans.packages_html()).replace("{{packages_home}}", plans.packages_html(table=False)).replace("{{plans}}", plans.tabs_html()).replace("{{builder}}", plans.builder_html()).replace("{{plans_json}}", plans.plans_json())
    body = body.replace("{{guide_cards_3}}", guide_cards(limit=3)).replace("{{guide_cards}}", guide_cards())
    body = re.sub(r"\{\{img:([0-9a-f-]+):(\d+):([^}]*)\}\}", img, body)
    # The first photo on a page is usually above the fold: load it right away.
    body = body.replace('loading="lazy" decoding="async"', 'loading="eager" fetchpriority="high" decoding="async"', 1)
    extra = guide_ld(gd) if gd else (service_ld(sp) + faq_ld(body)) if sp else (industry_ld(ipg) + faq_ld(body)) if ipg else (faq_ld(body) if fname in ("faq.html",) else "")
    mcta = "" if active in ("contact", "legal", "404") else '<aside aria-label="Free audit"><a class="btn mcta" href="contact.html">Get a free marketing audit</a></aside>\n'
    with open(os.path.join(DIST, fname), "w") as f:
        f.write(head(fname, title, desc, styles, active, extra) + nav("resources" if active == "guide" else active, fname) + '<main id="main">\n' + body + "\n</main>\n"
                + FOOTER.replace("__JSV__", ver("site.js")).replace("__MCTA__", mcta))

shutil.copy(os.path.join(ROOT, "style.css"), os.path.join(DIST, "style.css"))
with open(os.path.join(ROOT, "site.js")) as f_in, open(os.path.join(DIST, "site.js"), "w") as f_out:
    f_out.write(f_in.read().replace("__FORM_ENDPOINT__", FORM_ENDPOINT).replace("__EMAIL__", EMAIL))
shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(DIST, "assets"), dirs_exist_ok=True)

# Search engines: sitemap and robots
urls = [SITE_URL + ("" if f == "index.html" else f) for f in PAGES if f != "404.html"]
with open(os.path.join(DIST, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
with open(os.path.join(DIST, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n")
print("built", len(PAGES), "pages")
