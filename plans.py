"""Karla Digital service plans: one source for the pricing tabs, the plan builder and the JSON the page script reads."""
import json
from html import escape

TIERS = ["Essentials", "Growth", "Pro"]

PLANS = [
    {"id": "social", "name": "Social Media Management", "short": "Social media", "tag": "SMM",
     "pitch": "A steady, on-brand feed that gives people a reason to visit.",
     "tiers": [
        {"price": 250, "for": "Get consistent on one platform.",
         "items": ["1 platform (Instagram or Facebook)", "8 designed posts a month", "Captions and hashtags in your voice", "Scheduling and posting", "Monthly report"]},
        {"price": 650, "for": "Grow on the two platforms that matter most.", "popular": True,
         "items": ["2 platforms", "12 designed posts a month", "2 Reels or TikToks planned and edited", "Weekly Stories", "Comment and DM replies", "Monthly content calendar for approval"]},
        {"price": 1500, "for": "Full-service social, handled every day.",
         "items": ["Up to 3 platforms", "20 designed posts a month", "4 Reels or TikToks edited", "Daily community management", "Boosted post management (ad spend separate)", "Monthly strategy call"]},
     ]},
    {"id": "seo", "name": "Local SEO", "short": "Local SEO", "tag": "SEO",
     "pitch": "Show up when people nearby search on Google, Maps and AI assistants.",
     "tiers": [
        {"price": 250, "for": "Fix the foundations of local search.",
         "items": ["Google Business Profile optimization", "4 Google profile posts a month", "Listing cleanup on 10 directories", "Monthly ranking snapshot"]},
        {"price": 600, "for": "Climb for the searches that bring customers.", "popular": True,
         "items": ["Everything in Essentials", "On-page SEO for up to 5 pages", "Listings on 25 directories", "1 new service page or article a month", "10 local keywords tracked"]},
        {"price": 1200, "for": "Own your neighborhood in search.",
         "items": ["Everything in Growth", "2 new pages or articles a month", "Local link building", "Technical SEO fixes", "AI search visibility checks", "25 keywords tracked, monthly call"]},
     ]},
    {"id": "reviews", "name": "Online Reputation Management", "short": "Reputation", "tag": "ORM",
     "pitch": "More genuine reviews, and a thoughtful reply to every one.",
     "tiers": [
        {"price": 250, "for": "Never leave a review unanswered.",
         "items": ["Monitoring on Google, Facebook and Yelp", "Replies to up to 30 reviews a month", "Alerts for negative reviews", "Monthly reputation report"]},
        {"price": 400, "for": "Turn happy customers into new reviews.", "popular": True,
         "items": ["Everything in Essentials", "Unlimited review replies", "Review request system (links and QR cards)", "Negative reviews answered within 24 hours"]},
        {"price": 750, "for": "Reputation across every platform and location.",
         "items": ["Everything in Growth", "Up to 3 locations or extra platforms", "Review showcase on your website", "Quarterly customer sentiment report", "Response plan for difficult reviews"]},
     ]},
    {"id": "web", "name": "Website", "short": "Website", "tag": "WEB",
     "pitch": "A fast, mobile-friendly site that turns visitors into calls and bookings.",
     "tiers": [
        {"price": 250, "for": "Keep your current site fast, safe and up to date.",
         "items": ["Hosting, security and backups", "Uptime monitoring", "Up to 1 hour of updates a month", "Speed and form checks"]},
        {"price": 500, "for": "A new site with no big upfront cost.", "popular": True,
         "items": ["New 5-page website built for you", "No upfront build fee on a 12-month plan", "Hosting, security and backups", "Up to 2 hours of updates a month", "Booking or contact buttons on every page"]},
        {"price": 1000, "for": "A website that works as hard as you do.",
         "items": ["New site with up to 12 pages", "Online booking or ordering set up", "A new landing page every month", "Up to 4 hours of updates a month", "Monthly conversion review"]},
     ]},
]

BUNDLE = {"2": 10, "3": 15}  # % off with 2 services, with 3 or more


def money(n):
    return f"${n:,}"


def tabs_html():
    """Service tabs with three tier cards each. Static HTML, so every price is in the page."""
    tabs = "".join(
        f'<button type="button" role="tab" id="tab-{p["id"]}" aria-controls="panel-{p["id"]}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">'
        f'<span class="tab-tag">{p["tag"]}</span>{escape(p["short"])}<small>from {money(p["tiers"][0]["price"])}/mo</small></button>'
        for i, p in enumerate(PLANS))
    panels = ""
    for i, p in enumerate(PLANS):
        cards = ""
        for t, tier in zip(TIERS, p["tiers"]):
            pop = tier.get("popular")
            items = "".join(f"<li>{escape(x)}</li>" for x in tier["items"])
            cards += (f'<article class="tier{" pop" if pop else ""}">'
                      f'<div class="tier-top"><span class="tier-name">{t}</span>{"<span class=badge>Most popular</span>" if pop else ""}</div>'
                      f'<div class="tier-price">{money(tier["price"])}<small>/month</small></div>'
                      f'<p class="tier-for">{escape(tier["for"])}</p><ul>{items}</ul>'
                      f'<a class="btn{"" if pop else " ghost"}" href="contact.html" data-pick="{p["id"]}:{t}">Choose {t}</a></article>')
        panels += (f'<div class="plan-panel" role="tabpanel" id="panel-{p["id"]}" aria-labelledby="tab-{p["id"]}"{"" if i == 0 else " hidden"}>'
                   f'<p class="plan-pitch"><b>{escape(p["name"])}.</b> {escape(p["pitch"])}</p><div class="tiers">{cards}</div></div>')
    return f'<div class="plans"><div class="plan-tabs" role="tablist" aria-label="Services">{tabs}</div>{panels}</div>'


def builder_html():
    """Plan builder rows: tick a service, pick a level, see the monthly total."""
    rows = ""
    for p in PLANS:
        opts = "".join(
            f'<label class="seg"><input type="radio" name="lvl-{p["id"]}" value="{t}"{" checked" if t == "Growth" else ""}>'
            f'<span>{t}<em>{money(tier["price"])}</em></span></label>'
            for t, tier in zip(TIERS, p["tiers"]))
        rows += (f'<div class="b-row" data-service="{p["id"]}"><label class="b-pick"><input type="checkbox" value="{p["id"]}">'
                 f'<span><b>{escape(p["name"])}</b><small>from {money(p["tiers"][0]["price"])}/mo</small></span></label>'
                 f'<div class="segs" role="radiogroup" aria-label="{escape(p["short"])} level">{opts}</div></div>')
    return f'<div class="builder-rows">{rows}</div>'


def plans_json():
    data = {"tiers": TIERS, "bundle": BUNDLE, "founding": 15,
            "plans": [{"id": p["id"], "name": p["name"], "short": p["short"],
                       "prices": [t["price"] for t in p["tiers"]]} for p in PLANS]}
    return '<script type="application/json" id="plans-data">' + json.dumps(data) + "</script>"
