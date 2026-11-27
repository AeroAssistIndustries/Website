"""The blog: one entry per post, newest first. Post bodies live in src/blog/<slug>.html.
Reading time is worked out from the post's length, so it stays right when a post is edited."""
import os, re, math

ROOT = os.path.dirname(os.path.abspath(__file__))
AUTHOR = "Karla"

POSTS = [
    {"slug": "blog-holiday-marketing-checklist", "seo_title": "Holiday marketing checklist for local businesses", "cat": "Seasonal", "date": "2026-11-26",
     "title": "The holiday marketing checklist for local businesses",
     "desc": "Holiday hours, gift cards, posts and follow-ups: a short checklist to make the busiest weeks of the year count.",
     "photo": ("1597730763269-c49ab9f9db0f", "A street strung with glowing lanterns in the evening")},
    {"slug": "blog-ai-search-local-business", "seo_title": "How AI search is changing local discovery", "cat": "AI search", "date": "2026-11-24",
     "title": "How AI search is changing the way people find local businesses",
     "desc": "More people now ask an AI assistant where to eat or who to call. What that means for you, and the basics that still win.",
     "photo": ("1488998427799-e3362cec87c3", "A notebook, phone and laptop on a desk")},
    {"slug": "blog-instagram-facebook-tiktok", "seo_title": "Instagram, Facebook or TikTok: which one?", "cat": "Social media", "date": "2026-11-22",
     "title": "Instagram, Facebook or TikTok: where should a local business show up?",
     "desc": "You don't need to be everywhere. How to choose the one or two platforms that fit your customers and your time.",
     "photo": ("1690883793939-f8cca2f28ee0", "A phone screen showing a folder of social media apps")},
    {"slug": "blog-reply-to-negative-review", "seo_title": "How to reply to a negative review, with templates", "cat": "Reputation", "date": "2026-11-20",
     "title": "How to reply to a negative review (with templates you can copy)",
     "desc": "A calm, five-part reply that protects your reputation, plus ready-to-edit templates for the most common situations.",
     "photo": ("1531058240690-006c446962d8", "A shop owner standing behind the counter of her store")},
    {"slug": "blog-what-to-post", "seo_title": "What to post when you have nothing to post", "cat": "Social media", "date": "2026-11-18",
     "title": "What to post when you have nothing to post: 30 ideas",
     "desc": "Thirty post ideas for local businesses, grouped so you can fill a month in one sitting.",
     "photo": ("1544633909-3de7702b9602", "Someone photographing a plate of food with a phone")},
    {"slug": "blog-google-business-profile-features", "seo_title": "8 Google Business Profile features you're missing", "cat": "Google & Maps", "date": "2026-11-16",
     "title": "8 Google Business Profile features most local businesses ignore",
     "desc": "Free settings on your Google profile that help you show up for the right searches and turn views into visits.",
     "photo": ("1761850648640-2ee5870ee883", "A main street lined with small local shops")},
    {"slug": "blog-hello-digital-mondo", "cat": "News", "date": "2026-11-14",
     "title": "Hello from Digital Mondo",
     "desc": "Why I started a one-person marketing agency for local businesses, and what you can expect from this blog.",
     "photo": ("1441015401724-70d16b783f5c", "A laptop and a cup of tea on a wooden table")},
]


def body(p):
    return open(os.path.join(ROOT, "src", "blog", p["slug"] + ".html")).read()


for p in POSTS:
    words = len(re.sub(r"<[^>]+>", " ", body(p)).split())
    p["minutes"] = max(2, math.ceil(words / 230))
    p["words"] = words

CATS = []
for p in POSTS:
    if p["cat"] not in CATS:
        CATS.append(p["cat"])

BY_SLUG = {p["slug"]: p for p in POSTS}


def related(p, n=3):
    """Posts in the same category first, then the newest of the rest."""
    same = [q for q in POSTS if q is not p and q["cat"] == p["cat"]]
    rest = [q for q in POSTS if q is not p and q["cat"] != p["cat"]]
    return (same + rest)[:n]
