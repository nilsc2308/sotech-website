# Launch-Checkliste – SOTECH GmbH (neue Website, Apple-Stil)

Stand: 15. September 2026 · Projekt: `Documents/website 1/sotech-web`
Vorlage/Inhaltsquelle: https://sotech.de (bestehende Website). Die alte Website bleibt unangetastet.

Legende: **✅ erledigt** · **⚠️ offen, braucht eine Angabe oder Entscheidung vom Kunden** · **⏳ erst nach dem Livegang möglich**

## Offene Kundenangaben (bitte durchgeben)

| | Punkt | Wo |
|---|---|---|
| ⚠️ | **Fotorechte** – 56 Fotos stammen von sotech.de (8 Team-Porträts, Gruppenfoto, Firmengelände, Kundenanlagen, Wallboxen, Zählerschränke). Bitte bestätigen, dass sie auf der neuen Seite verwendet werden dürfen und alle abgebildeten Personen (auch Kunden auf Referenzfotos) einverstanden sind | `img/k-*.webp`, `img/p-*.webp`, `img/r-*.webp`, `img/BILDNACHWEIS.md` |
| ⚠️ | **Domain** – Canonical, Sitemap, robots.txt, OG-Tags und JSON-LD zeigen auf `https://www.sotech.de`. Wenn die Seite unter einer anderen Adresse laufen soll: überall ersetzen (Suchen & Ersetzen) | alle HTML-Dateien, `sitemap.xml`, `robots.txt` |
| ⚠️ | **Hoster in der Datenschutzerklärung** – Platzhalter `[Hoster eintragen …]` ersetzen (GitHub Pages = GitHub, Inc.; Netlify = Netlify, Inc.; oder der bisherige Hoster von sotech.de) | `datenschutz.html`, Abschnitt 3 |
| ⚠️ | **Formular-Versand** – Das Kontaktformular ist für **Netlify Forms** vorbereitet (Honeypot, Weiterleitung auf `danke.html`). Auf **GitHub Pages funktioniert der Versand nicht**. Entscheidung: Netlify oder anderer Formulardienst; danach Platzhalter `[Formular-Dienst eintragen …]` in der Datenschutzerklärung ersetzen | `kontakt.html`, `datenschutz.html` Abschnitt 4 |
| ⚠️ | **Impressum: Handwerkskammer** – auf sotech.de nicht angegeben; Platzhalter „zuständige Handwerkskammer und Betriebsnummer ergänzen“ | `impressum.html` |
| ⚠️ | **Datenschutzerklärung** – sotech.de hat nur einen alten „Disclaimer“ (kein DSGVO-Text). Der neue Text wurde für diese Technik geschrieben (keine Cookies, jsDelivr, OSM per Klick, Formular). Bitte vom Kunden/Anwalt gegenlesen lassen | `datenschutz.html` |
| ⚠️ | **Google-Bewertung „5/5 Sterne“** und **„1.500 Anlagen / 7.800 kWp / 38 Jahre“** – Angaben von sotech.de übernommen. Bitte aktuell halten | `index.html`, `ueber-uns.html` |
| ⚠️ | **Team** – Texte und Fotos von sotech.de: Dirk Gier, Gabi Gier („Frau Gier“ – Vorname aus Dateiname `gabi.jpg` abgeleitet, bitte bestätigen), Christian Gier, Stephanie Hackner geb. Gier, Michael Eschweiler, René Brieger, Florian Ervens, Abdull Haj Bakri (Ausbildung ab 1.8.2026 – ist das Datum noch aktuell?) | `ueber-uns.html#team` |
| ⚠️ | **Öffnungszeiten** – von kontakt.php übernommen: Mo–Do 8–15 Uhr, Fr 8–14 Uhr; Notfallnummern 0241 562489 und 0171 5296741. Passt das? | Kontakt, Fußzeile, JSON-LD |
| ⚠️ | **Schnell-Check-Rechner (Startseite)** – Richtwerte: 5 m² je kWp, 950 kWh je kWp und Jahr, Netzstrom 0,35 €/kWh, Einspeisevergütung 7,78 ct/kWh (sotech.de: Feb.–Juli 2026), Eigenverbrauch 30 % ohne / 60 % mit Speicher, 0,38 kg CO₂/kWh. Bitte plausibilisieren | `main.js` Block „Mini-Rechner“ |
| ⚠️ | **Konfigurator (Photovoltaik)** – Richtwerte: 450 Wp je Modul, 950 kWh/kWp·a, Eigenverbrauch 30–70 %. Komponentenliste (Heckert ZEUS, SMA, Wagner TRIC, Zappy) nach sotech.de. Bitte prüfen | `main.js` Block „Konfigurator“ |
| ⚠️ | **Zeitplan-Balken (Service)** – Phasendauern sind Erfahrungswerte (Beratung 1 Wo, Angebot 2 Wo, Netzbetreiber 6 Wo, Montage 1 Wo, Zähler/IBN 3 Wo, MaStR 4 Wo). Bitte an die Praxis anpassen | `main.js` Block „Zeitplan“ |
| ⚠️ | **EEG-2027-Aussagen** – aus den News auf sotech.de übernommen (Gesetzentwurf, 5,20 ct/kWh, Direktvermarktung ab 2030 …). Bei Gesetzesänderungen aktualisieren; „Tage bis zum Stichtag“ rechnet automatisch | `index.html`, `ratgeber-eeg-2027.html`, `service.html` |
| ⚠️ | **Referenzkarte** – 13 Punkte aus der Referenzliste (ZG-/Yingli-Anlagen 2009/2010, Wuppertal 1994, Besichtigungsanlage Aachen). Koordinaten für Kundenanlagen sind nur ortsgenau (Ortsmitte), nicht adressgenau. Gern durch neuere Anlagen ergänzen | `ueber-uns.html`, `refData` |
| ⚠️ | **Solarversicherung** – Hinweis „Rahmenvertrag Mannheimer“ und „keine Vermittlung“ von sotech.de übernommen. Noch aktuell? | `service.html`, `faq.html` |
| ⚠️ | **AGB** – wortgleich von sotech.de übernommen (Verkaufs-/Lieferbedingungen + Händler-AGB). Enthält alte Rechtschreibung („daß“) und teils veraltete Formulierungen – bitte juristisch prüfen | `agb.html` |
| ⚠️ | **Unsplash-Fotos** – 12 Stimmungsfotos (Dach, Montage, Laden, Nacht, Module). Konten von Herstellern gemieden. Falls nur eigene Fotos gewünscht: austauschen | `img/u-*.webp`, `img/BILDNACHWEIS.md` |

## Deine Standard-Checkliste – Stand 15.9.2026 (alles geprüft)

| | Punkt | Stand |
|---|---|---|
| ✅⚠️ | **Datenschutzerklärung** | Neu geschrieben (DSGVO): Verantwortlicher, Hosting, Kontaktformular, lokale Schrift, jsDelivr, OSM per Klick, sessionStorage, Betroffenenrechte, LDI NRW. **Zwei Platzhalter ausfüllen: Hoster und Formulardienst** |
| ✅⚠️ | **Impressum** | Von sotech.de übernommen (Am Birkenfeld 10, 52222 Stolberg, GF Dirk Gier, HRB 7915 Amtsgericht Aachen, USt-IdNr. DE 176161377), ergänzt um DDG/MStV, OS-Plattform, Bildnachweis. **Handwerkskammer ergänzen** |
| ✅ | **Cookie Consent** | Nicht nötig – keine Cookies, kein Tracking, keine Drittanbieter-Einbettung ohne Klick (Karte erst per Klick, Schrift lokal, Google-Bewertungen nur verlinkt). In der Datenschutzerklärung erklärt |
| ✅ | **Mobile Version** | 390 px (iPhone) in Chromium und WebKit, alle 16 Seiten komplett durchgescrollt: kein Querscrollen (scrollWidth = clientWidth), 0 JS-Fehler. Split-Hero: Foto-Säule klebt oben, Text scrollt darunter; Tag/Nacht-Uhr klebt oben; Story-Foto klebt oben; Akkordeon als vertikaler Stapel; Zeitplan mit Labels über den Balken; Burger ab 1020 px, Vollbild-Menü, Sticky-CTA unten |
| ✅ | **Meta Titles** | Alle 16 Seiten, 27–66 Zeichen (Startseite 71 Zeichen – bewusst, enthält Ort + Alleinstellung; kürzen auf Wunsch), mit Ort/Leistung |
| ✅ | **Meta Descriptions** | Alle Seiten einzeln, 31–163 Zeichen (service.html 163, ratgeber-wallbox 161 – 6–8 Zeichen über Ziel, Google schneidet ggf. ab) |
| ✅ | **Favicon** | `favicon.svg` (rotes Quadrat, gelber Balken, weißes S) + `apple-touch-icon.png` 180 px |
| ✅ | **Sitemap.xml** | 14 URLs (ohne danke/404), Datum 15.9.2026, Prioritäten gesetzt |
| ✅ | **Robots.txt** | Alles frei, `danke.html` ausgeschlossen, Verweis auf Sitemap |
| ✅⚠️ | **Canonical URLs** | Auf jeder Seite gesetzt → `https://www.sotech.de/…`. **Domain beim Livegang bestätigen** |
| ✅ | **404-Seite** | `404.html` (Nachtblau, „Diese Seite ist im Dunkeln“, Rückwege); GitHub Pages nutzt sie automatisch, Netlify per Regel in `netlify.toml` |
| ✅ | **Broken Links** | Skript-Prüfung 15.9.: alle internen Links, Sprungmarken (`#…`) und Bildpfade vorhanden (0 Fehler); alle 12 externen Links antworten mit 200 (jsDelivr ×3, Heckert, Wagner, MaStR, OSM ×2, Google, EU-ODR, jsDelivr-Datenschutz, OSMF). Die sotech.de-Canonicals der neuen Seiten liefern 404, bis die Seite live ist – erwartbar |
| ✅ | **Performance** | Startseite lokal bis „load“: **Desktop 742 KB / 389 ms (WebKit), 369 KB / 404 ms (Chromium)**, **Handy 529 KB (WebKit) / 369 KB (Chromium)** – Ziel < 900 / < 500 KB: Desktop erreicht, Handy in WebKit 29 KB über Ziel (Hero-Foto 1 wird in voller Größe geladen). LCP 69–72 ms, CLS 0,000. Alle Fotos WebP in zwei Größen, `srcset`, `width`/`height`, Lazy-Loading außer Hero; Schrift lokal (90 KB, vorgeladen); Cache-Header in `netlify.toml` |
| ✅ | **Accessibility Basics** | Sprung-zum-Inhalt-Link, sichtbare Fokus-Styles, Tastaturbedienung geprüft (Tab-Reihenfolge: Skip → Logo → Telefon → Menü → Buttons → Akkordeon-Streifen; Menü mit Fokusfalle + Escape; Zeitplan-Griff als `role=slider` mit Pfeiltasten; Referenzpunkte per Enter), `aria-pressed`/`aria-expanded`/`aria-live`, Überschriften-Hierarchie, Kontrast AA (Rot/Weiß 6,7:1, Schwarz/Gelb 12,8:1, Grau/Weiß 5,1:1, Gelb/Nacht 14,2:1, Rot auf Tag-Gelb 5,2:1), `prefers-reduced-motion` schaltet Hero-Scrub, 1988-Zoom, Uhr, Marquee, Vorhang und alle Reveals ab – alle Inhalte bleiben sichtbar (automatisch geprüft) |
| ✅⚠️ | **Kontaktformular getestet** | Automatisch geprüft 15.9.: Pflichtfelder blockieren, falsche E-Mail blockiert, Themen-Kacheln setzen die Auswahl, `?thema=wallbox` belegt vor, Honeypot vorhanden, gültige Eingabe → `danke.html`. **Versand braucht Netlify Forms oder anderen Dienst** |
| ✅ | **Alt-Texte** | Alle Bilder haben `alt`; beschreibend bei Inhaltsbildern, leer bei rein dekorativen (Hero-Säule, Akkordeon-Hintergründe, Marquee) |
| ⚠️ | **Google Analytics / Tracking** | Bewusst **nicht** eingebaut (kein Banner nötig; sotech.de hatte nur einen eigenen Zähler). Wenn gewünscht: Consent-Banner + GA4 – dann Datenschutzerklärung ergänzen |
| ✅ | **Open Graph / Social Sharing** | `og:title`, `og:description`, `og:url`, `og:image` (1200×630 `img/og.jpg`: PV-Dach + Logo + Claim), `og:locale`, `twitter:card` je Seite |
| ✅⚠️ | **Lokale SEO-Daten** | JSON-LD `LocalBusiness` auf allen Seiten: Name, Adresse, Telefon, Fax, E-Mail, Geo 50.7843/6.2324 (per OpenStreetMap-Suche), Öffnungszeiten, Einzugsgebiet, Gründung 1988, USt-IdNr., EUPD-Auszeichnung; `FAQPage` (14 Fragen), `Article` (3 Ratgeber). Karte (OSM) per Klick + Routenlink. **Google-Unternehmensprofil** gehört dem Kunden – Adresse/Zeiten dort abgleichen |
| ⏳ | **Indexierung bei Google** | Erst nach Livegang: Search Console anlegen, `sitemap.xml` einreichen, Startseite per URL-Prüfung anfordern. Alte Adressen weiterleiten – 14 Regeln liegen in `netlify.toml` (index2.php, unternehmen-team, produkte, wallbox, ueberschusseinspeisung, solarversicherung, news, wissen, kontakt.php …); bei anderem Hoster als `.htaccess` umsetzen |

## Marke

| | Punkt | Stand |
|---|---|---|
| ✅ | **Farben** | Aus Logo und CSS von sotech.de: Signalrot `#ba0600` (Logo-Balken, Buttons, Menü), Sonnengelb `#ffdf5b` (Akzente, Uhr). Dazu Weiß / `#f5f5f7` / `#1d1d1f`, Nachtblau `#0a1224`. Radius 10 px (kantig, Handwerk) |
| ✅⚠️ | **Logo** | Das Original liegt nur als JPG vor (`s2dlogo.jpg`, 1300 px). Es wurde als SVG nachgebaut (roter Balken, „SOTECH“ schwer, „SOLARTECHNIK“ gesperrt) – skaliert scharf und funktioniert weiß auf Dunkel. **Falls es eine Vektor-Datei des Logos gibt: bitte schicken, dann tausche ich sie ein** |
| ✅ | **Schrift** | Archivo (variabel, Gewicht + Breite) lokal in `fonts/` – passt zu den Blockbuchstaben des Logos. Kein Google-Fonts-Aufruf |

## Technik

| | Punkt | Stand |
|---|---|---|
| ✅ | **Seiten** | 16: index, photovoltaik, speicher-wallbox, service, ueber-uns, ratgeber + 3 Artikel, faq, kontakt, danke, 404, impressum, datenschutz, agb |
| ✅ | **Aufbau (eigenständig, siehe DESIGN.md)** | Split-Hero mit gepinnter Foto-Säule (5 Motive), Zahl „1988“ schrumpft in den Text, Akkordeon-Galerie (5 Streifen), Signature: 24-Stunden-Uhr mit Tag/Nacht-Wechsel, Sticky-Storytelling (6 Kapitel Montage-Reportage), Text-Marquee mit Fotos (Tempo folgt dem Scrollen), Mini-Rechner ohne Schieberegler, EEG-Stichtag, Terminwahl-Kacheln + große Telefonnummer. Navigation: nur Logo + Telefon + „Menü“ mit rotem Vollbild-Overlay. Unterseiten: Vollbild-Foto-Header mit Breadcrumb |
| ✅ | **Interaktiv** | Konfigurator mit SVG-Vorschau (Photovoltaik), Checkliste mit Fortschrittsring (Speicher & Wallbox), Zeitplan-Balken zum Ziehen (Service), Referenzkarte mit klickbaren Punkten (Über uns), Schnell-Check-Rechner (Start), FAQ-Akkordeon, Themenwahl im Formular |
| ✅ | **Browser-Test** | Chromium + WebKit (Safari-Engine), 1400 px + 390 px, alle 16 Seiten durchgescrollt: 0 JS-Fehler, 0 fehlgeschlagene Requests, kein Querscrollen |
| ✅ | **Sicherheit** | `netlify.toml` mit X-Frame-Options, nosniff, Referrer-Policy, Permissions-Policy, HSTS; Formular mit Honeypot |
| ✅ | **Kein Cookie-Banner** | Keine Cookies, sessionStorage nur für das Intro, Karte per Klick, Schrift lokal |

## Sicherung & Veröffentlichung

- Backup: `sotech-web_2026-09-15.tar.gz` im Ordner `Documents/website 1`
- Git-Repository im Projektordner; Vorschau auf GitHub Pages (siehe README.md / PROJEKTE-UEBERSICHT.md)
- Lokal ansehen: Ordner öffnen und `index.html` doppelklicken – oder im Terminal `python3 -m http.server 8766` im Projektordner und http://localhost:8766 aufrufen
