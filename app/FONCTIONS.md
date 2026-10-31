# Fonctions transversales · Application OKOHO Académie (v1)

Complète `ROLES.md`. Décidé avec Dr. Bertrand Toumi.

## 1. Notifications : e-mail et push
Canaux : e-mail (expéditeur academie@okoho.de) et notification push sur le téléphone (application installée, PWA ; permission demandée à la première connexion, expliquée en une phrase).
Chaque personne choisit dans son profil : e-mail, push ou les deux (par défaut : les deux).

| Événement | Apprenant | Formateur / Assistant |
|---|---|---|
| Séance de la semaine ouverte (vendredi) | ✅ | — |
| Rappel : séance en direct dans 1 heure | ✅ | ✅ |
| Devoir : échéance dans 24 heures, non rendu | ✅ | — |
| Rendu déposé | — | ✅ (résumé quotidien) |
| Rendu évalué, retour disponible | ✅ | — |
| Annonce publiée | ✅ | ✅ |
| Question posée / réponse reçue | ✅ réponse | ✅ question |
| Brouillon de l'Assistant à valider | — | ✅ Formateur, Admin |
| Jalon confirmé, attestation disponible | ✅ | ✅ |
Heures calmes : pas de push entre 21 h et 7 h, heure de Douala ; les messages attendent le matin.

## 2. Questions des apprenants : application et WhatsApp
- Dans chaque séance, bouton « Poser une question » : visible par l'apprenant et l'équipe (Formateur, Assistant, Admin) ; option « partager avec la cohorte » (FAQ de la séance).
- WhatsApp reste ouvert pour l'entraide rapide. Une question importante reçue sur WhatsApp est reportée dans l'application par l'équipe (bouton « Ajouter une question reçue ailleurs »), pour que la réponse reste dans la séance.
- Chaque question ouverte apparaît dans « À traiter » ; délai cible de réponse : 48 heures.

## 3. Attestation automatique par jalon
Source des critères : `manuel/jalons.yaml` (sans date) : titre du jalon, compétences démontrées (4 à 6 lignes), séances concernées, conditions.

Conditions par défaut d'un jalon :
1. Tous les livrables des séances du jalon rendus et évalués au niveau 2 ou plus.
2. Quiz des séances du jalon réussis à 70 % ou plus (meilleure tentative).
3. Présentation au Démo Day cochée par le Formateur.

Déroulement :
1. La vue « Jalons » montre pour chaque apprenant l'état des trois conditions (vert, orange, rouge).
2. Le Formateur clique « Confirmer le jalon » (possible seulement si tout est vert ; l'Admin peut forcer avec motif écrit, journalisé).
3. Le serveur génère aussitôt le PDF (A4 paysage, modèle `docs/attestation_modele.html`) avec : numéro unique ATT-C{cohorte}-J{n}-{0001}, nom, cohorte et période, compétences, livrables validés, niveau moyen, score quiz, date, signature image de Dr. Bertrand Toumi, QR code vers la page publique de vérification.
4. Le PDF est stocké, ajouté au portfolio, notifié par e-mail et push ; téléchargeable à tout moment.
5. Page publique `academie.okoho.de/verifier/<numéro>` : nom, jalon, date, statut valide ou révoqué. Aucune autre donnée.
6. Révocation (Admin seulement, motif écrit) : la page de vérification affiche « révoquée ».

Spécimen validé : `docs/Specimen_Attestation_J1.pdf`.
