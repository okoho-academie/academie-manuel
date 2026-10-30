---
name: academie-seance
description: Rédige ou complète une séance du Manuel OKOHO Académie dans seances/<CODE>/seance.md, conforme au schéma et au principe d'échafaudage.
---

# Rédiger une séance

Référence : `CLAUDE.md` (grundsätze, Scaffolding, Pflichtkennzeichnung), `schema/seance.schema.json`, `manuel/structure.yaml`.

- En-tête : copier code, titre, partie, module, livrable, outil, appareil depuis `structure.yaml` ; `echafaudage` = valeur de la partie (ou du module si surchargée).
- Corps, dans cet ordre : Ce que vous saurez faire · Pourquoi c'est utile · Je vous montre · Nous faisons ensemble · Vous faites avec appui (avec Coups de pouce 1 à 3) · Vous faites seul · Cas fil rouge · Erreurs fréquentes · Votre livrable · Kit NotebookLM · Mots-clés.
- Dosage selon `echafaudage` : 1 prompts complets et capture par étape ; 2 prompts à trous ; 3 checklist et critères ; 4 brief et critères.
- Français, « vous », phrases courtes. Exemples camerounais seulement dans « Cas fil rouge ». Aucune référence à une autre semaine.
- Captures : emplacement `![Étape n : action](captures/etape-n.png)` ; vraie interface Claude uniquement.
- Terminer par la mention OKOHO, la mention Anthropic, la version et la date des captures.
- Aucune date, aucune année, aucun numéro de semaine, aucun nom de cohorte : la séance sert à toutes les cohortes, dans n’importe quel ordre, et au parcours en autonomie. Échéance : « avant la prochaine séance ». Groupe : {{groupe}}. Les dates et semaines viennent de parcours/cohorte-N.yaml au build.
- Ne jamais inventer de fonction ou de prix de Claude.
