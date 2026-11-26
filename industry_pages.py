"""Dedicated pages per industry. The challenges, focus list, photo and content ideas are read from
src/industries.html so the overview and the pages never disagree; the rest lives here."""
import re, html, os

SRC = os.path.join(os.path.dirname(__file__), "src", "industries.html")

EXTRA = {
  "hotels": {"file": "marketing-for-hotels.html", "noun": "hotels and inns",
    "title": "Marketing for Hotels, Inns and Vacation Rentals",
    "h1": "More direct bookings for your hotel or inn.",
    "intro": "Guests compare you on Google, travel sites and Instagram before they book. I help them find you, trust you and book with you directly, so more of each stay stays with you.",
    "desc": "Marketing for independent hotels, inns and vacation rentals: Google hotel profile, book-direct messaging, local guides, social media and replies to every review.",
    "combo": "booked", "planner": "hotel", "guide": "guide-marketing-to-visitors",
    "month": ["Weekly Google profile posts with current offers and events", "Room, view and amenity photos kept fresh everywhere guests look", "A local guide or itinerary post that gives people a reason to stay longer", "Replies to every review on Google, Tripadvisor and booking sites"],
    "faqs": [("Can you help us get fewer bookings through travel sites?", "Travel sites will always bring some guests, but you can win more direct bookings by making your own website easy to book on, giving people a reason to book direct, such as a perk or better terms, and making sure your Google profile links to your own booking page."),
             ("Do you manage reviews on Tripadvisor and booking sites?", "Yes. Google, Facebook and Yelp are on every reputation plan, and Pro adds extra platforms such as Tripadvisor. Replies are written in your voice."),
             ("We are a small inn. Is this overkill?", "Not at all. Many small properties start with one service, often Local SEO or Reputation Management, and add more once they see results.")]},
  "restaurants": {"file": "marketing-for-restaurants.html", "noun": "restaurants and cafés",
    "title": "Restaurant and Café Marketing",
    "h1": "Fill more tables, on more nights.",
    "intro": "People choose where to eat from their phones, often in minutes. I make sure your menu, hours and photos are right everywhere, your feed makes them hungry, and your reviews seal the deal.",
    "desc": "Marketing for restaurants, cafés and bakeries: accurate menus and hours on Google, mouth-watering posts and Reels, specials and more reviews.",
    "combo": "chosen", "planner": "cafe", "guide": "guide-google-reviews",
    "month": ["Twelve or more designed posts and short videos of your food and people", "Specials and events promoted where locals look", "Menu, hours and holiday hours checked on Google, Apple Maps and Yelp", "A steady flow of new reviews from regulars, with every one answered"],
    "faqs": [("Will you come and take photos?", "You can send phone clips using a simple shot list, or book a content day where I spend a half-day on site and capture a month of photos and short videos."),
             ("Can you help fill quiet weekdays?", "Yes. We plan specials, events and posts around your slow times and promote them on Google and social media in the days before."),
             ("Do you handle delivery app listings?", "I make sure your name, hours and photos are consistent everywhere, including delivery apps where you have access. Ads inside those apps aren't included.")]},
  "salons": {"file": "marketing-for-salons.html", "noun": "salons and spas",
    "title": "Marketing for Salons, Spas and Barbers",
    "h1": "Keep your chairs full and your clients coming back.",
    "intro": "Your work is visual and your clients talk. I turn great results into posts people save, keep your Google profile and booking link front and center, and help fill last-minute gaps.",
    "desc": "Marketing for salons, spas and barbers: before-and-after posts, Stories that fill open slots, online booking on Google and more reviews.",
    "combo": "chosen", "planner": "salon", "guide": "guide-social-media-posting",
    "month": ["Before-and-after and style posts (with client permission)", "Stories that fill last-minute openings", "Your booking link on Google, Instagram and your website", "Review requests after appointments, and a reply to every review"],
    "faqs": [("Can you connect our booking system?", "Yes. I link the booking tool you already use, such as Square, Vagaro, Boulevard or Fresha, to your Google profile, Instagram and website so clients can book in a tap."),
             ("Do clients have to appear in photos?", "Only with their permission. Many great salon posts show hands, hair and results without faces."),
             ("What about stylists with their own followings?", "We can feature each stylist so clients get to know the team, and share posts stylists can repost to their own accounts.")]},
  "real-estate": {"file": "marketing-for-real-estate.html", "noun": "real estate agents",
    "title": "Real Estate Agent Marketing",
    "h1": "Be the agent people already know.",
    "intro": "Most buyers and sellers choose an agent they've seen around. I keep you visible between deals with listing content, neighborhood know-how and a strong Google profile full of reviews.",
    "desc": "Marketing for real estate agents: listing Reels and carousels, neighborhood guides, buyer and seller lead pages, and an agent Google profile with reviews.",
    "combo": "seen", "planner": None, "guide": "guide-google-business-profile",
    "month": ["Listing Reels and carousels for every new listing", "Neighborhood spotlights that show you know the area", "A buyer or seller lead page that collects inquiries", "Your agent Google profile kept active, with reviews from past clients"],
    "faqs": [("Do you follow brokerage and fair housing rules?", "Yes. Posts include the brokerage details your state and brokerage require, and listing copy describes the property, never who should live there. Your broker can review anything before it goes out."),
             ("Can you work with my brokerage's brand?", "Yes. I use your brokerage's colors and logo rules alongside your personal brand."),
             ("Do you run ads for listings?", "Ad management is an add-on, quoted after the audit. Housing ads have special rules on Meta and Google, and I set them up accordingly.")]},
  "contractors": {"file": "marketing-for-contractors.html", "noun": "contractors",
    "title": "Marketing for Contractors and Home Services",
    "h1": "Be the first call when something breaks.",
    "intro": "Homeowners search “near me”, check reviews and call the first business that looks trustworthy. I make sure that's you, with a strong Google profile, before-and-after proof and fast follow-up.",
    "desc": "Marketing for contractors and home services: Google profile and near-me searches, before-and-after posts, quote request pages and more reviews.",
    "combo": "found", "planner": "home", "guide": "guide-google-business-profile",
    "month": ["Weekly Google profile posts with recent project photos", "Before-and-after posts that show the quality of your work", "Service-area and service pages that match what people search", "Review requests after every job, and a reply to every review"],
    "faqs": [("We don't have a storefront. Can we still show up on Google Maps?", "Yes. A service-area business can have a Google Business Profile with the address hidden, showing the areas you serve instead."),
             ("We're busy in season and slow off-season. Can plans flex?", "Monthly plans have no long-term contract, so you can change level as the seasons change. Many contractors keep Local SEO running year-round and add social media in the busy season."),
             ("Do you write our quotes or estimates?", "No, but I can build a quote request page and quick replies so new inquiries hear back fast.")]},
  "dental": {"file": "marketing-for-dentists.html", "noun": "dental and wellness practices",
    "title": "Marketing for Dental and Wellness Practices",
    "h1": "Welcome more new patients, and keep the ones you have.",
    "intro": "Patients choose a practice they trust. I show your friendly team and office, answer the questions nervous patients have, and make your reviews and booking easy to find.",
    "desc": "Marketing for dental offices, clinics and wellness practices: friendly team content, helpful posts, review requests and an accurate Google profile.",
    "combo": "found", "planner": "health", "guide": "guide-google-reviews",
    "month": ["Team and office posts that make first visits feel easier", "Helpful myth-busting posts patients save and share", "Services, insurance and new-patient pages that answer common questions", "Review requests after visits, and replies that protect patient privacy"],
    "faqs": [("How do you handle patient privacy?", "Posts never include patient information without written permission, and review replies never confirm that someone is a patient or mention treatment. You approve content before it goes live."),
             ("Can you write about treatments?", "I write clear, friendly explanations based on information you provide or approve. Clinical claims always come from you."),
             ("Do you work with group practices?", "Yes. Extra locations can be added to any plan, quoted after the audit.")]},
  "retail": {"file": "marketing-for-retail.html", "noun": "retail shops",
    "title": "Marketing for Retail Shops and Boutiques",
    "h1": "Give people a reason to come in.",
    "intro": "Online stores are a tap away, so your shop needs to feel worth the trip. I show off new arrivals, promote in-store events and make sure people nearby can find you on Google.",
    "desc": "Marketing for retail shops and boutiques: new arrival posts, in-store events, an email list and a Google profile with products and hours.",
    "combo": "chosen", "planner": "retail", "guide": "guide-social-media-posting",
    "month": ["New arrival and staff pick posts", "In-store events and promotions shared on Google and social media", "Products and current hours on your Google profile", "Reviews from happy shoppers, with every one answered"],
    "faqs": [("Can you help with an online store too?", "Yes. The Website Pro plan includes online ordering set up, using the shop tool you prefer, such as Shopify or Square."),
             ("Do you do product photos?", "A content day covers product and in-store photos. Otherwise I'll give you a simple shot list for phone photos."),
             ("How do we build an email list?", "A sign-up at the register and on your website, with a small reason to join. The email newsletter is an add-on, quoted after the audit.")]},
  "services": {"file": "marketing-for-local-services.html", "noun": "local service businesses",
    "title": "Marketing for Local Service Businesses",
    "h1": "Stand out, answer fast and win the booking.",
    "intro": "When customers can't tell service businesses apart, they pick the one with clear prices, quick replies and good reviews. I help you be that business, without taking up your time.",
    "desc": "Marketing for local service businesses: clear services and pricing online, fast lead follow-up, reviews that build trust and simple monthly reporting.",
    "combo": "found", "planner": None, "guide": "guide-google-business-profile",
    "month": ["Clear service and pricing information on Google and your website", "Weekly Google profile posts", "Review requests after every job, and a reply to every review", "A simple monthly report: calls, website visits and new reviews"],
    "faqs": [("What counts as a local service business?", "Anyone who serves local customers: cleaners, pet groomers, tutors, photographers, movers, auto shops, accountants and many more."),
             ("We get most work from referrals. Why market?", "Even referred customers look you up first. A complete Google profile, good reviews and a clear website turn those referrals into bookings."),
             ("How quickly should we reply to new leads?", "As fast as you can. People often contact several businesses at once, and the first useful reply often wins. Lead follow-up is available as an add-on.")]},
}


def _text(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def load():
    s = open(SRC).read()
    out = []
    for m in re.finditer(r'<article id="([a-z-]+)" class="reveal">(.*?)</article>', s, re.S):
        aid, body = m.group(1), m.group(2)
        if aid not in EXTRA:
            continue
        photo = re.search(r"\{\{img:([^:]+):", body).group(1)
        name = _text(re.search(r"<h2>(.*?)</h2>", body).group(1))
        tag = _text(re.search(r"</h2><span>(.*?)</span>", body).group(1))
        lists = re.findall(r'<ul class="(x|ticks)">(.*?)</ul>', body, re.S)
        items = {k: [_text(li) for li in re.findall(r"<li>(.*?)</li>", v, re.S)] for k, v in lists}
        ideas = [_text(c) for c in re.findall(r'<span class="chip">(.*?)</span>', body)]
        ex = re.search(r'<a class="more" href="([^"]+)">(.*?)</a>', body)
        d = dict(EXTRA[aid], id=aid, photo=photo, name=name, tag=tag, challenges=items.get("x", []),
                 focus=items.get("ticks", []), ideas=ideas, example=(ex.group(1), _text(ex.group(2))) if ex else None)
        out.append(d)
    return out


PAGES = load()
BY_FILE = {p["file"]: p for p in PAGES}
