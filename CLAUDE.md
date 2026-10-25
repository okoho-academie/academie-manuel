# CLAUDE.md · academie-manuel

OKOHO Académie ist eine Marke der OKOHO Consulting GmbH (Detmold). Verantwortlich: Dr. Bertrand Toumi. Promesse : « De l'idée au service digital vendu, avec Claude. »

## Grundsätze
- Single Source: Inhalte nur in `seances/<CODE>/seance.md`. `out/`, App, Drive, PDFs, Videos sind Ausgaben und werden nie von Hand geändert.
- Keine Strategie, Finanzen, Gründungsunterlagen, Verträge oder Personendaten in diesem Repository.
- Materialien für Lernende auf Französisch, Anrede « vous », kurze Sätze. Kamerunische Beispiele nur im Kasten « Cas fil rouge ». Kein Bezug auf « letzte Woche »: jede Séance ist eigenständig.
- Jede Séance beginnt mit « Ce que vous saurez faire » und endet mit « Votre livrable ».
- Keine erfundenen Funktionen oder Preise von Claude. Im Zweifel prüfen und Datum angeben.

## Scaffolding (Fading)
Vier Phasen je Séance: Je vous montre → Nous faisons ensemble → Vous faites avec appui → Vous faites seul. Coups de pouce in drei Stufen (indice, solution partielle, solution complète).
Gerüststufe `echafaudage` nach Partie: I = 1, II = 2, III = 3, IV = 2 bei neuem Werkzeug sonst 3, V = 4.
- Stufe 1: alle Phasen voll ausgearbeitet, Musterprompts vollständig, Screenshot je Klick.
- Stufe 2: Musterprompt nur als Gerüst mit Lücken.
- Stufe 3: keine Musterprompts, nur Checkliste und Kriterien.
- Stufe 4: nur Briefing und Kriterien.

## Pflichtkennzeichnung
« Une formation OKOHO Consulting GmbH · Formateur : Dr. Bertrand Toumi », © <Jahr des Builds, automatisch> OKOHO Consulting GmbH, Markenhinweis (« Claude est une marque d'Anthropic … sans partenariat avec Anthropic »), Version und Datum der Screenshots. Gestaltung nur über `design/tokens.json` (OKOHO Design System 2.2 + Académie-Modus, academie-tint #FFF4E8).

## Design-Pflicht für jede Ausgabe
- Jedes Dokument entsteht über die Werkzeuge, nie als Rohtext: PDF `tools/build_pdf.py`, Word `tools/build_docx.py` (auch für interne deutsche Dokumente mit `--lang=de`), Drive-Paket `tools/build_drive.py`.
- Alle drei lesen `design/tokens.json` und `design/logos/`: Logo OKOHO Académie im Kopf, Montserrat für Titel, Open Sans für Text, Encadrés in academie-tint mit orangefarbener Linie, Tabellenkopf blue-deep, Fußzeile mit Kontakt und Seitenzahl, Pflichtkennzeichnung.
- Für Lernende im Drive: PDF. Word (.docx) nur für Dokumente zum Ausfüllen oder Bearbeiten. Keine unformatierten Google Docs aus Markdown.
- Folien: Claude Slides mit Design System OKOHO (Académie-Farben).

## Arbeitsablauf
- Jede Séance auf eigenem Branch `seance/<CODE>`, Merge nach `main` erst nach Freigabe durch Bertrand.
- Vor jeder Arbeit `git pull`. Nach jeder Änderung `python3 tools/validate.py`.
- Befehl `/produire-seance <CODE>`: validate → build → Commit auf `seance/<CODE>`.
- Glossar- und Indexbegriffe stehen im Metadatenkopf; `tools/build_index.py` erzeugt Inhaltsverzeichnis, Glossar und Index. Nie von Hand pflegen.

## Benennung für Lernende (Drive, WhatsApp, Abgaben)
- Quelle: `parcours/cohorte-<N>.yaml` (Woche, Datum, Lesereihenfolge). Ausgabe: `tools/build_drive.py` → `out/drive/cohorte-<N>/` mit `manifest.json`.
- Ordner: « Semaine NN · JJ.MM.AAAA · Titre ». Datei: « SNN-Reihenfolge · Type · Code Titre » (Types: Guide, À remplir, Séance en direct, En autonomie).
- Abgabe der Lernenden: « SNN-Reihenfolge_Prenom.ext ». Kein « : » in Dateinamen (Windows).
- Drive-Wurzel in Nutzungsreihenfolge: 00 · Formateur (privé), 01 · Programme et calendrier, 02 · Séances semaine par semaine, 03 · Réviser avec NotebookLM, 04 · Portfolios, 05 · Projets en équipe, 06 · Ressources et liens utiles. Einstieg: « 00 · COMMENCEZ ICI » (Quelle `parcours/drive/commencez-ici.md`).
- Wiederverwendung: Quellen (seances/, accueil/, parcours/drive/) enthalten NIE Datum, Jahr oder Kohortennamen. Statt dessen Variablen: {{date:SNN}} (« le samedi 7 novembre 2026 »), {{debut}}, {{fin}}, {{jour}}, {{cohorte}}, {{groupe}}, {{nb_semaines}}, {{calendrier}}, {{jalons}}. `validate.py` blockiert Datumsangaben.
- Ohne Kohorte (`out/pdf/`) entstehen neutrale PDFs für jede Kohorte und das Selbstlernen; mit Kohorte (`out/pdf/cohorte-N/`, `out/drive/cohorte-N/`) datierte Ausgaben.
- Neue Kohorte: `parcours/cohorte-1.yaml` kopieren, Daten und Gruppennamen ändern, `python3 tools/build.py`. Kein Dokument wird neu geschrieben. Déroulé ohne Datum: `parcours/modele.yaml`.
