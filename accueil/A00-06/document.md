---
code: A00-06
titre: "Apprendre à Claude à vous connaître"
type: document
public: apprenants
jalon: J1
version: "1.1"
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

| Niveau | Ce que c'est | Quand ça s'applique |
|---|---|---|
| **Instructions** | Le texte que vous écrivez sur vous et sur la façon de vous répondre | Dans toutes vos nouvelles conversations |
| **Mémoire** | Ce que Claude retient au fil de vos conversations | Dans les conversations suivantes |
| **Projet** | Un espace par client, avec ses instructions et ses fichiers | Seulement dans les conversations de ce projet |

Vous n'avez rien à chercher seul. Une seule consigne fait de Claude votre accompagnateur : il vous pose les questions, écrit les textes, puis vous dit à chaque étape où toucher, quoi copier et quoi activer. Vous avancez à votre rythme, une étape à la fois.

Durée : environ 1 heure. Appareil : le téléphone suffit. Si un réglage est introuvable dans l'application, ouvrez **claude.ai** dans le navigateur.

| Vous savez… | Vous le prouvez… | C'est réussi si… |
|---|---|---|
| Vous faites mener par Claude un entretien sur vous-même et vous obtenez le texte de vos instructions personnelles. | Vous déposez dans votre portfolio la capture de vos instructions enregistrées dans les réglages. | Les instructions contiennent les six rubriques (qui je suis, mes activités, mon client pilote, comment me répondre, ce que je ne veux pas, langue), tiennent sur un écran et ne contiennent aucune donnée sensible. |
| Vous vérifiez ce que Claude a retenu de vous et vous corrigez ce qui est faux ou manque. | Dans une nouvelle conversation, vous demandez « Que sais-tu de moi ? », vous faites une correction, et vous déposez la capture. | Claude cite votre activité, votre client pilote et votre façon préférée de recevoir les réponses, sans que vous les ayez écrits dans cette conversation. |
| Vous créez un projet pour votre client pilote, avec ses propres instructions. | Dans une nouvelle conversation du projet, vous demandez « Quel est le blocage de mon client pilote ? » et vous déposez la capture. | Claude nomme le blocage et ce qu'il coûte, tel qu'il figure dans votre fiche contexte. |

## Ce que vous réutilisez

| Geste | Appris dans | Utilisé ici pour |
|---|---|---|
| Les cinq éléments d'une bonne consigne (R, T, C, F, C) | M02-S1 | Comprendre pourquoi la consigne d'accompagnement fonctionne |
| Envoyer une capture d'écran à Claude | M01-S2 | Montrer à Claude où vous êtes quand vous ne trouvez pas un réglage |
| Corriger par un tour précis | M02-S2 | Corriger un bloc ou une information fausse |
| La fiche contexte du client pilote | M02-S1 ou guide A00-05 | Remplir le projet de votre client pilote |

## Avant de commencer

- [ ] Votre compte Claude est ouvert (guide **A00-01 · Bien démarrer**).
- [ ] Votre fiche contexte du client pilote est prête (guide **A00-05**, étape 3, ou séance M02-S1).
- [ ] Votre portfolio est ouvert (guide **A00-04**).
- [ ] Vous avez une heure sans interruption.

**Ce que vous ne donnez jamais à Claude :** mot de passe, numéro de carte d'identité ou de passeport, numéro de compte bancaire ou Mobile Money, données de santé, noms de patients, d'élèves ou de clients. Pour votre client pilote : des groupes (« les parents », « les patients du matin »), jamais des personnes.

## Étape 1 : envoyer la consigne d'accompagnement

Ouvrez une **nouvelle conversation**. Nommez-la « Mon profil Claude ». Copiez le message ci-dessous **en entier**, sans rien changer, et envoyez-le.

::: prompt
R · RÔLE
Tu es mon accompagnateur pour régler mon compte Claude. Je suis débutant : tu m'expliques avec des mots simples, en français, des phrases courtes.

T · TÂCHE
Tu fais trois choses, dans cet ordre, et tu attends ma réponse à chaque fois :
1. Tu me poses des questions pour bien me connaître.
2. Tu écris pour moi trois textes à copier.
3. Tu me guides, étape par étape, pour les mettre au bon endroit et vérifier que ça marche.

C · CONTEXTE
Voici où se trouvent les réglages (aide officielle de Claude, interface en anglais) :
- Instructions personnelles : mes initiales en bas à gauche › Settings › Your Claude › Instructions. Ancien affichage : Settings › Account › Instructions for Claude.
- Mémoire : Settings › Your Claude › « Generate memory from chats » doit être activé. Pour voir ce que tu as retenu : Manage, à côté de Your memory, puis Topics.
- Projets : menu Projects › créer un projet › instructions du projet et fichiers.
- Les instructions s'appliquent aux nouvelles conversations seulement.
Si mon écran ne correspond pas à ces indications, ne devine pas : demande-moi une capture d'écran et guide-moi à partir de ce que tu vois.

F · FORMAT
Partie 1, l'entretien : une seule question à la fois, douze questions au maximum, sur ces thèmes dans cet ordre : qui je suis (prénom, ville, métier ou situation) ; mes activités chaque semaine et pour qui ; mon client pilote (activité, publics, blocage et ce qu'il coûte) ; mon appareil et mes outils ; comment je veux tes réponses (longueur, ton, liste ou texte à copier) ; ce qui m'agace dans tes réponses ; ma langue. Si ma réponse est vague, demande un exemple concret.
Partie 2, les trois textes, chacun dans un bloc séparé facile à copier :
BLOC A · Mes instructions personnelles : six rubriques (Qui je suis, Mes activités, Mon client pilote, Comment me répondre, Ce que je ne veux pas, Langue), un écran au maximum.
BLOC B · À retenir : cinq à huit faits sur moi, une ligne chacun.
BLOC C · Instructions du projet client pilote : son contexte, son blocage, le ton à utiliser, ce que tu ne dois jamais inventer.
Demande-moi de relire et de corriger chaque bloc avant de continuer.
Partie 3, le guidage : une seule action par message. Chaque message dit : où toucher, quoi copier ou activer, ce que je dois voir à l'écran quand c'est réussi. Puis tu attends que j'écrive « fait » ou que je t'envoie une capture. Dans cet ordre :
a) enregistrer le BLOC A dans les instructions ;
b) vérifier que la mémoire est activée, puis me faire t'envoyer le BLOC B avec « Retiens ces informations sur moi » ;
c) me faire ouvrir une nouvelle conversation et te demander « Que sais-tu de moi ? », puis corriger ce qui est faux ;
d) créer le projet de mon client pilote, coller le BLOC C, ajouter ma fiche contexte, puis tester avec « Quel est le blocage de mon client pilote ? » ;
e) à chacune des étapes a, c et d, me rappeler de faire une capture pour mon portfolio : A00-06_Prenom_1.png, A00-06_Prenom_2.png, A00-06_Prenom_3.png.

C · CONTRAINTES
- Ne me demande jamais de mot de passe, de numéro de pièce d'identité, de compte bancaire ni de données de santé. Si j'en écris un par erreur, dis-le-moi et ne le mets dans aucun bloc.
- Pour mon client pilote, uniquement des groupes, jamais le nom d'un patient, d'un élève ou d'un client.
- N'invente aucun bouton ni aucun menu. En cas de doute, demande une capture.
- Si je suis perdu, reprends l'étape en cours avec d'autres mots, sans passer à la suite.

Commence par me dire en deux phrases ce que nous allons faire ensemble, puis pose ta première question.
:::

À partir de là, Claude mène. Répondez comme à une personne qui vous aide. Des réponses concrètes donnent de meilleurs résultats : « Je réponds aux clients surtout le soir sur WhatsApp » vaut mieux que « Je travaille beaucoup ».

**Pourquoi cette consigne fonctionne.** Elle contient les cinq éléments de M02-S1. Le **contexte** donne à Claude l'emplacement exact des réglages : il ne devine pas. Le **format** l'oblige à une seule action par message : vous ne vous perdez pas. Les **contraintes** protègent vos données.

## Étape 2 : suivre le guidage et vérifier

Claude vous guide maintenant. Pendant le guidage, trois phrases vous aident :

| Situation | Écrivez à Claude |
|---|---|
| Vous avez fini l'action | « Fait. » |
| Votre écran ne ressemble pas à ce que Claude décrit | « Je ne vois pas ça. Voici ma capture. » et joignez une capture d'écran |
| Vous n'avez pas compris | « Explique-moi encore, plus simplement. » |

Une ligne d'un bloc est fausse ? Corrigez par un tour précis :

::: prompt
Corrige dans le bloc [A, B ou C] : [ce qui est faux] devient [la bonne information]. Redonne-moi le bloc complet.
:::

**C'est terminé quand** vous avez les trois captures dans votre portfolio et que Claude répond juste aux deux questions de test.

## Repères : où se trouvent les réglages

Gardez ces repères pour vérifier ce que Claude vous dit, ou pour refaire un réglage plus tard.

| Pour… | Allez dans… |
|---|---|
| Vos instructions personnelles | Initiales en bas à gauche › **Settings** › **Your Claude** › **Instructions**. Ancien affichage : **Account** › **Instructions for Claude** |
| Activer la mémoire | **Settings** › **Your Claude** › **Generate memory from chats** |
| Voir, modifier ou supprimer ce que Claude a retenu | **Settings** › **Your Claude** › **Manage** à côté de **Your memory** › **Topics** |
| Créer le projet du client pilote | Menu **Projects** › nouveau projet › instructions du projet et fichiers |
| Une conversation sans mémoire | Icône fantôme en haut à droite (mode incognito) |

Les libellés sont ceux de l'interface en anglais. Si votre interface est en français, cherchez les mêmes rubriques sous leur nom traduit.

**Bon à savoir.** La mémoire existe aussi dans le plan gratuit. La recherche dans vos anciennes conversations (**Search and reference chats**) est réservée aux plans payants. Chaque projet a sa propre mémoire : dans un projet, Claude utilise la mémoire de ce projet et votre mémoire générale, pas celle des autres projets. Un projet par client, les informations ne se mélangent pas.

Pour faire oublier une information à Claude, écrivez simplement : « Oublie que [information]. »

## Étape 3 : entretenir, une fois par semaine

Claude vous connaît mieux chaque semaine si vous lui donnez l'occasion de faire le point. Une fois par semaine, dans une nouvelle conversation :

::: prompt
Voici mes instructions personnelles actuelles : [collez votre BLOC A]. D'après nos échanges de cette semaine, qu'est-ce qui manque ou n'est plus juste ? Propose une version mise à jour, toujours en six rubriques et sur un écran. Puis dis-moi où la coller, étape par étape.
:::

Relisez. Gardez seulement ce qui est vrai. Puis vérifiez avec « Que sais-tu de moi ? ».

::: coup-de-pouce
1. Claude pose plusieurs questions d'un coup ou donne plusieurs actions à la fois ? Répondez : « Une seule question, une seule action à la fois, s'il te plaît. »
2. Claude décrit un bouton que vous ne voyez pas ? Envoyez une capture d'écran et écrivez : « Voici mon écran. Où dois-je toucher ? » Si rien ne correspond, utilisez le tableau des repères.
3. Claude ne connaît rien de vous dans la nouvelle conversation ? Vérifiez que les instructions sont enregistrées et que la conversation n'est pas en mode incognito.
:::

::: erreurs
- **Changer la consigne d'accompagnement.** Copiez-la en entier. Si vous enlevez le contexte, Claude devine les menus et peut se tromper.
- **Tout raconter dans les instructions.** Un écran suffit. Les détails d'un client vont dans son projet.
- **Coller le BLOC C dans vos instructions personnelles.** Le contexte d'un client reste dans son projet.
- **Mettre des données sensibles.** Pas de mot de passe, pas de pièce d'identité, pas de compte, pas de noms de patients, d'élèves ou de clients.
- **Ne jamais vérifier.** La mémoire peut retenir une information fausse. « Que sais-tu de moi ? » une fois par semaine.
:::

::: fil-rouge
Aïcha est infirmière à Garoua et prépare des contenus de prévention pour le centre de santé de son quartier, son client pilote. Elle envoie la consigne d'accompagnement depuis son téléphone. Claude lui demande un exemple de ce qui l'agace : « Les réponses trop longues que je ne peux pas lire entre deux patients. » Au moment d'enregistrer les instructions, elle ne trouve pas **Your Claude** : elle envoie une capture, et Claude lui montre le bon endroit. Son BLOC A dit : « Réponses de cinq lignes au maximum, puis un texte prêt à copier pour WhatsApp. » Le lendemain, dans une nouvelle conversation, Claude lui répond en cinq lignes, sans qu'elle le redemande.
:::

::: livrable
Dans votre portfolio, avant la prochaine séance en direct : **A00-06_Prenom_1.png** (instructions enregistrées), **A00-06_Prenom_2.png** (« Que sais-tu de moi ? » et correction), **A00-06_Prenom_3.png** (projet client pilote).
:::
