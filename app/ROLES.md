# Rôles et droits · Application OKOHO Académie (v1)

Décidé avec Dr. Bertrand Toumi. Source de vérité pour `supabase/schema.sql` (RLS), `lib/acces.ts` et l'interface.
Un rôle s'applique **par cohorte** (table `membres`), sauf Administrateur (global).

| Rôle | Principe |
|---|---|
| Administrateur | Tout, toutes cohortes, rôles, suppression, réglages, journal |
| Formateur | Dirige pédagogiquement ses cohortes. Ne crée pas de cohorte |
| Assistant | Aide à la gestion : voit, relance, répond, inscrit ; ne décide pas, ne supprime pas |
| Apprenant | Apprend, rend, voit ses propres données et la galerie consentie |
| Responsable entreprise (plus tard) | Lit la progression des personnes de son entreprise |

Légende : ✅ autorisé · 👁 lecture · ✏️ brouillon validé par Formateur ou Admin · — interdit

| Domaine | Fonction | Admin | Formateur | Assistant | Apprenant |
|---|---|---|---|---|---|
| Cohortes | Créer (nom, début, jour, heure, lien Teams, calendrier) | ✅ | — | — | — |
| | Modifier, décaler une séance, ajouter une pause | ✅ | ✅ siennes | — | — |
| | Archiver | ✅ | — | — | — |
| Personnes | Inscrire des apprenants (un par un ou liste) | ✅ | ✅ siennes | ✅ siennes | — |
| | Voir le profil (nom, e-mail, téléphone) | ✅ | ✅ | ✅ | soi |
| | Voir le diagnostic d'entrée | ✅ | ✅ | — | soi |
| | Désactiver, supprimer | ✅ | — | — | — |
| | Attribuer les rôles Formateur, Assistant | ✅ | — | — | — |
| Contenus | Lire les séances | ✅ | ✅ | ✅ | ouvertes |
| | Ouvrir par groupe (matrice) | ✅ | ✅ | — | — |
| | Ouvrir pour une personne | ✅ | ✅ | ✏️ | — |
| Devoirs | Créer le devoir de la semaine, fixer l'échéance | ✅ | ✅ | — | — |
| | Prolonger l'échéance d'une personne | ✅ | ✅ | ✏️ | — |
| Rendus | Déposer, remplacer jusqu'à l'évaluation | — | — | — | ✅ |
| | Voir les rendus | ✅ | ✅ | 👁 | siens |
| | Évaluer (niveau 1 à 4) et commenter | ✅ | ✅ | ✏️ | — |
| | Partager un rendu dans la galerie de la cohorte | — | — | — | ✅ consentement par rendu |
| Quiz | Passer (tentatives illimitées, meilleur score retenu, explication après chaque réponse) | — | — | — | ✅ |
| | Voir les résultats | ✅ | ✅ | 👁 | siens |
| Progression | Vue cohorte et personne, alerte « en retard » | ✅ toutes | ✅ siennes | 👁 siennes | sienne |
| | Export (tableur, PDF) | ✅ | ✅ | — | sienne |
| Jalons | Confirmer un jalon | ✅ | ✅ | — | — |
| | Émettre l'attestation (QR) | ✅ | — | — | télécharger |
| Communication | Annonce à la cohorte | ✅ | ✅ | ✏️ | lire |
| | Relance individuelle (devoir manquant) | ✅ | ✅ | ✅ | — |
| | Questions des apprenants | répondre | répondre | répondre | poser |
| Système | Journal des modifications | ✅ | — | — | — |
| | Réglages, design, intégrations | ✅ | — | — | — |

## Règles transversales
- Toute action ✏️ crée un brouillon visible dans « À valider » du Formateur et de l'Admin ; rien n'est envoyé avant validation.
- Toute action est journalisée (qui, quoi, quand).
- Données minimales : l'Assistant ne voit ni diagnostic ni données contractuelles. Les contrats restent hors de l'application.
- Suppression de compte : Admin seulement, après export proposé à la personne.
