#!/usr/bin/env python3
"""Render the EduPlanet static site.

The site ships as plain HTML — no build step is needed to host it. This script
exists so the shared header, footer and metadata stay identical across all six
pages. Edit the templates or PAGES below, run `python3 tools/build_pages.py`
from the repo root, and the .html files are rewritten in place.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SITE = "EduPlanet Independent School"
TEL_DISPLAY = "041 451 1046"
TEL_HREF = "+27414511046"
WA_DISPLAY = "060 527 3468"
WA_HREF = "27605273468"
ADDRESS = "1 Eveready Road, Struandale, Gqeberha (Port Elizabeth), 6200"
MAPS = ("https://www.google.com/maps/search/?api=1&query="
        "1+Eveready+Road+Struandale+Gqeberha+6200")
APPLY_FORM = ("https://docs.google.com/forms/d/e/"
              "1FAIpQLScvcPgIQBKiv7iKn_6qZiruPIOeQ464HQEsWTzH6ri8QJT2MA/viewform")
APPLY_PDF = ("https://eduplanet.co.za/wp-content/uploads/2023/08/"
             "Eduplanet-Application-Form-2024.pdf")

# Opt in to scroll entrances, then fall back to plain visible content if the
# script that drives them never gets to run (blocked, failed, or throwing).
HEAD_SCRIPT = """<script>
document.documentElement.className += " js";
setTimeout(function () {
  if (!window.__epReady) {
    document.documentElement.className =
      document.documentElement.className.replace(/\\bjs\\b/, "");
  }
}, 4000);
</script>"""

HERO_GATE = """<script>
(function () {
  var v = document.currentScript.previousElementSibling;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var save = !!(navigator.connection && navigator.connection.saveData);
  if (!reduce && !save) return;          // the common path: let it autoplay
  v.removeAttribute('autoplay');
  while (v.firstChild) v.removeChild(v.firstChild);
  v.load();                              // poster attribute carries the hero
})();
</script>"""


def _symbol(path, sid):
    """Turn one of the traced logo files into a reusable <symbol>."""
    t = (ROOT / path).read_text(encoding="utf-8")
    vb = re.search(r'viewBox="([^"]+)"', t).group(1)
    inner = re.search(r"<g transform=.*</g>", t, re.S).group(0)
    return f'<symbol id="{sid}" viewBox="{vb}">{inner}</symbol>'


# Defined once per page; the header and footer reference it with <use>, so the
# geometry is not repeated and currentColor still resolves per instance.
SPRITE = ('<svg class="sprite" aria-hidden="true" focusable="false">'
          + _symbol("assets/img/eduplanet-mark.svg", "ep-mark")
          + _symbol("assets/img/eduplanet-wordmark.svg", "ep-word")
          + '</svg>')

BRAND = """<a class="brand" href="index.html" aria-label="EduPlanet Independent School, home">
        <svg class="brand__mark" aria-hidden="true"><use href="#ep-mark"/></svg>
        <span class="brand__text">
          <svg class="brand__word" aria-hidden="true"><use href="#ep-word"/></svg>
          <span class="brand__sub">Independent School</span>
        </span>
      </a>"""

NAV_ITEMS = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("academics.html", "Academics"),
    ("admissions.html", "Admissions"),
    ("school-life.html", "School Life"),
    ("contact.html", "Contact"),
]

ICON_PHONE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6'
              'A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1'
              'L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>')

ICON_WA = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
           '<path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3.1.8.8-3-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.6.8-.8 1-.3.2-.6.1a6.7 6.7 0 0 1-2-1.2 7.4 7.4 0 0 1-1.4-1.7c-.1-.3 0-.4.1-.6l.4-.5.3-.5v-.5c0-.2-.6-1.5-.8-2s-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.9 11.9 0 0 0 4.6 4 8.6 8.6 0 0 0 1.5.5 3.7 3.7 0 0 0 1.7.1 2.8 2.8 0 0 0 1.8-1.3 2.3 2.3 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></svg>')


def nav(active):
    out = []
    for href, label in NAV_ITEMS:
        cur = ' aria-current="page"' if href == active else ""
        out.append(f'<a href="{href}"{cur}>{label}</a>')
    out.append(f'<a class="btn btn--primary" href="{APPLY_FORM}" target="_blank" '
               f'rel="noopener">Apply Now</a>')
    return "\n          ".join(out)


HEAD = """<!doctype html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#07203C">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{site}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<!-- DEPLOY STEP: replace with the live absolute URLs once the domain is live -->
<meta property="og:url" content="https://eduplanet.co.za/{page}">
<meta property="og:image" content="https://eduplanet.co.za/assets/img/hero-poster.jpg">
{head_script}
<!-- The typeface is self-hosted, so there is no third-party font request to
     block rendering or to fail on a filtered network. -->
<link rel="preload" href="assets/fonts/figtree-variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/styles.css">
</head>
<body>
{sprite}
<a class="skip" href="#main">Skip to content</a>

<header class="header">
  <div class="wrap">
    <div class="header__bar">
      {brand}

      <nav class="nav" id="site-nav" aria-label="Main">
          {nav}
      </nav>

      <div class="header__cta">
        <a class="icon-link" href="tel:{tel_href}" aria-label="Call the school on {tel}">{icon_phone}</a>
        <a class="icon-link" href="https://wa.me/{wa_href}" target="_blank" rel="noopener" aria-label="Message the school on WhatsApp">{icon_wa}</a>
        <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Menu">
          <svg class="icon-open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
          <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M5 5l14 14M19 5L5 19"/></svg>
        </button>
      </div>
    </div>
  </div>
</header>

<main id="main" tabindex="-1">
"""

FOOTER = """</main>

<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        {brand}
        <p>A registered independent school in Struandale, Gqeberha, offering Grade&nbsp;RR to Grade&nbsp;12 since 2016.</p>
      </div>

      <div>
        <h3>Explore</h3>
        <ul>
          <li><a href="about.html">About the school</a></li>
          <li><a href="academics.html">Academics</a></li>
          <li><a href="admissions.html">Admissions</a></li>
          <li><a href="school-life.html">School life</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>

      <div>
        <h3>Apply</h3>
        <ul>
          <li><a href="{form}" target="_blank" rel="noopener">Online application form</a></li>
          <li><a href="{pdf}" target="_blank" rel="noopener">Application form (PDF)</a></li>
          <li><a href="mailto:accounts@eduplanet.co.za">accounts@eduplanet.co.za</a></li>
        </ul>
      </div>

      <div>
        <h3>Contact</h3>
        <ul>
          <li><a href="tel:{tel_href}">{tel}</a> <span aria-hidden="true">·</span> Phone</li>
          <li><a href="https://wa.me/{wa_href}" target="_blank" rel="noopener">{wa}</a> <span aria-hidden="true">·</span> WhatsApp</li>
          <li><a href="mailto:info@eduplanet.co.za">info@eduplanet.co.za</a></li>
          <li><a href="{maps}" target="_blank" rel="noopener">{address}</a></li>
        </ul>
      </div>
    </div>

    <div class="footer__legal">
      <span>&copy; <span id="year">2026</span> {site}. All rights reserved.</span>
      <span>EMIS 200100266 &nbsp;·&nbsp; Exam centre 4342022 &nbsp;·&nbsp; Reg 2016/040404/07</span>
    </div>
  </div>
</footer>

<script src="assets/js/main.js" defer
        onerror="document.documentElement.className=document.documentElement.className.replace(/\\bjs\\b/,'')"></script>
</body>
</html>
"""

CTA = """
<section class="cta">
  <div class="wrap">
    <div class="cta__inner reveal">
      <div>
        <h2>Enrol your child at EduPlanet</h2>
        <p class="lede" style="color:#D6E7F6">Complete the application form on your phone or computer to secure your child's place. If you need a hand, call us or come through to reception.</p>
      </div>
      <div class="btn-row">
        <a class="btn btn--primary" href="{form}" target="_blank" rel="noopener">Apply Now</a>
        <a class="btn btn--on-dark" href="contact.html">Talk to us</a>
      </div>
    </div>
  </div>
</section>
"""


def pagehead(crumb, eyebrow, title, lede):
    return f"""
<section class="pagehead">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a> &nbsp;/&nbsp; {crumb}</p>
    <p class="eyebrow">{eyebrow}</p>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>
"""


# --------------------------------------------------------------------------
# Page bodies
# --------------------------------------------------------------------------

HOME = """
<section class="hero">
  <div class="hero__media">
    <video poster="assets/img/hero-poster.jpg" autoplay muted loop playsinline
           preload="auto" aria-hidden="true" tabindex="-1">
      <source src="assets/video/edu-planet-hero.webm" type="video/webm">
      <source src="assets/video/edu-planet-hero.mp4" type="video/mp4">
    </video>
    {hero_gate}
  </div>
  <div class="hero__scrim" aria-hidden="true"></div>

  <div class="hero__inner">
    <div class="wrap">
      <p class="eyebrow">Independent School &nbsp;·&nbsp; Gqeberha, Eastern Cape</p>
      <h1>An education that builds minds, bodies and spirits.</h1>
      <p class="hero__lede">EduPlanet is a registered independent school offering Grade&nbsp;RR to Grade&nbsp;12 - high-quality teaching, healthy discipline and strong moral values, in Struandale since 2016.</p>
      <div class="btn-row">
        <a class="btn btn--primary" href="{form}" target="_blank" rel="noopener">Apply Now</a>
        <a class="btn btn--on-dark" href="academics.html">Explore academics</a>
      </div>
      <div class="hero__meta">
        <span>Established 2016</span>
        <span>Grades RR&ndash;12</span>
        <span>Registered with the Department of Education</span>
        <span>Exam centre 4342022</span>
      </div>
    </div>
  </div>
  <a class="hero__scroll" href="#discover" aria-label="Scroll to discover EduPlanet">
    <span>Scroll to explore</span>
    <svg viewBox="0 0 16 28" fill="none" aria-hidden="true">
      <path d="M8 1v24m-5-5 5 5 5-5"/>
    </svg>
  </a>
</section>

<section class="band band--paper" id="discover">
  <div class="wrap">
    <div class="section-head section-head--split reveal">
      <div>
        <p class="eyebrow">Who we are</p>
        <h2>A school where children are known, stretched and valued.</h2>
      </div>
      <p class="lede">We focus on high-quality education and healthy discipline while instilling strong moral values based on Christian principles. School life here is more than academics alone.</p>
    </div>

    <div class="stats stagger">
      <div class="stat"><div class="stat__value">2016</div><div class="stat__label">Year established</div></div>
      <div class="stat"><div class="stat__value">RR&ndash;12</div><div class="stat__label">Grades offered</div></div>
      <div class="stat"><div class="stat__value">CAPS</div><div class="stat__label">National curriculum</div></div>
      <div class="stat"><div class="stat__value stat__value--long">200100266</div><div class="stat__label">Department of Education EMIS</div></div>
    </div>
  </div>
</section>

<section class="band band--tint">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Why EduPlanet</p>
      <h2>Three things that shape every school day.</h2>
    </div>

    <div class="grid grid--3 stagger">
      <article class="card">
        <span class="card__num">01</span>
        <h3>Qualified, dedicated staff</h3>
        <p>Our foundation phase and intermediate phase teachers bring the CAPS curriculum to life through fun lessons designed to encourage participation and engage children.</p>
      </article>
      <article class="card">
        <span class="card__num">02</span>
        <h3>A private examination board</h3>
        <p>Our learners write through a private external examination board. It means they need to work harder, aim higher and achieve more &mdash; and their results are externally verified.</p>
      </article>
      <article class="card">
        <span class="card__num">03</span>
        <h3>A holistic approach</h3>
        <p>We value a variety of cultural and sporting activities. School life should be more than simply academics, so we build the minds, bodies and spirits of our learners.</p>
      </article>
    </div>
  </div>
</section>

<section class="band band--paper">
  <div class="wrap">
    <div class="split reveal">
      <div class="split__media">
        <figure class="figure figure--tall">
          <img src="assets/img/colouring-classroom.jpg" alt="Two EduPlanet learners colouring at their desks during a foundation phase lesson." loading="lazy" width="739" height="986">
          <figcaption>Foundation phase &mdash; a colouring lesson</figcaption>
        </figure>
      </div>
      <div>
        <p class="eyebrow">In the classroom</p>
        <h2>Lessons children want to take part in.</h2>
        <p class="lede">Participation is the point. Our teachers design lessons that pull children into the work rather than sitting them in front of it, so the curriculum is something they do, not something they watch.</p>
        <ul class="ticks" style="margin-top:26px">
          <li>CAPS curriculum delivered by qualified phase specialists</li>
          <li>Foundation phase built on play, movement and creative work</li>
          <li>Healthy discipline and clear, consistent expectations</li>
          <li>Externally examined, so standards are independently held</li>
        </ul>
        <p style="margin-top:28px"><a class="arrow-link" href="academics.html">See how each phase works <span aria-hidden="true">&rarr;</span></a></p>
      </div>
    </div>
  </div>
</section>

<section class="band band--navy">
  <div class="wrap">
    <div class="split reveal">
      <div>
        <p class="eyebrow">Our ethos</p>
        <h2>Christian values, lived out daily.</h2>
        <p class="lede">EduPlanet aspires to instil strong moral values based on Christian principles. Through those values we set a positive example in education by promoting self-discipline and excellence in learning.</p>
        <ul class="values" style="margin-top:30px">
          <li>Respect</li><li>Kindness</li><li>Love</li><li>Joy</li><li>Helpfulness</li>
          <li>Patience</li><li>Unity</li><li>Gentleness</li><li>Spirit</li>
        </ul>
        <p style="margin-top:32px"><a class="arrow-link" href="about.html">Read our mission <span aria-hidden="true">&rarr;</span></a></p>
      </div>
      <div class="quote">
        <blockquote>To celebrate success and make children feel valued.</blockquote>
        <cite>From the EduPlanet mission</cite>
      </div>
    </div>
  </div>
</section>


<section class="band band--tint">
  <div class="wrap">
    <div class="section-head section-head--split reveal">
      <div>
        <p class="eyebrow">Phases at a glance</p>
        <h2>One school, from first day to matric.</h2>
      </div>
      <p class="lede">A child can start with us in Grade RR and leave with a matric certificate, without ever changing schools or curricula.</p>
    </div>

    <div class="grid grid--4 stagger">
      <article class="card">
        <span class="card__num">Grades RR&ndash;3</span>
        <h3>Foundation</h3>
        <p>English, Afrikaans, Mathematics and Life Skills, taught through play, movement and creative work.</p>
      </article>
      <article class="card">
        <span class="card__num">Grades 4&ndash;6</span>
        <h3>Intermediate</h3>
        <p>Separate subjects begin, adding Natural Sciences and Technology and Social Sciences to the core.</p>
      </article>
      <article class="card">
        <span class="card__num">Grades 7&ndash;9</span>
        <h3>Senior</h3>
        <p>Nine subjects, the broadest spread of the school career, ending in an informed Grade 9 subject choice.</p>
      </article>
      <article class="card">
        <span class="card__num">Grades 10&ndash;12</span>
        <h3>FET</h3>
        <p>Four compulsory core subjects plus electives from Physical Sciences through to Tourism and CAT.</p>
      </article>
    </div>

    <p style="margin-top:34px"><a class="arrow-link" href="academics.html">See every subject, phase by phase <span aria-hidden="true">&rarr;</span></a></p>
  </div>
</section>

<section class="band band--navy">
  <div class="wrap">
    <div class="split reveal" style="align-items:start">
      <div>
        <p class="eyebrow">The school week</p>
        <h2>When our doors are open.</h2>
        <p class="lede">Reception is staffed through the school day. You are welcome to call ahead, or simply come through and ask for a look around.</p>
        <div class="btn-row" style="margin-top:30px">
          <a class="btn btn--primary" href="tel:{tel_href}">Call {tel}</a>
          <a class="btn btn--on-dark" href="{maps}" target="_blank" rel="noopener">Get directions</a>
        </div>
      </div>
      <ul class="day">
        <li><time>Mon&ndash;Thu</time><div><strong>07:30 &ndash; 16:00</strong><span>Full school day, reception open throughout</span></div></li>
        <li><time>Friday</time><div><strong>07:30 &ndash; 15:00</strong><span>Early close</span></div></li>
        <li><time>Weekends</time><div><strong>Closed</strong><span>Fixtures and events are arranged separately</span></div></li>
      </ul>
    </div>
  </div>
</section>

<section class="band band--paper">
  <div class="wrap">
    <div class="section-head section-head--split reveal">
      <div>
        <p class="eyebrow">School life</p>
        <h2>More than simply academics.</h2>
      </div>
      <p class="lede">Sport, culture and creative work sit alongside the classroom &mdash; because a child is built by all of it.</p>
    </div>

    <div class="gallery stagger">
      <figure class="g-half"><img src="assets/img/netball-match.jpg" alt="An EduPlanet netball team shooting for goal during a match on the school court." loading="lazy" width="739" height="555"></figure>
      <figure class="g-half"><img src="assets/img/hope-mural-group.jpg" alt="A large group of EduPlanet learners gathered in front of the painted HOPE mural." loading="lazy" width="739" height="555"></figure>
      <figure class="g-wide"><img src="assets/img/mascot-visit.jpg" alt="Learners seated at their desks during a classroom visit from the school mascot." loading="lazy" width="768" height="395"></figure>
      <figure><img src="assets/img/creative-play.jpg" alt="Young learners working with modelling clay at a classroom table." loading="lazy" width="739" height="986"></figure>
    </div>

    <p style="margin-top:34px"><a class="arrow-link" href="school-life.html">See more of school life <span aria-hidden="true">&rarr;</span></a></p>
  </div>
</section>
"""

ABOUT = pagehead(
    "About",
    "About the school",
    "Registered, rigorous and rooted in Christian values.",
    "EduPlanet Independent School began in 2016 in Struandale, Gqeberha, and is registered with the Department of Education for Grade RR to Grade 12.",
) + """
<section class="band band--paper">
  <div class="wrap">
    <div class="split reveal">
      <div>
        <p class="eyebrow">Our story</p>
        <h2>A school built in Struandale, for Struandale.</h2>
        <p class="lede">EduPlanet Independent School began in 2016. We are a registered independent school in Gqeberha (Port Elizabeth), South Africa, focused on providing high-quality education and healthy discipline, whilst instilling strong moral values.</p>
        <p style="margin-top:22px">Qualified and dedicated foundation phase and intermediate phase staff bring the CAPS curriculum to life through fun lessons designed to encourage participation and engage children. A private external examination board means that our learners need to work harder, aim higher and achieve more.</p>
      </div>
      <div class="split__media">
        <figure class="figure figure--wide">
          <img src="assets/img/hope-mural-group.jpg" alt="EduPlanet learners gathered in front of the school's painted HOPE mural." loading="lazy" width="739" height="555">
          <figcaption>The HOPE mural at the school</figcaption>
        </figure>
      </div>
    </div>
  </div>
</section>

<section class="band band--navy">
  <div class="wrap">
    <div class="section-head reveal" style="max-width:60ch">
      <p class="eyebrow">Our ethos</p>
      <h2>Strong moral values, based on Christian principles.</h2>
      <p class="lede">Our ethos is not a page in a prospectus. It sets the tone for how children are spoken to, how discipline is handled, and what we celebrate.</p>
    </div>

    <div class="split reveal" style="align-items:start">
      <div>
        <h3 style="color:#fff">Our mission</h3>
        <p>Through Christian values we set a positive example in education by promoting self-discipline and excellence in learning. To empower learners by developing a sense of uniqueness in a stimulating environment that instils responsibility and pride. To celebrate success and make children feel valued.</p>
      </div>
      <div>
        <h3 style="color:#fff">Our core values</h3>
        <ul class="values" style="margin-top:18px">
          <li>Respect</li><li>Kindness</li><li>Love</li><li>Joy</li><li>Helpfulness</li>
          <li>Patience</li><li>Unity</li><li>Gentleness</li><li>Spirit</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="band band--paper">
  <div class="wrap">
    <div class="split reveal">
      <div class="split__media">
        <figure class="figure figure--tall">
          <img src="assets/img/creative-play.jpg" alt="Foundation phase learners shaping modelling clay at a classroom table." loading="lazy" width="739" height="986">
          <figcaption>Creative work in the foundation phase</figcaption>
        </figure>
      </div>
      <div>
        <p class="eyebrow">Our approach</p>
        <h2>Minds, bodies and spirits.</h2>
        <p class="lede">At EduPlanet we value a variety of cultural and sporting activities. School life should be more than simply academics, so we take a holistic approach that builds the whole child.</p>
        <ul class="ticks" style="margin-top:26px">
          <li>High-quality teaching with healthy, consistent discipline</li>
          <li>A stimulating environment that instils responsibility and pride</li>
          <li>Cultural and sporting activities alongside the curriculum</li>
          <li>Success celebrated, so children feel genuinely valued</li>
        </ul>
      </div>
    </div>
  </div>
</section>


<section class="band band--paper">
  <div class="wrap">
    <div class="section-head section-head--split reveal">
      <div>
        <p class="eyebrow">Independent, and registered</p>
        <h2>What that actually means for your child.</h2>
      </div>
      <p class="lede">Independent does not mean unaccountable. It means we answer to an outside standard as well as to you.</p>
    </div>

    <div class="grid grid--3 stagger">
      <article class="card">
        <span class="card__num">01</span>
        <h3>Registered with the DBE</h3>
        <p>We hold EMIS number 200100266 and are registered for Grade RR to Grade 12. Our examination centre number is 4342022.</p>
      </article>
      <article class="card">
        <span class="card__num">02</span>
        <h3>Externally examined</h3>
        <p>A private external examination board sets and marks the papers, so results are independent of the school that taught them.</p>
      </article>
      <article class="card">
        <span class="card__num">03</span>
        <h3>The national curriculum</h3>
        <p>We teach CAPS in full. A learner moving to or from EduPlanet moves between schools on the same curriculum.</p>
      </article>
    </div>
  </div>
</section>

<section class="band band--tint">
  <div class="wrap wrap--narrow">
    <div class="section-head reveal">
      <p class="eyebrow">Registration &amp; compliance</p>
      <h2>Registered with the Department of Education.</h2>
      <p class="lede">EduPlanet is a registered independent school. Our registration details are published here so parents can verify them.</p>
    </div>
    <dl class="rows reveal">
      <div><dt>School type</dt><dd>Registered independent school, Grade RR to Grade 12</dd></div>
      <div><dt>Curriculum</dt><dd>CAPS, with a private external examination board</dd></div>
      <div><dt>DBE EMIS number</dt><dd>200100266</dd></div>
      <div><dt>Examination centre</dt><dd>4342022</dd></div>
      <div><dt>Company registration</dt><dd>2016/040404/07</dd></div>
      <div><dt>Established</dt><dd>2016</dd></div>
    </dl>
  </div>
</section>
"""

ACADEMICS = pagehead(
    "Academics",
    "Academics",
    "The full CAPS curriculum, externally examined.",
    "Grade RR right through to Grade 12, taught by qualified phase specialists and assessed by a private external examination board.",
) + """
<section class="band band--paper">
  <div class="wrap">
    <div class="section-head section-head--split reveal">
      <div>
        <p class="eyebrow">Curriculum</p>
        <h2>A national curriculum, held to an outside standard.</h2>
      </div>
      <p class="lede">We teach CAPS &mdash; the same National Curriculum Statement every South African school follows. What differs at EduPlanet is who sets and marks the papers.</p>
    </div>

    <div class="grid grid--2 stagger">
      <article class="card">
        <h3>Why an external board matters</h3>
        <p>When an independent body sets and marks the examinations, nobody inside the school can quietly soften the standard. Our learners need to work harder, aim higher and achieve more &mdash; and when a result comes back, a parent can trust it, because the school did not award it to itself.</p>
      </article>
      <article class="card">
        <h3>Taught by phase specialists</h3>
        <p>Qualified and dedicated foundation phase and intermediate phase staff bring the curriculum to life through lessons built around participation. Children engage with the work rather than sitting through it, and the habit of taking part carries up into the senior grades.</p>
      </article>
    </div>
  </div>
</section>

<section class="band band--tint">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Subjects by phase</p>
      <h2>What your child studies, year by year.</h2>
      <p class="lede">Four phases carry a learner from the pre-primary classroom to matric. Each one builds directly on the last, so nothing has to be unlearned along the way.</p>
    </div>

    <div class="phase reveal">
      <div>
        <p class="phase__grades">Grades RR&ndash;3</p>
        <h3>Foundation Phase</h3>
        <p class="phase__note">Reading, writing and numeracy laid down properly, through play, movement and creative work. This is where a child decides how they feel about school.</p>
      </div>
      <ul class="subjects">
        <li>English Home Language</li>
        <li>Afrikaans First Additional Language</li>
        <li>Mathematics</li>
        <li>Life Skills</li>
      </ul>
    </div>

    <div class="phase reveal">
      <div>
        <p class="phase__grades">Grades 4&ndash;6</p>
        <h3>Intermediate Phase</h3>
        <p class="phase__note">Separate subjects begin in earnest, and with them a steady rise in independence, note-taking and responsibility for one's own work.</p>
      </div>
      <ul class="subjects subjects--split">
        <li>English Home Language</li>
        <li>Afrikaans First Additional Language</li>
        <li>Mathematics</li>
        <li>Natural Sciences and Technology</li>
        <li>Social Sciences (History and Geography)</li>
        <li>Life Skills</li>
      </ul>
    </div>

    <div class="phase reveal">
      <div>
        <p class="phase__grades">Grades 7&ndash;9</p>
        <h3>Senior Phase</h3>
        <p class="phase__note">The widest spread of subjects a learner will study. It is deliberately broad, so that the Grade 9 subject choice is made from experience rather than guesswork.</p>
      </div>
      <ul class="subjects subjects--split">
        <li>English Home Language</li>
        <li>Afrikaans First Additional Language</li>
        <li>Mathematics</li>
        <li>Natural Sciences</li>
        <li>Social Sciences (History and Geography)</li>
        <li>Technology</li>
        <li>Economic Management Sciences</li>
        <li>Life Orientation</li>
        <li>Creative Arts</li>
      </ul>
    </div>

    <div class="phase reveal">
      <div>
        <p class="phase__grades">Grades 10&ndash;12</p>
        <h3>FET Phase</h3>
        <p class="phase__note">The matric years. Four core subjects are compulsory for every learner; the rest of the timetable is built from the elective list alongside.</p>
      </div>
      <div>
        <div class="subjects__group">
          <p class="subjects__head">Core compulsory subjects</p>
          <ul class="subjects">
            <li>English Home Language</li>
            <li>Afrikaans Additional Language <em>or</em> IsiXhosa Additional Language</li>
            <li>Pure Mathematics <em>or</em> Mathematical Literacy</li>
            <li>Life Orientation</li>
          </ul>
        </div>
        <div class="subjects__group">
          <p class="subjects__head">Elective subjects</p>
          <ul class="subjects subjects--split">
            <li>Physical Sciences</li>
            <li>Life Sciences</li>
            <li>Business Studies</li>
            <li>History</li>
            <li>Tourism</li>
            <li>Computer Applications Technology</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="band band--paper">
  <div class="wrap">
    <div class="split split--reverse reveal">
      <div class="split__media">
        <figure class="figure figure--wide">
          <img src="assets/img/mascot-visit.jpg" alt="An EduPlanet class seated at their desks during a visit from the school mascot." loading="lazy" width="768" height="395">
          <figcaption>Learn &middot; Play &middot; Grow &mdash; in the classroom</figcaption>
        </figure>
      </div>
      <div>
        <p class="eyebrow">How we teach</p>
        <h2>Participation first.</h2>
        <p class="lede">A lesson a child takes part in is a lesson a child remembers. That principle runs from the pre-primary classroom right up to the matric year.</p>
        <ul class="ticks" style="margin-top:26px">
          <li>Lessons designed to be joined in, not watched</li>
          <li>Creative and practical work alongside written work</li>
          <li>Healthy discipline and clear expectations in every class</li>
          <li>Independent external assessment of learner results</li>
          <li>Subject choice in Grade 9 made from real experience</li>
        </ul>
      </div>
    </div>
  </div>
</section>
"""

ADMISSIONS = pagehead(
    "Admissions",
    "Admissions",
    "Enrol your child at EduPlanet.",
    "Complete the application form on your phone or computer to secure your child's place. If you do not have access to a computer or printer, come to reception and we will help you.",
) + """
<section class="band band--paper">
  <div class="wrap">
    <div class="section-head section-head--split reveal">
      <div>
        <p class="eyebrow">How to apply</p>
        <h2>Four steps, start to finish.</h2>
      </div>
      <p class="lede">Applications are handled by our accounts office. Nothing here needs to be done in person unless you would prefer it that way.</p>
    </div>

    <div class="steps reveal">
      <div class="step">
        <div class="step__n"></div>
        <div>
          <h3>Complete the application form</h3>
          <p>Fill in the online form on your phone or computer, or print the PDF application document and complete it in full.</p>
        </div>
      </div>
      <div class="step">
        <div class="step__n"></div>
        <div>
          <h3>Gather the supporting documents</h3>
          <p>Have the documents listed below ready before you submit &mdash; an incomplete application cannot be processed.</p>
        </div>
      </div>
      <div class="step">
        <div class="step__n"></div>
        <div>
          <h3>Return it to the accounts office</h3>
          <p>Send the completed application and documents to <a href="mailto:accounts@eduplanet.co.za">accounts@eduplanet.co.za</a>, or hand them in at reception.</p>
        </div>
      </div>
      <div class="step">
        <div class="step__n"></div>
        <div>
          <h3>We come back to you</h3>
          <p>Our office confirms receipt and takes you through the next steps. If you need help at any point, call {tel} or WhatsApp {wa}.</p>
        </div>
      </div>
    </div>

    <div class="btn-row" style="margin-top:40px">
      <a class="btn btn--primary" href="{form}" target="_blank" rel="noopener">Apply online now</a>
      <a class="btn btn--ghost" href="{pdf}" target="_blank" rel="noopener">Download the PDF form</a>
    </div>
  </div>
</section>

<section class="band band--navy">
  <div class="wrap">
    <div class="split reveal" style="align-items:start">
      <div>
        <p class="eyebrow">What you will need</p>
        <h2>Documents to have ready.</h2>
        <p class="lede">Please have all of the following on hand when you apply.</p>
      </div>
      <ul class="ticks" style="gap:14px">
        <li>Cellphone number</li>
        <li>ID document of the child</li>
        <li>ID documents of the parents</li>
        <li>Proof of address</li>
        <li>The previous report of the child</li>
        <li>Transfer documents</li>
        <li>Bank statements</li>
      </ul>
    </div>
  </div>
</section>

<section class="band band--tint">
  <div class="wrap wrap--narrow">
    <div class="section-head reveal" style="margin-bottom:0">
      <p class="eyebrow">No computer or printer?</p>
      <h2>Come to reception and we will assist you.</h2>
      <p class="lede">Anyone who does not have access to a computer or printer can come to our reception area at school, where you will be assisted in completing and submitting the application. We are open {hours_short}.</p>
      <div class="btn-row" style="margin-top:30px">
        <a class="btn btn--primary" href="tel:{tel_href}">Call {tel}</a>
        <a class="btn btn--ghost" href="https://wa.me/{wa_href}" target="_blank" rel="noopener">WhatsApp {wa}</a>
      </div>
    </div>
  </div>
</section>

<section class="band band--paper">
  <div class="wrap wrap--narrow">
    <div class="section-head reveal">
      <p class="eyebrow">Questions parents ask</p>
      <h2>Before you apply.</h2>
    </div>

    <div class="faq reveal">
      <div class="faq__item">
        <button class="faq__q" type="button" aria-expanded="false" aria-controls="faq1">Which grades does EduPlanet take?</button>
        <div class="faq__a" id="faq1" hidden>
          <p>Grade RR through to Grade 12. We are registered with the Department of Education for the full range, so a child can join in the pre-primary year and stay with us until matric.</p>
        </div>
      </div>
      <div class="faq__item">
        <button class="faq__q" type="button" aria-expanded="false" aria-controls="faq2">Is the school properly registered?</button>
        <div class="faq__a" id="faq2" hidden>
          <p>Yes. EduPlanet is a registered independent school. Our Department of Education EMIS number is 200100266 and our examination centre number is 4342022. The company registration is 2016/040404/07. You are welcome to verify any of these.</p>
        </div>
      </div>
      <div class="faq__item">
        <button class="faq__q" type="button" aria-expanded="false" aria-controls="faq3">Which curriculum do you follow?</button>
        <div class="faq__a" id="faq3" hidden>
          <p>CAPS, the same national curriculum used across South African schools. Our learners are assessed through a private external examination board, which means the standard is set and marked independently of the school.</p>
        </div>
      </div>
      <div class="faq__item">
        <button class="faq__q" type="button" aria-expanded="false" aria-controls="faq4">Which languages are offered?</button>
        <div class="faq__a" id="faq4" hidden>
          <p>English Home Language throughout, with Afrikaans First Additional Language from the Foundation Phase. In Grades 10 to 12 a learner takes either Afrikaans Additional Language or IsiXhosa Additional Language.</p>
        </div>
      </div>
      <div class="faq__item">
        <button class="faq__q" type="button" aria-expanded="false" aria-controls="faq5">When can I visit the school?</button>
        <div class="faq__a" id="faq5" hidden>
          <p>Reception is open Monday to Thursday from 07:30 to 16:00, and Friday from 07:30 to 15:00. We are at 1 Eveready Road, Struandale. Call 041 451 1046 or WhatsApp 060 527 3468 if you would like us to expect you.</p>
        </div>
      </div>
      <div class="faq__item">
        <button class="faq__q" type="button" aria-expanded="false" aria-controls="faq6">What if I cannot print the form?</button>
        <div class="faq__a" id="faq6" hidden>
          <p>Use the online application form on your phone, or come to our reception area at school and we will assist you in completing and submitting the application from start to finish.</p>
        </div>
      </div>
    </div>
  </div>
</section>
"""

SCHOOL_LIFE = pagehead(
    "School Life",
    "School life",
    "School life should be more than simply academics.",
    "Sport, culture, creative work and the ordinary good days in between — the parts of school that build bodies and spirits alongside minds.",
) + """
<section class="band band--paper">
  <div class="wrap">
    <div class="split reveal">
      <div class="split__media">
        <figure class="figure figure--wide">
          <img src="assets/img/netball-match.jpg" alt="EduPlanet netball players competing for a goal on the school court, watched by learners along the sideline." loading="lazy" width="739" height="555">
          <figcaption>Netball on the school court</figcaption>
        </figure>
      </div>
      <div>
        <p class="eyebrow">Sport</p>
        <h2>Competitive sport, on our own courts.</h2>
        <p class="lede">We value a variety of sporting activities. Teams train and compete on site, and the rest of the school turns out along the sideline to watch them play.</p>
      </div>
    </div>
  </div>
</section>

<section class="band band--tint">
  <div class="wrap">
    <div class="split split--reverse reveal">
      <div class="split__media">
        <figure class="figure figure--tall">
          <img src="assets/img/creative-play.jpg" alt="Two young learners holding tubs of modelling clay at their classroom table." loading="lazy" width="739" height="986">
          <figcaption>Modelling clay in the foundation phase</figcaption>
        </figure>
      </div>
      <div>
        <p class="eyebrow">Creative &amp; cultural</p>
        <h2>Hands busy, minds working.</h2>
        <p class="lede">Modelling, drawing, colouring and play-based work are how the youngest grades do serious learning. Fine motor control, patience and pride in finished work all start here.</p>
        <ul class="ticks" style="margin-top:26px">
          <li>Creative activities built into the foundation phase timetable</li>
          <li>Cultural activities alongside sport through the year</li>
          <li>Classroom celebrations that make children feel valued</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="band band--paper">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Gallery</p>
      <h2>Around the school.</h2>
    </div>

    <div class="gallery stagger">
      <figure class="g-half"><img src="assets/img/hope-mural-group.jpg" alt="A large group of EduPlanet learners seated and standing in front of the painted HOPE mural." loading="lazy" width="739" height="555"></figure>
      <figure class="g-half"><img src="assets/img/netball-match.jpg" alt="A netball match in progress on the school court." loading="lazy" width="739" height="555"></figure>
      <figure><img src="assets/img/colouring-classroom.jpg" alt="A learner smiling while colouring in a foundation phase lesson." loading="lazy" width="739" height="986"></figure>
      <figure><img src="assets/img/creative-play.jpg" alt="Learners working with modelling clay in class." loading="lazy" width="739" height="986"></figure>
      <figure class="g-half"><img src="assets/img/mascot-visit.jpg" alt="The school mascot visiting a classroom of seated learners." loading="lazy" width="768" height="395"></figure>
    </div>
  </div>
</section>
"""

CONTACT = pagehead(
    "Contact",
    "Contact",
    "Come and see the school.",
    "Call us, send a WhatsApp, or come through to reception at 1 Eveready Road. We are glad to show parents around.",
) + """
<section class="band band--paper">
  <div class="wrap">
    <div class="split reveal" style="align-items:start">
      <div>
        <p class="eyebrow">Get in touch</p>
        <h2>How to reach us.</h2>
        <dl class="rows" style="margin-top:30px">
          <div><dt>Phone</dt><dd><a href="tel:{tel_href}">{tel}</a></dd></div>
          <div><dt>WhatsApp</dt><dd><a href="https://wa.me/{wa_href}" target="_blank" rel="noopener">{wa}</a></dd></div>
          <div><dt>Principal</dt><dd><a href="mailto:principal@eduplanet.co.za">principal@eduplanet.co.za</a></dd></div>
          <div><dt>General enquiries</dt><dd><a href="mailto:info@eduplanet.co.za">info@eduplanet.co.za</a></dd></div>
          <div><dt>Applications &amp; accounts</dt><dd><a href="mailto:accounts@eduplanet.co.za">accounts@eduplanet.co.za</a></dd></div>
          <div><dt>Address</dt><dd><a href="{maps}" target="_blank" rel="noopener">{address}</a></dd></div>
        </dl>
      </div>

      <div>
        <p class="eyebrow">Office hours</p>
        <h2>When we are open.</h2>
        <dl class="rows" style="margin-top:30px">
          <div><dt>Monday</dt><dd>07:30 &ndash; 16:00</dd></div>
          <div><dt>Tuesday</dt><dd>07:30 &ndash; 16:00</dd></div>
          <div><dt>Wednesday</dt><dd>07:30 &ndash; 16:00</dd></div>
          <div><dt>Thursday</dt><dd>07:30 &ndash; 16:00</dd></div>
          <div><dt>Friday</dt><dd>07:30 &ndash; 15:00</dd></div>
          <div><dt>Saturday</dt><dd>Closed</dd></div>
          <div><dt>Sunday</dt><dd>Closed</dd></div>
        </dl>
        <div class="btn-row" style="margin-top:32px">
          <a class="btn btn--primary" href="tel:{tel_href}">Call the school</a>
          <a class="btn btn--ghost" href="{maps}" target="_blank" rel="noopener">Get directions</a>
        </div>
      </div>
    </div>
  </div>
</section>


<section class="band band--tint">
  <div class="wrap">
    <div class="section-head section-head--split reveal">
      <div>
        <p class="eyebrow">Find us</p>
        <h2>1 Eveready Road, Struandale.</h2>
      </div>
      <p class="lede">We are on Eveready Road in Struandale, Gqeberha. Parking is on site, and reception is straight ahead as you come in.</p>
    </div>

    <figure class="map reveal">
      <iframe
        title="Map showing EduPlanet Independent School, 1 Eveready Road, Struandale, Gqeberha"
        src="https://maps.google.com/maps?q=1+Eveready+Road,+Struandale,+Gqeberha,+6200&amp;z=15&amp;output=embed"
        loading="lazy" referrerpolicy="no-referrer-when-downgrade"
        allowfullscreen></iframe>
    </figure>

    <div class="btn-row" style="margin-top:26px">
      <a class="btn btn--primary" href="{maps}" target="_blank" rel="noopener">Open in Google Maps</a>
      <a class="btn btn--ghost" href="tel:{tel_href}">Call before you come</a>
    </div>
  </div>
</section>

<section class="band band--navy">
  <div class="wrap wrap--narrow">
    <div class="section-head reveal" style="margin-bottom:0">
      <p class="eyebrow">School details</p>
      <h2>Registration information.</h2>
      <dl class="rows" style="margin-top:30px">
        <div><dt>School</dt><dd>EduPlanet Independent School</dd></div>
        <div><dt>Grades</dt><dd>Grade RR to Grade 12</dd></div>
        <div><dt>DBE EMIS number</dt><dd>200100266</dd></div>
        <div><dt>Examination centre</dt><dd>4342022</dd></div>
        <div><dt>Company registration</dt><dd>2016/040404/07</dd></div>
      </dl>
    </div>
  </div>
</section>
"""

PAGES = {
    "index.html": dict(
        title=f"{SITE} — Grades RR to 12, Gqeberha",
        desc="EduPlanet Independent School is a registered independent school in Struandale, Gqeberha, offering the CAPS curriculum from Grade RR to Grade 12 since 2016.",
        body=HOME, active="index.html", cta=True),
    "about.html": dict(
        title=f"About — {SITE}",
        desc="EduPlanet began in 2016 as a registered independent school in Gqeberha, teaching CAPS from Grade RR to 12 with strong Christian values.",
        body=ABOUT, active="about.html", cta=True),
    "academics.html": dict(
        title=f"Academics — {SITE}",
        desc="The CAPS curriculum from Grade RR to Grade 12, taught by qualified phase specialists and assessed through a private external examination board.",
        body=ACADEMICS, active="academics.html", cta=True),
    "admissions.html": dict(
        title=f"Admissions — {SITE}",
        desc="How to apply to EduPlanet Independent School: the online application form, the documents you need, and where to send them.",
        body=ADMISSIONS, active="admissions.html", cta=True),
    "school-life.html": dict(
        title=f"School Life — {SITE}",
        desc="Sport, culture and creative work at EduPlanet Independent School in Struandale, Gqeberha.",
        body=SCHOOL_LIFE, active="school-life.html", cta=True),
    "contact.html": dict(
        title=f"Contact — {SITE}",
        desc="Contact EduPlanet Independent School: 041 451 1046, WhatsApp 060 527 3468, 1 Eveready Road, Struandale, Gqeberha.",
        body=CONTACT, active="contact.html", cta=False),
}

FIELDS = dict(
    site=SITE, tel=TEL_DISPLAY, tel_href=TEL_HREF,
    wa=WA_DISPLAY, wa_href=WA_HREF, address=ADDRESS, maps=MAPS,
    form=APPLY_FORM, pdf=APPLY_PDF,
    icon_phone=ICON_PHONE, icon_wa=ICON_WA, head_script=HEAD_SCRIPT,
    sprite=SPRITE, brand=BRAND,
    hero_gate=HERO_GATE,
    hours_short="Monday to Thursday 07:30 to 16:00 and Friday 07:30 to 15:00",
)


def build():
    for page, cfg in PAGES.items():
        html = HEAD.format(title=cfg["title"], desc=cfg["desc"], page=page,
                           nav=nav(cfg["active"]), **FIELDS)
        html += cfg["body"].format(**FIELDS)
        if cfg["cta"]:
            html += CTA.format(**FIELDS)
        html += FOOTER.format(**FIELDS)
        (ROOT / page).write_text(html, encoding="utf-8")
        print(f"wrote {page}  ({len(html):,} bytes)")


if __name__ == "__main__":
    build()
