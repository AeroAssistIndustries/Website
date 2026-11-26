"""Wraps each page partial in src/ with the shared head, nav and footer; writes the finished site to docs/."""
import os, re, shutil, hashlib, json
import plans, guides
from html import escape as esc

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC, DIST = os.path.join(ROOT, "src"), os.path.join(ROOT, "docs")

# Where the site lives. Change both when it moves to its own domain (e.g. https://karladigital.com and "/").
SITE_URL = "https://aeroassistindustries.github.io/Website/"
SITE_PATH = "/Website/"
EMAIL = "hello@karladigital.com"

PAGES = {
    "index.html":         ("Karla Digital · Local Marketing with a Worldly Eye", "Social media, local SEO, reputation management and websites for local businesses, from $250 a month. One person, real attention, month to month.", "home"),
    "services.html":      ("Services · Karla Digital", "Social media management, local SEO, online reputation management and websites for local businesses, each from $250 a month.", "services"),
    "industries.html":    ("Industries · Karla Digital", "Marketing for hotels, restaurants, salons, real estate, contractors, dental and wellness practices, retail and local services.", "industries"),
    "pricing.html":       ("Pricing · Karla Digital", "Plans from $250 a month, all four services from $595 a month, combos up to 20% off, and 2 months free when you pay yearly.", "pricing"),
    "social.html":        ("Social Media Examples · Karla Digital", "Sample social media posts, Reels and content calendars for local businesses.", "social"),
    "about.html":         ("About · Karla Digital", "Meet Karla, a well-traveled founder bringing a worldly eye to local marketing.", "about"),
    "faq.html":           ("FAQ · Karla Digital", "Answers about plans, pricing, contracts, accounts, reporting and how working with Karla Digital works.", "faq"),
    "resources.html":     ("Guides & Free Tools · Karla Digital", "Plain-English guides to Google reviews, your Google Business Profile, social media and reaching visitors, plus free marketing tools.", "resources"),
    "checklist.html":     ("Google Business Profile Checklist · Karla Digital", "A free, interactive checklist to see how complete your Google Business Profile is.", "checklist"),
    "contact.html":       ("Free Marketing Audit · Karla Digital", "Request a free marketing audit and website speed check from Karla Digital.", "contact"),
    "terms.html":         ("Terms of Service · Karla Digital", "The terms that apply to using this website and to Karla Digital's marketing services.", "legal"),
    "privacy.html":       ("Privacy Policy · Karla Digital", "How Karla Digital collects, uses and protects personal information.", "legal"),
    "accessibility.html": ("Accessibility · Karla Digital", "Karla Digital's commitment to an accessible website, and how to report a barrier.", "legal"),
    "404.html":           ("Page not found · Karla Digital", "The page you were looking for isn't here.", "404"),
}

NAV = [("services.html", "Services", "services"), ("industries.html", "Industries", "industries"),
       ("pricing.html", "Pricing", "pricing"), ("social.html", "Our work", "social"), ("resources.html", "Guides", "resources"), ("about.html", "About", "about")]

SCHEMA = {
    "@context": "https://schema.org", "@type": "ProfessionalService", "name": "Karla Digital",
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
<meta name="theme-color" content="#16181c">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="assets/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<meta property="og:type" content="{"article" if active == "guide" else "website"}">
<meta property="og:site_name" content="Karla Digital">
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
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Figtree:wght@400;500;600;700&family=Bricolage+Grotesque:opsz,wght@12..96,600..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v={ver('style.css')}">
<script>document.documentElement.classList.add('js')</script>
{style}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""

def nav(active):
    items = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if k == active else ""}>{t}</a></li>' for h, t, k in NAV)
    return f"""<nav class="nav" aria-label="Main">
  <div class="wrap">
    <a class="logo" href="index.html"><img src="assets/logo.svg" alt="Karla Digital" width="178" height="40"></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="navlist">Menu</button>
    <ul id="navlist">{items}<li><a class="btn" href="contact.html">Free audit</a></li></ul>
  </div>
</nav>
"""

FOOTER = f"""<footer>
  <div class="wrap">
    <div class="f-brand">
      <a class="logo" href="index.html"><img src="assets/logo-reversed.svg" alt="Karla Digital" width="214" height="48"></a>
      <p class="f-tag">Local marketing with a worldly eye. Social media, local SEO, reputation and websites for small businesses, from $250 a month.</p>
      <a class="f-mail" href="mailto:{EMAIL}">{EMAIL}</a>
      <a class="btn f-cta" href="contact.html">Get a free marketing audit</a>
    </div>
    <div>
      <h4>Services</h4>
      <ul><li><a href="services.html#social">Social media management</a></li><li><a href="services.html#seo">Local SEO</a></li><li><a href="services.html#reviews">Reputation management</a></li><li><a href="services.html#web">Websites</a></li><li><a href="pricing.html">Plans and pricing</a></li></ul>
    </div>
    <div>
      <h4>Company</h4>
      <ul><li><a href="about.html">About Karla</a></li><li><a href="industries.html">Industries</a></li><li><a href="social.html">Social media examples</a></li><li><a href="faq.html">FAQ</a></li><li><a href="contact.html">Contact</a></li></ul>
    </div>
    <div>
      <h4>Free tools</h4>
      <ul><li><a href="contact.html">Free marketing audit</a></li><li><a href="contact.html#speed">Website speed check</a></li><li><a href="checklist.html">Google profile checklist</a></li><li><a href="pricing.html#value">Customer value calculator</a></li><li><a href="pricing.html#builder">Plan builder</a></li><li><a href="resources.html">Guides</a></li></ul>
    </div>
    <div class="f-notice">All company names, brands, logos and trademarks shown on this site, including Google, Instagram, Facebook, TikTok, YouTube, LinkedIn, Yelp and others, are the property of their respective owners. They are used for identification and reference purposes only and do not imply any affiliation with, sponsorship by or endorsement from the trademark holders. Businesses shown in social media examples are fictional sample brands. Karla Digital LLC is an independent marketing agency.</div>
    <div class="legal"><span>© 2026 Karla Digital LLC. All rights reserved.</span><span class="legal-links"><a href="terms.html">Terms of Service</a><a href="privacy.html">Privacy Policy</a><a href="accessibility.html">Accessibility</a><a href="contact.html">Contact</a></span></div>
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
    return '<div class="g-cards">' + "".join(
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
    <p class="g-meta rise" style="--d:.2s"><img src="assets/ka-seal.svg" alt="" width="34" height="34"><span>By {guides.AUTHOR}, founder of Karla Digital · {nice} · {g["minutes"]} min read</span></p>
  </div>
  <div class="wrap"><div class="ph g-cover rise" style="--d:.25s">{{{{img:{g["photo"][0]}:1200:{g["photo"][1]}}}}}</div></div>
</header>
<div class="wrap g-layout">
  <aside class="g-side">
    <nav class="toc" aria-label="In this guide"><b>In this guide</b><ol>{toc}</ol></nav>
  </aside>
  <div class="g-main">
    <div class="takeaways"><span class="metal-label">Key takeaways</span><ul>{take}</ul></div>
    <div class="prose g-prose">{body}</div>
    <div class="g-author"><img src="assets/ka-seal.svg" alt="" width="56" height="56"><div><b>Written by Karla</b><p>Karla is the founder of Karla Digital, a one-person marketing agency for local businesses. She has traveled widely and used social media the way people around the world actually use it. <a href="about.html">More about Karla →</a></p></div></div>
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
           "publisher": {"@type": "Organization", "name": "Karla Digital", "logo": {"@type": "ImageObject", "url": SITE_URL + "assets/apple-touch-icon.png"}}}
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


for g in guides.GUIDES:
    PAGES[g["slug"] + ".html"] = (g["title"] + " · Karla Digital", g["desc"], "guide")

os.makedirs(DIST, exist_ok=True)
for fname, (title, desc, active) in PAGES.items():
    gd = guides.BY_SLUG.get(fname[:-5])
    src = guide_page(gd) if gd else open(os.path.join(SRC, fname)).read()
    styles = "\n".join(re.findall(r"<style>.*?</style>", src, re.S))
    body = re.sub(r"<style>.*?</style>", "", src, flags=re.S).strip()
    body = body.replace("{{packages}}", plans.packages_html()).replace("{{packages_home}}", plans.packages_html(table=False)).replace("{{plans}}", plans.tabs_html()).replace("{{builder}}", plans.builder_html()).replace("{{plans_json}}", plans.plans_json())
    body = body.replace("{{guide_cards_3}}", guide_cards(limit=3)).replace("{{guide_cards}}", guide_cards())
    body = re.sub(r"\{\{img:([0-9a-f-]+):(\d+):([^}]*)\}\}", img, body)
    # The first photo on a page is usually above the fold: load it right away.
    body = body.replace('loading="lazy" decoding="async"', 'loading="eager" fetchpriority="high" decoding="async"', 1)
    extra = guide_ld(gd) if gd else (faq_ld(body) if fname in ("faq.html",) else "")
    mcta = "" if active in ("contact", "legal", "404") else '<a class="btn mcta" href="contact.html">Get a free marketing audit</a>\n'
    with open(os.path.join(DIST, fname), "w") as f:
        f.write(head(fname, title, desc, styles, active, extra) + nav("resources" if active == "guide" else active) + '<main id="main">\n' + body + "\n</main>\n"
                + FOOTER.replace("__JSV__", ver("site.js")).replace("__MCTA__", mcta))

for asset in ["style.css", "site.js"]:
    shutil.copy(os.path.join(ROOT, asset), os.path.join(DIST, asset))
shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(DIST, "assets"), dirs_exist_ok=True)

# Search engines: sitemap and robots
urls = [SITE_URL + ("" if f == "index.html" else f) for f in PAGES if f != "404.html"]
with open(os.path.join(DIST, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
with open(os.path.join(DIST, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n")
print("built", len(PAGES), "pages")
