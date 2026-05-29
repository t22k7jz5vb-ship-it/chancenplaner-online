# Chancenplaner 2026 – Online-App

Ziel: dieselbe App über eine feste URL auf Mac, Samsung und anderen Geräten nutzen.

## Aktiver Stand
- Live-URL: `https://t22k7jz5vb-ship-it.github.io/chancenplaner-online/`
- Hosting: GitHub Pages
- Daten + Login: Supabase
- GitHub-Repo: `git@github.com:t22k7jz5vb-ship-it/chancenplaner-online.git`

## Wichtige Dateien
- `index.html` – aktueller veröffentlichbarer Stand
- `dev/index.html` – Arbeitsstand für Änderungen
- `config.js` – aktive Supabase-Konfiguration
- `config.example.js` – Vorlage für neue Konfigurationen
- `supabase_schema_v4_json.sql` – aktuelles Supabase-Schema
- `archive/` – lokale Snapshot-Ablage veröffentlichter Stände

## Supabase einrichten
1. Neues Supabase-Projekt anlegen
2. Im SQL Editor `supabase_schema_v4_json.sql` ausführen
3. Unter Authentication -> Sign In / Providers -> Email aktiv lassen
4. Unter Project Settings -> API diese Werte kopieren:
   - Project URL
   - anon public key
5. `config.example.js` nach `config.js` kopieren und Platzhalter ersetzen

## Lokal prüfen
Einfacher Testserver:

```bash
cd /Volumes/2_Projekte/H_Chancenplaner/online_app
python3 -m http.server 8080
```

Dann öffnen:
- `http://localhost:8080`

## Testen
Regressionstests für den Arbeitsstand:

```bash
cd /Volumes/2_Projekte/H_Chancenplaner/online_app/dev
python3 -m unittest discover -s tests -v
```

## Arbeitsregel
Die Projektregel liegt hier:
- `/Volumes/2_Projekte/H_Chancenplaner/WORKFLOW.md`

Kurz:
- Änderungen zuerst in `dev/index.html`
- dann testen
- danach nach `index.html` übernehmen
- veröffentlichten Stand zusätzlich in `archive/` sichern
- anschließend GitHub/GitHub Pages prüfen

## Nutzung
- Beim ersten Mal Account mit E-Mail + Passwort anlegen
- Danach überall mit derselben URL einloggen
- Tages-, Wochen- und Jahresinhalte bleiben online verfügbar
