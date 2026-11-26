"""Digital Mondo service plans: one source for the pricing tabs, the plan builder and the JSON the page script reads."""
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

BUNDLE = {"2": 10, "3": 15, "4": 20}  # % off with 2, 3 or all 4 services
FOUNDING = 15
YEAR_MONTHS = 10  # pay yearly: 12 months for the price of 10

# The All-in-One Starter: all four services in one lighter plan, cheaper than any combo.
STARTER = {"price": 595, "summary": {
    "social": "1 platform, 4 posts a month",
    "seo": "Google profile setup + 2 profile posts a month",
    "reviews": "Replies to 15 reviews a month",
    "web": "Hosting, security and backups"}}

# One-line summary of each level, used on combo cards and the rate card.
SUMMARY = {
    "social": ["1 platform, 8 posts a month", "2 platforms, 12 posts + 2 Reels", "3 platforms, 20 posts + 4 Reels, daily care"],
    "seo": ["Google profile + 10 directories", "On-page SEO, 25 directories, 1 article", "2 articles, links, technical and AI search"],
    "reviews": ["Replies to 30 reviews, alerts", "Unlimited replies + review requests", "3 locations, showcase, sentiment report"],
    "web": ["Hosting, security, 1 hr updates", "New 5-page site, 2 hrs updates", "Up to 12 pages, booking, monthly landing page"],
}

# Named combos. Every combo uses the same level for each service; the plan builder mixes levels.
COMBOS = [
    {"id": "complete", "name": "The Complete Package", "services": ["social", "seo", "reviews", "web"],
     "pitch": "Everything a local business needs to get found, get chosen and get booked, run by one person who sees the whole picture.",
     "perks": ["One combined monthly report", "Quarterly strategy session", "Monthly strategy session"]},
    {"id": "found", "name": "Get Found", "services": ["seo", "reviews"],
     "pitch": "Rank on Google and Maps, and win the click with strong reviews."},
    {"id": "chosen", "name": "Get Chosen", "services": ["social", "reviews"],
     "pitch": "An active feed and a five-star reputation that make people pick you."},
    {"id": "booked", "name": "Get Booked", "services": ["web", "seo"],
     "pitch": "A site that ranks locally and turns visits into calls and bookings."},
    {"id": "seen", "name": "Get Seen", "services": ["social", "web"],
     "pitch": "A feed people follow and a website ready for the traffic it sends."},
    {"id": "growth", "name": "Local Growth", "services": ["social", "seo", "reviews"],
     "pitch": "The big three for steady growth, when your website is already in good shape."},
]


def per_month_yearly(n):
    """Monthly equivalent when paying yearly (2 months free), rounded down."""
    return n * YEAR_MONTHS // 12


def M(n, cls="amt"):
    """A price that switches between monthly and yearly billing."""
    return f'<span class="{cls}" data-m="{n}">{money(n)}</span>'


def billed(n):
    return f'<span class="billed">Billed {money(n * YEAR_MONTHS)} a year · 2 months free</span>'


def money(n):
    return f"${n:,}"


def tier_cards(p):
    cards = ""
    for t, tier in zip(TIERS, p["tiers"]):
        pop = tier.get("popular")
        items = "".join(f"<li>{escape(x)}</li>" for x in tier["items"])
        cards += (f'<article class="tier{" pop" if pop else ""}">'
                  f'<div class="tier-top"><span class="tier-name">{t}</span>{"<span class=badge>Most popular</span>" if pop else ""}</div>'
                  f'<div class="tier-price">{M(tier["price"])}<small>/month</small></div>{billed(tier["price"])}'
                  f'<p class="tier-for">{escape(tier["for"])}</p><ul>{items}</ul>'
                  f'<a class="btn{"" if pop else " ghost"}" href="contact.html" data-pick="{p["id"]}:{t}">Choose {t}</a></article>')
    return cards


def service_plans_html(sid):
    """One service's three plans with the billing switch, for its own page."""
    p = BY_ID[sid]
    return (f'<div class="pk-top">{billing_switch()}</div><div class="tiers">{tier_cards(p)}</div>')


def tabs_html():
    """Service tabs with three tier cards each. Static HTML, so every price is in the page."""
    tabs = "".join(
        f'<button type="button" role="tab" id="tab-{p["id"]}" aria-controls="panel-{p["id"]}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">'
        f'<span class="tab-tag">{p["tag"]}</span>{escape(p["short"])}<small>from {M(p["tiers"][0]["price"])}/mo</small></button>'
        for i, p in enumerate(PLANS))
    panels = ""
    for i, p in enumerate(PLANS):
        cards = tier_cards(p)
        panels += (f'<div class="plan-panel" role="tabpanel" id="panel-{p["id"]}" aria-labelledby="tab-{p["id"]}"{"" if i == 0 else " hidden"}>'
                   f'<p class="plan-pitch"><b>{escape(p["name"])}.</b> {escape(p["pitch"])}</p><div class="tiers">{cards}</div></div>')
    return f'<div class="plans"><div class="plan-tabs" role="tablist" aria-label="Services">{tabs}</div>{panels}</div>'


def builder_html():
    """Plan builder rows: tick a service, pick a level, see the monthly total."""
    rows = ""
    for p in PLANS:
        opts = "".join(
            f'<label class="seg"><input type="radio" name="lvl-{p["id"]}" value="{t}"{" checked" if t == "Growth" else ""}>'
            f'<span>{t}<em>{M(tier["price"])}</em></span></label>'
            for t, tier in zip(TIERS, p["tiers"]))
        rows += (f'<div class="b-row" data-service="{p["id"]}"><label class="b-pick"><input type="checkbox" value="{p["id"]}">'
                 f'<span><b>{escape(p["name"])}</b><small>from {M(p["tiers"][0]["price"])}/mo</small></span></label>'
                 f'<div class="segs" role="radiogroup" aria-label="{escape(p["short"])} level">{opts}</div></div>')
    return f'<div class="builder-rows">{rows}</div>'


def plans_json():
    data = {"tiers": TIERS, "bundle": BUNDLE, "founding": FOUNDING, "yearMonths": YEAR_MONTHS,
            "plans": [{"id": p["id"], "name": p["name"], "short": p["short"],
                       "prices": [t["price"] for t in p["tiers"]]} for p in PLANS]}
    return '<script type="application/json" id="plans-data">' + json.dumps(data) + "</script>"


BY_ID = {p["id"]: p for p in PLANS}


def pct_for(n):
    return BUNDLE.get(str(min(n, 4)), 0) if n >= 2 else 0


def discounted(total, pct):
    """Bundle price: the discount, rounded down to the nearest $5 in the client's favor."""
    return int(total * (100 - pct) / 100 // 5 * 5)


def combo_prices(services):
    """[(full, price)] per tier for a set of services, all at the same level."""
    pct = pct_for(len(services))
    out = []
    for i in range(3):
        full = sum(BY_ID[s]["tiers"][i]["price"] for s in services)
        out.append((full, discounted(full, pct)))
    return out


def _chips(services):
    return "".join(f'<span class="chip-s">{BY_ID[s]["short"]}</span>' for s in services)


def complete_html():
    """The Complete Package: all four services at each level, 20% off."""
    c = COMBOS[0]; pr = combo_prices(c["services"]); pct = pct_for(4)
    st = STARTER["price"]
    lines = "".join(f'<li><b>{BY_ID[s]["short"]}</b> {escape(STARTER["summary"][s])}</li>' for s in c["services"])
    cards = (f'<article class="tier combo starter">'
             f'<div class="tier-top"><span class="tier-name">All-in-One Starter</span><span class="badge">Lowest price</span></div>'
             f'<div class="tier-price">{M(st)}<small>/month</small></div>{billed(st)}'
             f'<p class="tier-for">All four services in one lighter plan. The easiest way to start.</p><ul>{lines}<li class=perk>One combined monthly report</li></ul>'
             f'<a class="btn ghost" href="contact.html" data-label="All-in-One Starter, {money(st)}/month">Choose Starter</a></article>')
    for i, t in enumerate(TIERS):
        full, price = pr[i]; pop = i == 1
        lines = "".join(f'<li><b>{BY_ID[s]["short"]}</b> {escape(SUMMARY[s][i])}</li>' for s in c["services"])
        perks = "".join(f"<li class=perk>{escape(x)}</li>" for x in ([c["perks"][0]] + ([c["perks"][i]] if i else [])))
        label = f'{c["name"]} ({t}), {money(price)}/month'
        cards += (f'<article class="tier combo{" pop" if pop else ""}">'
                  f'<div class="tier-top"><span class="tier-name">Complete {t}</span><span class="badge">Save {money(full - price)}/mo</span></div>'
                  f'<div class="tier-price">{M(price)}<small>/month</small></div>{billed(price)}'
                  f'<p class="tier-for"><s>{M(full, "amt")}</s> à la carte · {pct}% off all four</p><ul>{lines}{perks}</ul>'
                  f'<a class="btn{"" if pop else " ghost"}" href="contact.html" data-label="{escape(label)}">Choose {t}</a></article>')
    return (f'<div class="complete"><div class="complete-head"><span class="tab-tag">ALL 4 SERVICES IN ONE PLAN · FROM {money(st)}/MO</span>'
            f'<h3>All-in-One Packages</h3><p>Social media, local SEO, reputation and your website in one plan, run by one person who sees the whole picture. Start light with the Starter, or take the Complete Package at 20% off à la carte.</p></div><div class="tiers">{cards}</div></div>')


def combos_html():
    """Smaller named combos with one level switch for all cards."""
    seg = "".join(f'<button type="button" data-lvl="{i}" aria-pressed="{"true" if i == 1 else "false"}">{t}</button>' for i, t in enumerate(TIERS))
    cards = ""
    for c in COMBOS[1:]:
        pr = combo_prices(c["services"]); pct = pct_for(len(c["services"]))
        data = " ".join(f'data-p{i}="{p}" data-f{i}="{f}" data-s{i}="{money(f - p)}"' for i, (f, p) in enumerate(pr))
        f, p = pr[1]
        cards += (f'<article class="combo-card" data-name="{escape(c["name"])}" {data}>'
                  f'<div class="cc-top"><h4>{escape(c["name"])}</h4><span class="cc-off">{pct}% off</span></div>'
                  f'<div class="cc-chips">{_chips(c["services"])}</div><p>{escape(c["pitch"])}</p>'
                  f'<div class="cc-price"><b class="amt" data-m="{p}">{money(p)}</b><small>/month</small><s class="amt" data-m="{f}">{money(f)}</s></div>{billed(p)}'
                  f'<span class="cc-save">You save {money(f - p)} a month</span>'
                  f'<a class="btn ghost" href="contact.html" data-label="{escape(c["name"])} (Growth), {money(p)}/month">Choose {escape(c["name"])}</a></article>')
    return (f'<div class="combos-bar"><div><h3>Popular combos</h3><p>Two services save {BUNDLE["2"]}%, three save {BUNDLE["3"]}%. Pick a level to see prices.</p></div>'
            f'<div class="lvl-switch" role="group" aria-label="Combo level">{seg}</div></div><div class="combo-grid">{cards}</div>')


def combo_table_html():
    """Every possible combination at every level."""
    from itertools import combinations
    ids = [p["id"] for p in PLANS]
    rows = ""
    for n in (4, 3, 2):
        for combo in combinations(ids, n):
            pr = combo_prices(list(combo)); pct = pct_for(n)
            named = next((c["name"] for c in COMBOS if sorted(c["services"]) == sorted(combo)), "")
            cells = "".join(f'<td><b class="amt" data-m="{p}">{money(p)}</b><s class="amt" data-m="{f}">{money(f)}</s></td>' for f, p in pr)
            label = " + ".join(BY_ID[s]["short"] for s in combo)
            rows += (f'<tr><th scope="row">{label}{f"<em>{escape(named)}</em>" if named else ""}</th>'
                     f'<td class="off">{pct}%</td>{cells}</tr>')
    head = "".join(f"<th scope=col>{t}</th>" for t in TIERS)
    return (f'<div class="ctable-wrap"><table class="ctable"><caption>Monthly price for every combination, with each service at the same level. '
            f'Crossed-out prices are à la carte.</caption><thead><tr><th scope="col">Services</th><th scope="col">Off</th>{head}</tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


def billing_switch(extra=""):
    return (f'<div class="billing{extra}" role="group" aria-label="Billing">'
            '<button type="button" data-bill="m" aria-pressed="true">Monthly</button>'
            '<button type="button" data-bill="y" aria-pressed="false">Yearly <span class="free">2 months free</span></button></div>')


def packages_html(table=True):
    """À la carte / Combos switch wrapping the service tabs and the combo packages."""
    modes = ('<div class="pk-modes" role="tablist" aria-label="How to buy">'
             '<button type="button" role="tab" id="mode-alc" aria-controls="pk-alc" aria-selected="true">À la carte<small>One service at a time</small></button>'
             f'<button type="button" role="tab" id="mode-combo" aria-controls="pk-combo" aria-selected="false" tabindex="-1">Combos &amp; packages<small>Save up to {BUNDLE["4"]}%</small></button></div>')
    modes = f'<div class="pk-top">{modes}{billing_switch()}</div>'
    extra = ""
    if table:
        extra = f'<details class="every"><summary>See the price of every combination</summary>{combo_table_html()}</details>'
    return (modes + f'<div class="pk-panel" role="tabpanel" id="pk-alc" aria-labelledby="mode-alc">{tabs_html()}</div>'
            f'<div class="pk-panel" role="tabpanel" id="pk-combo" aria-labelledby="mode-combo" hidden>{complete_html()}{combos_html()}{extra}</div>')
