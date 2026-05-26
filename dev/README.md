# Chancenplaner 2026 – Online-Version mit Supabase

Ziel: dieselbe App über eine feste URL in Chrome-Favoriten auf Mac und Samsung nutzen.

## Live-Stand
- Live-URL: `https://t22k7jz5vb-ship-it.github.io/chancenplaner-online/`
- Hosting: GitHub Pages
- Daten + Login: Supabase
- Basis: V4-Oberfläche inkl. `Woche planen`

## Dateien
- `index.html` – statische App mit Supabase-Login und V4-Oberfläche
- `config.example.js` – Vorlage für Supabase URL + Anon Key
- `config.js` – Laufzeit-Konfiguration
- `supabase_schema_v4_json.sql` – V4-kompatibles Supabase-Schema
- `supabase_schema.sql` – älteres Schema der früheren Online-Variante

## Supabase einrichten
1. Neues Supabase-Projekt anlegen
2. In Supabase SQL Editor den Inhalt aus `supabase_schema_v4_json.sql` ausführen
3. Unter Authentication -> Sign In / Providers -> Email aktiv lassen
4. Unter Project Settings -> API folgende Werte kopieren:
   - Project URL
   - anon public key
5. `config.example.js` nach `config.js` kopieren und beide Platzhalter ersetzen

## Lokal testen
Einfacher Testserver, z. B.:

```bash
cd /Volumes/2_Projekte/H_Chancenplaner/online_app
python3 -m http.server 8080
```

Dann öffnen:
- `http://localhost:8080`

## Online hosten
Aktueller Weg:
- GitHub Pages

Repo:
- `https://github.com/t22k7jz5vb-ship-it/chancenplaner-online`

Wichtig:
- `index.html` und `config.js` müssen zusammen deployed werden
- nach Änderungen beide Dateien im Repo aktuell halten

## Nutzung
- Beim ersten Mal Account mit E-Mail + Passwort anlegen
- Danach überall mit derselben URL einloggen
- Strategieblock bleibt dauerhaft
- Tagesdaten bleiben pro Datum
- Mac muss für die Live-URL nicht laufen
