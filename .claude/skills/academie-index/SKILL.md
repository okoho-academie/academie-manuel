---
name: academie-index
description: Tient le glossaire et l'index du Manuel OKOHO Académie à jour à partir des métadonnées des séances.
---

# Glossaire et index

- Les termes d'index et de glossaire vivent uniquement dans l'en-tête de chaque séance (`index`, `glossaire`) et dans `glossaire/glossaire.yaml`.
- Chaque terme de `glossaire` d'une séance doit exister dans `glossaire/glossaire.yaml` avec une définition française simple (une ou deux phrases) et la liste des séances.
- 5 à 10 termes d'index par séance ; un terme d'index d'une séance = occurrence principale (en gras dans l'index).
- Générer : `python3 tools/build_index.py` → `out/table-des-matieres.md`, `out/glossaire.md`, `out/index.md`. Ne jamais modifier `out/` à la main.
- Tri alphabétique français, accents ignorés au premier niveau (`tools/common.py`).
