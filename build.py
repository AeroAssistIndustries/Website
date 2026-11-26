"""Wraps each page partial in src/ with the shared head, nav and footer; writes to dist/."""
import os, re, shutil, hashlib
import plans

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC, DIST = os.path.join(ROOT, "src"), os.path.join(ROOT, "docs")

PAGES = {
    "index.html":     ("Karla's Agency", "Karla's Agency helps local businesses get found on Google, stay active on social media and earn more reviews.", "home"),
    "services.html":  ("Services · Karla's Agency", "Google Business Profile, social media, reviews, local SEO, websites, ads, email and AI search visibility for local businesses.", "services"),
    "industries.html":("Industries · Karla's Agency", "Marketing for hotels, restaurants, salons, real estate, contractors, dental and wellness practices, retail and local services.", "industries"),
    "pricing.html":   ("Pricing · Karla's Agency", "Month-to-month marketing packages for local businesses, plus add-ons and one-time projects.", "pricing"),
    "social.html":    ("Social Media Examples · Karla's Agency", "Sample social media posts, Reels and content calendars from Karla's Agency.", "social"),
    "about.html":     ("About · Karla's Agency", "How Karla's Agency works: honest, consistent, clearly reported local marketing.", "about"),
    "checklist.html": ("Google Business Profile Checklist · Karla's Agency", "A free, interactive checklist to see how complete your Google Business Profile is.", "checklist"),
    "contact.html":   ("Free Marketing Audit · Karla's Agency", "Request a free marketing audit from Karla's Agency.", "contact"),
}

NAV = [("services.html", "Services", "services"), ("industries.html", "Industries", "industries"),
       ("pricing.html", "Pricing", "pricing"), ("social.html", "Our work", "social"), ("about.html", "About", "about")]

def ver(name):
    return hashlib.md5(open(os.path.join(ROOT, name), "rb").read()).hexdigest()[:8]

def head(title, desc, style):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="assets/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="assets/og-image.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=Figtree:wght@400;500;600;700&family=Fraunces:ital,opsz,wght@0,9..144,500..800;1,9..144,500..700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v={ver('style.css')}">
<script>document.documentElement.classList.add('js')</script>
{style}
</head>
<body>
"""

def nav(active):
    items = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if k == active else ""}>{t}</a></li>' for h, t, k in NAV)
    return f"""<nav class="nav" aria-label="Main">
  <div class="wrap">
    <a class="logo" href="index.html"><img src="assets/logo.svg" alt="Karla's Agency" width="180" height="38"></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="navlist">Menu</button>
    <ul id="navlist">{items}<li><a class="btn" href="contact.html">Free audit</a></li></ul>
  </div>
</nav>
"""

FOOTER = """<footer>
  <div class="wrap">
    <div>
      <a class="logo" href="index.html"><img src="assets/logo-reversed.svg" alt="Karla's Agency" width="200" height="42"></a>
      <p style="margin-top:14px;max-width:34ch">Local marketing for small businesses: Google profiles, social media and reviews, done every month.</p>
      <p style="margin-top:14px">hello@karlasagency.com</p>
    </div>
    <div>
      <h4>Services</h4>
      <ul><li><a href="services.html#social">Social media management</a></li><li><a href="services.html#seo">Local SEO</a></li><li><a href="services.html#reviews">Reputation management</a></li><li><a href="services.html#web">Websites</a></li><li><a href="pricing.html">Plans from $250/month</a></li></ul>
    </div>
    <div>
      <h4>Company</h4>
      <ul><li><a href="about.html">About</a></li><li><a href="industries.html">Industries</a></li><li><a href="pricing.html">Pricing</a></li><li><a href="social.html">Social media examples</a></li></ul>
    </div>
    <div>
      <h4>Free resources</h4>
      <ul><li><a href="contact.html">Free marketing audit</a></li><li><a href="checklist.html">Google profile checklist</a></li></ul>
    </div>
    <div class="legal">© 2026 Karla's Agency. All rights reserved. Brands shown in examples are sample businesses created to illustrate our work.</div>
  </div>
</footer>
__MCTA__<script src="site.js?v=__JSV__"></script>
</body>
</html>
"""

os.makedirs(DIST, exist_ok=True)
for fname, (title, desc, active) in PAGES.items():
    src = open(os.path.join(SRC, fname)).read()
    styles = "\n".join(re.findall(r"<style>.*?</style>", src, re.S))
    body = re.sub(r"<style>.*?</style>", "", src, flags=re.S).strip()
    # {{img:PHOTO-ID:WIDTH:alt text}} -> responsive Unsplash image
    def img(m):
        pid, w, alt = m.group(1), int(m.group(2)), m.group(3)
        base = f"https://images.unsplash.com/photo-{pid}?auto=format&fit=crop&q=75"
        return (f'<img src="{base}&w={w}" srcset="{base}&w={w//2} {w//2}w, {base}&w={w} {w}w, {base}&w={int(w*1.6)} {int(w*1.6)}w" '
                f'sizes="(max-width: 700px) 100vw, {w}px" alt="{alt}" loading="lazy" decoding="async">')
    body = body.replace("{{plans}}", plans.tabs_html()).replace("{{builder}}", plans.builder_html()).replace("{{plans_json}}", plans.plans_json())
    body = re.sub(r"\{\{img:([0-9a-f-]+):(\d+):([^}]*)\}\}", img, body)
    with open(os.path.join(DIST, fname), "w") as f:
        f.write(head(title, desc, styles) + nav(active) + "<main>\n" + body + "\n</main>\n" + FOOTER.replace("__JSV__", ver("site.js")).replace("__MCTA__", "" if active == "contact" else '<a class="btn mcta" href="contact.html">Get a free marketing audit</a>\n'))
for asset in ["style.css", "site.js"]:
    shutil.copy(os.path.join(ROOT, asset), os.path.join(DIST, asset))
shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(DIST, "assets"), dirs_exist_ok=True)
print("built", len(PAGES), "pages")
