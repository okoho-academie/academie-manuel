# Handoff Claude Code · Application OKOHO Académie v1

Commanditaire : Dr. Bertrand Toumi (OKOHO Consulting GmbH). Décisions validées le 31.10. Langue de l'interface : français, « vous ».
Lire d'abord : `../CLAUDE.md`, `ROLES.md`, `FONCTIONS.md`, `README_APP.md`, `../schema/seance.schema.json`, `../parcours/cohorte-1.yaml`, `../quiz/*.yaml`, `../design/tokens.json`.

## 1. Objectif et échéances
| Livraison | Contenu | En ligne |
|---|---|---|
| L1 · Apprenants | Connexion, Ma semaine, Parcours, Séance, dépôt des rendus, quiz, annonces (lecture), questions, portfolio, PWA installable, mode économie de données | **mardi 03.11** |
| L2 · Équipe | Devoirs, matrice d'ouverture, progression, file de correction avec brouillon Claude, annonces, « À traiter », bilan hebdomadaire, jalons et attestations | **vendredi 06.11** |
| Étape 14.11 | Évaluation entre pairs (galerie), formulaire « Nouvelle cohorte », filigrane nominatif des PDF, offres Autonomie et Entreprise (structure), notifications complètes | 14.11 |
| Étape J1 (28.11) | Données produit (taux d'achèvement, abandons, satisfaction par jalon), témoignages avec consentement | 28.11 |
| Plus tard | Paiement (Stripe) dès la première vente, version Play Store (TWA), anglais et allemand | sur décision |

Séance 01 en direct le samedi 07.11 : les apprenants utilisent l'application dès cette séance. Google Drive reste la solution de secours pour chaque fonction.

## 2. Décisions fonctionnelles (toutes validées)
- Application web installable (PWA) : icône, plein écran, push, hors ligne. Pas de magasin d'applications en v1.
- Connexion : Google (OAuth) + lien par e-mail. Aucun mot de passe.
- Rôles par cohorte selon `ROLES.md` (Admin, Formateur, Assistant, Apprenant ; Responsable entreprise plus tard).
- Rendus : dépôt dans l'application (photo, PDF, texte), remplaçable jusqu'à l'évaluation ; galerie de cohorte avec consentement par rendu.
- Quiz dans l'application depuis `quiz/*.yaml` : tentatives illimitées, meilleur score, explication après chaque réponse.
- Notifications e-mail (academie@okoho.de) et push ; préférences par personne ; heures calmes 21 h à 7 h (Douala). Détail : `FONCTIONS.md` §1.
- Questions dans l'application (FAQ de séance) et report depuis WhatsApp. `FONCTIONS.md` §2.
- Attestation PDF générée automatiquement à la confirmation du jalon, vérification publique par QR. `FONCTIONS.md` §3, modèle `docs/attestation_modele.html`.
- Optimisations v1 : mode économie de données par défaut (séance hors ligne, vidéo basse qualité ou audio, fiche PDF) ; bouton unique « Mon prochain pas » et barre de progression vers le jalon ; bouton « Copier la consigne » sur chaque prompt ; file de correction triée par échéance avec grille en un clic et brouillon de retour par l'API Claude ; bilan hebdomadaire automatique le samedi après la séance ; liste unique « À traiter » ; niveau Organisation dans le modèle de données ; structure multilingue (fr seul rempli).

## 3. Modèle de données (Supabase, RLS partout)
Étendre `supabase/schema.sql` par migrations versionnées :
`organisations` (OKOHO par défaut) → `cohortes` (ex-`groupes` : nom, début, jour, heure, fuseau Africa/Douala, lien visio, calendrier) → `membres` (personne, cohorte, rôle) · `profiles` (nom, e-mail, téléphone, langue, préférences de notification) · `regles_acces` · `devoirs` (séance, cohorte, consigne, échéance, prolongations par personne) · `rendus` (fichier dans Storage privé, texte, statut, partage galerie) · `evaluations` (niveau 1 à 4, grille, retour, brouillon_ia, auteur) · `quiz_tentatives` · `progression` · `annonces` · `questions` / `reponses` · `brouillons_a_valider` (type, contenu, auteur, statut) · `notifications` + `push_abonnements` · `jalons` + `jalons_conditions` · `attestations` (numéro unique, PDF, statut valide/révoquée) · `journal` (qui, quoi, quand).
Les droits de `ROLES.md` sont la spécification des politiques RLS ; un test par ligne du tableau.

## 4. Pistes parallèles (sous-agents, worktrees)
0 · Contrat (en premier, 2 h) : migrations, types TypeScript, interfaces entre pistes, critères d'acceptation. Toutes les pistes partent de ce contrat.
A · Infrastructure : projet Supabase région Francfort (eu-central-1), Storage privé, OAuth Google, envoi e-mail (fournisseur à vérifier, coût et limites datés), Vercel (Root `app`, fichiers hors racine inclus), domaine academie.okoho.de, clés VAPID, clé API Claude côté serveur.
B · Comptes et droits : connexion, rôles par cohorte, RLS, `lib/acces.ts` étendu (ouvertures programmées vendredi 00:00 Douala), journal.
C · Contenus et quiz : séances et accueil depuis le dépôt, Ma semaine depuis `parcours/cohorte-*.yaml`, quiz depuis YAML, jalons depuis `manuel/jalons.yaml` (à créer, sans date ; textes validés par Bertrand).
D · Interface : écrans apprenants puis équipe, design `design/tokens.json` (Montserrat, Open Sans, bleu #2C5697, orange #FFA142, academie-tint #FFF4E8), téléphone d'abord, PWA, hors ligne, économie de données.
E · Qualité : tests RLS par rôle, parcours complet sur téléphone Android en 3G simulée, accessibilité, `get_advisors` Supabase sans alerte de sécurité.

## 5. Critères d'acceptation L1 (03.11)
1. Un apprenant invité se connecte avec Google ou par lien e-mail sur un téléphone Android, installe l'application, voit Ma semaine en moins de 5 s en 3G simulée.
2. Il voit S00 ouvert et S01 « Disponible le vendredi » jusqu'au 06.11 00:00 Douala.
3. Il dépose une photo pour un devoir, la remplace, la voit dans son portfolio.
4. Il passe un quiz, recommence, son meilleur score s'affiche.
5. Il pose une question dans une séance.
6. Il ne voit aucune donnée d'une autre personne hors galerie consentie (test RLS).
7. Tout le texte visible est en français, sans faute, sans date en dur dans les sources.

## 6. Critères d'acceptation L2 (06.11)
1. Le Formateur crée le devoir S01, fixe l'échéance, ouvre une séance pour une personne.
2. La file de correction montre les rendus par échéance ; un clic sur la grille ; le brouillon Claude apparaît ; le Formateur valide ; l'apprenant reçoit e-mail et push.
3. L'Assistant inscrit un apprenant, envoie une relance, propose une prolongation qui arrive dans « À valider » ; il ne peut ni supprimer ni voir le diagnostic (test RLS).
4. Confirmer un jalon (données de test) produit le PDF conforme au spécimen, vérifiable via QR.
5. Le bilan hebdomadaire est généré automatiquement et téléchargeable.

## 7. Règles
- Aucun e-mail ni push vers de vrais apprenants avant le « OK invitations » de Bertrand (prévu jeudi 05.11 au plus tard, idéalement mardi 03.11 après son test).
- Aucune donnée personnelle, aucun secret dans le dépôt. Secrets dans Vercel et Supabase uniquement.
- Création de comptes ou projets chez des tiers (Supabase, Vercel, Google Cloud, fournisseur e-mail, Anthropic API) : approuvée le 31.10 ; avant chaque création, indiquer le plan gratuit utilisé, ses limites et la date de vérification.
- Branche `app/v1`, petits commits, merge vers `main` après validation de Bertrand ; `python3 tools/validate.py` et `npm test` verts avant chaque merge.
- Ce que Bertrand doit faire lui-même (minimum) : clics de consentement OAuth dans Google Cloud Console (pas à pas fourni), une entrée DNS (valeur exacte fournie), test personnel, « OK invitations ».

## 8. Compte rendu quotidien à Bertrand (en allemand)
Format : livré · en cours · bloqué (avec ce dont il a besoin) · prochaine étape pour lui (outil, lieu, texte exact). Mettre à jour le Cockpit 07 dans `academie-pilotage` à chaque changement d'état.

## 9. Feuille de route automatique
Après L2, enchaîner sans nouvelle demande : étape 14.11 (à partir du 07.11), étape J1 (à partir du 21.11), puis éléments « plus tard » seulement sur décision. Chaque étape commence par un plan court envoyé à Bertrand.
