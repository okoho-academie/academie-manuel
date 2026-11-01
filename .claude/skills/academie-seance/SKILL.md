---
name: academie-seance
description: Rédige ou complète une séance du Manuel OKOHO Académie dans seances/<CODE>/seance.md, conforme au schéma et au principe d'échafaudage.
---

# Rédiger une séance

Référence : `CLAUDE.md` (grundsätze, Scaffolding, Pflichtkennzeichnung), `schema/seance.schema.json`, `manuel/structure.yaml`.

- Avant d'écrire, répondre aux trois questions (CLAUDE.md, « Drei Leitfragen ») : que sait faire l'apprenant à la fin, comment le prouve-t-il, à quoi le reconnaît-on. Les écrire dans `competences` (2 à 4, `savoir_faire` commence par « Vous », `jalon` = compétence de `manuel/jalons.yaml`).
- En-tête : copier code, titre, partie, module, livrable, outil, appareil depuis `structure.yaml` ; `echafaudage` = valeur de la partie (ou du module si surchargée).
- Corps, dans cet ordre : Ce que vous saurez faire (tableau Vous savez… / Vous le prouvez… / C'est réussi si…, textes identiques aux métadonnées) · Pourquoi c'est utile · Je vous montre · Nous faisons ensemble · Vous faites avec appui (avec Coups de pouce 1 à 3) · Vous faites seul · Cas fil rouge · Erreurs fréquentes · Vérifiez vos acquis (une case par compétence, avec l'étape à refaire) · Votre livrable (un élément par compétence, sous-section « Comment votre livrable est évalué », niveaux 1 à 4) · Kit NotebookLM · Mots-clés.
- Dosage selon `echafaudage` : 1 prompts complets et capture par étape ; 2 prompts à trous ; 3 checklist et critères ; 4 brief et critères.
- Français, « vous », phrases courtes. Exemples camerounais seulement dans « Cas fil rouge ». Aucune référence à une autre semaine.
- Captures : emplacement `![Étape n : action](captures/etape-n.png)` ; vraie interface Claude uniquement.
- Terminer par la mention OKOHO, la mention Anthropic, la version et la date des captures.
- Aucune date, aucune année, aucun numéro de semaine, aucun nom de cohorte : la séance sert à toutes les cohortes, dans n’importe quel ordre, et au parcours en autonomie. Échéance : « avant la prochaine séance ». Groupe : {{groupe}}. Les dates et semaines viennent de parcours/cohorte-N.yaml au build.
- Ne jamais inventer de fonction ou de prix de Claude.
- Quiz `quiz/<CODE>.yaml` : chaque question porte `competence`, chaque compétence a au moins une question, seuil `reussite` à 70 %.
- Séance en direct : la dramaturgie contient la grille d'observation et le contrôle de sortie.
