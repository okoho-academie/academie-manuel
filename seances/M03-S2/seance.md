---
code: M03-S2
partie: I
module: M03
titre: Protéger les données, respecter les droits
type: autonomie
outil: Claude Chat
appareil: smartphone
duree: {seance: 45, devoir: 30}
prerequis: [M02-S1, M03-S1]
echafaudage: 1
acces_defaut: programme
jalon: J1
livrable: Charte personnelle d'utilisation
competences:
  - code: M03-S2-C1
    jalon: J1-C4
    savoir_faire: Vous classez les données de votre client pilote en vert, orange et rouge.
    preuve: Votre livrable contient le tableau des données de votre client pilote, classées en trois couleurs.
    reussi_si: Au moins trois données par couleur, et le rouge contient les données sensibles de l'activité, comme les noms et notes d'élèves, les dossiers de patients, les salaires, les pièces d'identité et les données bancaires.
  - code: M03-S2-C2
    jalon: J1-C4
    savoir_faire: Vous rendez un document anonyme avant de le confier à Claude.
    preuve: Votre livrable montre le même extrait avant et après anonymisation.
    reussi_si: Dans la version envoyée à Claude, aucun nom, numéro, adresse précise ou visage ne permet de reconnaître une personne.
  - code: M03-S2-C3
    jalon: J1-C4
    savoir_faire: Vous rédigez la charte d'utilisation de Claude pour votre client pilote et vous la faites valider.
    preuve: Votre livrable contient la charte de six règles avec la mention de validation.
    reussi_si: Six règles courtes, dont une sur les données rouges et une sur les droits des personnes et des auteurs, et la mention « validé par ».
fil_client: {produit: "Charte des données du client pilote", page_dossier: 6}
glossaire: [Donnée sensible, Anonymiser, Charte d'utilisation, Feux des données, Instructions personnelles]
index: [Données personnelles, Donnée sensible, Anonymiser, Charte d'utilisation, Feux des données, Droit à l'image, Droits d'auteur, Confidentialité, Instructions personnelles, Données agrégées]
videos: {tutoriel: false, vitrine: false, shorts: 0, signature: false}
verifie: "2026-11-22"
version: "1.0"
captures: null
status: relecture
---

# M03-S2 · Protéger les données, respecter les droits

## Ce que vous saurez faire

| Vous savez… | Vous le prouvez… | C'est réussi si… |
|---|---|---|
| Vous classez les données de votre client pilote en vert, orange et rouge. | Votre livrable contient le tableau des données de votre client pilote, classées en trois couleurs. | Au moins trois données par couleur, et le rouge contient les données sensibles de l'activité, comme les noms et notes d'élèves, les dossiers de patients, les salaires, les pièces d'identité et les données bancaires. |
| Vous rendez un document anonyme avant de le confier à Claude. | Votre livrable montre le même extrait avant et après anonymisation. | Dans la version envoyée à Claude, aucun nom, numéro, adresse précise ou visage ne permet de reconnaître une personne. |
| Vous rédigez la charte d'utilisation de Claude pour votre client pilote et vous la faites valider. | Votre livrable contient la charte de six règles avec la mention de validation. | Six règles courtes, dont une sur les données rouges et une sur les droits des personnes et des auteurs, et la mention « validé par ». |

Ces trois compétences comptent pour le jalon **J1 · Utilisateur autonome** (compétence J1-C4 : vérifier les informations et respecter la confidentialité).

## Pourquoi c'est utile

Un client vous confie ses documents parce qu'il vous fait confiance. Une liste d'élèves, un registre de patients, une fiche de paie : si l'une de ces données sort, la confiance est perdue, et parfois la loi est enfreinte.

Le bon prestataire sait trois choses : quelles données ne sortent jamais, comment retirer les noms avant de travailler, et quelles règles il suit avec chaque client. Écrites sur une page, ces règles deviennent une charte. Elle rassure le client et elle vous protège.

Durée : 45 minutes, puis 30 minutes de travail personnel. Appareil : téléphone ou tablette.

## Avant de commencer

- [ ] L'application Claude est ouverte.
- [ ] Votre **fiche contexte** est sous la main.
- [ ] Vous avez un document réel de votre client pilote qui contient des noms ou des numéros : une liste, un registre, un tableau. **Ne l'envoyez pas encore à Claude.**
- [ ] Vous savez qui peut valider une règle chez votre client : le client lui-même, ou la personne qui a autorité dans votre structure.

## Ce que vous réutilisez

| Geste déjà appris | Séance | Où il sert aujourd'hui |
|---|---|---|
| La fiche contexte et la consigne R-T-C-F-C (fiche-outil 03) | M02-S1 | La fiche contexte vous dit quels publics et quelles données votre client possède (étape 1) |
| Trois questions avant d'utiliser une information (fiche-outil 06) | M03-S1 | Après l'anonymisation, vous vérifiez que la réponse de Claude n'invente aucun nom (étape 6) |
| Vos instructions personnelles (guide A00-06) | Parcours | Vous relisez ce que Claude sait de vous : aucune donnée rouge ne doit y figurer (étape 8) |

## Je vous montre

### Les feux des données

| Couleur | Règle | Exemples |
|---|---|---|
| Vert | Peut être confié à Claude | Horaires, services, textes publics, chiffres totaux (« 312 élèves ») |
| Orange | Seulement après anonymisation | Une liste de présence, des réponses de clients, un compte rendu de réunion |
| Rouge | Ne sort jamais | Noms et notes d'élèves, dossiers de patients, salaires, pièces d'identité, données bancaires, mots de passe |

La question à se poser : **si cette information était lue par un inconnu, quelqu'un serait-il gêné ou en danger ?** Si oui, elle est orange ou rouge.

### Anonymiser : trois gestes

| Geste | Avant | Après |
|---|---|---|
| Remplacer les noms | « Mbarga Paul, absent 4 jours » | « Élève A, absent 4 jours » |
| Retirer les numéros et adresses | « Tél. 6 99 … , quartier Nlongkak, porte bleue » | « [téléphone] , [quartier] » |
| Regrouper | Une ligne par élève | « 12 élèves absents plus de 3 jours » |

On anonymise **avant** d'envoyer, sur son téléphone. Demander à Claude de retirer les noms, c'est déjà lui avoir envoyé les noms.

### Les droits des autres

- **Droit à l'image :** une photo où l'on reconnaît une personne ne se publie qu'avec son accord ; pour un enfant, avec l'accord de ses parents.
- **Droits d'auteur :** le logo, le texte ou la photo d'un autre ne se copie pas sur la page de votre client. Utilisez les contenus de votre client ou des contenus créés pour lui.

## Nous faisons ensemble

**Étape 1 : lister les données.** Dans une nouvelle conversation nommée « Charte · client pilote », envoyez :

::: prompt
Voici la fiche contexte de mon client pilote : [collez votre fiche contexte]. Fais la liste des types de données que cette activité manipule chaque semaine : documents, listes, messages, photos, chiffres. Pour chacun, propose une couleur : vert (peut être confié à une intelligence artificielle), orange (seulement après anonymisation), rouge (ne sort jamais). Présente un tableau à trois colonnes : donnée, couleur, raison en une ligne. Ne me demande aucune donnée réelle.
:::

![Étape 1 : le tableau des données en trois couleurs](captures/etape-1.png)

**Étape 2 : corriger le classement.** Relisez le tableau. Vous connaissez votre client mieux que Claude. Changez une couleur si elle est fausse. Une donnée manque ? Ajoutez-la. Copiez le tableau final dans votre livrable.

**Étape 3 : choisir un extrait orange.** Prenez votre document réel de l'étape « Avant de commencer ». Copiez cinq lignes dans l'application Notes de votre téléphone, **pas dans Claude**.

**Étape 4 : anonymiser à la main.** Dans Notes : remplacez chaque nom par une lettre (Personne A, Personne B), chaque numéro par [numéro], chaque adresse par [quartier]. Si les lignes individuelles ne servent pas, regroupez-les en un total.

**Étape 5 : comparer.** Faites deux captures : l'extrait avant (gardez-la dans votre portfolio, jamais dans Claude) et l'extrait après.

## Un geste, trois contextes

Le geste de cette séance : avant d'envoyer, se demander « vert, orange ou rouge ? », et anonymiser ce qui est orange.

| Contexte | Ce que vous faites | Où |
|---|---|---|
| Guidé | La liste de présence anonymisée de l'exemple | Je vous montre |
| Transfert | Le fichier clients d'une boutique : noms et numéros remplacés, achats regroupés | Étape 7 |
| Client pilote | Un extrait réel de votre client, anonymisé, puis traité par Claude | Étapes 3 à 6 |

Un commerce, une école, un centre de santé : les données changent, la règle reste.

## Vous faites avec appui

**Étape 6 : travailler avec l'extrait anonyme.** Envoyez l'extrait anonymisé à Claude avec une tâche utile, par exemple :

::: prompt
Voici un extrait anonymisé de [type de document] : [collez l'extrait après]. Tâche : [résumer, compter, préparer un message général, faire un tableau]. Format : [format]. Contraintes : n'ajoute aucun nom ni aucun chiffre qui ne figure pas dans l'extrait.
:::

Relisez la réponse avec la fiche-outil 06 : Claude n'a inventé aucun nom ni aucun chiffre.

**Étape 7 : le transfert.** Une boutique veut remercier ses dix meilleurs clients. Sa liste contient noms, numéros et montants d'achat. Écrivez en trois lignes ce que la boutique peut confier à Claude et comment : par exemple, Claude écrit un message modèle avec [prénom], la boutique remplit les prénoms elle-même.

**Étape 8 : vos instructions personnelles.** Si vous avez suivi le guide A00-06, ouvrez une nouvelle conversation et demandez « Que sais-tu de moi ? ». Une donnée rouge apparaît (numéro, nom d'un élève ou d'un patient) ? Retirez-la de vos instructions personnelles et corrigez la mémoire, comme indiqué dans le guide.

**Étape 9 : écrire la charte.** Envoyez :

::: prompt
Tu es conseiller en protection des données pour une petite structure. Voici le tableau des données de mon client pilote : [collez votre tableau]. Rédige une charte d'utilisation de Claude en six règles courtes, une phrase chacune, pour [nom de l'activité]. Règles obligatoires : une règle sur les données rouges, une règle sur l'anonymisation, une règle sur le droit à l'image, une règle sur les droits d'auteur, une règle sur la vérification des informations, une règle sur la validation avant publication. Format : titre, six règles numérotées, une ligne « Validé par : … le … ». Ton simple, vouvoiement.
:::

**Étape 10 : faire valider.** Montrez la charte à votre client ou à la personne qui a autorité. Corrigez si elle le demande. Écrivez « Validé par [nom ou fonction] » avec la date.

Vérifiez votre travail :

- [ ] Le tableau a au moins trois données par couleur, et le rouge contient les données sensibles de l'activité
- [ ] L'extrait avant n'a jamais été envoyé à Claude
- [ ] L'extrait après ne permet de reconnaître personne
- [ ] La charte a six règles, dont les données rouges et les droits
- [ ] La mention « Validé par » est remplie

::: coup-de-pouce
1. **Indice.** Une donnée est rouge si elle concerne la santé, l'argent, l'identité ou un enfant, et qu'on peut savoir de qui il s'agit.
2. **Solution partielle.** Pour anonymiser vite : gardez la colonne utile (absences, montants, motifs), supprimez les colonnes nom, téléphone et adresse, et numérotez les lignes.
3. **Solution complète.** Charte d'une école : 1. Aucun nom ni aucune note d'élève n'est envoyé à Claude. 2. Les listes sont anonymisées ou regroupées avant tout usage. 3. Aucune photo d'élève n'est publiée sans l'accord écrit des parents. 4. Nous n'utilisons que nos propres textes, logos et photos. 5. Toute date, tout chiffre et toute règle sont vérifiés à la source avant envoi. 6. Rien n'est publié sans la validation du chef d'établissement. Validé par : le chef d'établissement.
:::

::: defi
**La charte pour le client.** Transformez votre charte en un message de cinq lignes que vous enverrez à un futur client pour expliquer comment vous protégez ses données. Il doit donner envie de vous confier le travail.
:::

## Pour votre client pilote

Cette séance produit la **page 6 de votre Dossier client pilote** : la charte des données du client pilote.

1. Ouvrez votre **Dossier client pilote** dans votre portfolio.
2. Page 6 : le tableau vert, orange, rouge, la charte validée, et un exemple de document anonymisé que vous avez pu traiter avec Claude.
3. Effet observé : ce que le client peut maintenant confier sans crainte, et ce qui reste chez lui.

::: structure
Pour votre propre structure, la charte dit « ce qui ne sort jamais de la structure ». Elle est validée par la personne qui en a le droit (direction, hiérarchie, conseil). Les rapports à la hiérarchie se préparent avec des chiffres regroupés, jamais avec la liste des personnes.
:::

## Vous faites seul

Avant la prochaine séance :

1. **Appliquez la charte** à une vraie tâche de votre client : un document orange anonymisé, puis traité par Claude.
2. **Relisez vos livrables déjà faits** (page web, messages, bibliothèque) : aucune donnée rouge, aucune photo ou texte d'un autre sans accord.
3. **Montrez votre charte à votre binôme.** Il vérifie les six règles et la mention « Validé par », puis écrit « vu par [prénom] » sur votre livrable.

Critères de qualité :

- Chaque règle de la charte tient en une phrase et se comprend sans explication.
- Aucun document du livrable ne permet de reconnaître une personne.
- La charte est validée par la bonne personne.

## Votre fiche-outil

**Fiche-outil 08 · Les feux des données.** À garder sur votre téléphone.

Avant d'envoyer quoi que ce soit à Claude :

1. **Vert ?** Envoyez.
2. **Orange ?** Anonymisez d'abord sur votre téléphone : noms en lettres, numéros et adresses retirés, ou totaux.
3. **Rouge ?** N'envoyez pas. Travaillez avec un modèle à trous, le client remplit lui-même.

Pour classer les données d'un nouveau client :

::: prompt
Voici la fiche contexte d'un client : [fiche contexte]. Liste les types de données qu'il manipule et classe-les en vert, orange, rouge, avec une raison en une ligne. Ne me demande aucune donnée réelle.
:::

La règle : on anonymise avant d'envoyer, jamais après.

## Cas fil rouge

Mme Ateba est infirmière-major d'un centre de santé intégré à Bafia. Chaque mois, elle passe une soirée sur le rapport des vaccinations pour le district. Elle voulait photographier le registre et l'envoyer à Claude : noms des enfants, dates de naissance, quartiers. Avec les feux des données, elle classe le registre en rouge. Elle compte d'abord à la main, par vaccin et par tranche d'âge, puis envoie seulement les totaux à Claude avec le modèle du district. Le rapport est prêt en quarante minutes. Sa charte de six règles, validée par le chef de centre, est affichée dans la salle de soins : plus personne ne photographie le registre.

## Erreurs fréquentes

- **Envoyer d'abord, anonymiser ensuite.** Une fois envoyée, la donnée est partie. On anonymise sur son téléphone, avant.
- **Croire qu'un prénom seul est anonyme.** Dans un petit quartier ou une petite classe, un prénom suffit pour reconnaître quelqu'un.
- **Oublier les photos.** Un visage, une plaque, un document en arrière-plan sont des données.
- **Copier le logo ou les photos d'un autre site.** Utilisez les contenus du client ou créez-les pour lui.
- **Écrire une charte que personne n'a validée.** Sans validation, ce n'est qu'un brouillon.

## Vérifiez vos acquis

Cochez seulement ce que vous venez de faire vous-même, sans aide.

- [ ] Vous avez classé les données de votre client en vert, orange et rouge, au moins trois par couleur. Sinon : étapes 1 et 2.
- [ ] Vous avez anonymisé un extrait réel avant de l'envoyer, et personne n'y est reconnaissable. Sinon : étapes 3 à 5.
- [ ] Votre charte a six règles et la mention « Validé par ». Sinon : étapes 9 et 10.
- [ ] Quiz S04-2 : au moins 6 bonnes réponses sur 8.

## Votre livrable

Un document nommé **S04-2_Prenom** (par exemple S04-2_Aicha), dans votre portfolio, avant la prochaine séance. Chaque élément prouve une compétence :

1. **Feux des données :** le tableau des données de votre client pilote, classées en vert, orange et rouge.
2. **Anonymisation :** la capture de l'extrait après anonymisation. L'extrait avant reste dans votre portfolio, dans un fichier à part, jamais dans Claude.
3. **Charte :** les six règles et la mention « Validé par ».

Et dans votre **Dossier client pilote**, la page 6 remplie.

### Comment votre livrable est évalué

| Niveau | Ce que montre votre livrable |
|---|---|
| 1 · Découverte | Un tableau ou une charte, mais incomplets, ou une donnée rouge visible dans le livrable. |
| 2 · Application guidée | Les trois éléments présents, aucune personne reconnaissable. |
| 3 · Autonomie | Niveau 2, avec la charte validée, un document anonymisé traité par Claude et la page 6 du Dossier client pilote remplie. |
| 4 · Transfert | Niveau 3, et la charte est appliquée chez le client (affichée, envoyée à l'équipe ou utilisée pour une vraie tâche). |

La séance est validée au niveau 3. Le jalon J1 demande au moins le niveau 2 à chaque livrable.

## Kit NotebookLM

Ajoutez cette fiche à votre notebook « Parcours Claude Pro ». Les sources et consignes de la semaine se trouvent dans le dossier « 03 · Réviser avec NotebookLM ».

## Mots-clés

Données personnelles · Donnée sensible · Anonymiser · Feux des données · Charte d'utilisation · Droit à l'image · Droits d'auteur · Données regroupées

---

Une formation OKOHO Consulting GmbH · Formateur : Dr. Bertrand Toumi
Claude est une marque d'Anthropic. Le Parcours Claude Pro est une formation indépendante proposée par OKOHO Consulting GmbH, sans partenariat avec Anthropic. Reproduction et diffusion interdites sans autorisation écrite d'OKOHO Consulting GmbH.
Version 1.0 · Fonctions vérifiées le 22.11.2026 (claude.com) · Captures d'écran réalisées le — · © 2026 OKOHO Consulting GmbH
