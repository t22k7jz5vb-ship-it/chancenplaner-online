# V4-Entkopplung: Ist-Zustand und nächster Schritt

## Ist-Zustand
- Die aktuell sichtbare V4 in online_app/index.html ist funktional an /api/strategy, /api/entries/... und /api/weekly/... gebunden.
- Deshalb läuft sie aktuell nur, wenn der Mac den Python-Server aus webapp/app.py bereitstellt.
- Das alte online_app-Supabase-Frontend war eine andere App-Variante und deckt V4 nicht vollständig ab.

## Wichtigste Lücke
Das vorhandene Supabase-Schema ist für die alte Online-App gedacht.
Es fehlt für V4 insbesondere:
- Wocheneinträge
- V4-Strategiefelder in voller Breite
- 1:1-Ablage der aktuellen JSON-Payloads

## Bewusste Entscheidung
Keine funktionale Reduktion.
Darum für V4 zuerst JSONB-Speicherung in Supabase statt Neudesign der Datenstruktur.

## Neuer Artefakt-Stand
- supabase_schema_v4_json.sql
  - V4-kompatible Tabellen:
    - strategy_profiles_v4
    - daily_entries_v4
    - weekly_entries_v4
  - inklusive RLS und Triggern

## Nächster technischer Schritt
1. supabase_schema_v4_json.sql im Supabase SQL Editor ausführen
2. danach online_app/index.html von /api/... auf Supabase-Reads/Writes umstellen
3. dann die App statisch hosten
