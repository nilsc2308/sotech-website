# -*- coding: utf-8 -*-
"""Generator für die SOTECH-Website: gemeinsamer Kopf/Fuß, alle Seiten, Sitemap."""
import json, os, re, datetime
OUT = '/Users/nilscremerius/Documents/website 1/sotech-web/'
DOMAIN = 'https://www.sotech.de'
TODAY = '2026-09-15'
CO = dict(name='SOTECH GmbH', street='Am Birkenfeld 10', zip='52222', city='Stolberg', tel='02402 7097620', telh='+4924027097620', mobil='0171 5296741', mobilh='+491715296741', tel2='0241 562489', tel2h='+49241562489', fax='02402 7097621', mail='info@sotech.de', lat='50.7842942', lon='6.2324344')

LOGO = '''<svg viewBox="0 0 300 86" role="img" aria-label="SOTECH Solartechnik" xmlns="http://www.w3.org/2000/svg"><rect x="0" y="0" width="300" height="12" fill="#ba0600"/><text x="0" y="58" font-family="Archivo,'Arial Black',Arial,sans-serif" font-weight="900" font-size="54" font-stretch="110%" letter-spacing="-1.5" fill="currentColor" textLength="300" lengthAdjust="spacingAndGlyphs">SOTECH</text><text x="0" y="82" font-family="Archivo,Arial,sans-serif" font-weight="600" font-size="15" fill="currentColor" textLength="300" lengthAdjust="spacing">SOLARTECHNIK</text></svg>'''
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
TEL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.9 2z"/></svg>'
MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>'
CHEV = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 6 6 6-6 6"/></svg>'

NAV = [('index.html', 'Start', '01'), ('photovoltaik.html', 'Photovoltaik', '02'), ('speicher.html', 'Stromspeicher', '03'), ('wallbox.html', 'Wallbox', '04'), ('service.html', 'Service & Anmeldung', '05'), ('referenzen.html', 'Referenzen', '06'), ('ueber-uns.html', 'Über uns', '07'), ('ratgeber.html', 'Ratgeber', '08'), ('faq.html', 'Fragen', '09'), ('kontakt.html', 'Kontakt', '10')]

def img(name, alt, w, h, cls='', lazy=True, sizes='(max-width: 820px) 100vw, 50vw', fetch=False):
    small = int(w*0.55) if w > 900 else 500
    load = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ''
    return f'<img src="img/{name}.webp" srcset="img/{name}-m.webp {small}w, img/{name}.webp {w}w" sizes="{sizes}" width="{w}" height="{h}" alt="{alt}"{load}{c}>'

def menu_items(p):
    out=''
    for f,t,n in NAV:
        act=' class="active"' if p['file']==f or p.get('parent')==f else ''
        out+=f'<li><a href="{f}"{act}><small>{n}</small>{t}</a></li>'
    return out

def head(p):
    ld = [{
        "@context": "https://schema.org", "@type": "LocalBusiness", "@id": DOMAIN + "/#business", "name": CO['name'], "alternateName": "SOTECH Solartechnik",
        "description": "Familienbetrieb für Photovoltaik, Stromspeicher und Wallboxen in Stolberg und Aachen – seit 1988.",
        "url": DOMAIN + "/", "telephone": "+49 2402 7097620", "email": CO['mail'], "faxNumber": "+49 2402 7097621", "image": DOMAIN + "/img/og.jpg", "logo": DOMAIN + "/img/logo.svg", "priceRange": "€€",
        "address": {"@type": "PostalAddress", "streetAddress": CO['street'], "postalCode": CO['zip'], "addressLocality": CO['city'], "addressRegion": "Nordrhein-Westfalen", "addressCountry": "DE"},
        "geo": {"@type": "GeoCoordinates", "latitude": float(CO['lat']), "longitude": float(CO['lon'])},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday"], "opens": "08:00", "closes": "15:00"}, {"@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "08:00", "closes": "14:00"}],
        "areaServed": ["Stolberg", "Aachen", "Eschweiler", "Düren", "Jülich", "Städteregion Aachen"], "foundingDate": "1988", "founder": {"@type": "Person", "name": "Dirk Gier"},
        "vatID": "DE176161377", "award": "EUPD Research: Ausgezeichneter Installateur Deutschland 2023 und 2024"
    }]
    if p.get('ld'): ld.append(p['ld'])
    ogimg = DOMAIN + '/img/og.jpg'
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{p['title']}</title>
<meta name="description" content="{p['desc']}">
<link rel="canonical" href="{DOMAIN}/{'' if p['file']=='index.html' else p['file']}">
{'<meta name="robots" content="noindex, follow">' if p.get('noindex') else ''}
<meta property="og:type" content="{'article' if p.get('article') else 'website'}">
<meta property="og:site_name" content="SOTECH GmbH Solartechnik">
<meta property="og:locale" content="de_DE">
<meta property="og:title" content="{p['title']}">
<meta property="og:description" content="{p['desc']}">
<meta property="og:url" content="{DOMAIN}/{'' if p['file']=='index.html' else p['file']}">
<meta property="og:image" content="{ogimg}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#ba0600">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preload" href="fonts/archivo-latin-wdth-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="styles.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">Zum Inhalt springen</a>
<div class="curtain intro" aria-hidden="true">{LOGO.replace('fill="currentColor"', 'fill="#fff"').replace('fill="#ba0600"', 'fill="#ffdf5b"')}</div>
<div class="curtain leave" aria-hidden="true"></div>
<div class="progress" id="progress" aria-hidden="true"></div>
<header class="nav" id="nav">
  <div class="wrap" style="padding-inline:clamp(16px,3vw,40px)">
    <a class="logo" href="index.html" aria-label="SOTECH Solartechnik – Startseite">{LOGO}</a>
    <div class="nav-right">
      <a class="nav-tel" href="tel:{CO['telh']}">{TEL}<span>{CO['tel']}</span></a>
      <button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="menu"><span class="lbl">Menü</span><span class="lines"><span></span><span></span></span></button>
    </div>
  </div>
</header>
<nav class="menu" id="menu" aria-label="Hauptmenü">
  <ul>{menu_items(p)}</ul>
  <div class="menu-foot">
    <div><b>{CO['name']}</b>{CO['street']} · {CO['zip']} {CO['city']}<br>Gewerbegebiet Steinfurt</div>
    <div><a href="tel:{CO['telh']}"><b>{CO['tel']}</b></a><a href="mailto:{CO['mail']}">{CO['mail']}</a></div>
    <div>Mo–Do 8–15 Uhr · Fr 8–14 Uhr<br><a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a></div>
  </div>
</nav>
<main id="main">
'''

def cta_section(title='Sprechen wir über Ihr Dach.', sub='Kostenlose Beratung durch Elektromeister Dirk Gier – bei Ihnen vor Ort oder an unserer Besichtigungsanlage in Aachen.'):
    return f'''
<section class="sec cta" id="termin">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Termin wählen</p><h2 class="h-l split">{title}</h2><p class="lead">{sub}</p></div>
    <div class="tiles">
      <a class="tile tilt reveal hot" href="kontakt.html?thema=beratung"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="#ba0600" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11 12 3l9 8v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/></svg></span><h3>Vor-Ort-Beratung</h3><p>Herr Gier kommt zu Ihnen, schaut sich Dach und Zählerschrank an und berät kostenlos.</p><span class="link-arrow">Termin anfragen {ARROW}</span></a>
      <a class="tile tilt reveal" href="kontakt.html?thema=besichtigung"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="#1d1d1f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg></span><h3>Besichtigungsanlage</h3><p>Speicher, Wallboxen und Wärmepumpe im Betrieb sehen – Mehrfamilienhaus in Aachen, nach Absprache.</p><span class="link-arrow">Besichtigung vereinbaren {ARROW}</span></a>
      <a class="tile tilt reveal" href="kontakt.html?thema=rueckruf"><span class="ic">{TEL.replace('stroke="currentColor"','stroke="#1d1d1f"')}</span><h3>Rückruf</h3><p>Sie nennen uns Zeit und Nummer – wir rufen zurück. Auch außerhalb der Bürozeiten erreichbar.</p><span class="link-arrow">Rückruf wünschen {ARROW}</span></a>
      <a class="tile tilt reveal" href="kontakt.html?thema=angebot"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="#1d1d1f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h8"/></svg></span><h3>Angebot anfordern</h3><p>Eckdaten zu Dach und Verbrauch senden – Sie bekommen ein unverbindliches, kostenloses Angebot.</p><span class="link-arrow">Angebot anfragen {ARROW}</span></a>
    </div>
    <div class="phone">
      <div><p class="lab">Oder direkt anrufen</p><a class="bigtel" href="tel:{CO['telh']}">{CO['tel']}</a></div>
      <p class="hours"><b>Mo–Do 8–15 Uhr · Fr 8–14 Uhr</b><br>Außerhalb der Geschäftszeiten: <a href="tel:{CO['tel2h']}">{CO['tel2']}</a> oder <a href="tel:{CO['mobilh']}">{CO['mobil']}</a></p>
    </div>
  </div>
</section>'''

def foot():
    return f'''
</main>
<footer class="foot">
  <div class="wrap">
    <div class="top">
      <div><a class="logo" href="index.html" aria-label="SOTECH – Startseite">{LOGO}</a><p>Familienbetrieb für Solartechnik seit 1988. Photovoltaik, Speicher, Wallboxen und Elektroarbeiten aus Meisterhand – im Umkreis von rund 50 km um Aachen und Stolberg.</p></div>
      <div><h4>Leistungen</h4><ul><li><a href="photovoltaik.html">Photovoltaik</a></li><li><a href="speicher.html">Stromspeicher</a></li><li><a href="wallbox.html">Wallbox</a></li><li><a href="service.html">Service &amp; Anmeldung</a></li><li><a href="referenzen.html">Referenzen</a></li></ul></div>
      <div><h4>Unternehmen</h4><ul><li><a href="ueber-uns.html">Über uns</a></li><li><a href="ueber-uns.html#team">Team</a></li><li><a href="ratgeber.html">Ratgeber</a></li><li><a href="faq.html">Häufige Fragen</a></li><li><a href="kontakt.html">Kontakt</a></li></ul></div>
      <div><h4>Kontakt</h4><ul><li>{CO['name']}</li><li>{CO['street']}</li><li>{CO['zip']} {CO['city']}</li><li><a href="tel:{CO['telh']}">{CO['tel']}</a></li><li><a href="mailto:{CO['mail']}">{CO['mail']}</a></li></ul></div>
    </div>
    <div class="bottom">
      <span>© 2026 {CO['name']} · Elektromeisterbetrieb · Stolberg (Rhld.)</span>
      <span><a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a> · <a href="agb.html">AGB</a> · <a href="#" class="totop">Nach oben ↑</a></span>
    </div>
  </div>
</footer>
<div class="sticky-cta" aria-hidden="false"><a class="a1" href="tel:{CO['telh']}">{TEL} Anrufen</a><a class="a2" href="kontakt.html?thema=angebot">{MAIL} Angebot</a></div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.18/dist/lenis.min.js"></script>
<script src="main.js"></script>
</body>
</html>
'''

def page_hero(p, image, alt, crumb, h1, lead, eyebrow, meta=None, short=False, w=1800, h=1200):
    m = ''.join(f'<span><b>{a}</b> {b}</span>' for a, b in (meta or []))
    return f'''
<section class="ph{' short' if short else ''}">
  {img(image, alt, w, h, lazy=False, sizes='100vw')}
  <nav class="crumb" aria-label="Brotkrumen"><a href="index.html">Start</a>{CHEV}<span>{crumb}</span></nav>
  <div class="wrap"><p class="eyebrow">{eyebrow}</p><h1 class="split">{h1}</h1><p class="lead">{lead}</p>{f'<div class="ph-meta">{m}</div>' if m else ''}</div>
</section>'''

pages = []

# ============================ STARTSEITE ============================
INDEX = f'''
<section class="scene" id="top" aria-label="Einstieg">
  <div class="stage">
    <div class="layer l1"><img src="img/u-viertel.webp" srcset="img/u-viertel-m.webp 990w, img/u-viertel.webp 1800w" sizes="100vw" width="1800" height="1200" alt="" fetchpriority="high"><div class="cap"><p class="k">Photovoltaik · Stolberg &amp; Aachen</p><h1>Solarstrom vom eigenen Dach.</h1><p>Familienbetrieb mit Elektromeister – seit 1988.</p></div></div>
    <div class="layer l2"><img data-src="img/u-modul-3.webp" data-srcset="img/u-modul-3-m.webp 990w, img/u-modul-3.webp 1800w" sizes="100vw" width="1800" height="1200" alt="" loading="lazy"><div class="cap"><p class="k">Erfahrung</p><h2>1.500 Anlagen. 7.800 kWp.</h2><p>Jedes Dach einzeln geplant – kein Schema F.</p></div></div>
    <div class="layer l3" data-img="img/k-speicher.webp" data-img-m="img/k-speicher-m.webp"><div class="strips" aria-hidden="true"></div><div class="cap"><p class="k">Stromspeicher</p><h2>Sonne auch nach Sonnenuntergang.</h2><p>SMA- und Tesla-Speicher mit Notstromfunktion.</p></div></div>
    <div class="layer l4"><img data-src="img/k-flachdach.webp" data-srcset="img/k-flachdach-m.webp 900w, img/k-flachdach.webp 1600w" sizes="100vw" width="1600" height="910" alt="" loading="lazy"><div class="cap"><p class="k">Montage aus Meisterhand</p><h2>Eingespielte Teams, seit der Ausbildung im Betrieb.</h2><p>Dachhaken, Schienen, Module, Anmeldung – alles aus einer Hand.</p></div></div>
    <div class="layer l5" data-img="img/u-dach-haus.webp" data-img-m="img/u-dach-haus-m.webp"><div class="tiles" aria-hidden="true"></div><img class="dive" data-src="img/u-dach-haus.webp" data-srcset="img/u-dach-haus-m.webp 990w, img/u-dach-haus.webp 1800w" sizes="100vw" width="1800" height="1201" alt="" loading="lazy"><div class="flash" aria-hidden="true"></div></div>
    <div class="final"><div class="cap"><p class="k">Familienbetrieb seit 1988</p><h2>Auch nach 38 Jahren noch am selben Standort.</h2><p>Der Chef steht selbst auf dem Dach und berät am Küchentisch. Kostenlos, vor Ort, mit Handschlag.</p><div class="actions"><a class="btn btn-sun" href="kontakt.html?thema=beratung">Kostenlose Beratung {ARROW}</a><a class="btn btn-ghost" href="#leistungen">Leistungen</a></div></div></div>
  </div>
</section>

<section class="year" aria-label="Seit 1988">
  <div class="stage">
    <div class="wrap">
      <div class="big" aria-hidden="true">19<em>88</em></div>
      <div class="copy">
        <p>Seit <span class="slot"><span class="slot-t">1988</span></span> im Einsatz für die Energiewende: In 38 Jahren hat SOTECH rund 1.500 Anlagen mit 7.800 kWp errichtet – und unzählige PV-Systeme in alle Welt versandt.</p>
        <div class="facts"><div><b>1.500</b>errichtete Anlagen</div><div><b>7.800 kWp</b>installierte Leistung</div><div><b>Meisterbetrieb</b>Elektrohandwerk, bildet aus</div><div><b>EUPD 2024</b>Ausgezeichneter Installateur</div></div>
      </div>
    </div>
  </div>
</section>

<section class="sec acc-sec" id="leistungen">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Leistungen</p><h2 class="h-l split">Alles aus einer Hand – vom Dachhaken bis zur Anmeldung.</h2></div>
    <div class="acc">
      <div class="strip on" tabindex="0" role="button" aria-expanded="true" data-href="photovoltaik.html">{img('u-modul-2', '', 1800, 1200, sizes='(max-width: 820px) 100vw, 60vw')}<div class="lab"><span class="num">01</span><h3>Photovoltaik</h3><p>Planung und Montage von PV-Anlagen auf Sattel-, Pult- und Flachdächern. Module von Heckert Solar (Chemnitz), Wechselrichter von SMA, Montagesystem TRIC von Wagner Solar.</p><a class="go" href="photovoltaik.html">Mehr zur Photovoltaik {ARROW}</a></div></div>
      <div class="strip" tabindex="0" role="button" aria-expanded="false" data-href="speicher.html">{img('k-speicher', '', 1800, 1350, sizes='(max-width: 820px) 100vw, 60vw')}<div class="lab"><span class="num">02</span><h3>Stromspeicher</h3><p>SMA-DC-Speichersysteme und Tesla-Speicher mit Notstrom- und Ersatzstromfunktion. Wir dimensionieren den Speicher passend zu Ihrem Verbrauch.</p><a class="go" href="speicher.html">Mehr zu Speichern {ARROW}</a></div></div>
      <div class="strip" tabindex="0" role="button" aria-expanded="false" data-href="wallbox.html">{img('k-wallbox-2', '', 1200, 1600, sizes='(max-width: 820px) 100vw, 60vw')}<div class="lab"><span class="num">03</span><h3>Wallbox</h3><p>Zappy Wallbox 11 kW – sicheres, schnelles Laden zu Hause. Prüfung vor Ort, Montage und Anmeldung beim Netzbetreiber inklusive.</p><a class="go" href="wallbox.html">Mehr zur Wallbox {ARROW}</a></div></div>
      <div class="strip" tabindex="0" role="button" aria-expanded="false" data-href="service.html">{img('k-zaehlerschrank', '', 796, 600, sizes='(max-width: 820px) 100vw, 60vw')}<div class="lab"><span class="num">04</span><h3>Service</h3><p>Anmeldung beim Netzbetreiber und im Marktstammdatenregister, Anmeldung von Wärmepumpen, Wartung, Monitoring und Solarversicherung – die Bürokratie übernehmen wir.</p><a class="go" href="service.html">Mehr zum Service {ARROW}</a></div></div>
      <div class="strip" tabindex="0" role="button" aria-expanded="false" data-href="referenzen.html">{img('r-zg30', '', 1204, 1065, sizes='(max-width: 820px) 100vw, 60vw')}<div class="lab"><span class="num">05</span><h3>Referenzen</h3><p>Rund 1.500 Anlagen in 38 Jahren – auf der Karte, in Bildern und als Besichtigungsanlage in Aachen.</p><a class="go" href="referenzen.html">Zu den Referenzen {ARROW}</a></div></div>
    </div>
  </div>
</section>

<section class="day" aria-label="Ein Tag mit Solarstrom">
  <div class="stage">
    <div class="head" aria-hidden="true"><span>Ein Tag mit Solarstrom</span><span class="hl">Morgen</span></div>
    <div class="dial" aria-hidden="true">
      <svg viewBox="-40 -40 580 580">
        <circle class="ring" cx="250" cy="250" r="210"/>
        <g class="ticks"></g>
        <path class="arc" d=""/>
        <g class="house">
          <path class="flow d" d="M250 178 L250 205 M250 205 L214 232" />
          <path class="flow n" d="M214 300 L250 300 L250 322" />
          <polygon class="roof-glow" points="175,205 250,150 325,205" />
          <polygon points="180,205 250,152 320,205" fill="#2b2b30"/>
          <rect x="196" y="176" width="24" height="12" fill="#ffdf5b" opacity=".9" transform="rotate(-36 208 182)"/>
          <rect x="222" y="160" width="24" height="12" fill="#ffdf5b" opacity=".9" transform="rotate(-36 234 166)"/>
          <rect x="262" y="160" width="24" height="12" fill="#ffdf5b" opacity=".9" transform="rotate(36 274 166)"/>
          <rect x="288" y="176" width="24" height="12" fill="#ffdf5b" opacity=".9" transform="rotate(36 300 182)"/>
          <rect class="wall" x="190" y="205" width="120" height="70"/>
          <rect class="win" x="204" y="220" width="22" height="22"/><rect class="win lit" x="204" y="220" width="22" height="22"/>
          <rect class="win" x="274" y="220" width="22" height="22"/><rect class="win lit" x="274" y="220" width="22" height="22"/>
          <rect x="238" y="240" width="24" height="35" fill="#1d1d1f"/>
          <rect x="190" y="275" width="120" height="6" fill="#1d1d1f"/>
          <rect class="bat" x="200" y="316" width="26" height="48" rx="4"/><rect x="209" y="311" width="8" height="5" fill="#fff"/>
          <rect class="bat-fill" x="204" y="340" width="18" height="20" rx="2"/>
          <text x="213" y="380" font-size="10" text-anchor="middle" opacity=".8">Speicher</text>
          <rect x="262" y="336" width="44" height="18" rx="7" fill="#ba0600"/><rect x="270" y="328" width="26" height="12" rx="5" fill="#ba0600"/><circle cx="272" cy="356" r="5" fill="#1d1d1f"/><circle cx="296" cy="356" r="5" fill="#1d1d1f"/>
          <text x="284" y="380" font-size="10" text-anchor="middle" opacity=".8">E-Auto</text>
        </g>
        <circle class="moon" cx="0" cy="0" r="11"/>
        <circle class="orb" cx="0" cy="0" r="14"/>
        <text class="clock-l" x="250" y="76">UHRZEIT</text>
        <text class="clock" x="250" y="126">05:00</text>
      </svg>
    </div>
    <div class="txt">
      <div class="st"><p class="kicker">05–09 Uhr · Morgen</p><h2>Die Anlage <span>wacht auf.</span></h2><p>Mit dem ersten Licht beginnen die Module zu arbeiten. Der Speicher hat die Nacht überbrückt – jetzt übernimmt wieder das Dach: Kühlschrank, Kaffee, Warmwasser laufen mit Solarstrom.</p></div>
      <div class="st"><p class="kicker">09–16 Uhr · Mittag</p><h2>Das Dach lädt <span>Speicher und Auto.</span></h2><p>Zur Mittagszeit produziert die Anlage mehr, als das Haus braucht. Der Überschuss fließt in den Speicher und über die Wallbox ins E-Auto. Erst wenn beides voll ist, geht Strom ins Netz.</p></div>
      <div class="st"><p class="kicker">16–21 Uhr · Abend</p><h2>Der Speicher <span>übernimmt.</span></h2><p>Wenn die Sonne sinkt und der Verbrauch steigt – Kochen, Licht, Fernseher – versorgt der Speicher das Haus. Teuren Netzstrom brauchen Sie kaum noch.</p></div>
      <div class="st"><p class="kicker">21–05 Uhr · Nacht</p><h2>Unabhängig – <span>auch bei Stromausfall.</span></h2><p>Mit Ersatzstromfunktion trennt sich das System bei Netzausfall automatisch vom Netz und versorgt die wichtigsten Verbraucher weiter. Am nächsten Morgen lädt die Sonne den Speicher wieder auf.</p><p style="margin-top:18px"><a class="link-arrow" href="speicher.html">So funktioniert Speicher mit Notstrom {ARROW}</a></p></div>
    </div>
  </div>
</section>

<section class="mq" aria-label="Einsatzgebiet">
  <div class="track"><div class="row">
    <span>Stolberg</span><img src="img/r-zg30-m.webp" width="200" height="150" alt="" loading="lazy"><span class="ol">Aachen</span><span class="dot"></span><span>Eschweiler</span><img src="img/r-haus-2-m.webp" width="200" height="150" alt="" loading="lazy"><span class="ol">Düren</span><span class="dot"></span><span>Jülich</span><img src="img/r-yingli-m.webp" width="200" height="150" alt="" loading="lazy"><span class="ol">Herzogenrath</span><span class="dot"></span><span>Hürtgenwald</span><img src="img/r-baur-m.webp" width="200" height="150" alt="" loading="lazy"><span class="ol">Würselen</span><span class="dot"></span><span>Alsdorf</span><img src="img/r-carport-m.webp" width="200" height="150" alt="" loading="lazy"><span class="ol">Roetgen</span><span class="dot"></span>
  </div></div>
  <p class="mq-note">Unser Einsatzgebiet: rund 50 km um Aachen und Stolberg – Städteregion Aachen, Kreis Düren und Kreis Heinsberg.</p>
</section>

<section class="sec dark eeg rounded-top">
  <div class="glow" aria-hidden="true"></div>
  <div class="wrap">
    <div class="grid">
      <div class="reveal"><div class="date">1.1.<br>2027<small>Stichtag EEG 2027</small></div><div class="days"><b id="daysLeft">–</b><span>Tage bis zum Stichtag</span></div></div>
      <div>
        <p class="eyebrow">Jetzt handeln</p>
        <h2 class="h-m split" style="margin-bottom:22px">Schnelles Handeln ist gefordert: Errichten Sie Ihre PV-Anlage vor dem 1.1.2027.</h2>
        <p class="reveal">Die feste Einspeisevergütung wird für Neuanlagen zum 1. Januar 2027 abgeschafft. Anlagen, die danach ans Netz gehen, erhalten nur noch eine abgesenkte Übergangszahlung und müssen später in die Direktvermarktung – mit Smart Meter, Steuerbox und Dienstleister.</p>
        <p class="reveal">Wer bis Ende 2026 in Betrieb geht, sichert sich die Vergütung nach EEG 2023 für 20 Jahre. Die Mehrwertsteuerbefreiung für neue PV-Anlagen bleibt zunächst bestehen.</p>
        <div class="reveal" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:26px"><a class="btn btn-sun" href="service.html#zeitplan">Zeitplan prüfen {ARROW}</a><a class="btn btn-ghost" href="ratgeber-eeg-2027.html">Was sich ändert</a></div>
      </div>
    </div>
  </div>
</section>
''' + cta_section()

STORY_SEC = f'''<section class="sec story" id="ablauf">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">So läuft die Montage</p><h2 class="h-l split">Vom ersten Dachhaken bis zur Inbetriebnahme.</h2><p class="lead">Eine Reportage von einer unserer Baustellen – ein steiles Pfannendach, 48 Module, ein Tag.</p></div>
    <div class="grid">
      <div class="stick"><div class="frame">
        {img('k-haken-1', 'Monteur befestigt Dachhaken an den Sparren eines Pfannendachs', 768, 768, sizes='(max-width: 820px) 100vw, 50vw')}
        {img('k-haken-2', 'Profilschienen werden auf den Dachhaken montiert', 768, 768, sizes='(max-width: 820px) 100vw, 50vw')}
        {img('k-tragen', 'Zwei Monteure tragen ein Solarmodul aufs Dach', 628, 541, sizes='(max-width: 820px) 100vw, 50vw')}
        {img('r-reihen', 'Fertig montierte Modulreihen auf dem Dach', 768, 576, sizes='(max-width: 820px) 100vw, 50vw')}
        {img('k-speicher', 'SMA-Wechselrichter und Speicher im Keller', 1800, 1350, sizes='(max-width: 820px) 100vw, 50vw')}
        {img('k-zaehler', 'Zweirichtungszähler im Zählerschrank', 800, 600, sizes='(max-width: 820px) 100vw, 50vw')}
        <span class="cnt">01 / 06</span><span class="bar"><i></i></span>
      </div></div>
      <div class="chaps">
        <div class="chap"><span class="n">Kapitel 1</span><h3>Klettertour für Schwindelfreie</h3><p>Das Dach ist zu steil, um auf den Pfannen zu laufen. Daher entfernen die Monteure zunächst ein paar Ziegel. Einige Lücken dienen dazu, die Dachhaken zu befestigen: Sie werden mit Holzschrauben an den Sparren montiert und danach wieder mit Dachpfannen bedeckt.</p></div>
        <div class="chap"><span class="n">Kapitel 2</span><h3>Die Schienen</h3><p>Auf die Dachhaken kommen die Profilschienen in vertikaler Richtung. Die horizontalen Profile des Montagesystems werden mit Edelstahlschrauben auf den senkrechten Schienen befestigt. Das System ist recht belastbar – und die Installation geht schnell.</p></div>
        <div class="chap"><span class="n">Kapitel 3</span><h3>Module aufs Dach</h3><p>Nun geht es an die Verkabelung. Alle Kabelbrücken werden mit UV-beständigen Kabelbindern an den Schienen fixiert. Dann kommen die Module in Einzelbefestigung aufs Dach: Innerhalb von zwei Stunden sind 48 Module verkabelt und befestigt.</p></div>
        <div class="chap"><span class="n">Kapitel 4</span><h3>Strangspannung prüfen</h3><p>Bevor etwas angeschlossen wird, messen wir jeden Strang. Erst wenn die Werte stimmen, werden die Strangleitungen nach unten geführt – sauber verlegt, damit auch in 20 Jahren nichts scheuert.</p></div>
        <div class="chap"><span class="n">Kapitel 5</span><h3>Wechselrichter im Keller</h3><p>Die Strangleitungen werden an den Wechselrichter im Keller angeschlossen – hier unten arbeiten Wechselrichter am besten, kühl und geschützt. Noch ein Erdungskabel, dann steht das System.</p></div>
        <div class="chap"><span class="n">Kapitel 6</span><h3>Zähler und Inbetriebnahme</h3><p>Der Netzbetreiber setzt den Zweirichtungszähler im separaten Zählerplatz. Wir nehmen die Anlage in Betrieb, weisen Sie ein und übernehmen die Anmeldung im Marktstammdatenregister. Ab jetzt arbeitet die Sonne für Sie.</p></div>
      </div>
    </div>
  </div>
</section>

'''
CALC_SEC = f'''<section class="sec calc" id="rechner">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Schnell-Check</p><h2 class="h-l split">Was bringt Ihr Dach?</h2><p class="lead">Dachfläche und Stromverbrauch eingeben – das Ergebnis rechnet live mit. Richtwerte für die Region Aachen, keine Angebotsgrundlage.</p></div>
    <div class="box">
      <div>
        <div class="field"><label class="f" for="cArea">Nutzbare Dachfläche in m²</label><input type="number" id="cArea" value="50" min="10" max="400" step="5" inputmode="numeric"></div>
        <div class="field"><label class="f" for="cUse">Stromverbrauch im Jahr in kWh</label><input type="number" id="cUse" value="4000" min="500" max="30000" step="100" inputmode="numeric"></div>
        <div class="field"><span class="f" id="cDirLbl">Ausrichtung</span><div class="seg" id="cDir" role="group" aria-labelledby="cDirLbl"><button type="button" data-f="1" aria-pressed="true">Süd</button><button type="button" data-f=".95" aria-pressed="false">Süd-Ost / Süd-West</button><button type="button" data-f=".85" aria-pressed="false">Ost / West</button></div></div>
        <label class="sw"><input type="checkbox" id="cBat" checked> Mit Stromspeicher</label>
      </div>
      <div class="out" aria-live="polite">
        <div class="o"><b><span id="oKwp">0</span><em>kWp</em></b><small>Anlagengröße</small></div>
        <div class="o"><b><span id="oYr">0</span><em>kWh</em></b><small>Ertrag pro Jahr</small></div>
        <div class="o"><b><span id="oSelf">0</span><em>kWh</em></b><small>davon selbst genutzt (<span id="oPct">0 %</span>)</small></div>
        <div class="o"><b><span id="oCo2">0</span><em>t</em></b><small>CO₂-Einsparung pro Jahr</small></div>
        <div class="o big"><b><span id="oSave">0</span><em>€ / Jahr</em></b><small>Ersparnis aus Eigenverbrauch und Einspeisevergütung</small></div>
        <p class="note">Richtwerte: 5 m² je kWp, 950 kWh je kWp und Jahr, Netzstrom 0,35 €/kWh, Einspeisevergütung 7,78 ct/kWh (Stand Feb.–Juli 2026), Eigenverbrauch ca. 30 % ohne / 60 % mit Speicher, 0,38 kg CO₂ je kWh. Genaue Zahlen gibt es beim Vor-Ort-Termin.</p>
      </div>
    </div>
  </div>
</section>

'''
pages.append(dict(file='index.html', title='Photovoltaik Stolberg & Aachen – SOTECH GmbH, Familienbetrieb seit 1988', desc='PV-Anlagen, Stromspeicher und Wallboxen vom Elektromeisterbetrieb in Stolberg. Seit 1988, rund 1.500 Anlagen, alles aus einer Hand – kostenlose Beratung.', body=INDEX))

# ============================ PHOTOVOLTAIK ============================
PV = page_hero({}, 'u-modul-3', 'Solarmodule auf einem Dach unter blauem Himmel', 'Photovoltaik', 'Photovoltaik, die zu Ihrem Dach passt.', 'Individuelle Planung statt Schema F: Wir begutachten jedes Dach, holen die maximale Effizienz aus Ausrichtung und Verschattung heraus und montieren mit eigenem Team.', 'Leistung 02', meta=[('Module', 'Heckert Solar, Chemnitz'), ('Wechselrichter', 'SMA'), ('Montage', 'Wagner Solar TRIC')]) + f'''
<section class="sec">
  <div class="wrap">
    <div class="two">
      <div><p class="eyebrow">Unser Ansatz</p><h2 class="h-l split">Es geht nicht nur um Module auf dem Dach.</h2><p class="lead" style="margin-top:22px">Sondern um das Zusammenspiel von Anlage, Speicher, Wallbox und smarter Steuerung – abgestimmt auf Ihren Verbrauch. Die wichtigste Voraussetzung für Wirtschaftlichkeit ist ein möglichst hoher Eigenverbrauch.</p>
        <ul class="prose" style="margin-top:26px;padding-left:22px"><li class="reveal"><b>Individuelle Planung:</b> Jedes Dach wird detailliert begutachtet – Ausrichtung, Neigung, Verschattung, Statik, Eindeckung.</li><li class="reveal"><b>Ganzheitlich:</b> Speicher, Wallbox und Wärmepumpe werden von Anfang an mitgedacht.</li><li class="reveal"><b>Wirtschaftlichkeit und Optik</b> stehen für uns an erster Stelle – auch mit Full-Black-Modulen ohne sichtbare Leiterbahnen.</li></ul></div>
      <div class="ph-img reveal">{img('r-schwarz', 'Schwarze Solarmodule auf einem Ziegeldach', 768, 576)}</div>
    </div>
  </div>
</section>

<section class="sec" style="background:var(--bg-2)" id="konfigurator">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Konfigurator</p><h2 class="h-l split">Stellen Sie Ihre Anlage zusammen.</h2><p class="lead">Dachform, Größe, Modulfarbe, Speicher und Wallbox wählen – die Vorschau und die Kennzahlen passen sich sofort an. Richtwerte, kein Angebot.</p></div>
    <div class="cfg">
      <div class="opts">
        <div class="opt"><span id="lRoof">Dachform</span><div class="seg" data-k="roof" role="group" aria-labelledby="lRoof"><button type="button" data-v="sattel" aria-pressed="true">Satteldach</button><button type="button" data-v="pult" aria-pressed="false">Pultdach</button><button type="button" data-v="flach" aria-pressed="false">Flachdach</button></div></div>
        <div class="opt"><span id="lSize">Anlagengröße</span><div class="seg" data-k="size" role="group" aria-labelledby="lSize"><button type="button" data-v="6" aria-pressed="false">ca. 6 kWp</button><button type="button" data-v="10" aria-pressed="true">ca. 10 kWp</button><button type="button" data-v="15" aria-pressed="false">ca. 15 kWp</button></div></div>
        <div class="opt"><span id="lMod">Module</span><div class="seg" data-k="mod" role="group" aria-labelledby="lMod"><button type="button" data-v="black" aria-pressed="true">Full Black</button><button type="button" data-v="std" aria-pressed="false">Glas-Glas Standard</button></div></div>
        <div class="opt"><span id="lBat">Stromspeicher</span><div class="seg" data-k="bat" role="group" aria-labelledby="lBat"><button type="button" data-v="0" aria-pressed="false">Ohne</button><button type="button" data-v="5" aria-pressed="true">ca. 5 kWh</button><button type="button" data-v="10" aria-pressed="false">ca. 10 kWh</button></div></div>
        <div class="opt"><span id="lWb">Wallbox</span><div class="seg" data-k="wb" role="group" aria-labelledby="lWb"><button type="button" data-v="1" aria-pressed="true">Mit Wallbox 11 kW</button><button type="button" data-v="0" aria-pressed="false">Ohne</button></div></div>
        <p class="muted" style="font-size:13px;line-height:1.5">Richtwerte: 450 Wp je Modul, 950 kWh je kWp und Jahr, Eigenverbrauch 30 % (ohne Speicher) bis 70 % (Speicher + Wallbox). Die tatsächliche Belegung hängt von Dachmaßen, Fenstern und Verschattung ab.</p>
      </div>
      <div class="preview" aria-live="polite">
        <svg viewBox="0 0 600 400" role="img" aria-label="Schematische Vorschau der gewählten Anlage"></svg>
        <div class="sum"><div><b id="kMods">–</b>Belegung</div><div><b id="kKwp">–</b>Leistung</div><div><b id="kYr">–</b>Ertrag (Richtwert)</div><div><b id="kShare">–</b>Eigenverbrauch (Richtwert)</div></div>
        <p class="parts" id="kParts"></p>
        <a class="btn btn-primary" id="kLink" href="kontakt.html?thema=photovoltaik">Diese Konfiguration anfragen {ARROW}</a>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Komponenten</p><h2 class="h-l split">Wir verarbeiten Qualität, die überzeugt.</h2></div>
    <div class="cards">
      <div class="card tilt reveal"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="#1d1d1f" stroke-width="2"><rect x="3" y="4" width="18" height="16" rx="1"/><path d="M3 10h18M3 15h18M9 4v16M15 4v16"/></svg></span><h3>Solarmodule – Heckert Solar</h3><p>Deutscher Hersteller aus Chemnitz, „Made in Germany“. ZEUS-Serie: Glas-Glas-Module mit TOPCon-/bifazialer Technik, ca. 445–460 Wp für Hausdächer, Back-Contact ohne sichtbare Leiterbahnen. ZEUS Full Black für Design-Anlagen, Fassaden und schwierige Dächer.</p><a class="link-arrow" href="https://www.heckertsolar.com/" target="_blank" rel="noopener">heckertsolar.com {ARROW}</a></div>
      <div class="card tilt reveal"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="#1d1d1f" stroke-width="2"><rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/></svg></span><h3>Wechselrichter &amp; Speicher – SMA</h3><p>Sunny Boy und Sunny Tripower Smart Energy als Hybridsysteme mit DC-Speicher, Notstromsteckdose oder Ersatzstromversorgung, Monitoring per App. Bei Netzausfall trennt sich das System normgerecht (VDE-AR-N 4105) und versorgt das Haus weiter.</p><a class="link-arrow" href="speicher.html">Speicher im Detail {ARROW}</a></div>
      <div class="card tilt reveal"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="#1d1d1f" stroke-width="2"><path d="M3 20 12 5l9 15z"/><path d="M7 20l5-8 5 8"/></svg></span><h3>Montagesystem – Wagner Solar TRIC</h3><p>Seit 1979 in Kirchhain (Hessen), Eigenproduktion, TÜV-zertifiziert mit bauaufsichtlicher Zulassung. Aufdach-Systeme für Pfannen-, Schiefer- und Trapezblechdächer sowie Flachdach-Aufständerungen.</p><a class="link-arrow" href="https://wagner-solar.com/de/" target="_blank" rel="noopener">wagner-solar.com {ARROW}</a></div>
    </div>
  </div>
</section>

''' + STORY_SEC + cta_section('Ihr Dach, unser Angebot.', 'Kostenlos und unverbindlich – vom Familienbetrieb, der nach der Installation nicht verschwindet.')
pages.append(dict(file='photovoltaik.html', title='Photovoltaik Stolberg & Aachen – Planung & Montage | SOTECH', desc='PV-Anlagen für Sattel-, Pult- und Flachdach: Heckert-Module, SMA-Wechselrichter, eigenes Montageteam. Konfigurator mit Vorschau, kostenlose Beratung vor Ort.', body=PV))

# ============================ SPEICHER & WALLBOX ============================
SP = page_hero({}, 'k-speicher', 'SMA-Speichersystem und Wechselrichter an einer Kellerwand', 'Stromspeicher', 'Sonne auch nach Sonnenuntergang.', 'Ein Batteriespeicher hebt den Eigenverbrauch von rund 30 auf 60 Prozent – und mit Ersatzstromfunktion bleibt das Haus auch bei Netzausfall versorgt.', 'Leistung 03', w=1800, h=1350, meta=[('Systeme', 'SMA DC-System, Tesla'), ('Notstrom', 'Steckdose oder Ersatzstrom'), ('Monitoring', 'per App')]) + f'''
<section class="sec">
  <div class="wrap">
    <div class="two">
      <div class="ph-img reveal">{img('k-speicher', 'SMA-Speichersystem und Wechselrichter an einer Kellerwand', 1800, 1350)}</div>
      <div><p class="eyebrow">Stromspeicher</p><h2 class="h-l split">Sonne auch nach Sonnenuntergang.</h2><p class="lead" style="margin-top:22px">Ohne Speicher nutzen Sie rund 30 % Ihres Solarstroms selbst, mit Speicher etwa 60 % – der Rest wird günstig eingespeist statt teuer zugekauft. Wir dimensionieren den Speicher nach Ihrem Verbrauch, nicht nach Katalog.</p>
      <div class="prose" style="margin-top:22px"><h3>Was läuft bei Netzausfall weiter?</h3><p><b>Notstromsteckdose</b> (SMA Sunny Boy bis 4,6 kW SE): eine separat abgesicherte 16-A-Steckdose liefert Strom, sofern ein SMA-Akku mit mindestens 3,28 kWh vorhanden ist und noch rund 20 % Restkapazität hat – eine kurzfristige Lösung.</p><p><b>Ersatzstrom</b> (SMA DC-Speichersystem): Der Wechselrichter muss dreiphasig sein. Im Zählerschrank werden auf einer Phase bestimmte Stromkreise mit definierten Verbrauchern angeklemmt. Im Winter empfehlen wir, die Entladung auf ca. 50 % zu begrenzen, damit im Ernstfall Reserve bleibt. In jedem Fall lädt der Akku auch bei Stromausfall weiter, wenn genügend Sonne auf die Module fällt.</p><p><a href="ratgeber-notstrom-speicher.html">Ausführlich im Ratgeber: Notstrom und Ersatzstrom</a></p></div></div>
    </div>
  </div>
</section>

<section class="sec night rounded-top" style="background:var(--night)">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">So arbeitet ein Hybridsystem bei Stromausfall</p><h2 class="h-l split">Erst trennen, dann takten, dann versorgen.</h2></div>
    <div class="steps">
      <div class="step reveal" style="background:var(--night-2);border-color:rgba(255,255,255,.1)"><h3>Galvanische Trennung</h3><p style="color:var(--dark-ink-2)">Nach Norm (VDE-AR-N 4105) trennt sich der Wechselrichter bei Netzausfall innerhalb von Millisekunden vom öffentlichen Netz. Eine automatische Umschalteinrichtung kappt die Verbindung vollständig.</p></div>
      <div class="step reveal" style="background:var(--night-2);border-color:rgba(255,255,255,.1)"><h3>Inselnetz-Aufbau</h3><p style="color:var(--dark-ink-2)">Erst wenn das Haus zu 100 % isoliert ist, übernimmt der SMA-Wechselrichter selbst die Taktung mit 50 Hz und 230 bzw. 400 V.</p></div>
      <div class="step reveal" style="background:var(--night-2);border-color:rgba(255,255,255,.1)"><h3>Eigenversorgung</h3><p style="color:var(--dark-ink-2)">DC-Speicher und PV-Module versorgen ausschließlich die Verbraucher im eigenen Haushalt – Kühlschrank, Heizungssteuerung, Licht, Router.</p></div>
    </div>
  </div>
</section>

''' + CALC_SEC.replace('Was bringt Ihr Dach?', 'Was bringt Ihr Dach – mit Speicher?').replace('id="rechner"', 'id="rechner"') + cta_section('Welcher Speicher passt zu Ihnen?', 'Wir dimensionieren nach Ihrem Verbrauch, nicht nach Katalog – kostenlos und unverbindlich.')
pages.append(dict(file='speicher.html', title='Stromspeicher mit Notstrom – SMA & Tesla | SOTECH Stolberg', desc='Batteriespeicher für Ihre PV-Anlage: SMA DC-System und Tesla, Notstrom oder Ersatzstrom bei Netzausfall. Rechner: Was bringt Ihr Dach mit Speicher?', body=SP))
WB = page_hero({}, 'u-laden', 'Elektroauto lädt an einer Wallbox', 'Wallbox', 'Tanken in der eigenen Garage.', 'Wir installieren Wallboxen mit 11 kW – in der Garage, am Carport oder in der Tiefgarage – inklusive der verpflichtenden Anmeldung beim Netzbetreiber.', 'Leistung 04', w=1200, h=1620, meta=[('Wallbox', 'Zappy 11 kW'), ('Anmeldung', 'inklusive'), ('Steuerbar', 'nach § 14a EnWG')]) + f'''
<section class="sec">
  <div class="wrap">
    <div class="two">
      <div><p class="eyebrow">Wallbox 11 kW</p><h2 class="h-l split">Tanken zu Hause – sicher, schnell, angemeldet.</h2><p class="lead" style="margin-top:22px">Elektroautos dürfen aus Sicherheitsgründen nicht dauerhaft an der Haushaltssteckdose geladen werden. Wir installieren leistungsstarke Wallboxen (11 kW) – in der Garage, am Carport oder in der Tiefgarage. Wir prüfen die Gegebenheiten vor Ort und kümmern uns um alles, inklusive der verpflichtenden Anmeldung beim Netzbetreiber.</p>
      <div class="prose" style="margin-top:22px"><h3>Zappy Wallbox 11 kW</h3><p>Unsere Standard-Wallbox: kompakt, mit PV-Überschussladung kombinierbar und steuerbar nach § 14a EnWG – so lädt das Auto bevorzugt dann, wenn das Dach Überschuss produziert.</p></div></div>
      <div class="gal" style="grid-template-columns:1fr 1fr">
        <figure class="tall">{img('k-wallbox-2', 'Zappy Wallbox 11 kW an einer Hauswand', 1200, 1600, sizes='(max-width: 820px) 50vw, 25vw')}<figcaption>Zappy 11 kW</figcaption></figure>
        <figure>{img('k-wallbox-3', 'Wallbox an einer Klinkerfassade', 768, 768, sizes='(max-width: 820px) 50vw, 25vw')}<figcaption>Klinkerfassade</figcaption></figure>
        <figure>{img('k-wallbox-4', 'Wallbox mit Ladekabel in einer Garage', 768, 576, sizes='(max-width: 820px) 50vw, 25vw')}<figcaption>Garage</figcaption></figure>
      </div>
    </div>
  </div>
</section>

<section class="sec" style="background:var(--bg-2)" id="checkliste">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Checkliste</p><h2 class="h-l split">Ist Ihr Hausanschluss bereit für die Wallbox?</h2><p class="lead">Haken Sie ab, was bei Ihnen schon geklärt ist. Alles Offene übernehmen wir beim Vor-Ort-Termin.</p></div>
    <div class="chk">
      <ul>
        <li><label><input type="checkbox"><div><b>Stellplatz mit Stromweg</b><span>Garage, Carport oder Tiefgarage – und eine mögliche Kabelstrecke vom Zählerschrank bis zur Wallbox (Länge grob bekannt).</span></div></label></li>
        <li><label><input type="checkbox"><div><b>Ladeleistung ≤ 11 kW gewählt</b><span>Bis 11 kW ist die Anmeldung beim Netzbetreiber kostenlos und darf nicht abgelehnt werden. Über 11 kW (z. B. 22 kW) braucht es vorab eine Genehmigung.</span></div></label></li>
        <li><label><input type="checkbox"><div><b>Anmeldepflicht bekannt</b><span>Jede Ladeeinrichtung über 4,2 kW muss dem Netzbetreiber gemeldet werden – auch eine CEE-Dose, die zum Laden genutzt wird.</span></div></label></li>
        <li><label><input type="checkbox"><div><b>Steuerbarkeit nach § 14a EnWG</b><span>Neue Wallboxen müssen vom Netzbetreiber dimmbar sein. Ein einfacher CEE-Stecker erfüllt das oft nicht – es braucht eine schaltbare Steckdose mit Steuerschütz oder eine steuerbare Wallbox.</span></div></label></li>
        <li><label><input type="checkbox"><div><b>Zählerschrank ausreichend</b><span>Platz für FI-Schutzschalter, Leitungsschutz und ggf. Steuerbox. Fotos vom offenen Zählerschrank aus 1,5 m Entfernung helfen uns bei der Einschätzung.</span></div></label></li>
        <li><label><input type="checkbox"><div><b>Netzbetreiber bekannt</b><span>Steht auf der Stromrechnung oder direkt auf dem Zähler. Die Anmeldung läuft über das Inbetriebsetzungsportal – meist durch uns als Fachbetrieb.</span></div></label></li>
        <li><label><input type="checkbox"><div><b>PV-Überschussladen gewünscht?</b><span>Wenn eine PV-Anlage vorhanden oder geplant ist, stimmen wir Wallbox und Energiemanagement so ab, dass bevorzugt Solarstrom ins Auto fließt.</span></div></label></li>
      </ul>
      <div class="res" aria-live="polite"><div class="ring"><svg viewBox="0 0 100 100"><circle class="bg" cx="50" cy="50" r="42" pathLength="1"/><circle class="fg" cx="50" cy="50" r="42" pathLength="1"/></svg><b>0 %</b></div><p></p><a class="btn btn-sun" href="kontakt.html?thema=wallbox">Wallbox anfragen {ARROW}</a></div>
    </div>
  </div>
</section>
''' + cta_section('Bereit für die Wallbox?', 'Vor-Ort-Prüfung, Montage und Anmeldung aus einer Hand – kostenlos beraten lassen.')
pages.append(dict(file='wallbox.html', title='Wallbox 11 kW installieren – Stolberg, Aachen | SOTECH', desc='Zappy Wallbox 11 kW mit Anmeldung beim Netzbetreiber, steuerbar nach § 14a EnWG. Checkliste: Ist Ihr Hausanschluss bereit? Elektromeisterbetrieb seit 1988.', body=WB))

# ============================ SERVICE & ANMELDUNG ============================
SV = page_hero({}, 'k-zaehlerschrank', 'Geöffneter Zählerschrank mit Zweirichtungszähler', 'Service & Anmeldung', 'Die Bürokratie übernehmen wir.', 'Anmeldung beim Netzbetreiber, Marktstammdatenregister, Wärmepumpen-Anmeldung, Versicherung, Wartung und Monitoring – das größte Plus eines Familienbetriebs ist die Entlastung nach dem Kauf.', 'Leistung 04', w=796, h=600, meta=[('Bürozeiten', 'Mo–Do 8–15, Fr 8–14 Uhr'), ('Notfall', CO['tel2'])]) + f'''
<section class="sec">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Was wir für Sie erledigen</p><h2 class="h-l split">Anmelden, versichern, warten – alles aus einer Hand.</h2></div>
    <div class="cards">
      <div class="card tilt reveal"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="#1d1d1f" stroke-width="2" stroke-linecap="round"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg></span><h3>Anmeldung beim Netzbetreiber</h3><p>PV-Anlage, Speicher und Wallbox werden über das Inbetriebsetzungsportal des regionalen Netzbetreibers angemeldet – wir übernehmen das als Fachbetrieb. Bis 11 kW Ladeleistung kostenlos und nicht ablehnbar.</p></div>
      <div class="card tilt reveal"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="#1d1d1f" stroke-width="2" stroke-linecap="round"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9h10M7 13h6"/></svg></span><h3>Marktstammdatenregister</h3><p>Jede Anlage muss innerhalb eines Monats nach Inbetriebnahme im Register der Bundesnetzagentur eingetragen sein – sonst ruht die Vergütung. Wir registrieren gemeinsam mit Ihnen.</p><a class="link-arrow" href="https://www.marktstammdatenregister.de" target="_blank" rel="noopener">marktstammdatenregister.de {ARROW}</a></div>
      <div class="card tilt reveal"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="#1d1d1f" stroke-width="2" stroke-linecap="round"><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/><circle cx="12" cy="12" r="4"/></svg></span><h3>Wärmepumpen-Anmeldung</h3><p>Auch Wärmepumpen sind steuerbare Verbrauchseinrichtungen nach § 14a EnWG und anmeldepflichtig. Wir melden Ihre Wärmepumpe beim Netzbetreiber an – und stimmen sie mit PV und Speicher ab.</p></div>
      <div class="card tilt reveal"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="#1d1d1f" stroke-width="2" stroke-linecap="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></span><h3>Solarversicherung</h3><p>Für unsere Kunden besteht ein Rahmenvertrag mit der Mannheimer Solarversicherung (Allgefahren: Hagel, Brand, Diebstahl, Überspannung, Ausfallkosten). Ein passendes Angebot legen wir der Angebotsmappe bei – wir vermitteln nicht, wir informieren.</p></div>
      <div class="card tilt reveal"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="#1d1d1f" stroke-width="2" stroke-linecap="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9z"/></svg></span><h3>Wartung &amp; Monitoring</h3><p>Sichtprüfung, Messung, Reinigung bei Bedarf, Überwachung der Erträge per SMA-Monitoring – damit die Anlage 20 Jahre und länger liefert. Auch für Anlagen, die wir nicht selbst gebaut haben.</p></div>
      <div class="card tilt reveal red"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="#ba0600" stroke-width="2" stroke-linecap="round"><path d="M13 2 3 14h9l-1 8 10-12h-9z"/></svg></span><h3>Steuern &amp; Vergütung</h3><p>Nullsteuersatz auf neue PV-Anlagen bleibt zunächst bestehen. Einspeisevergütung aktuell 7,78 ct/kWh (Feb.–Juli 2026) bei Überschusseinspeisung. Ab 1.1.2027 ändert sich vieles – siehe Zeitplan unten.</p><a class="link-arrow" href="ratgeber-eeg-2027.html">EEG 2027 verstehen {ARROW}</a></div>
    </div>
  </div>
</section>

<section class="sec" style="background:var(--bg-2)" id="zeitplan">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Planer</p><h2 class="h-l split">Schaffen wir es vor dem 1.1.2027?</h2><p class="lead">Wählen Sie, wann wir starten können – der Planer rechnet die Phasen bis zur Inbetriebnahme durch. Die Dauern sind Erfahrungswerte, die Netzbetreiber-Bearbeitung schwankt regional stark.</p></div>
    <div class="plan2">
      <div class="pick">
        <p class="lab" id="startLbl">Wann können wir starten?</p>
        <div class="starts" role="group" aria-labelledby="startLbl">
          <button type="button" data-w="0" aria-pressed="true"><b>Sofort</b><span>diese Woche</span></button>
          <button type="button" data-w="2" aria-pressed="false"><b>In 2 Wochen</b><span></span></button>
          <button type="button" data-w="4" aria-pressed="false"><b>In 1 Monat</b><span></span></button>
          <button type="button" data-w="8" aria-pressed="false"><b>In 2 Monaten</b><span></span></button>
          <button type="button" data-w="12" aria-pressed="false"><b>In 3 Monaten</b><span></span></button>
          <button type="button" data-w="20" aria-pressed="false"><b>Im neuen Jahr</b><span></span></button>
        </div>
        <div class="result" aria-live="polite"><p class="lab">Inbetriebnahme voraussichtlich</p><b class="date"></b><p class="verdict"></p><a class="btn btn-sun" href="kontakt.html?thema=beratung">Jetzt Termin sichern {ARROW}</a></div>
      </div>
      <ol class="phases" aria-label="Phasen bis zur Inbetriebnahme"></ol>
    </div>
    <p class="muted" style="font-size:13px;line-height:1.5;margin-top:16px;max-width:760px">Richtwerte: Beratung 1 Woche, Angebot &amp; Planung 2 Wochen, Netzbetreiber-Anmeldung ca. 6 Wochen, Montage 1 Woche, Zählersetzung &amp; Inbetriebnahme ca. 3 Wochen, danach Registrierung im Marktstammdatenregister innerhalb von 4 Wochen. Keine Zusage – Lieferzeiten und Netzbetreiber entscheiden mit.</p>
  </div>
</section>

<section class="sec" id="elektro">
  <div class="wrap">
    <div class="two">
      <div class="ph-img reveal">{img('k-zaehler', 'Zähler in einem Zählerschrank', 800, 600)}</div>
      <div><p class="eyebrow">Elektroarbeiten</p><h2 class="h-l split">Der Meisterbetrieb hinter der Solartechnik.</h2><p class="lead" style="margin-top:22px">SOTECH ist ein Elektromeisterbetrieb. Herr Eschweiler kümmert sich um Hausinstallationen in Alt- und Neubauten; Sat-Antennen und Türsprechanlagen stehen genauso auf dem Plan wie Zählerschrank-Modernisierung – die Voraussetzung für Speicher, Wallbox und Wärmepumpe.</p>
      <ul class="prose" style="margin-top:22px;padding-left:22px"><li class="reveal">Zählerschränke und Unterverteilungen erneuern</li><li class="reveal">Hausinstallation in Alt- und Neubau</li><li class="reveal">Sat-Antennen, Türsprechanlagen</li><li class="reveal">Ladesäulen und Wallboxen für Gewerbe</li></ul></div>
    </div>
  </div>
</section>

''' + cta_section('Fragen zur Anmeldung? Wir kennen die Netzbetreiber.', 'Regionale Verwurzelung heißt: Wir kennen die lokalen Gegebenheiten, das Wetter und die Netzbetreiber.')
pages.append(dict(file='service.html', title='Anmeldung, Wartung & Elektroservice für PV – Stolberg | SOTECH', desc='Netzbetreiber-Anmeldung, Marktstammdatenregister, Wärmepumpe, Solarversicherung, Wartung, Elektroarbeiten. Zeitplan: Inbetriebnahme vor dem 1.1.2027?', body=SV))

# ============================ ÜBER UNS ============================
REFS = [
 dict(ort='Stolberg', lat=50.7843, lon=6.2324, home=True, titel='SOTECH-Firmengelände, Gewerbegebiet Steinfurt', text='Büro, Lager und Schulungsraum in Stolberg – Am Birkenfeld 10. Auf den eigenen Dächern: Photovoltaik und Solarcarport, an dem seit 2012 täglich E-Autos geladen werden.', img='k-gelaende', alt='Luftaufnahme des SOTECH-Firmengeländes mit Solardächern', jahr='Standort seit 2011'),
 dict(ort='Stolberg', lat=50.762, lon=6.20, titel='Flachdach und Fassade, 29,97 kWp', text='162 Module ZG 185 Wp, Inbetriebnahme Dezember 2010. Flachdach- und vorgehängte Fassadenanlage mit PVI-Wechselrichtern.', img='r-zg30', alt='Flachdach- und Fassadenanlage in Stolberg', kwp='29,97', mod='162', jahr='12/2010'),
 dict(ort='Aachen', lat=50.776, lon=6.084, titel='Besichtigungsanlage im Mehrfamilienhaus', text='Bestandsumrüstung mit Batteriesystem (Tesla III bzw. SMA DC-System 5 × 3,28 kWh), Wallboxen und Wärmepumpe. Nach Terminabsprache mit Frau Gier zu besichtigen – am Demodach lassen sich verschiedene Befestigungssysteme vergleichen.', img='k-luftbild', alt='Luftbild einer Wohnsiedlung mit Photovoltaik-Dächern', jahr='Besichtigung möglich'),
 dict(ort='Aachen', lat=50.79, lon=6.11, titel='Dachanlage, 10,98 kWp', text='61 Module Yingli 180 Wp, Inbetriebnahme Mai 2009. Eine von mehreren Aachener Anlagen aus dem Jahr 2009 (u. a. 7,56 kWp mit 42 Modulen, März 2009).', img='r-haus-2', alt='Wohnhaus mit Photovoltaik auf dem Satteldach', kwp='10,98', mod='61', jahr='5/2009'),
 dict(ort='Walheim', lat=50.70, lon=6.13, titel='Dachanlage, 4,32 kWp', text='24 Module Yingli 180 Wp, Inbetriebnahme März 2009.', img='r-hpim0333', alt='Bungalow mit Solaranlage auf dem Dach', kwp='4,32', mod='24', jahr='3/2009'),
 dict(ort='Jülich', lat=50.92, lon=6.36, titel='Großanlage, 46,44 kWp', text='258 Module Yingli 180 Wp, Inbetriebnahme Juli 2009 – eine unserer größten Dachanlagen. Dazu in Jülich: 10,08 kWp mit 56 Modulen (Juni 2009).', img='r-yingli', alt='Große Dachanlage mit 258 Modulen', kwp='46,44', mod='258', jahr='7/2009'),
 dict(ort='Hürtgenwald', lat=50.71, lon=6.37, titel='Dachanlage, 6,3 kWp', text='35 Module Yingli 180 Wp, Inbetriebnahme Mai 2009.', img='r-hpim0575', alt='Einfamilienhaus mit Solarmodulen', kwp='6,3', mod='35', jahr='5/2009'),
 dict(ort='Grevenbroich', lat=51.09, lon=6.58, titel='Dachanlage, 7,92 kWp', text='44 Module Yingli 180 Wp, Inbetriebnahme Mai 2009.', img='r-hpim0581', alt='Ziegeldach mit Gaube und Photovoltaik', kwp='7,92', mod='44', jahr='5/2009'),
 dict(ort='Jüchen', lat=51.10, lon=6.50, titel='Dachanlage, 7,215 kWp', text='39 Module ZG 185 Wp, Inbetriebnahme September 2010.', img='r-hpim0634', alt='Rotes Ziegeldach mit Solarmodulen', kwp='7,215', mod='39', jahr='9/2010'),
 dict(ort='Herzogenrath', lat=50.87, lon=6.09, titel='Schule und Kohlscheider Kirche', text='Öffentliche Gebäude in Herzogenrath: Schuldach mit Flachdach-Aufständerung und die PV-Anlage der Kohlscheider Kirche.', img='k-schule', alt='Schulgebäude mit Solarmodulen auf dem Flachdach', jahr='Referenz'),
 dict(ort='Wuppertal', lat=51.26, lon=7.15, titel='Erich-Fried-Gesamtschule, 5 kWp', text='Netzgekoppeltes Solarkraftwerk des Fördervereins, seit 1994 – SOTECH lieferte die Anlage und übernahm die Bauleitung. Ca. 4.000 kWh im Jahr, rund 3 t CO₂-Einsparung, Anzeigedisplay im Foyer.', img=None, kwp='5', jahr='seit 1994'),
 dict(ort='Erkrath', lat=51.22, lon=6.91, titel='Reithalle', text='Wechselrichter-Installation an einer Reithalle – Beispiel für landwirtschaftliche und gewerbliche Dächer.', img='k-wr-halle', alt='Wechselrichter an einer Holzwand einer Reithalle', jahr='Referenz'),
 dict(ort='Siegburg', lat=50.80, lon=7.20, titel='Gewerbedach', text='Modulreihen auf einem großen Gewerbegebäude in Siegburg.', img='k-siegburg', alt='Großes Backsteingebäude mit Solaranlage', jahr='Referenz'),
]
UU = page_hero({}, 'k-gelaende', 'Luftaufnahme des SOTECH-Firmengeländes in Stolberg mit Solardächern', 'Über uns', 'Ein Familienbetrieb in Sachen Energiewende.', 'Während große Konzerne auf Masse und Standardisierung setzen, punkten wir mit Vertrauen, Menschlichkeit und einer langfristigen Perspektive. Bei SOTECH arbeitet die Sonne – seit 1988.', 'Unternehmen', w=1280, h=856, meta=[('Gegründet', '1988 in Düsseldorf'), ('Geschäftsführer', 'Dirk Gier, Elektromeister'), ('Auszeichnung', 'EUPD Installateur 2023 & 2024')]) + f'''
<section class="sec">
  <div class="wrap">
    <div class="two">
      <div><p class="eyebrow">Unser Fundament</p><h2 class="h-l split">Vertrauen, Nähe und Zuverlässigkeit.</h2>
        <div class="prose" style="margin-top:24px"><h3>Persönliche Verantwortung</h3><p>Der Chef steht oft noch selbst auf dem Dach oder berät am Küchentisch. Wir verkaufen kein anonymes Produkt, sondern eine Lösung, für die wir mit unserem Namen bürgen.</p><h3>Regionale Verwurzelung</h3><p>Wir kennen die lokalen Gegebenheiten, das Wetter und die Netzbetreiber. Ein Familienbetrieb ist kein „Ghost“ nach der Installation – man findet uns auch nach 37 Jahren noch am selben Standort.</p><h3>Generationendenken</h3><p>Wir denken nicht in Quartalszahlen, sondern an die nächsten Generationen. Viele Monteure und Elektriker sind seit ihrer Ausbildung im Betrieb – das sorgt für eingespielte Teams und Expertise über die reine Montage hinaus. Wir gehören zu den wenigen Betrieben, die heute noch ausbilden.</p></div></div>
      <div><div class="ph-img reveal" style="aspect-ratio:1">{img('k-team', 'Das SOTECH-Team in roten Shirts vor einem Solarmodul', 900, 881)}</div>
        <blockquote class="prose" style="margin-top:26px"><p style="margin:0">„Ein Familienbetrieb für Solartechnik ist der Partner, der die Energiewende nahbar macht – durch handwerkliche Präzision, persönliche Beratung und das Versprechen, auch dann noch da zu sein, wenn die Sonne mal Pause macht.“</p></blockquote></div>
    </div>
  </div>
</section>

<section class="sec" style="background:var(--bg-2)" id="team">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Team</p><h2 class="h-l split">Die Menschen hinter SOTECH.</h2></div>
    <div class="team">
      <div class="member reveal"><div class="pic">{img('p-gier', 'Dirk Gier', 640, 640, sizes='(max-width: 600px) 50vw, 25vw')}</div><div class="t"><span class="role">Geschäftsführer · Elektromeister</span><h3>Dirk Gier</h3><p>Kommt zu Ihnen und berät kostenlos über umweltfreundlichen Solarstrom. Ein Mann vom Fach.</p></div></div>
      <div class="member reveal"><div class="pic">{img('p-gabi', 'Gabi Gier', 640, 640, sizes='(max-width: 600px) 50vw, 25vw')}</div><div class="t"><span class="role">Beratung · Förderung</span><h3>Gabi Gier</h3><p>Die rechte Hand des Chefs, seit Jahren im Betrieb. Berät umfassend zu Fördermöglichkeiten und Photovoltaik – und vergibt Termine für die Besichtigungsanlage.</p></div></div>
      <div class="member reveal"><div class="pic">{img('p-christian', 'Christian Gier', 464, 640, sizes='(max-width: 600px) 50vw, 25vw')}</div><div class="t"><span class="role">Elektroniker für Automatisierungstechnik</span><h3>Christian Gier</h3><p>Geselle, steckt in der Meisterausbildung im Elektrohandwerk – die Grundlage, um den Betrieb einmal zu übernehmen.</p></div></div>
      <div class="member reveal"><div class="pic">{img('p-stephanie', 'Stephanie Hackner', 455, 640, sizes='(max-width: 600px) 50vw, 25vw')}</div><div class="t"><span class="role">Elektrotechnikermeisterin</span><h3>Stephanie Hackner, geb. Gier</h3><p>Bestandene Meisterprüfung im Elektrotechniker-Handwerk – Fleiß und fachliches Können in der nächsten Generation.</p></div></div>
      <div class="member reveal"><div class="pic">{img('p-eschweiler', 'Michael Eschweiler', 500, 640, sizes='(max-width: 600px) 50vw, 25vw')}</div><div class="t"><span class="role">Elektromonteur</span><h3>Michael Eschweiler</h3><p>Kümmert sich um Hausinstallationen in Alt- und Neubauten; Sat-Antennen und Türsprechanlagen gehören ebenso zu seinem Tag.</p></div></div>
      <div class="member reveal"><div class="pic">{img('p-rene', 'René Brieger', 592, 640, sizes='(max-width: 600px) 50vw, 25vw')}</div><div class="t"><span class="role">Elektroniker für Energie- und Gebäudetechnik</span><h3>René Brieger</h3><p>Begann 2014 seine Ausbildung bei SOTECH – plant und installiert elektrotechnische Anlagen von Gebäuden.</p></div></div>
      <div class="member reveal"><div class="pic">{img('p-florian', 'Florian Ervens', 480, 640, sizes='(max-width: 600px) 50vw, 25vw')}</div><div class="t"><span class="role">Montagehelfer</span><h3>Florian Ervens</h3><p>Unterstützt bei den Dachmontagen und der Elektrik nach Anweisung.</p></div></div>
      <div class="member reveal"><div class="pic">{img('p-abdul', 'Abdull Haj Bakri', 430, 640, sizes='(max-width: 600px) 50vw, 25vw')}</div><div class="t"><span class="role">Auszubildender ab August 2026</span><h3>Abdull Haj Bakri</h3><p>Beginnt am 1.8.2026 seine Ausbildung. Wir wünschen viel Spaß und Erfolg.</p></div></div>
    </div>
    <div class="kbox" style="margin-top:14px;display:flex;flex-wrap:wrap;gap:20px;align-items:center;justify-content:space-between"><div><h3 style="margin-bottom:6px">Schülerpraktikum &amp; Ausbildung</h3><p>Ein Schülerpraktikum ist eine hervorragende Möglichkeit, den Berufswunsch auszutesten. Wir bilden aus: Elektroniker/in für Energie- und Gebäudetechnik.</p></div><a class="btn btn-primary" href="kontakt.html?thema=praktikum">Praktikum anfragen {ARROW}</a></div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Geschichte</p><h2 class="h-l split">Solarpionier seit 1988.</h2></div>
    <ul class="hist">
      <li class="reveal"><b>1988</b><span>Gründung der SOTECH in Düsseldorf als Ingenieurbüro.</span></li>
      <li class="reveal"><b>1994</b><span>Solarkraftwerk an der Erich-Fried-Gesamtschule Wuppertal – Lieferung und Bauleitung.</span></li>
      <li class="reveal"><b>1995</b><span>Umwandlung in eine GmbH, Niederlassung in Aachen.</span></li>
      <li class="reveal"><b>2000</b><span>Zwei Jahre Tochtergesellschaft der Shell Solar GmbH, Sitz Aachen.</span></li>
      <li class="reveal"><b>2008</b><span>Gründung der SOTECH Vertrieb GmbH (Großhandel und Versand).</span></li>
      <li class="reveal"><b>2011</b><span>Neues Firmengebäude mit Schulungsraum und Lager in Stolberg, Am Birkenfeld.</span></li>
      <li class="reveal"><b>2012</b><span>Das erste Elektroauto (Opel Ampera) lädt täglich unter dem Solarcarport.</span></li>
      <li class="reveal"><b>2013</b><span>25-jähriges Bestehen – gefeiert mit 120 Personen, darunter viele Altkunden.</span></li>
      <li class="reveal"><b>2016</b><span>SOTECH montiert den ersten Tesla-Speicher in Aachen.</span></li>
      <li class="reveal"><b>2018</b><span>Montage diverser Ladesäulen; der Betrieb fährt inzwischen drei E-Fahrzeuge.</span></li>
      <li class="reveal"><b>2023/24</b><span>EUPD Research: SOTECH GmbH ist „Ausgezeichneter Installateur Deutschland“.</span></li>
      <li class="reveal"><b>2026</b><span>38 Jahre, rund 1.500 Anlagen, 7.800 kWp – und die nächste Generation in der Meisterausbildung.</span></li>
    </ul>
  </div>
</section>

<section class="sec" style="background:var(--bg-2)">
  <div class="wrap">
    <div class="two">
      <div class="ph-img reveal" style="aspect-ratio:auto;background:none;max-width:300px">{img('k-siegel', 'EUPD Research Siegel: Ausgezeichneter Installateur Deutschland 2024', 600, 733, sizes='300px')}</div>
      <div><p class="eyebrow">Auszeichnung</p><h2 class="h-l split">Ausgezeichneter Installateur Deutschland 2023 und 2024.</h2><p class="lead" style="margin-top:22px">Das Marktforschungsunternehmen EUPD Research zeichnet Installateure aus, die von Kunden und Herstellern besonders gut bewertet werden. Dazu 5/5 Sterne bei Google – wir geben unser Bestes.</p><p style="margin-top:22px"><a class="link-arrow" href="https://www.google.com/search?q=SOTECH+GmbH+Rezensionen" target="_blank" rel="noopener">Google-Bewertungen ansehen {ARROW}</a></p></div>
    </div>
  </div>
</section>
''' + cta_section('Lernen Sie uns kennen.', 'Am besten bei Ihnen zu Hause – oder an unserer Besichtigungsanlage in Aachen.')
pages.append(dict(file='ueber-uns.html', title='Über SOTECH – Familienbetrieb für Solartechnik seit 1988, Stolberg', desc='Elektromeisterbetrieb aus Stolberg: Team, Geschichte seit 1988, EUPD-Auszeichnung 2023 und 2024. Persönlich, regional, ausbildend.', body=UU))

RF = page_hero({}, 'k-luftbild', 'Luftbild einer Wohnsiedlung mit Photovoltaik-Dächern', 'Referenzen', 'Rund 1.500 Anlagen in 38 Jahren.', 'Von der 4-kWp-Dachanlage bis zur 46-kWp-Großanlage, von Aachen bis Wuppertal – eine Auswahl unserer Arbeit. Und eine Anlage, die Sie besichtigen können.', 'Referenzen', w=1204, h=652, meta=[('Anlagen', 'ca. 1.500'), ('Leistung', '7.800 kWp'), ('Besichtigung', 'Aachen, nach Absprache')]) + f'''
<section class="sec dark" id="karte">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Karte</p><h2 class="h-l split">Wo wir gebaut haben.</h2><p class="lead">Punkt anklicken oder Ort wählen. Die vollständige Referenzliste 1988–2023 (PDF) zeigen wir Ihnen gern beim Beratungstermin – zusammen mit der Referenzbildermappe.</p></div>
    <div class="rmap">
      <div class="map"><svg viewBox="0 0 800 560" role="img" aria-label="Karte der Region mit Referenzanlagen"></svg><div class="list" role="group" aria-label="Referenzorte"></div></div>
      <div class="info"><div class="pic"></div><div class="t"><h3></h3><p></p><div class="kv"></div></div></div>
    </div>
    <script type="application/json" id="refData">{json.dumps(REFS, ensure_ascii=False)}</script>
  </div>
</section>

<section class="sec" style="background:var(--bg-2)">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Bilder</p><h2 class="h-l split">Sattel, Pult, Flach – und das steile Pfannendach.</h2><p class="lead">Wir montieren auf allen gängigen Dachformen. Bei sehr flachen Ziegeldächern (unter 22°) beraten wir ehrlich: Dort ist das Risiko für Undichtigkeiten nach dem Ausklinken der Ziegel erhöht.</p></div>
    <div class="gal">
      <figure class="wide">{img('r-zg30', 'Flachdach- und Fassadenanlage in Stolberg mit 29,97 kWp', 1204, 1065, sizes='(max-width: 820px) 100vw, 50vw')}<figcaption>Stolberg · Flachdach + Fassade · 29,97 kWp</figcaption></figure>
      <figure>{img('r-baur', 'Satteldach mit Photovoltaik-Modulen', 1204, 903, sizes='(max-width: 820px) 50vw, 25vw')}<figcaption>Satteldach</figcaption></figure>
      <figure>{img('r-carport', 'Glas-Glas-Module als Carportdach von unten', 796, 600, sizes='(max-width: 820px) 50vw, 25vw')}<figcaption>Solarcarport, Glas-Glas</figcaption></figure>
      <figure>{img('r-hpim0597', 'Flachdach-Aufständerung auf einem Bürogebäude', 796, 600, sizes='(max-width: 820px) 50vw, 25vw')}<figcaption>Flachdach, aufgeständert</figcaption></figure>
      <figure>{img('r-hpim0581', 'Photovoltaik auf einem roten Ziegeldach mit Gaube', 796, 600, sizes='(max-width: 820px) 50vw, 25vw')}<figcaption>Ziegeldach mit Gaube</figcaption></figure>
      <figure class="wide">{img('r-yingli', 'Große Dachanlage in Jülich mit 258 Modulen', 1204, 903, sizes='(max-width: 820px) 100vw, 50vw')}<figcaption>Jülich · 46,44 kWp · 258 Module</figcaption></figure>
    </div>
    <p class="muted" style="margin-top:18px;font-size:14px">Alle Fotos: Kundenanlagen von SOTECH.</p>
  </div>
</section>


<section class="sec">
  <div class="wrap">
    <div class="two">
      <div class="ph-img reveal">{img('k-gelaende', 'SOTECH-Firmengelände mit Solardächern und Solarcarport', 1280, 856)}</div>
      <div><p class="eyebrow">Besichtigungsanlage</p><h2 class="h-l split">Anfassen statt Prospekt.</h2><p class="lead" style="margin-top:22px">In Aachen können Sie nach Terminabsprache eine Anlage im Mehrfamilienhaus besichtigen: Batteriesystem (Tesla III bzw. SMA DC-System 5 × 3,28 kWh), Wallboxen und Wärmepumpe im laufenden Betrieb. Am Demodach lassen sich verschiedene Befestigungssysteme vergleichen.</p><p style="margin-top:26px"><a class="btn btn-primary" href="kontakt.html?thema=besichtigung">Besichtigung vereinbaren {ARROW}</a></p></div>
    </div>
  </div>
</section>
''' + cta_section('Ihr Dach könnte das nächste sein.', 'Kostenlose Beratung vor Ort – oder an der Besichtigungsanlage in Aachen.')
pages.append(dict(file='referenzen.html', title='Referenzen – 1.500 PV-Anlagen in Aachen, Stolberg & Region | SOTECH', desc='Referenzanlagen auf der Karte: Stolberg, Aachen, Jülich, Grevenbroich, Wuppertal. Fotos von Sattel-, Pult- und Flachdach. Besichtigungsanlage in Aachen.', body=RF))

# ============================ RATGEBER ============================
ARTS = [
 dict(file='ratgeber-eeg-2027.html', tag='Gesetz', img='u-abend', alt='Sonnenuntergang über Dächern', title='EEG 2027: Warum Sie vor dem 1.1.2027 ans Netz gehen sollten', short='Die feste Einspeisevergütung wird für Neuanlagen abgeschafft. Was Übergangsvergütung, Direktvermarktung und Nullvergütung bedeuten.', mtitle='EEG 2027: PV-Anlage vor dem 1.1.2027 errichten | SOTECH Ratgeber', mdesc='Feste Einspeisevergütung endet für Neuanlagen ab 2027. Übergangszahlung, Direktvermarktung, Smart Meter, Nullvergütung – was das für Ihre PV-Anlage heißt.', w=1800, h=1170, body='''
<p>Eine Novelle des Erneuerbare-Energien-Gesetzes (EEG) wurde im Kabinett beschlossen. Sie soll zum 1. Januar 2027 in Kraft treten – bis dahin gilt das EEG 2023. Unser Fazit vorweg: <strong>Schnelles Handeln ist gefordert. Errichten Sie Ihre PV-Anlage unbedingt vor dem 1.1.2027.</strong></p>
<h2>Was heute gilt (EEG 2023)</h2>
<p>Besitzer von Photovoltaikanlagen erhalten für jede Kilowattstunde Sonnenstrom, die sie ins öffentliche Netz einspeisen, einen festen Betrag. Die Höhe richtet sich nach dem Zeitpunkt der Inbetriebnahme und dem Einspeisemodell – Teileinspeisung (Solarstrom wird selbst verbraucht, nur der Überschuss geht ins Netz) oder Volleinspeisung. Die Vergütung wird 20 Jahre ab Inbetriebnahme und Eintragung im Marktstammdatenregister gewährt. Aktuell (Februar bis Juli 2026) beträgt sie für Überschusseinspeisung bei Neuanlagen ca. 7,78 Cent/kWh.</p>
<p>Für Anlagen, die ab Februar 2025 in Betrieb gingen, gilt die sogenannte <strong>Nullvergütung</strong> (§ 51 EEG): Bei negativem Börsenpreis wird die Einspeisung vorübergehend mit 0 ct/kWh vergütet. Die vergütungsfreie Zeit wird aber an die Förderdauer angehängt – dem Betreiber geht kein Geld verloren.</p>
<h2>Was sich ab 2027 ändert</h2>
<ul>
<li><strong>Die garantierte Einspeisevergütung für Dachanlagen wird abgeschafft.</strong> Anlagen, die zwischen 2027 und 2029 ans Netz gehen, erhalten eine abgesenkte Übergangszahlung für 3 Jahre, bevor sie auf Direktvermarktung umstellen müssen.</li>
<li>Der Anspruch wird schrittweise eingeschränkt: 2027 für Neuanlagen unter 50 kW, 2028 unter 25 kW, 2029 nur noch unter 7 kW. Die Pauschale sinkt ab August 2027 halbjährlich.</li>
<li>Beispiel: Für eine 10-kWp-Anlage, die Anfang 2027 in Betrieb geht, gibt es 5,20 Cent/kWh (Basiswert 6,20 Cent minus 1,0 Cent Abschlag) bei Teileinspeisung – maximal 50 % der Anlagenleistung, wenn kein Speicher vorhanden ist.</li>
<li><strong>Volleinspeisung ist ab 2027 nicht mehr möglich.</strong> Betreiber müssen ihren Sonnenstrom an der Strombörse verkaufen – über einen Direktvermarkter. Statt einer festen Pauschale gibt es nur noch einen variablen Börsenpreis.</li>
<li>Die Übergangsvergütung gibt es nur bis 2030. Danach müssen alle Anlagen automatisch in die Direktvermarktung.</li>
<li>Für die Direktvermarktung gibt es einen Bonus von 1,5 Cent/kWh, maximal 48 Monate – aber nur in Monaten, in denen auch eingespeist wird (§ 50c EEG 2027).</li>
</ul>
<h2>Das Problem: Smart Meter und Steuerbox</h2>
<p>Für die Direktvermarktung sind ein Smart Meter mit Smart Meter Gateway sowie eine Steuerbox nötig. Vielerorts dauert es sehr lange, bis diese intelligenten Messsysteme eingebaut werden – die EU hat Deutschland wegen des langsamen Rollouts bereits im Blick. Kommen die Messstellenbetreiber nicht hinterher, bekommen Betreiber kein Geld: Die „Ausfallvergütung“ aus dem alten EEG greift ab 2027 nicht mehr.</p>
<div class="note"><b>Achtung:</b> Eine „moderne Messeinrichtung“ ist nicht automatisch ein „intelligentes Messsystem“. Letzteres liegt erst vor, wenn auch ein Smart Meter Gateway eingebaut ist und die Messeinrichtung mit dem Netzbetreiber kommunizieren kann.</div>
<h2>Was bleibt, was hilft</h2>
<p>Die Nullvergütung bei negativen Preisen bleibt bestehen; die unvergütete Zeit wird angerechnet. Die Mehrwertsteuerbefreiung für neue PV-Anlagen bleibt zunächst ebenfalls bestehen.</p>
<p>Die wichtigste Voraussetzung für Wirtschaftlichkeit ist ein möglichst hoher <strong>Eigenverbrauch</strong>. Vorteilhaft ist deshalb die Kombination der PV-Anlage mit steuerbaren Verbrauchern (Wärmepumpe, E-Auto), einem Batteriespeicher und einem modernen Energiemanagement. Alternativ ist die Nulleinspeisung als künftiger Regelfall vorgesehen – hier lohnen sich Direktverbrauch und Speicherladung weiterhin.</p>
<blockquote>Kleinere PV-Anlagen bis 25 kW verlieren ab dem Inbetriebnahmedatum 1.1.2027 die garantierte Einspeisevergütung. Wer bis dahin in Betrieb geht, sichert sich 20 Jahre feste Vergütung.</blockquote>
<p><a href="service.html#zeitplan">Zum Zeitplan: Schaffen wir es vor dem 1.1.2027?</a></p>
'''),
 dict(file='ratgeber-wallbox-anmeldung.html', tag='Wallbox', img='k-wallbox-4', alt='Wallbox mit Ladekabel in einer Garage', title='Wallbox anmelden: Wann ist es Pflicht – und was heißt § 14a EnWG?', short='CEE-Dose oder Wallbox, 4,2 kW, 11 kW, 22 kW: Wann der Netzbetreiber informiert werden muss und warum ein einfacher Kraftstromstecker oft nicht reicht.', mtitle='Wallbox anmelden: Pflicht ab 4,2 kW, § 14a EnWG | SOTECH', mdesc='Wann muss eine Wallbox beim Netzbetreiber angemeldet werden? Grenzen 4,2 kW und 11 kW, Steuerbarkeit nach § 14a EnWG, Anmeldung über das Portal.', w=768, h=576, body='''
<p>Sie haben sich für ein Elektroauto entschieden? Dann brauchen Sie einen sicheren Ladepunkt zu Hause. Elektroautos dürfen aus Sicherheitsgründen nicht dauerhaft an der haushaltsüblichen Steckdose geladen werden. Und: Fast jeder Ladepunkt ist anmeldepflichtig.</p>
<h2>CEE-Steckdose – anmeldepflichtig oder nicht?</h2>
<p>Eine reine CEE-Steckdose (Kraftstrom/Starkstrom) muss an sich nicht beim Netzbetreiber angemeldet werden, wenn sie als normale Steckdose dient. Nutzen Sie die CEE-Leitung jedoch dauerhaft als Ladeeinrichtung für ein Elektroauto – zum Beispiel mit einer mobilen Wallbox oder einem mobilen Ladegerät ab 3,7 kW / 4,2 kW –, gilt eine gesetzliche Anmeldepflicht.</p>
<h2>Wann eine Anmeldung Pflicht ist</h2>
<table><tr><th>Situation</th><th>Regel</th></tr>
<tr><td>Ladeleistung über 4,2 kW</td><td>Jede feste oder mobile Ladeeinrichtung, die mehr als 4,2 kW zieht, muss dem Netzbetreiber gemeldet werden.</td></tr>
<tr><td>CEE-Dose fürs Auto</td><td>Wird eine CEE-Dose extra zum Laden installiert oder genutzt, stuft das Gesetz sie als Ladeeinrichtung ein.</td></tr>
<tr><td>Leistung bis 11 kW</td><td>Die Anmeldung ist kostenlos, und der Netzbetreiber darf den Anschluss nicht einfach ablehnen.</td></tr>
<tr><td>Leistung über 11 kW (z. B. 22 kW)</td><td>Sie benötigen vorab eine Genehmigung vom Netzbetreiber.</td></tr></table>
<h2>Steuerbarkeit nach § 14a EnWG</h2>
<p>Neue steuerbare Verbrauchseinrichtungen – wie moderne Wallboxen und Wärmepumpen – unterliegen Vorgaben zur Dimmbarkeit durch den Netzbetreiber. Ein einfacher CEE-Stecker kann diese technischen Anforderungen oft nicht erfüllen: <strong>Es muss eine schaltbare Steckdose mit Steuerschütz sein.</strong> Und alle Wallboxen sind über das Inbetriebsetzungsportal anzumelden.</p>
<h2>Wie die Anmeldung läuft</h2>
<p>Die Meldung erfolgt unkompliziert über die Online-Portale der regionalen Netzbetreiber – oft direkt durch den installierenden Elektrofachbetrieb, also durch uns. Den zuständigen Netzbetreiber finden Sie auf Ihrer Stromrechnung oder direkt auf Ihrem Stromzähler.</p>
<div class="note"><b>Unser Standard:</b> Zappy Wallbox 11 kW – steuerbar nach § 14a, kombinierbar mit PV-Überschussladen. Vor-Ort-Prüfung, Montage und Anmeldung aus einer Hand. <a href="wallbox.html#checkliste">Zur Checkliste: Ist Ihr Hausanschluss bereit?</a></div>
'''),
 dict(file='ratgeber-notstrom-speicher.html', tag='Speicher', img='k-speicher', alt='SMA-Speichersystem im Keller', title='Notstrom: Läuft mein Speicher bei Stromausfall weiter?', short='Notstromsteckdose oder Ersatzstrom? Warum sich der Wechselrichter bei Netzausfall abschaltet, wie ein Inselnetz entsteht und was Sie im Winter beachten sollten.', mtitle='Notstrom & Ersatzstrom mit PV-Speicher – so geht’s | SOTECH', mdesc='Läuft der SMA-Speicher bei Stromausfall weiter? Notstromsteckdose vs. Ersatzstrom, galvanische Trennung, Inselnetz, Winterreserve – erklärt vom Fachbetrieb.', w=1800, h=1350, body='''
<p>Eine der häufigsten Fragen bei der Speicherberatung: „Und wenn der Strom ausfällt – habe ich dann Licht?“ Die Antwort hängt davon ab, wie Ihr System ausgerüstet ist.</p>
<h2>Fall 1: Notstromsteckdose</h2>
<p>Beim SMA Sunny Boy Wechselrichter bis 4,6 kW SE gibt es eine Notstromsteckdose. Das ist eine kurzfristige Lösung: Über eine separat mit 16 A abgesicherte Steckdose kann Strom bezogen werden, sofern ein Akku von SMA mit mindestens 3,28 kWh vorhanden ist und noch mindestens 20 % Restkapazität enthält.</p>
<h2>Fall 2: Ersatzstrom mit dem SMA DC-Speichersystem</h2>
<p>Beim SMA DC-Speichersystem muss der Wechselrichter dreiphasig sein, da der Speicher ebenfalls dreiphasig ist. Auch hier sollte der Speicher mindestens 20 % Restkapazität enthalten. Im Zählerschrank werden dann auf einer Phase bestimmte Stromkreise mit definierten Verbrauchern angeklemmt – zum Beispiel Kühlschrank, Heizungssteuerung, Licht und Router.</p>
<div class="note"><b>Tipp für den Winter:</b> Begrenzen Sie die Entladung des Akkus auf ca. 50 %, um im Falle eines Stromausfalls noch Reserven zu haben. In jedem Fall wird der Akku auch bei Stromausfall weiter geladen, wenn genügend Sonnenlicht auf die PV-Anlage fällt.</div>
<h2>Warum schaltet der Wechselrichter überhaupt ab?</h2>
<p><strong>Gesetzliche Vorschrift:</strong> Wechselrichter müssen sich nach Norm (VDE-AR-N 4105) bei einem Netzausfall innerhalb von Millisekunden automatisch vom öffentlichen Netz trennen – damit kein Strom in ein Netz zurückgespeist wird, an dem gerade Monteure arbeiten.</p>
<p><strong>Fehlende Frequenz- und Taktvorgabe:</strong> Ein klassischer Wechselrichter produziert von sich aus keinen eigenständigen Stromtakt, sondern „hängt“ sich an das öffentliche Netz an. Er nutzt die 50 Hz des Netzes als Taktgeber. Fällt das Netz weg, fehlt ihm die Orientierung – er schaltet sich aus Sicherheitsgründen ab.</p>
<h2>Was passiert dann mit dem Strom im Haus?</h2>
<p>Obwohl der Speicher nichts mehr nach außen abgeben darf, kann er das eigene Haus weiterversorgen – vorausgesetzt, das System ist für Ersatzstrom ausgerüstet:</p>
<ol>
<li><strong>Galvanische Trennung:</strong> Eine automatische Umschalteinrichtung (oder eine im Wechselrichter integrierte Trennung) kappt die Verbindung zum öffentlichen Netz vollständig.</li>
<li><strong>Inselnetz-Aufbau:</strong> Erst wenn das Haus zu 100 % isoliert ist, übernimmt der SMA-Wechselrichter selbst die Taktung (50 Hz / 230 V bzw. 400 V).</li>
<li><strong>Eigenversorgung:</strong> DC-Speicher und PV-Module versorgen nun ausschließlich die Verbraucher im eigenen Haushalt.</li>
</ol>
<p>Bei einem Stromausfall verhält sich ein SMA-Hybridsystem (Sunny Tripower Smart Energy oder Sunny Boy Smart Energy) also völlig anders als im Normalbetrieb – und genau das ist der Sinn. <a href="speicher.html">Mehr zu Speichern und Wallboxen</a></p>
'''),
]
RG = f'''
<section class="ph short">
  {img('u-regenbogen', 'Regenbogen über einem Ziegeldach mit Solarmodulen', 1800, 1200, lazy=False, sizes='100vw')}
  <nav class="crumb" aria-label="Brotkrumen"><a href="index.html">Start</a>{CHEV}<span>Ratgeber</span></nav>
  <div class="wrap"><p class="eyebrow">Wissen</p><h1 class="split">Ratgeber.</h1><p class="lead">Aus 38 Jahren Praxis: Gesetz, Technik und Anmeldung – verständlich erklärt.</p></div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="posts">{''.join(f'<a class="post tilt reveal" href="{a["file"]}"><div class="pic">{img(a["img"], a["alt"], a["w"], a["h"], sizes="(max-width: 900px) 100vw, 33vw")}</div><div class="t"><span class="tag">{a["tag"]}</span><h3>{a["title"]}</h3><p>{a["short"]}</p><span class="link-arrow">Lesen {ARROW}</span></div></a>' for a in ARTS)}</div>
    <div class="kbox" style="margin-top:40px"><h3>Weitere Themen auf Anfrage</h3><p>Dachformen und Energieerträge, Dachneigung unter 22°, Umsatzsteuer bei PV, Solarversicherung, Brandschutz für PV-Anlagen, Aufbau einer netzgekoppelten Anlage – fragen Sie uns, wir erklären es gern persönlich. <a class="link-arrow" href="faq.html">Häufige Fragen {ARROW}</a></p></div>
  </div>
</section>
''' + cta_section('Lieber persönlich erklärt?', 'Rufen Sie an oder vereinbaren Sie eine kostenlose Beratung.')
pages.append(dict(file='ratgeber.html', title='Ratgeber Photovoltaik, Speicher & Wallbox | SOTECH Stolberg', desc='EEG 2027, Wallbox-Anmeldung, Notstrom mit Speicher – Ratgeber aus 38 Jahren Praxis des Familienbetriebs SOTECH aus Stolberg bei Aachen.', body=RG))
for a in ARTS:
    body = f'''
<section class="art-head"><div class="wrap"><nav class="crumb" style="position:static;color:var(--ink-2);margin-bottom:10px" aria-label="Brotkrumen"><a href="index.html">Start</a>{CHEV}<a href="ratgeber.html">Ratgeber</a>{CHEV}<span>{a['tag']}</span></nav><p class="eyebrow">{a['tag']}</p><h1 class="split">{a['title']}</h1><div class="meta"><span>SOTECH GmbH</span><span>Stand: September 2026</span></div></div></section>
<section><div class="wrap"><div class="art-img">{img(a['img'], a['alt'], a['w'], a['h'], lazy=False, sizes='(max-width: 1240px) 100vw, 1200px')}</div><div class="prose">{a['body']}</div>
<p style="margin-top:40px"><a class="link-arrow" href="ratgeber.html">Alle Ratgeber-Artikel {ARROW}</a></p></div></section>
''' + cta_section('Fragen dazu? Wir antworten persönlich.', 'Kostenlose Beratung durch den Elektromeister – vor Ort oder am Telefon.')
    pages.append(dict(file=a['file'], title=a['mtitle'], desc=a['mdesc'], body=body, article=True, parent='ratgeber.html', ld={"@context": "https://schema.org", "@type": "Article", "headline": a['title'], "description": a['mdesc'], "image": DOMAIN + '/img/' + a['img'] + '.webp', "datePublished": TODAY, "dateModified": TODAY, "author": {"@type": "Organization", "name": "SOTECH GmbH"}, "publisher": {"@type": "Organization", "name": "SOTECH GmbH", "logo": {"@type": "ImageObject", "url": DOMAIN + "/img/logo.svg"}}, "mainEntityOfPage": DOMAIN + '/' + a['file']}))

# ============================ FAQ ============================
FAQS = [
 ('Kostet die Beratung oder das Angebot etwas?', 'Nein. Angebote gibt es bei uns noch kostenlos – das nennt man Service im Familienbetrieb. Herr Gier kommt zu Ihnen, berät kostenlos und unverbindlich. Vergleichsangebote einzuholen empfehlen wir ausdrücklich, damit Sie Preise, Komponenten und Leistungen zuverlässig vergleichen können.'),
 ('In welchem Gebiet arbeitet SOTECH?', 'Wir errichten und planen PV-Anlagen, Wallboxen und Speicher sowie die Anmeldung von Wärmepumpen im Umkreis von zirka 50 km um Aachen und Stolberg – also in der Städteregion Aachen, im Kreis Düren und im Kreis Heinsberg.'),
 ('Was brauchen Sie von mir für ein Angebot?', 'Standort (PLZ, Ort, Straße), jährlicher Stromverbrauch in kWh, Dachart und Ausrichtung, Eindeckung (Pfannen, Schiefer, Trapezblech), gewünschte Komponenten (PV, Speicher, Wallbox – bei der Wallbox die ungefähre Kabelstrecke vom Zählerschrank) und der geplante Zeitraum. Sehr hilfreich: Fotos vom offenen Zählerschrank aus 1,5 m Entfernung und von den Dachflächen.'),
 ('Welche Komponenten verbauen Sie?', 'Solarmodule von Heckert Solar (deutscher Hersteller aus Chemnitz, ZEUS-Serie, auch Full Black), Wechselrichter und Speicher von SMA, Montagesysteme TRIC von Wagner Solar (TÜV-zertifiziert, bauaufsichtliche Zulassung) sowie Zappy Wallboxen mit 11 kW. Auf Wunsch auch Tesla-Speicher.'),
 ('Läuft mein Speicher bei Stromausfall weiter?', 'Das hängt vom System ab. SMA Sunny Boy bis 4,6 kW SE hat eine Notstromsteckdose (16 A, separat abgesichert) – sofern ein SMA-Akku ab 3,28 kWh mit mindestens 20 % Rest vorhanden ist. Das SMA DC-Speichersystem kann mit dreiphasigem Wechselrichter echten Ersatzstrom für definierte Stromkreise liefern. Details im Ratgeber „Notstrom“.'),
 ('Muss ich meine Wallbox anmelden?', 'Ja. Jede Ladeeinrichtung über 4,2 kW muss dem Netzbetreiber gemeldet werden – auch eine CEE-Dose, die zum Laden genutzt wird. Bis 11 kW ist die Anmeldung kostenlos und darf nicht abgelehnt werden; über 11 kW braucht es vorab eine Genehmigung. Wir übernehmen die Anmeldung über das Inbetriebsetzungsportal.'),
 ('Kann ich mein E-Auto an der Kraftstromdose laden?', 'Dauerhaft nur mit Einschränkungen: Neue steuerbare Verbrauchseinrichtungen müssen nach § 14a EnWG vom Netzbetreiber dimmbar sein. Ein einfacher CEE-Stecker erfüllt das oft nicht – es muss eine schaltbare Steckdose mit Steuerschütz sein. Sicherer und komfortabler ist eine Wallbox mit 11 kW.'),
 ('Wie hoch ist die Einspeisevergütung aktuell?', 'Für Überschusseinspeisung bei Neuanlagen ca. 7,78 Cent/kWh (Stand Februar bis Juli 2026), garantiert für 20 Jahre. Die Hauptrentabilität entsteht aber durch Eigenverbrauch: Teurer Netzstrom (ca. 30–40 Cent/kWh) wird durch kostenlosen Solarstrom ersetzt.'),
 ('Was ändert sich ab 2027?', 'Die feste Einspeisevergütung wird für Neuanlagen zum 1.1.2027 abgeschafft. Es gibt dann nur noch eine abgesenkte Übergangszahlung für 3 Jahre, Volleinspeisung entfällt, später ist Direktvermarktung mit Smart Meter Pflicht. Deshalb: vor dem 1.1.2027 in Betrieb gehen. Alles Weitere im Ratgeber „EEG 2027“.'),
 ('Muss ich Umsatzsteuer auf die Anlage zahlen?', 'Die Mehrwertsteuerbefreiung (Nullsteuersatz) für neue PV-Anlagen bleibt nach aktuellem Stand zunächst bestehen. Steuerliche Details klären Sie bitte mit Ihrem Steuerberater – wir informieren, beraten aber nicht steuerlich.'),
 ('Ist mein Dach geeignet, wenn es sehr flach ist?', 'Bei Ziegeldächern mit sehr geringer Neigung (z. B. 10–12°) ist das Risiko für Undichtigkeiten nach der Montage erhöht, weil Ziegel für die Dachhaken ausgeklinkt werden müssen und Wasser langsamer abfließt. Die Regeldachneigung klassischer Ziegel liegt bei 22–30°. Wir beraten ehrlich und finden Alternativen – etwa Aufständerung oder andere Befestigungssysteme.'),
 ('Brauche ich eine Solarversicherung?', 'Wir empfehlen sie. Eine Allgefahren-Solarversicherung deckt Hagel, Brand, Diebstahl, Vandalismus, Kurzschluss oder Überspannung, Wasser und Feuchtigkeit sowie Ausfallkosten ab. Über die Gebäudeversicherung ist die Anlage oft nicht sicher abgedeckt – lassen Sie sich das schriftlich bestätigen. Für unsere Kunden besteht ein Rahmenvertrag mit der Mannheimer; wir vermitteln nicht, sondern legen ein Angebot bei.'),
 ('Kann ich eine Anlage vorher ansehen?', 'Ja. In Aachen können Sie nach Terminabsprache eine Besichtigungsanlage im Mehrfamilienhaus sehen: Batteriesystem (Tesla III bzw. SMA DC 5 × 3,28 kWh), Wallboxen und Wärmepumpe im Betrieb. Am Demodach lassen sich verschiedene Befestigungssysteme vergleichen. Termin bei Frau Gier, Tel. 02402 7097620.'),
 ('Wann sind Sie erreichbar?', 'Büro und Lager im Gewerbegebiet Steinfurt in Stolberg: Mo–Do 8–15 Uhr, Fr 8–14 Uhr. Außerhalb der Geschäftszeiten erreichen Sie uns unter 0241 562489 oder 0171 5296741.'),
]
FQ = f'''
<section class="ph short">
  {img('k-schulung', 'Schulungsraum bei SOTECH mit Teilnehmern', 1204, 542, lazy=False, sizes='100vw')}
  <nav class="crumb" aria-label="Brotkrumen"><a href="index.html">Start</a>{CHEV}<span>Fragen</span></nav>
  <div class="wrap"><p class="eyebrow">FAQ</p><h1 class="split">Häufige Fragen.</h1><p class="lead">Kosten, Anmeldung, Speicher, Wallbox, EEG – kurz beantwortet. Alles Weitere am Telefon.</p></div>
</section>
<section class="sec"><div class="wrap"><div class="faq">{''.join(f'<details class="q"><summary>{q}<span class="pm"></span></summary><div class="a"><p>{a}</p></div></details>' for q,a in FAQS)}</div></div></section>
''' + cta_section('Ihre Frage war nicht dabei?', 'Rufen Sie an – wir antworten persönlich, nicht per Chatbot.')
pages.append(dict(file='faq.html', title='Häufige Fragen zu Photovoltaik, Speicher & Wallbox | SOTECH', desc='Kostet die Beratung etwas? Muss ich die Wallbox anmelden? Läuft der Speicher bei Stromausfall? Antworten vom Familienbetrieb SOTECH aus Stolberg bei Aachen.', body=FQ, ld={"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}))

# ============================ KONTAKT ============================
ANGEBOT_SEC = f'''<section class="sec" style="background:var(--bg-2)">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Angebot anfordern</p><h2 class="h-l split">Was wir für ein Angebot brauchen.</h2><p class="lead">Je genauer die Eckdaten, desto genauer das Angebot. Diese Angaben helfen uns – Sie können sie direkt im Kontaktformular eintragen.</p></div>
    <div class="steps">
      <div class="step reveal"><h3>Standort</h3><p>PLZ, Ort, Straße und Hausnummer – damit wir Dach und Verschattung vorab einschätzen können.</p></div>
      <div class="step reveal"><h3>Stromverbrauch</h3><p>Jahresverbrauch in kWh (steht auf der Stromrechnung), z. B. 4.000 kWh.</p></div>
      <div class="step reveal"><h3>Dach</h3><p>Dachart (Sattel, Pult, Flach), Ausrichtung (Süd, Ost-West …), Eindeckung (Pfannen, Schiefer, Trapezblech).</p></div>
      <div class="step reveal"><h3>Gewünschte Komponenten</h3><p>PV-Anlage, Stromspeicher, Wallbox – bei der Wallbox grob die Kabelstrecke vom Zählerschrank bis zum Stellplatz.</p></div>
      <div class="step reveal"><h3>Fotos</h3><p>Offener Zählerschrank aus 1,5 m Entfernung (nur Türen öffnen) und Dachflächen, gern von der anderen Straßenseite oder aus dem Garten.</p></div>
      <div class="step reveal"><h3>Zeitraum</h3><p>Zeitnah oder in den nächsten 3–6 Monaten? Mit Blick auf den 1.1.2027 lohnt sich Tempo.</p></div>
    </div>
    <p style="margin-top:28px"><a class="btn btn-primary" href="kontakt.html?thema=angebot">Angebot anfordern {ARROW}</a></p>
  </div>
</section>
'''
KO = f'''
<section class="ph short">
  {img('k-fuhrpark', 'SOTECH-Firmengebäude mit Fahrzeugen', 768, 576, lazy=False, sizes='100vw')}
  <nav class="crumb" aria-label="Brotkrumen"><a href="index.html">Start</a>{CHEV}<span>Kontakt</span></nav>
  <div class="wrap"><p class="eyebrow">Kontakt</p><h1 class="split">Planen Sie gerade ein Projekt? Fragen Sie uns einfach.</h1><p class="lead">Büro und Lager im Gewerbegebiet Steinfurt in Stolberg. Mo–Do 8–15 Uhr, Fr 8–14 Uhr.</p></div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="kon">
      <form class="form" id="contactForm" name="kontakt" method="POST" action="danke.html" data-netlify="true" netlify-honeypot="firma" novalidate>
        <input type="hidden" name="form-name" value="kontakt">
        <p class="hp" aria-hidden="true"><label>Firma (bitte leer lassen) <input name="firma" tabindex="-1" autocomplete="off"></label></p>
        <p class="eyebrow">Worum geht es?</p>
        <div class="topics" role="group" aria-label="Thema wählen">
          <button type="button" data-v="beratung" aria-pressed="true">Vor-Ort-Beratung</button><button type="button" data-v="angebot" aria-pressed="false">Angebot</button><button type="button" data-v="photovoltaik" aria-pressed="false">Photovoltaik</button><button type="button" data-v="speicher" aria-pressed="false">Speicher</button><button type="button" data-v="wallbox" aria-pressed="false">Wallbox</button><button type="button" data-v="besichtigung" aria-pressed="false">Besichtigungsanlage</button><button type="button" data-v="rueckruf" aria-pressed="false">Rückruf</button><button type="button" data-v="service" aria-pressed="false">Service / Wartung</button><button type="button" data-v="praktikum" aria-pressed="false">Praktikum / Ausbildung</button>
        </div>
        <label style="display:none"><span>Thema</span><select id="thema" name="thema"><option value="beratung">Vor-Ort-Beratung</option><option value="angebot">Angebot</option><option value="photovoltaik">Photovoltaik</option><option value="speicher">Speicher</option><option value="wallbox">Wallbox</option><option value="besichtigung">Besichtigungsanlage</option><option value="rueckruf">Rückruf</option><option value="service">Service / Wartung</option><option value="praktikum">Praktikum / Ausbildung</option></select></label>
        <div class="row"><label><span>Name *</span><input name="name" required autocomplete="name"></label><label><span>Telefon *</span><input name="telefon" type="tel" required autocomplete="tel"></label></div>
        <div class="row"><label><span>E-Mail *</span><input name="email" type="email" required autocomplete="email"></label><label><span>PLZ / Ort</span><input name="ort" autocomplete="postal-code"></label></div>
        <div class="row"><label><span>Stromverbrauch (kWh/Jahr)</span><input name="verbrauch" inputmode="numeric" placeholder="z. B. 4000"></label><label><span>Dachart / Ausrichtung</span><input name="dach" placeholder="z. B. Satteldach, Süd"></label></div>
        <label><span>Ihre Nachricht</span><textarea name="nachricht" placeholder="Gewünschte Komponenten, geplanter Zeitraum, Fragen …"></textarea></label>
        <label class="check"><input type="checkbox" name="datenschutz" required><div>Ich habe die <a href="datenschutz.html" style="text-decoration:underline">Datenschutzerklärung</a> gelesen und bin mit der Verarbeitung meiner Angaben zur Bearbeitung der Anfrage einverstanden. *</div></label>
        <p class="err" role="alert"></p>
        <button class="btn btn-primary" type="submit">Anfrage senden {ARROW}</button>
        <p class="muted" style="font-size:13px;margin-top:14px">Fotos von Zählerschrank und Dach können Sie nach unserer Antwort einfach per E-Mail an <a href="mailto:{CO['mail']}" style="text-decoration:underline">{CO['mail']}</a> schicken.</p>
      </form>
      <div>
        <div class="kbox"><h3>{CO['name']}</h3><p>{CO['street']}<br>{CO['zip']} {CO['city']}<br>Gewerbegebiet Steinfurt</p><a class="big" href="tel:{CO['telh']}">{CO['tel']}</a><ul><li>Fax {CO['fax']}</li><li>Mobil <a href="tel:{CO['mobilh']}">{CO['mobil']}</a></li><li>Außerhalb der Geschäftszeiten: <a href="tel:{CO['tel2h']}">{CO['tel2']}</a></li><li><a href="mailto:{CO['mail']}">{CO['mail']}</a></li></ul></div>
        <div class="kbox"><h3>Öffnungszeiten</h3><ul><li>Montag – Donnerstag: 8–15 Uhr</li><li>Freitag: 8–14 Uhr</li></ul></div>
        <div class="map-box" id="map"><div class="cover"><b>Karte anzeigen</b><p>Beim Laden der Karte werden Daten an OpenStreetMap übertragen.</p><button class="btn btn-ghost" data-map="map" data-pos="{CO['lat']},{CO['lon']}" data-title="SOTECH GmbH, Am Birkenfeld 10, Stolberg">OpenStreetMap laden</button><p style="margin-top:14px"><a class="link-arrow" href="https://www.openstreetmap.org/?mlat={CO['lat']}&mlon={CO['lon']}#map=16/{CO['lat']}/{CO['lon']}" target="_blank" rel="noopener">Route planen {ARROW}</a></p></div></div>
        <div class="kbox" style="margin-top:14px"><h3>Hinweis für Lieferanten: E-Rechnung</h3><p>Wir verarbeiten Ihre Rechnung auch elektronisch und erteilen dafür im Voraus unsere Zustimmung. Bitte im PDF-Format an <a href="mailto:rechnungen@sotech.de" style="text-decoration:underline">rechnungen@sotech.de</a> – eine E-Mail darf nur eine Rechnung (inklusive Anlagen) enthalten, und diese bitte nicht zusätzlich per Post.</p></div>
      </div>
    </div>
  </div>
</section>
''' + ANGEBOT_SEC + f'''
'''
pages.append(dict(file='kontakt.html', title='Kontakt – SOTECH GmbH, Am Birkenfeld 10, Stolberg', desc='Kostenlose Beratung anfragen: Telefon 02402 7097620, info@sotech.de. Büro im Gewerbegebiet Steinfurt, Stolberg. Mo–Do 8–15 Uhr, Fr 8–14 Uhr.', body=KO))

pages.append(dict(file='danke.html', noindex=True, title='Vielen Dank für Ihre Anfrage | SOTECH', desc='Ihre Anfrage ist bei SOTECH eingegangen. Wir melden uns in Kürze.', body=f'''
<section class="sec" style="padding-top:calc(var(--nav-h) + 100px);min-height:80vh;display:flex;align-items:center"><div class="wrap center"><p class="eyebrow" style="justify-content:center">Anfrage gesendet</p><h1 class="h-xl split">Vielen Dank.</h1><p class="lead" style="margin-top:22px">Ihre Anfrage ist bei uns eingegangen. Herr oder Frau Gier meldet sich in Kürze – meist innerhalb weniger Werktage. Wenn es eilig ist: <a href="tel:{CO['telh']}" style="text-decoration:underline">{CO['tel']}</a>.</p><p style="margin-top:30px;display:flex;gap:12px;justify-content:center;flex-wrap:wrap"><a class="btn btn-primary" href="index.html">Zur Startseite</a><a class="btn btn-ghost" href="ratgeber.html">Ratgeber lesen</a></p></div></section>'''))

pages.append(dict(file='404.html', noindex=True, title='Seite nicht gefunden | SOTECH', desc='Diese Seite gibt es nicht mehr.', body=f'''
<section class="err-page"><div class="wrap"><div class="big">404</div><h1 class="h-m" style="margin:20px 0 14px">Diese Seite ist im Dunkeln.</h1><p class="lead">Vielleicht ein alter Link von sotech.de. Die wichtigsten Seiten:</p><p style="margin-top:26px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-sun" href="index.html">Startseite</a><a class="btn btn-ghost" href="photovoltaik.html">Photovoltaik</a><a class="btn btn-ghost" href="kontakt.html">Kontakt</a></p></div></section>'''))

# ============================ IMPRESSUM / DATENSCHUTZ / AGB ============================
LEGAL_HEAD = lambda t, s: f'<section class="art-head"><div class="wrap"><p class="eyebrow">Rechtliches</p><h1 class="split">{t}</h1><p class="lead">{s}</p></div></section>'
IMP = LEGAL_HEAD('Impressum', 'Angaben gemäß § 5 DDG.') + f'''
<section><div class="wrap"><div class="prose">
<h2>Anbieter</h2><p><strong>{CO['name']}</strong><br>{CO['street']}<br>{CO['zip']} {CO['city']}</p>
<p>Telefon: {CO['tel']}<br>Fax: {CO['fax']}<br>E-Mail: <a href="mailto:{CO['mail']}">{CO['mail']}</a></p>
<h2>Vertreten durch</h2><p>Geschäftsführer: Dirk Gier</p>
<h2>Registereintrag</h2><p>Handelsregister: Amtsgericht Aachen, HRB 7915<br>Gerichtsstand ist Aachen.</p>
<h2>Umsatzsteuer-ID</h2><p>Umsatzsteuer-Identifikationsnummer gemäß § 27a UStG: DE 176161377</p>
<h2>Berufsbezeichnung</h2><p>Elektrotechniker-Handwerk (Meisterbetrieb), Bundesrepublik Deutschland. Eintragung in der Handwerksrolle der Handwerkskammer Aachen. <em>[Bitte prüfen: zuständige Handwerkskammer und Betriebsnummer ergänzen.]</em></p>
<h2>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2><p>Dirk Gier, Anschrift wie oben.</p>
<h2>Streitschlichtung</h2><p>Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung (OS) bereit: <a href="https://ec.europa.eu/consumers/odr/" target="_blank" rel="noopener">https://ec.europa.eu/consumers/odr/</a>. Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
<h2>Haftung für Inhalte</h2><p>Als Diensteanbieter sind wir für eigene Inhalte auf diesen Seiten nach den allgemeinen Gesetzen verantwortlich. Wir sind jedoch nicht verpflichtet, übermittelte oder gespeicherte fremde Informationen zu überwachen oder nach Umständen zu forschen, die auf eine rechtswidrige Tätigkeit hinweisen. Alle Angebote sind freibleibend und unverbindlich. Wir behalten uns vor, Teile der Seiten oder das gesamte Angebot ohne gesonderte Ankündigung zu verändern, zu ergänzen oder zu löschen.</p>
<h2>Haftung für Links</h2><p>Unser Angebot enthält Links zu externen Websites Dritter, auf deren Inhalte wir keinen Einfluss haben. Für diese Inhalte ist stets der jeweilige Anbieter verantwortlich. Zum Zeitpunkt der Verlinkung waren keine rechtswidrigen Inhalte erkennbar. Bei Bekanntwerden von Rechtsverletzungen entfernen wir derartige Links umgehend.</p>
<h2>Urheberrecht</h2><p>Die durch den Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen dem deutschen Urheberrecht. Vervielfältigung, Bearbeitung, Verbreitung und jede Art der Verwertung außerhalb der Grenzen des Urheberrechts bedürfen der schriftlichen Zustimmung.</p>
<h2>Bildnachweis</h2><p>Fotos von Kundenanlagen, Team und Firmengelände: SOTECH GmbH. Weitere Fotos: Unsplash (Unsplash-Lizenz) – Einzelnachweise siehe <code>img/BILDNACHWEIS.md</code>. Hersteller-Logos und Produktnamen (Heckert Solar, SMA, Wagner Solar, Zappy, Tesla) sind Marken der jeweiligen Inhaber.</p>
<p><a href="agb.html">Allgemeine Geschäftsbedingungen</a> · <a href="datenschutz.html">Datenschutzerklärung</a></p>
</div></div></section>'''
pages.append(dict(file='impressum.html', title='Impressum | SOTECH GmbH, Stolberg', desc='Impressum der SOTECH GmbH, Am Birkenfeld 10, 52222 Stolberg. Geschäftsführer Dirk Gier, HRB 7915 Amtsgericht Aachen.', body=IMP))

DS = LEGAL_HEAD('Datenschutzerklärung', 'Stand: September 2026. Kurz gesagt: keine Cookies, kein Tracking, Karte nur auf Klick.') + f'''
<section><div class="wrap"><div class="prose">
<h2>1. Verantwortlicher</h2><p>{CO['name']}, {CO['street']}, {CO['zip']} {CO['city']}, Telefon {CO['tel']}, E-Mail <a href="mailto:{CO['mail']}">{CO['mail']}</a>. Vertreten durch den Geschäftsführer Dirk Gier.</p>
<h2>2. Allgemeines</h2><p>Wir nehmen den Schutz Ihrer persönlichen Daten sehr ernst und behandeln Ihre personenbezogenen Daten vertraulich und entsprechend der Datenschutz-Grundverordnung (DSGVO), dem Bundesdatenschutzgesetz (BDSG) und dem Telekommunikation-Digitale-Dienste-Datenschutz-Gesetz (TDDDG). Diese Website verwendet <strong>keine Cookies</strong>, keine Analyse- oder Tracking-Dienste und bindet keine Inhalte Dritter ohne Ihre Handlung ein.</p>
<h2>3. Hosting</h2><p>Diese Website wird bei <em>[Hoster eintragen: z. B. GitHub, Inc. (GitHub Pages) oder Netlify, Inc.]</em> gehostet. Beim Aufruf werden automatisch Server-Logfiles verarbeitet (IP-Adresse, Datum und Uhrzeit, aufgerufene Seite, Browsertyp, Referrer). Die Verarbeitung erfolgt auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an einer sicheren und stabilen Bereitstellung). Mit dem Hoster besteht ein Vertrag über Auftragsverarbeitung; bei einem Anbieter mit Sitz in den USA erfolgt die Übermittlung auf Basis des EU-U.S. Data Privacy Framework bzw. der EU-Standardvertragsklauseln.</p>
<h2>4. Kontaktformular und Kontaktaufnahme</h2><p>Wenn Sie uns über das Kontaktformular, per E-Mail oder telefonisch Anfragen zukommen lassen, werden Ihre Angaben (Name, Telefon, E-Mail, ggf. Ort, Verbrauchs- und Dachangaben, Nachricht) zur Bearbeitung der Anfrage und für Anschlussfragen bei uns gespeichert. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO (vorvertragliche Maßnahmen) bzw. Art. 6 Abs. 1 lit. f DSGVO. Die Daten werden gelöscht, sobald sie für die Bearbeitung nicht mehr erforderlich sind und keine gesetzlichen Aufbewahrungspflichten entgegenstehen. Der Formularversand erfolgt über <em>[Formular-Dienst eintragen: z. B. Netlify Forms (Netlify, Inc.)]</em>; das Formular enthält ein unsichtbares Feld zur Spam-Abwehr (Honeypot).</p>
<h2>5. Schriften, Skripte und Bibliotheken</h2><p>Die verwendete Schrift (Archivo) ist lokal auf unserem Server gespeichert; es findet keine Verbindung zu Google Fonts oder anderen Schriftanbietern statt. Für Animationen werden die JavaScript-Bibliotheken GSAP und Lenis vom Content Delivery Network jsDelivr (Prospect One, Polen) geladen. Dabei wird Ihre IP-Adresse an jsDelivr übermittelt, damit die Dateien ausgeliefert werden können. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an schneller, sicherer Auslieferung). Weitere Informationen: <a href="https://www.jsdelivr.com/terms/privacy-policy" target="_blank" rel="noopener">jsdelivr.com/terms/privacy-policy</a>.</p>
<h2>6. Karte (OpenStreetMap) – nur auf Klick</h2><p>Auf der Kontaktseite können Sie eine Karte von OpenStreetMap (OpenStreetMap Foundation, Großbritannien) laden. Erst nach Ihrem Klick auf „OpenStreetMap laden“ wird eine Verbindung zu den Servern von OpenStreetMap hergestellt und Ihre IP-Adresse übertragen. Rechtsgrundlage ist Ihre Einwilligung nach Art. 6 Abs. 1 lit. a DSGVO. Datenschutzhinweise: <a href="https://wiki.osmfoundation.org/wiki/Privacy_Policy" target="_blank" rel="noopener">wiki.osmfoundation.org/wiki/Privacy_Policy</a>.</p>
<h2>7. Lokale Speicherung im Browser</h2><p>Die Website merkt sich in Ihrem Browser (sessionStorage) lediglich, ob die Start-Animation bereits gezeigt wurde. Dieser Eintrag enthält keine personenbezogenen Daten, wird nicht an uns übertragen und beim Schließen des Browsers automatisch gelöscht.</p>
<h2>8. Externe Links</h2><p>Unsere Website enthält Links zu externen Websites (z. B. Hersteller, Marktstammdatenregister, Google-Bewertungen). Beim Anklicken gelten die Datenschutzbestimmungen des jeweiligen Anbieters.</p>
<h2>9. Ihre Rechte</h2><p>Sie haben das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) sowie Widerspruch gegen die Verarbeitung (Art. 21 DSGVO). Eine erteilte Einwilligung können Sie jederzeit mit Wirkung für die Zukunft widerrufen. Zudem haben Sie das Recht, sich bei einer Aufsichtsbehörde zu beschweren; zuständig ist die Landesbeauftragte für Datenschutz und Informationsfreiheit Nordrhein-Westfalen, Kavalleriestraße 2–4, 40213 Düsseldorf.</p>
<h2>10. Datensicherheit</h2><p>Diese Website nutzt eine SSL/TLS-Verschlüsselung. Wir setzen technische und organisatorische Maßnahmen ein, um Ihre Daten gegen Manipulation, Verlust und unbefugten Zugriff zu schützen.</p>
<h2>11. Hinweis zu gefälschten E-Mails</h2><p>Immer wieder werden Viren und Phishing-Mails unter gefälschtem Absender versendet – häufig im Namen bekannter Firmen. Die SOTECH GmbH beteiligt sich nicht an einer solchen Verbreitung. Wir bitten Sie, verdächtige E-Mails, die vorgeblich von uns stammen, nicht zu öffnen und uns telefonisch zu informieren.</p>
</div></div></section>'''
pages.append(dict(file='datenschutz.html', title='Datenschutzerklärung | SOTECH GmbH', desc='Datenschutzerklärung der SOTECH GmbH: keine Cookies, kein Tracking, Kontaktformular, lokale Schriften, Karte nur auf Klick, Ihre Rechte.', body=DS))

agb = json.load(open('/private/tmp/claude-501/-Users-nilscremerius/1e2d3651-e0eb-4b4c-83b4-c32fae196ff1/scratchpad/agb.json'))
def agb_html(lines):
    out = []
    for l in lines:
        if re.match(r'^(§\s*\d+|[IVX]+\.)\s', l) or l.startswith('Allgemeine'): out.append(f'<h3>{l}</h3>')
        else: out.append(f'<p>{l}</p>')
    return ''.join(out)
AGB = LEGAL_HEAD('Allgemeine Geschäftsbedingungen', 'Verkaufs- und Lieferbedingungen der SOTECH GmbH – wortgleich von sotech.de übernommen.') + f'''
<section><div class="wrap"><div class="prose"><h2>Allgemeine Verkaufs- und Lieferbedingungen</h2>{agb_html(agb[0][1:])}<h2 style="margin-top:70px">Händler-AGB</h2>{agb_html(agb[1])}</div></div></section>'''
pages.append(dict(file='agb.html', title='AGB | SOTECH GmbH, Stolberg', desc='Allgemeine Verkaufs- und Lieferbedingungen sowie Händler-AGB der SOTECH GmbH.', body=AGB))

# ============================ SCHREIBEN ============================
for p in pages:
    html = head(p) + p['body'] + foot()
    open(OUT + p['file'], 'w', encoding='utf-8').write(html)
    print(p['file'], len(html) // 1024, 'KB', len(p['title']), len(p['desc']))
urls = [p['file'] for p in pages if not p.get('noindex')]
open(OUT + 'sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{DOMAIN}/{"" if u=="index.html" else u}</loc><lastmod>{TODAY}</lastmod><changefreq>{"weekly" if u=="index.html" else "monthly"}</changefreq><priority>{"1.0" if u=="index.html" else "0.8" if u in ("photovoltaik.html","speicher.html","wallbox.html","service.html","kontakt.html") else "0.6"}</priority></url>\n' for u in urls) + '</urlset>\n')
open(OUT + 'robots.txt', 'w').write(f'User-agent: *\nAllow: /\nDisallow: /danke.html\n\nSitemap: {DOMAIN}/sitemap.xml\n')
open(OUT + 'img/logo.svg', 'w').write(LOGO.replace('fill="currentColor"', 'fill="#1d1d1f"'))
print('ok', len(pages))
