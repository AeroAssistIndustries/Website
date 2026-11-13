"""Wraps each page partial in src/ with the shared head, nav and footer; writes to dist/."""
import os, re, shutil

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
       ("pricing.html", "Pricing", "pricing"), ("social.html", "Social examples", "social"), ("about.html", "About", "about")]

def head(title, desc, style):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=Figtree:wght@400;500;600;700&family=Fraunces:ital,opsz,wght@0,9..144,500..800;1,9..144,500..700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
{style}
</head>
<body>
"""

def nav(active):
    items = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if k == active else ""}>{t}</a></li>' for h, t, k in NAV)
    return f"""<nav class="nav" aria-label="Main">
  <div class="wrap">
    <a class="logo" href="index.html"><span class="dot"></span>Karla's Agency</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="navlist">Menu</button>
    <ul id="navlist">{items}<li><a class="btn" href="contact.html">Free audit</a></li></ul>
  </div>
</nav>
"""

FOOTER = """<footer>
  <div class="wrap">
    <div>
      <a class="logo" href="index.html"><span class="dot"></span>Karla's Agency</a>
      <p style="margin-top:14px;max-width:34ch">Local marketing for small businesses: Google profiles, social media and reviews, done every month.</p>
      <p style="margin-top:14px">hello@karlasagency.com</p>
    </div>
    <div>
      <h4>Services</h4>
      <ul><li><a href="services.html#gbp">Google Business Profile</a></li><li><a href="services.html#social">Social media</a></li><li><a href="services.html#reviews">Reputation</a></li><li><a href="services.html#seo">Local SEO</a></li><li><a href="services.html#web">Websites</a></li><li><a href="services.html#ads">Advertising</a></li></ul>
    </div>
    <div>
      <h4>Company</h4>
      <ul><li><a href="about.html">About</a></li><li><a href="industries.html">Industries</a></li><li><a href="pricing.html">Pricing</a></li><li><a href="social.html">Social examples</a></li></ul>
    </div>
    <div>
      <h4>Free resources</h4>
      <ul><li><a href="contact.html">Free marketing audit</a></li><li><a href="checklist.html">Google profile checklist</a></li></ul>
    </div>
    <div class="legal">© 2026 Karla's Agency. All rights reserved. Brands shown in examples are sample businesses created to illustrate our work.</div>
  </div>
</footer>
<script src="site.js"></script>
</body>
</html>
"""

os.makedirs(DIST, exist_ok=True)
for fname, (title, desc, active) in PAGES.items():
    src = open(os.path.join(SRC, fname)).read()
    styles = "\n".join(re.findall(r"<style>.*?</style>", src, re.S))
    body = re.sub(r"<style>.*?</style>", "", src, flags=re.S).strip()
    with open(os.path.join(DIST, fname), "w") as f:
        f.write(head(title, desc, styles) + nav(active) + "<main>\n" + body + "\n</main>\n" + FOOTER)
for asset in ["style.css", "site.js"]:
    shutil.copy(os.path.join(ROOT, asset), os.path.join(DIST, asset))
print("built", len(PAGES), "pages")
