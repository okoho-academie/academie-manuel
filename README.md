# OKOHO Académie · academie-manuel

**FR.** Source unique du *Manuel* de l'OKOHO Académie (Parcours Claude Pro). Chaque séance existe une seule fois ici, en Markdown avec en-tête de métadonnées. Tout le reste est généré : application academie.okoho.de, PDF, copie Google Drive, sources NotebookLM, vidéos, table des matières, glossaire et index.

**DE.** Einzige Quelle des Manuel der OKOHO Académie (Parcours Claude Pro). Jede Séance existiert genau einmal hier, als Markdown mit Metadatenkopf. Alles andere wird erzeugt: App academie.okoho.de, PDFs, Drive-Kopie, NotebookLM-Quellen, Videos, Inhaltsverzeichnis, Glossar und Index.

## Structure / Struktur

| Dossier | Inhalt |
|---|---|
| `manuel/structure.yaml` | 5 Parties, 18 Modules, 50 Séances (Soll-Struktur) |
| `seances/<CODE>/seance.md` | Inhalt je Séance mit Metadatenkopf |
| `schema/seance.schema.json` | Schema des Metadatenkopfs |
| `glossaire/glossaire.yaml` | Glossareinträge (FR) |
| `design/` | Tokens und Logos der Markenschicht OKOHO Académie |
| `tools/` | validate, build_index, build |
| `.claude/` | Befehl `/produire-seance`, Skills |
| `out/` | Erzeugte Ausgaben (nicht versioniert) |

## Single Source, Multi Output

```
seances/*.md  ──►  tools/build.py  ──►  out/  ──►  App · PDF · Drive · NotebookLM · Vidéo
```

Build: `python3 tools/build.py` (PyYAML erforderlich).

## Marque / Marke

Gestaltung nach OKOHO Design System 2.2 mit der Markenschicht OKOHO Académie (Dokument 02, Version 3.0; Ergänzungsdokument „Markenschicht OKOHO Académie“ 1.0). Tokens in `design/tokens.json`.

© 2026 OKOHO Consulting GmbH, tous droits réservés. Claude est une marque d'Anthropic ; aucun partenariat avec Anthropic.
