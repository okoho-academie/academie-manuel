# PDF du Manuel · conventions de rédaction

    python3 tools/build_pdf.py              # toutes les séances et documents d'accueil
    python3 tools/build_pdf.py M01-S1 A00-01 # seulement ces codes
    python3 tools/build_pdf.py --fixtures   # + documents de test (tests/fixtures)
    python3 tools/build.py [CODE]           # validate → index → pdf → (drive, vidéo)

Sortie : `out/pdf/OKOHO_PCP_<CODE>_<Type>_v<version>.pdf` (Type : `Fiche` pour `seances/`, `Guide` pour `accueil/`). Gabarit : A4, Design System OKOHO 2.2 + mode Académie (`design/tokens.css`, polices `design/fonts/`).

Le gabarit ajoute lui-même : en-tête (logo, code · titre, fil de progression selon `jalon`), libellé PARTIE · MODULE ou ACCUEIL, titre, mention « Une formation OKOHO Consulting GmbH · Formateur : Dr. Bertrand Toumi », pied de page (contact, page), mentions finales (Anthropic, version, date des captures, ©). Le titre `#` et le bloc de mentions final du fichier source sont ignorés.

## Sources

- `seances/<CODE>/seance.md` : schéma `schema/seance.schema.json`.
- `accueil/<CODE>/document.md` : schéma `schema/document.schema.json` ; code `A00-NN` ; champs `code`, `titre`, `type: document`, `version`, `public` (`apprenants` | `formateur`), facultatifs `jalon`, `captures` (AAAA-MM-JJ), `glossaire`, `index`, `status`.

## Conventions Markdown

| Écrire | Résultat |
|---|---|
| `## Titre` | Chapitre numéroté (bloc bleu foncé, chiffre blanc, trait orange) |
| `::: objectifs` … `:::` | Encadré academie-tint « CE QUE VOUS SAUREZ FAIRE » |
| `::: livrable` … `:::` | Encadré academie-tint « VOTRE LIVRABLE » |
| `::: fil-rouge` … `:::` | Encadré blue-tint « CAS FIL ROUGE » |
| `::: erreurs` … `:::` | Cadre orange « ERREURS FRÉQUENTES » |
| `::: coup-de-pouce` + liste `1.` `2.` `3.` | Coups de pouce numérotés |
| `::: prompt` … `:::` | Cadre « CONSIGNE À COPIER » |
| `![Étape 3 : Cliquez sur …](captures/x.png)` | Capture avec légende ; fichier absent → cadre « Capture à venir » et avertissement |
| `- [ ]` / `- [x]` | Cases à cocher |
| Tableau Markdown | En-tête bleu foncé, lignes alternées |

Dans une séance, les titres `## Ce que vous saurez faire`, `## Votre livrable`, `## Cas fil rouge` et `## Erreurs fréquentes` deviennent automatiquement les encadrés correspondants. Les blocs `:::` ne s'imbriquent pas. Captures : dossier `captures/` à côté du fichier source.
