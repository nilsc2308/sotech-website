# SOTECH GmbH – Website (Apple-Stil, statisch)

Neue Website für SOTECH Solartechnik, Stolberg. Vorlage/Inhalte: https://sotech.de (alte Seite bleibt unangetastet).

## Ansehen
- Ordner öffnen und `index.html` doppelklicken – oder im Terminal im Projektordner `python3 -m http.server 8766` und http://localhost:8766 aufrufen.
- Online-Vorschau (GitHub Pages): siehe PROJEKTE-UEBERSICHT.md im Ordner „website 1“.

## Aufbau
- 16 Seiten: index, photovoltaik, speicher-wallbox, service, ueber-uns, ratgeber (+3 Artikel), faq, kontakt, danke, 404, impressum, datenschutz, agb
- `styles.css` / `main.js` gemeinsam, kein Build. Die HTML-Seiten werden aus einem Python-Generator erzeugt (Scratchpad, `build.py`) – Änderungen am Kopf/Fuß dort machen, sonst direkt in den HTML-Dateien.
- Schrift Archivo (variabel) lokal in `fonts/`, Fotos in `img/` (WebP, zwei Größen, Nachweis in `img/BILDNACHWEIS.md`)
- Gestaltungsregeln: `DESIGN.md` · Offene Punkte: `LAUNCH-CHECKLISTE.md`

## Veröffentlichen
Netlify-fertig (`netlify.toml` mit Security-Headern, Weiterleitungen alter sotech.de-Adressen, Formular per Netlify Forms). Auf GitHub Pages funktioniert alles außer dem Formularversand.
