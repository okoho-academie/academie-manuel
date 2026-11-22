---
code: A00-06
titre: "Apprendre à Claude à vous connaître"
type: document
public: apprenants
jalon: J1
version: "1.0"
captures: "2026-11-22"
---

::: objectifs
- Vous faites mener par Claude un entretien sur vous-même et vous obtenez le texte de vos instructions personnelles.
- Vous vérifiez ce que Claude a retenu de vous et vous corrigez ce qui est faux ou manque.
- Vous créez un projet pour votre client pilote, avec ses propres instructions.
:::

## Pourquoi c'est utile

Sans réglage, Claude vous traite comme un inconnu à chaque conversation. Vous répétez qui vous êtes, ce que vous faites, comment vous voulez la réponse. Vous perdez du temps et les réponses restent générales.

Claude peut vous connaître à trois niveaux :

| Niveau | Ce que c'est | Où | Quand ça s'applique |
|---|---|---|---|
| **Instructions** | Le texte que vous écrivez sur vous et sur la façon de vous répondre | Réglages de votre compte | Dans toutes vos conversations |
| **Mémoire** | Ce que Claude retient de lui-même au fil de vos conversations | Réglages de votre compte, rubrique Memory | Dans les conversations suivantes |
| **Projet** | Un espace par client, avec ses instructions et ses fichiers | Menu Projets | Seulement dans les conversations de ce projet |

Ce guide vous fait faire les trois, dans cet ordre. Le plus simple : c'est Claude qui vous pose les questions.

Durée : environ 1 heure. Appareil : téléphone, tablette ou ordinateur. Pour les réglages, l'ordinateur ou le navigateur du téléphone (claude.ai) est le plus sûr.

| Vous savez… | Vous le prouvez… | C'est réussi si… |
|---|---|---|
| Vous faites mener par Claude un entretien sur vous-même et vous obtenez le texte de vos instructions personnelles. | Vous déposez dans votre portfolio la capture de vos instructions enregistrées dans les réglages. | Les instructions contiennent les six rubriques (qui je suis, mes activités, mon client pilote, comment me répondre, ce que je ne veux pas, langue), tiennent sur un écran et ne contiennent aucune donnée sensible. |
| Vous vérifiez ce que Claude a retenu de vous et vous corrigez ce qui est faux ou manque. | Dans une nouvelle conversation, vous demandez « Que sais-tu de moi ? », vous faites une correction, et vous déposez la capture. | Claude cite votre activité, votre client pilote et votre façon préférée de recevoir les réponses, sans que vous les ayez écrits dans cette conversation. |
| Vous créez un projet pour votre client pilote, avec ses propres instructions. | Dans une nouvelle conversation du projet, vous demandez « Quel est le blocage de mon client pilote ? » et vous déposez la capture. | Claude nomme le blocage et ce qu'il coûte, tel qu'il figure dans votre fiche contexte. |

## Avant de commencer

- [ ] Votre compte Claude est ouvert (guide **A00-01 · Bien démarrer**).
- [ ] Votre fiche contexte du client pilote est prête (guide **A00-05**, étape 3, ou séance M02-S1).
- [ ] Votre portfolio est ouvert (guide **A00-04**).
- [ ] Vous avez 45 minutes sans interruption pour l'entretien.

**Ce que vous ne donnez jamais à Claude, ni dans l'entretien ni dans les réglages :** mot de passe, numéro de carte d'identité ou de passeport, numéro de compte bancaire ou Mobile Money, données de santé, noms de patients, d'élèves ou de clients. Pour votre client pilote : des groupes (« les parents », « les patients du matin »), jamais des personnes.

## Étape 1 : l'entretien

Ouvrez une **nouvelle conversation**. Nommez-la « Mon profil Claude ». Copiez ce message en entier, sans rien changer :

::: prompt
Je veux que tu me connaisses bien pour mieux m'aider. Mène un entretien avec moi.

Règles :
- Pose une seule question à la fois et attends ma réponse.
- Douze questions au maximum, en français simple.
- Si ma réponse est vague, demande un exemple concret.
- Ne me demande jamais de mot de passe, de numéro de pièce d'identité, de compte bancaire ni de données de santé.

Thèmes, dans cet ordre :
1. Qui je suis : prénom, ville, métier ou situation.
2. Mes activités : ce que je fais chaque semaine, pour qui.
3. Mon client pilote : son activité, ses publics, son blocage et ce qu'il coûte.
4. Mes outils et mon appareil : téléphone, ordinateur, WhatsApp, autres.
5. Comment je veux tes réponses : longueur, ton, format (liste, tableau, texte à copier).
6. Ce que je ne veux pas : ce qui m'agace ou me fait perdre du temps dans tes réponses.
7. Ma langue : la langue de tes réponses et le niveau de langue.

À la fin de l'entretien, donne-moi trois blocs séparés, prêts à copier :
BLOC A · Mes instructions personnelles : six rubriques (Qui je suis, Mes activités, Mon client pilote, Comment me répondre, Ce que je ne veux pas, Langue), phrases courtes, un écran au maximum.
BLOC B · À retenir : cinq à huit faits sur moi, une ligne chacun.
BLOC C · Instructions du projet client pilote : le contexte du client, son blocage, le ton à utiliser, ce que Claude ne doit jamais inventer.

Commence par la première question.
:::

Répondez à chaque question comme à une personne qui vous aide. Des réponses concrètes donnent de meilleurs résultats : « Je réponds aux clients surtout le soir sur WhatsApp » vaut mieux que « Je travaille beaucoup ».

À la fin, relisez les trois blocs. Une ligne est fausse ? Écrivez :

::: prompt
Corrige dans le bloc [A, B ou C] : [ce qui est faux] devient [la bonne information]. Redonne-moi le bloc complet.
:::

## Étape 2 : enregistrer vos instructions

1. Touchez ou cliquez vos **initiales** en bas à gauche, puis **Settings** (Paramètres).
2. Ouvrez **Your Claude**, puis la rubrique **Instructions**. Dans l'ancien affichage : **Account**, puis **Instructions for Claude**.
3. Collez le **BLOC A**. Enregistrez.
4. Faites une capture de vos instructions enregistrées. Déposez-la dans votre portfolio sous le nom **A00-06_Prenom_1.png**.

Les libellés de ce guide sont ceux de l'interface en anglais. Si votre interface est en français, cherchez les mêmes rubriques sous leur nom traduit. Vous ne trouvez pas le réglage dans l'application ? Ouvrez **claude.ai** dans le navigateur.

Les instructions s'appliquent aux **nouvelles** conversations, pas à celle qui est déjà ouverte.

## Étape 3 : vérifier et corriger la mémoire

1. Dans **Settings**, puis **Your Claude**, vérifiez que **Generate memory from chats** est activé.
2. Revenez à la conversation « Mon profil Claude ». Envoyez le **BLOC B** avec cette phrase devant :

::: prompt
Retiens ces informations sur moi pour nos prochaines conversations :
[collez ici le BLOC B]
:::

3. Ouvrez une **nouvelle conversation** et envoyez :

::: prompt
Que sais-tu de moi ? Réponds en cinq lignes : mon activité, mon client pilote, comment je veux tes réponses, ce que je ne veux pas, ma langue.
:::

4. Une information est fausse ou manque ? Corrigez-la tout de suite :

::: prompt
Corrige ce que tu sais de moi : [information fausse] est faux. La bonne information est : [information juste].
:::

Pour oublier une information : « Oublie que [information]. »

5. Faites une capture de la réponse et de votre correction. Déposez-la sous le nom **A00-06_Prenom_2.png**.

Pour voir tout ce que Claude a retenu : **Settings**, puis **Your Claude**, puis **Manage** à côté de **Your memory**. La liste s'affiche sous **Topics**. Vous pouvez y modifier ou supprimer chaque élément.

**Bon à savoir.** La mémoire existe aussi dans le plan gratuit. La recherche dans vos anciennes conversations (**Search and reference chats**) est réservée aux plans payants. Une conversation en mode incognito (icône fantôme en haut à droite) n'utilise pas la mémoire et n'y ajoute rien.

## Étape 4 : le projet de votre client pilote

1. Ouvrez **Projects** (Projets) dans le menu, puis créez un projet. Nom : l'activité de votre client pilote, sans nom de famille, par exemple « Boutique de pagnes · Bonamoussadi ».
2. Dans les instructions du projet, collez le **BLOC C**.
3. Ajoutez votre **fiche contexte** comme fichier du projet.
4. Dans ce projet, ouvrez une **nouvelle conversation** et envoyez :

::: prompt
Quel est le blocage de mon client pilote, et que lui coûte-t-il ?
:::

5. Claude répond avec le blocage de votre fiche ? C'est réussi. Faites une capture et déposez-la sous le nom **A00-06_Prenom_3.png**.

Chaque projet a sa propre mémoire. Dans un projet, Claude utilise la mémoire de ce projet et votre mémoire générale, pas celle des autres projets. Un projet par client : les informations ne se mélangent pas.

## Étape 5 : entretenir, une fois par semaine

Claude vous connaît mieux chaque semaine si vous lui donnez l'occasion de faire le point. Une fois par semaine, dans une nouvelle conversation :

::: prompt
Voici mes instructions personnelles actuelles : [collez votre BLOC A]. D'après nos échanges de cette semaine, qu'est-ce qui manque ou n'est plus juste ? Propose une version mise à jour, toujours en six rubriques et sur un écran.
:::

Relisez. Gardez seulement ce qui est vrai. Collez la nouvelle version dans **Instructions**.

::: coup-de-pouce
1. Claude pose plusieurs questions d'un coup ? Répondez : « Une seule question à la fois, s'il te plaît. »
2. Claude ne connaît rien de vous dans la nouvelle conversation ? Vérifiez que vous avez enregistré les instructions (étape 2) et que la conversation n'est pas en mode incognito.
3. Le BLOC A est trop long ? Écrivez : « Raccourcis le bloc A à dix lignes. Garde les six rubriques. »
:::

::: erreurs
- **Tout raconter dans les instructions.** Un écran suffit. Les détails d'un client vont dans son projet, pas dans vos instructions personnelles.
- **Coller le BLOC C dans vos instructions personnelles.** Le contexte d'un client reste dans son projet.
- **Mettre des données sensibles.** Pas de mot de passe, pas de pièce d'identité, pas de compte, pas de noms de patients, d'élèves ou de clients.
- **Ne jamais vérifier.** La mémoire peut retenir une information fausse. « Que sais-tu de moi ? » une fois par semaine.
:::

::: fil-rouge
Aïcha est infirmière à Garoua et prépare des contenus de prévention pour le centre de santé de son quartier, son client pilote. Pendant l'entretien, Claude lui demande un exemple concret de ce qui l'agace : « Les réponses trop longues que je ne peux pas lire entre deux patients. » Son BLOC A dit : « Réponses de cinq lignes au maximum, puis un texte prêt à copier pour WhatsApp. » Dans le projet « Centre de santé · prévention », le BLOC C précise : « Ne jamais inventer d'horaires ni de tarifs, toujours demander au centre. » Le lendemain, dans une nouvelle conversation, Claude lui répond en cinq lignes, sans qu'elle le redemande.
:::

::: livrable
Dans votre portfolio, avant la prochaine séance en direct : **A00-06_Prenom_1.png** (instructions enregistrées), **A00-06_Prenom_2.png** (« Que sais-tu de moi ? » et correction), **A00-06_Prenom_3.png** (projet client pilote).
:::
