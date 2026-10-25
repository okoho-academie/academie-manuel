---
description: Produit une séance de l'OKOHO Académie de bout en bout (validate → build → commit sur seance/<CODE>)
argument-hint: <CODE, ex. M02-S1>
---

Séance à produire : $ARGUMENTS

1. `git pull`, puis `git checkout -B seance/$ARGUMENTS`.
2. Charger le skill `academie-seance`. Lire `CLAUDE.md`, `manuel/structure.yaml` (entrée $ARGUMENTS) et `schema/seance.schema.json`.
3. Créer ou compléter `seances/$ARGUMENTS/seance.md` : en-tête conforme au schéma, contenu en français selon les quatre phases et le niveau d'échafaudage de la partie.
4. `python3 tools/validate.py` : corriger toute ERREUR avant de continuer. Signaler les AVERT.
5. Nouveaux termes : les ajouter à `glossaire/glossaire.yaml` (skill `academie-index`).
6. `python3 tools/build.py $ARGUMENTS`.
7. `git add seances/$ARGUMENTS glossaire && git commit -m "seance($ARGUMENTS): <résumé>"`. Ne pas fusionner dans `main` sans validation de Dr. Bertrand Toumi.
8. Répondre en allemand : fichiers modifiés, résultat de validate, TODO restants (pdf, drive, vidéo).
