#!/usr/bin/env python3
"""Builds the static site from one shell template + per-page content.

Run:      python3 build.py            (production build)
Staging:  STAGING=1 python3 build.py  (GitHub Pages URL + noindex)
Test:     python3 build.py --test

Edit page copy in the *_BODY constants below; edit header/footer in SHELL.
"""
import os
import pathlib
import re

STAGING = os.environ.get("STAGING") == "1"
SITE = ("https://maximer111.github.io/nadia-photo"
        if STAGING else "https://nadiaphoto.mensreactivation.com")
ROOT = pathlib.Path(__file__).parent

NAV = [
    ("/sessions.html", "Sessions"),
    ("/presets.html", "Presets"),
    ("/workshop.html", "1:1 Workshop"),
    ("/schedule.html", "Schedule"),
]

BRAND = "Nadiia Loban Photography"
PHONE = "+380&nbsp;67&nbsp;690&nbsp;32&nbsp;62"
PHONE_HREF = "+380676903262"
INSTAGRAM = "https://www.instagram.com/nadi_loban/"

SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{site}{url}">
<meta name="robots" content="index, follow, max-image-preview:large">

<meta property="og:type" content="website">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="Nadiia Loban Photography">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{site}{url}">
<meta property="og:image" content="{site}/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Jost:wght@300;400&display=swap" rel="stylesheet">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%231A1917'/%3E%3Ctext x='16' y='23' font-family='Georgia,serif' font-size='20' fill='%23F7F5F1' text-anchor='middle'%3EN%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="/css/style.css">
{schema}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="site-head">
  <a class="brand" href="/">Nadiia Loban<small>Photography &middot; Budapest</small></a>
  <button class="burger" type="button" aria-expanded="false" aria-controls="nav" aria-label="Menu">
    <span></span><span></span>
  </button>
  <nav class="nav" id="nav" aria-label="Main navigation">
    <ul>{nav}</ul>
  </nav>
</header>

<main id="main">
{body}
</main>

<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <p class="label">Nadiia Loban Photography</p>
        <p class="lede" style="font-size:var(--step-1);max-width:24ch">Individual. Couple.<br>Family. Event.</p>
      </div>
      <div>
        <p class="label">Pages</p>
        <ul>{footnav}</ul>
      </div>
      <div>
        <p class="label">Get in touch</p>
        <ul>
          <li><a href="tel:{phone_href}">{phone}</a></li>
          <li><a href="{ig}" rel="me noopener" target="_blank">Instagram: @nadi_loban</a></li>
          <li>Budapest, Hungary</li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>&copy; 2026 Nadiia Loban Photography. All photographs are protected by copyright.</span>
      <span><a href="/terms.html">Terms</a> &nbsp;&middot;&nbsp; <a href="/policy.html">Privacy</a></span>
    </div>
  </div>
</footer>

<script src="/js/main.js" defer></script>
</body>
</html>
"""


def ld(obj):
    return '<script type="application/ld+json">\n%s\n</script>' % obj


# --------------------------------------------------------------------------
# Page content
# --------------------------------------------------------------------------

# NOTE: the phrases in the intro, the services line and the tagline are
# Nadiia's own words, kept verbatim. Do not reword them.
HOME_BODY = """
  <section class="intro">
    <div class="wrap narrow">
      <h1 class="display intro__title">Photography in Budapest</h1>
      <p class="intro__line">We will never be so young again!<br>Save the moment!</p>
    </div>
  </section>

  <figure class="portrait">
    <img src="img/nadia-hero-1400.jpg"
         srcset="img/nadia-hero-800.jpg 800w, img/nadia-hero-1400.jpg 1400w"
         sizes="(max-width: 760px) 92vw, 720px"
         width="1400" height="2100" fetchpriority="high"
         alt="Black and white portrait: a woman in a plaid shirt in backlit evening sun, hair caught by the wind">
  </figure>

  <section class="contacts">
    <div class="wrap narrow">
      <p class="contacts__name display rv">Nadiia Loban Photography</p>
      <ul class="contacts__lines rv">
        <li><span class="contacts__key">Phone</span>
            <a href="tel:__PHONE_HREF__">__PHONE__</a></li>
        <li><span class="contacts__key">Instagram</span>
            <a href="__CONTACT__" rel="me noopener" target="_blank">@nadi_loban</a></li>
      </ul>
      <p class="label contacts__services rv">Individual. Couple. Family. Event</p>
      <hr class="rule rv" style="margin:3.5rem 0">
      <p class="contacts__tagline display rv">I create cinematic portraits for those who want to remember themselves alive</p>
    </div>
  </section>

  <section class="band" style="padding-top:0" aria-labelledby="portfolio-h">
    <div class="wrap">
      <p class="label rv" style="margin-bottom:3rem">01 / Portfolio</p>
      <h2 id="portfolio-h" style="position:absolute;left:-9999px">Portfolio</h2>
      <div class="duo" style="margin-bottom:var(--band)">
        <figure class="plate plate--r34 ph rv" data-ph="Photo 3:4"></figure>
        <figure class="plate plate--r23 ph rv" data-ph="Photo 2:3"></figure>
      </div>
      <div class="trio" style="margin-bottom:var(--band)">
        <figure class="plate plate--r23 ph rv" data-ph="Photo 2:3"></figure>
        <figure class="plate plate--r43 ph rv" data-ph="Photo 4:3"></figure>
        <figure class="plate plate--r34 ph rv" data-ph="Photo 3:4"></figure>
      </div>
    </div>
    <figure class="plate plate--r169 ph bleed rv" data-ph="Full-width photo"></figure>
  </section>

  <section class="band" style="padding-top:0" aria-labelledby="work-h">
    <div class="wrap">
      <p class="label rv" style="margin-bottom:3rem">02 / What I do</p>
      <h2 id="work-h" class="display rv" style="font-size:var(--step-2);max-width:20ch;margin-bottom:4rem">
        Photo sessions, teaching and my <em style="font-style:italic">presets</em>
      </h2>
      <div class="offers">
        <a class="offer rv" href="sessions.html">
          <div class="offer__name"><span>Shooting</span>Photo sessions</div>
          <p class="offer__desc">Individual. Couple. Family. Event. In Budapest and travelling across Europe.</p>
          <div class="offer__price">from 000&nbsp;&euro;</div>
        </a>
        <a class="offer rv" href="presets.html">
          <div class="offer__name"><span>Editing</span>My presets</div>
          <p class="offer__desc">The Lightroom Classic packs I use on my own shoots. Colour and black and white.</p>
          <div class="offer__price">from 00&nbsp;&euro;</div>
        </a>
        <a class="offer rv" href="workshop.html">
          <div class="offer__name"><span>Teaching</span>1:1 Workshop</div>
          <p class="offer__desc">A full day together: theory, shooting a real couple, selection and editing.</p>
          <div class="offer__price">from 0&nbsp;000&nbsp;&euro;</div>
        </a>
        <a class="offer rv" href="schedule.html">
          <div class="offer__name"><span>Groups</span>Workshop schedule</div>
          <p class="offer__desc">Two-day group workshops in European cities. Dates, languages and places.</p>
          <div class="offer__price">2026</div>
        </a>
      </div>
    </div>
  </section>

  <section class="band cta">
    <div class="wrap">
      <h2 class="display rv">Save the moment</h2>
      <p class="rv">Message me on Instagram or call, and I will tell you which dates are open.</p>
      <a class="btn rv" href="__CONTACT__" rel="noopener" target="_blank"><span>Message me on Instagram</span></a>
    </div>
  </section>
"""

SESSIONS_BODY = """
  <section class="page-head">
    <div class="wrap">
      <span class="label rv">Shooting</span>
      <h1 class="display rv">Photo sessions<em> in Budapest</em></h1>
      <p class="lede rv">Two hours, coffee, conversation, and a camera you will forget about after ten minutes.</p>
    </div>
  </section>

  <figure class="plate plate--r169 ph bleed rv" data-ph="Full-width photo"></figure>

  <section class="band">
    <div class="wrap split">
      <div class="split__media">
        <figure class="plate plate--r34 ph rv" data-ph="Photo 3:4"></figure>
      </div>
      <div class="split__body prose rv">
        <h2>How a session works</h2>
        <p>We do not start with the camera. We start with coffee. Fifteen minutes
          of talking does more for the pictures than an hour of posing. The moment
          you stop watching the lens is the moment the work really begins.</p>
        <p>I will not put you into poses. I give you simple things to do, and I
          photograph what happens in between them: the pauses, the glances,
          the movement.</p>

        <h2>What is included</h2>
        <ul>
          <li>About two hours of shooting</li>
          <li>Guidance on what to wear and where to meet, sent in advance</li>
          <li>150+ edited photographs</li>
          <li>Delivered within NUMBER weeks after the session</li>
        </ul>
        <p style="color:var(--ink-faint);font-size:var(--step--1);letter-spacing:.06em">
          I do not retouch skin. That is a deliberate choice, not a shortcut.</p>
      </div>
    </div>
  </section>

  <section class="band" style="padding-top:0">
    <div class="wrap">
      <div class="trio">
        <figure class="plate plate--r23 ph rv" data-ph="Photo 2:3"></figure>
        <figure class="plate plate--r43 ph rv" data-ph="Photo 4:3"></figure>
        <figure class="plate plate--r34 ph rv" data-ph="Photo 3:4"></figure>
      </div>
    </div>
  </section>

  <section class="band" style="background:var(--paper-deep)">
    <div class="wrap">
      <p class="label rv" style="margin-bottom:3rem">Pricing</p>
      <div class="offers">
        <div class="offer rv">
          <div class="offer__name"><span>Budapest</span>Session in the city</div>
          <p class="offer__desc">Individual, couple or family. We choose the location together: the Danube, Buda, the courtyards of Pest, the baths.</p>
          <div class="offer__price">000&nbsp;&euro;</div>
        </div>
        <div class="offer rv">
          <div class="offer__name"><span>Europe</span>Travel session</div>
          <p class="offer__desc">Vienna, Prague, Paris, Lisbon and beyond. The fee and travel costs are agreed per destination.</p>
          <div class="offer__price">on request</div>
        </div>
      </div>
      <p style="margin-top:2rem;color:var(--ink-faint);font-size:var(--step--1);letter-spacing:.06em">
        Prices exclude VAT. The date is held with a deposit.</p>
    </div>
  </section>

  <section class="band cta">
    <div class="wrap">
      <h2 class="display rv">Ask about open dates</h2>
      <p class="rv">Tell me when you are in Budapest and I will let you know whether the date is free.</p>
      <a class="btn rv" href="__CONTACT__" rel="noopener" target="_blank"><span>Check a date</span></a>
    </div>
  </section>
"""

PRESETS_BODY = """
  <section class="page-head">
    <div class="wrap">
      <span class="label rv">Editing</span>
      <h1 class="display rv">My <em>presets</em></h1>
      <p class="lede rv">The same packs I use on my own shoots. For Adobe Lightroom Classic.</p>
    </div>
  </section>

  <section class="band" style="padding-top:0">
    <div class="wrap split split--flip">
      <div class="split__media">
        <figure class="plate plate--r43 ph rv" data-ph="Before / after"></figure>
      </div>
      <div class="split__body prose rv">
        <h2>Why you might want them</h2>
        <p>I love shooting, but editing is not a chore to me. It is the second
          half of the picture. A preset will not make the light for you, but it
          gives you a starting point and saves the hours that otherwise go into
          matching colour by hand.</p>
        <p>All packs work with Adobe Lightroom Classic. The file is sent to your
          email straight after payment.</p>
      </div>
    </div>
  </section>

  <section class="band" style="padding-top:0">
    <div class="wrap">
      <p class="label rv" style="margin-bottom:3rem">The packs</p>
      <div class="offers">
        <div class="offer rv">
          <div class="offer__name"><span>New</span>Pack name, 00 colour presets</div>
          <p class="offer__desc">Short description: which light it suits, which film base it leans on, which shoots it fits.</p>
          <div class="offer__price">00&nbsp;&euro;</div>
        </div>
        <div class="offer rv">
          <div class="offer__name"><span>Classic</span>Pack name, the first pack</div>
          <p class="offer__desc">Short description: how many colour and how many black and white, and how it differs from the new one.</p>
          <div class="offer__price">00&nbsp;&euro;</div>
        </div>
        <div class="offer rv">
          <div class="offer__name"><span>Black and white</span>Pack name, b&amp;w presets</div>
          <p class="offer__desc">Short description: contrast, grain, and the kind of frames it was built for.</p>
          <div class="offer__price">00&nbsp;&euro;</div>
        </div>
        <div class="offer rv">
          <div class="offer__name"><span>Everything</span>Full pack</div>
          <p class="offer__desc">Every pack in one file, including future updates. Cheaper than buying them separately.</p>
          <div class="offer__price">000&nbsp;&euro;</div>
        </div>
        <div class="offer rv">
          <div class="offer__name"><span>Try first</span>Test pack</div>
          <p class="offer__desc">One colour and one black and white preset, for anyone who wants to try the style first.</p>
          <div class="offer__price">00&nbsp;&euro;</div>
        </div>
      </div>
      <p style="margin-top:2.5rem;color:var(--ink-faint);font-size:var(--step--1);letter-spacing:.06em">
        Payment and file delivery are handled separately (Gumroad / Lemon Squeezy).
        Digital goods are non-refundable once downloaded.</p>
    </div>
  </section>

  <section class="band cta">
    <div class="wrap">
      <h2 class="display rv">Not sure the style is yours?</h2>
      <p class="rv">Take the two-preset test pack. If it fits, I will credit the price towards the full pack.</p>
      <a class="btn rv" href="__CONTACT__" rel="noopener" target="_blank"><span>Message me</span></a>
    </div>
  </section>
"""

WORKSHOP_BODY = """
  <section class="page-head">
    <div class="wrap">
      <span class="label rv">Teaching</span>
      <h1 class="display rv">The <em>1:1</em> workshop</h1>
      <p class="lede rv">A full day, just the two of us. Not to show you how I shoot, but to explain why I shoot that way.</p>
    </div>
  </section>

  <figure class="plate plate--r169 ph bleed rv" data-ph="Full-width photo"></figure>

  <section class="band">
    <div class="wrap prose rv">
      <h2>How the day is built</h2>
      <p>We start with theory: the principles I lean on when I work with a couple,
        when I pick a location, when I read the light and the movement, and when
        I build a story out of separate frames.</p>
      <p>Then we shoot. We photograph a couple together and you watch the work
        happen: how I talk to people, how I guide instead of posing, how I choose
        a lens and a point of view, and how I make decisions on the spot.</p>
      <p>Afterwards we sit down with the material. I show you how I select and
        edit, and I connect the final frames back to the principles we started
        the morning with.</p>

      <h2>What is included</h2>
      <ul>
        <li>The theory block and my core principles</li>
        <li>A practical shoot with a couple</li>
        <li>Commentary and discussion throughout the shoot</li>
        <li>Selection and editing</li>
        <li>A final review of the results</li>
        <li>Your questions, all day</li>
      </ul>
      <p>Not included and paid separately: lunch, transport if needed, and the
        models' fee. You are also welcome to find and arrange the couple yourself.</p>

      <h2>An extra day of practice</h2>
      <p>If you want more time behind the camera, you can add a second practical
        session on the following day, in a different location and focused on
        your own questions.</p>
    </div>
  </section>

  <section class="band" style="background:var(--paper-deep);padding-top:0">
    <div class="wrap" style="padding-top:var(--band)">
      <div class="offers">
        <div class="offer rv">
          <div class="offer__name"><span>Main</span>Full day, 1:1</div>
          <p class="offer__desc">About NUMBER hours: theory, shooting, selection, editing, review.</p>
          <div class="offer__price">0&nbsp;000&nbsp;&euro;</div>
        </div>
        <div class="offer rv">
          <div class="offer__name"><span>Optional</span>Extra practice day</div>
          <p class="offer__desc">One more shoot the next day, a different location, your own questions.</p>
          <div class="offer__price">000&nbsp;&euro;</div>
        </div>
      </div>
      <p style="margin-top:2rem;color:var(--ink-faint);font-size:var(--step--1);letter-spacing:.06em">
        Prices exclude VAT.</p>
    </div>
  </section>

  <section class="band cta">
    <div class="wrap">
      <h2 class="display rv">Book your day</h2>
      <p class="rv">Tell me when suits you and what feels hardest in your photography right now.</p>
      <a class="btn rv" href="__CONTACT__" rel="noopener" target="_blank"><span>Message me</span></a>
    </div>
  </section>
"""

WORKSHOPS_2026 = [
    # (dates, weekdays, language, places, city, country, status)
    ("00-00 March", "MON-TUE", "English", "12", "Budapest", "Hungary", "open"),
    ("00-00 April", "SAT-SUN", "English", "12", "Vienna", "Austria", "open"),
    ("00-00 May", "THU-FRI", "English", "9", "Paris", "France", "open"),
    ("00-00 September", "TUE-WED", "English", "12", "Budapest", "Hungary", "full"),
]


def schedule_rows():
    out = []
    for when, days, lang, seats, city, country, status in WORKSHOPS_2026:
        full = status == "full"
        out.append(f"""        <div class="date-row rv{' is-full' if full else ''}">
          <div class="date-row__when">{when}<span>{days}</span></div>
          <div class="date-row__where">{city}, {country}</div>
          <div class="date-row__meta">Language: {lang} &nbsp;&middot;&nbsp; {seats} places</div>
          <a class="btn btn--ghost" href="__CONTACT__" rel="noopener" target="_blank"><span>{'Sold out' if full else 'Join'}</span></a>
        </div>""")
    return "\n".join(out)


SCHEDULE_BODY = """
  <section class="page-head">
    <div class="wrap">
      <span class="label rv">Groups</span>
      <h1 class="display rv">Workshops in <em>2026</em></h1>
      <p class="lede rv">Two-day group workshops in the cities where I want to shoot myself.</p>
    </div>
  </section>

  <section class="band" style="padding-top:0">
    <div class="wrap narrow prose rv">
      <p>Learning has always been what moved me forward. The courses I took did
        not only speed things up, they helped me work out where I actually
        wanted to go.</p>
      <p>Most photographers get stuck on technique. While the camera is still a
        problem to solve, there is no attention left for the person in front of
        it. Once the settings become automatic, room opens up for what matters:
        the light, the composition, and the connection you are there to catch.</p>
    </div>
  </section>

  <section class="band" style="padding-top:0">
    <div class="wrap">
      <p class="label rv" style="margin-bottom:2.5rem">Dates</p>
      <div class="dates">
__ROWS__
      </div>
      <p style="margin-top:2rem;color:var(--ink-faint);font-size:var(--step--1);letter-spacing:.06em">
        A place is held with a deposit. Cancel 30 days ahead and the deposit is returned.</p>
    </div>
  </section>

  <section class="band cta">
    <div class="wrap">
      <h2 class="display rv">Your city is not on the list?</h2>
      <p class="rv">Write to me. If a group comes together, I will come. That is how half of these dates happened.</p>
      <a class="btn rv" href="__CONTACT__" rel="noopener" target="_blank"><span>Suggest a city</span></a>
    </div>
  </section>
"""

LEGAL_TERMS = """
  <section class="page-head">
    <div class="wrap">
      <span class="label">Legal</span>
      <h1 class="display">Terms</h1>
    </div>
  </section>
  <section class="band" style="padding-top:0">
    <div class="wrap prose">
      <p><strong>Draft.</strong> This page must be filled in with real terms before
        anything goes on sale. Below is the minimum required to sell digital goods
        and services in the EU.</p>
      <h2>Who the seller is</h2>
      <p>Legal name, registration number, address, contact email.</p>
      <h2>What is sold</h2>
      <p>Photo sessions, workshops, digital presets. Prices, currency, whether VAT is included.</p>
      <h2>Payment and delivery</h2>
      <p>Payment methods. Digital files are sent by email immediately after payment.</p>
      <h2>Refunds</h2>
      <p>How deposits for sessions and workshops are refunded. For digital goods the
        right of withdrawal is lost once the file has been downloaded, which the
        buyer confirms at checkout.</p>
      <h2>Copyright</h2>
      <p>Rights to the photographs and the presets. What the buyer may and may not do.</p>
    </div>
  </section>
"""

LEGAL_POLICY = """
  <section class="page-head">
    <div class="wrap">
      <span class="label">Legal</span>
      <h1 class="display">Privacy policy</h1>
    </div>
  </section>
  <section class="band" style="padding-top:0">
    <div class="wrap prose">
      <p><strong>Draft.</strong> This page must be filled in before launch. Below is
        the GDPR minimum.</p>
      <h2>Who processes your data</h2>
      <p>Name of the data controller and a contact email.</p>
      <h2>What is collected</h2>
      <p>Name and email when you get in touch, payment data held by the payment
        provider, and website analytics.</p>
      <h2>Why</h2>
      <p>To answer your enquiry, to perform the contract, and for accounting.</p>
      <h2>Who it is shared with</h2>
      <p>Payment provider, email service, hosting, analytics.</p>
      <h2>Your rights</h2>
      <p>Access, correction, erasure, portability, withdrawal of consent, and the
        right to complain to a supervisory authority.</p>
      <h2>Cookies</h2>
      <p>Which cookies are used and how to opt out.</p>
    </div>
  </section>
"""

PAGES = [
    dict(
        file="index.html", url="/",
        title="Nadiia Loban Photography, Photographer in Budapest",
        desc="Individual, couple, family and event photography in Budapest and across "
             "Europe. Cinematic portraits by Nadiia Loban.",
        body=HOME_BODY,
        schema=ld("""{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Person",
      "@id": "%(site)s/#person",
      "name": "Nadiia Loban",
      "jobTitle": "Photographer",
      "url": "%(site)s/",
      "telephone": "+380676903262",
      "sameAs": ["https://www.instagram.com/nadi_loban/"],
      "address": { "@type": "PostalAddress", "addressLocality": "Budapest", "addressCountry": "HU" },
      "knowsAbout": ["Portrait photography", "Couple photography", "Family photography", "Event photography"]
    },
    {
      "@type": "ProfessionalService",
      "@id": "%(site)s/#business",
      "name": "Nadiia Loban Photography",
      "image": "%(site)s/img/og.jpg",
      "url": "%(site)s/",
      "founder": { "@id": "%(site)s/#person" },
      "telephone": "+380676903262",
      "sameAs": ["https://www.instagram.com/nadi_loban/"],
      "areaServed": [
        { "@type": "City", "name": "Budapest" },
        { "@type": "Place", "name": "Europe" }
      ],
      "address": { "@type": "PostalAddress", "addressLocality": "Budapest", "addressCountry": "HU" },
      "priceRange": "€€"
    },
    {
      "@type": "WebSite",
      "@id": "%(site)s/#website",
      "url": "%(site)s/",
      "name": "Nadiia Loban Photography",
      "inLanguage": "en",
      "publisher": { "@id": "%(site)s/#person" }
    }
  ]
}""" % {"site": SITE}),
    ),
    dict(
        file="sessions.html", url="/sessions.html",
        title="Photo Sessions in Budapest | Nadiia Loban Photography",
        desc="Couple, family and individual photo sessions in Budapest and across Europe. "
             "Two hours, natural light, 150+ edited photographs.",
        body=SESSIONS_BODY,
        schema=ld("""{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Photo session in Budapest",
  "serviceType": "Portrait, couple and family photography",
  "provider": { "@type": "Person", "@id": "%(site)s/#person", "name": "Nadiia Loban" },
  "areaServed": [
    { "@type": "City", "name": "Budapest" },
    { "@type": "Place", "name": "Europe" }
  ],
  "url": "%(site)s/sessions.html"
}""" % {"site": SITE}),
    ),
    dict(
        file="presets.html", url="/presets.html",
        title="Lightroom Presets | Nadiia Loban Photography",
        desc="Adobe Lightroom Classic preset packs used on my own shoots. Colour and "
             "black and white sets, plus a two-preset test pack.",
        body=PRESETS_BODY,
        schema=ld("""{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Lightroom presets",
  "itemListElement": []
}"""),
    ),
    dict(
        file="workshop.html", url="/workshop.html",
        title="1:1 Photography Workshop | Nadiia Loban",
        desc="A full day of one-to-one photography teaching: theory, a practical shoot "
             "with a couple, selection and editing.",
        body=WORKSHOP_BODY,
        schema=ld("""{
  "@context": "https://schema.org",
  "@type": "Course",
  "name": "1:1 photography workshop",
  "description": "A full day of one-to-one photography teaching: theory, a practical shoot with a couple, selection and editing.",
  "inLanguage": "en",
  "provider": { "@type": "Person", "@id": "%(site)s/#person", "name": "Nadiia Loban" },
  "url": "%(site)s/workshop.html"
}""" % {"site": SITE}),
    ),
    dict(
        file="schedule.html", url="/schedule.html",
        title="Workshop Schedule 2026 | Nadiia Loban",
        desc="Dates for two-day group photography workshops in 2026: city, language, "
             "number of places and how to join.",
        body=SCHEDULE_BODY.replace("__ROWS__", schedule_rows()),
        schema=ld("""{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Photography workshops, 2026",
  "itemListElement": []
}"""),
    ),
    dict(file="terms.html", url="/terms.html",
         title="Terms | Nadiia Loban Photography",
         desc="Terms of service and sale of digital goods.",
         body=LEGAL_TERMS, schema="", noindex=True),
    dict(file="policy.html", url="/policy.html",
         title="Privacy Policy | Nadiia Loban Photography",
         desc="How personal data of website visitors is processed.",
         body=LEGAL_POLICY, schema="", noindex=True),
]


def nav_html(current):
    return "".join(
        '<li><a href="%s"%s>%s</a></li>' % (
            href, ' aria-current="page"' if href == current else "", text)
        for href, text in NAV)


def foot_html():
    return "".join('<li><a href="%s">%s</a></li>' % (h, t) for h, t in NAV)


def build():
    urls = []
    for page in PAGES:
        html = SHELL.format(
            title=page["title"], desc=page["desc"], site=SITE, url=page["url"],
            schema=page["schema"], nav=nav_html(page["url"]), footnav=foot_html(),
            body=page["body"], ig=INSTAGRAM, phone=PHONE, phone_href=PHONE_HREF,
        )
        html = (html.replace("__CONTACT__", INSTAGRAM)
                    .replace("__PHONE_HREF__", PHONE_HREF)
                    .replace("__PHONE__", PHONE))

        if STAGING:
            html = html.replace('content="index, follow, max-image-preview:large"',
                                'content="noindex, nofollow"')
        if page.get("noindex"):
            html = html.replace('content="index, follow, max-image-preview:large"',
                                'content="noindex, follow"')
        else:
            urls.append(page["url"])

        # Internal links are made relative: pages sit flat in the root, so they
        # work both on the real domain and on a sub-path like
        # user.github.io/nadia-photo/. Absolute /css/... breaks on a sub-path.
        html = re.sub(r'(href|src)="/([^"/][^"]*)"', r'\1="\2"', html)
        html = html.replace('href="/"', 'href="./"')

        (ROOT / page["file"]).write_text(html, encoding="utf-8")
        print("  ✓", page["file"])

    entries = "\n".join(
        f"  <url><loc>{SITE}{u}</loc><changefreq>monthly</changefreq>"
        f"<priority>{'1.0' if u == '/' else '0.8'}</priority></url>" for u in urls)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n</urlset>\n", encoding="utf-8")
    print("  ✓ sitemap.xml")

    (ROOT / "robots.txt").write_text(
        "User-agent: *\nDisallow: /\n" if STAGING else
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print("  ✓ robots.txt")


def selftest():
    """Small guard: template filled in, no leftover tokens, one h1 per page."""
    build()
    for page in PAGES:
        html = (ROOT / page["file"]).read_text(encoding="utf-8")
        f = page["file"]
        assert "{title}" not in html and "{body}" not in html, f
        for token in ("__CONTACT__", "__PHONE__", "__PHONE_HREF__", "__ROWS__"):
            assert token not in html, f"{f}: leftover {token}"
        assert "mailto:" not in html, f"{f}: mailto left behind, there is no email"
        assert html.count("<h1") == 1, f"{f}: expected exactly one h1"
        assert f'<link rel="canonical" href="{SITE}{page["url"]}">' in html, f
        assert 'lang="en"' in html, f"{f}: page must be in English"
        assert not re.search(r"[А-Яа-яЁё]", html), f"{f}: Cyrillic left in an English page"
        assert "—" not in html and "&mdash;" not in html, f"{f}: em dash found"
        # the Instagram handle must be labelled, not bare
        if f == "index.html":
            assert "Instagram</span>" in html, "index: Instagram handle is not labelled"
        if not STAGING:
            assert ("noindex" in html) == bool(page.get("noindex")), f
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert "/terms.html" not in sm and "/policy.html" not in sm, "legal pages leaked into sitemap"
    assert sm.count("<url>") == len([p for p in PAGES if not p.get("noindex")])
    print("selftest: ok")


if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        selftest()
    else:
        build()
        print("Done.")
