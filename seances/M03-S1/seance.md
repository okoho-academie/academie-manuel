---
code: M03-S1
partie: I
module: M03
titre: "Vérifier : erreurs, sources, limites"
type: autonomie
outil: Claude Chat + recherche web
appareil: smartphone
duree: {seance: 60, devoir: 45}
prerequis: [M01-S2, M02-S2]
echafaudage: 1
acces_defaut: programme
jalon: J1
livrable: Vérification d'un message WhatsApp viral
competences:
  - code: M03-S1-C1
    jalon: J1-C4
    savoir_faire: Vous repérez dans une réponse de Claude les informations qui demandent une vérification.
    preuve: Votre livrable montre une réponse de Claude avec les informations à vérifier marquées.
    reussi_si: Au moins trois informations, chiffre, prix, date, nom ou règle, sont marquées, chacune avec la personne ou la source qui peut la confirmer.
  - code: M03-S1-C2
    jalon: J1-C4
    savoir_faire: Vous vérifiez une information avec la recherche web de Claude et une source officielle.
    preuve: Votre livrable montre la question, la réponse, la source et la date de consultation.
    reussi_si: La source est l'organisme qui publie l'information, pas un blog ni un message transféré, et tout écart est signalé à Claude.
  - code: M03-S1-C3
    jalon: J1-C4
    savoir_faire: Vous demandez au client les informations que lui seul possède, au lieu de les faire inventer.
    preuve: Votre livrable contient le message envoyé à votre client pilote pour confirmer ses prix, ses horaires ou ses règles.
    reussi_si: Le message liste les points à confirmer et ne contient aucun chiffre proposé par Claude.
fil_client: {produit: "Une information vérifiée avec sa source", page_dossier: 4}
glossaire: [Hallucination, Source officielle, Recherche web, Message viral]
index: [Hallucination, Vérification des faits, Sources (vérifier), Source officielle, Recherche web, Message viral, Prix (ne jamais inventer), Information du client]
videos: {tutoriel: false, vitrine: false, shorts: 0, signature: false}
verifie: "2026-11-15"
version: "1.0"
captures: null
status: relecture
---

# M03-S1 · Vérifier : erreurs, sources, limites

## Ce que vous saurez faire

| Vous savez… | Vous le prouvez… | C'est réussi si… |
|---|---|---|
| Vous repérez dans une réponse de Claude les informations qui demandent une vérification. | Votre livrable montre une réponse de Claude avec les informations à vérifier marquées. | Au moins trois informations, chiffre, prix, date, nom ou règle, sont marquées, chacune avec la personne ou la source qui peut la confirmer. |
| Vous vérifiez une information avec la recherche web de Claude et une source officielle. | Votre livrable montre la question, la réponse, la source et la date de consultation. | La source est l'organisme qui publie l'information, pas un blog ni un message transféré, et tout écart est signalé à Claude. |
| Vous demandez au client les informations que lui seul possède, au lieu de les faire inventer. | Votre livrable contient le message envoyé à votre client pilote pour confirmer ses prix, ses horaires ou ses règles. | Le message liste les points à confirmer et ne contient aucun chiffre proposé par Claude. |

Ces trois compétences comptent pour le jalon **J1 · Utilisateur autonome** (compétence J1-C4 : vérifier les informations et respecter la confidentialité).

## Pourquoi c'est utile

Claude écrit bien, même quand il se trompe. Une date fausse, un prix inventé, une règle qui n'existe plus : la phrase est claire et sûre d'elle. C'est une **hallucination**. Si elle part chez votre client, c'est votre réputation de prestataire qui en souffre.

Vérifier n'est pas compliqué. Il faut savoir trois choses : quoi vérifier, où vérifier, et qui seul peut répondre. Avec ces trois gestes, chaque texte que vous livrez est juste.

Durée : 60 minutes, puis 45 minutes de travail personnel. Appareil : téléphone ou tablette.

## Avant de commencer

- [ ] L'application Claude est ouverte.
- [ ] Vous avez sous la main un texte produit par Claude pour votre client pilote : la page web, un message, une affiche.
- [ ] Vous avez reçu, ou vous trouvez, un message transféré « Transféré plusieurs fois » sur WhatsApp. Sinon, utilisez l'exemple de l'étape 5.

## Ce que vous réutilisez

Cette séance s'appuie sur ce que vous savez déjà faire. Gardez votre **Kit du prestataire** ouvert.

| Geste déjà appris | Séance | Où il sert aujourd'hui |
|---|---|---|
| Comparer deux valeurs avec le document original (fiche-outil 02) | M01-S2 | Vous comparez la réponse de Claude avec la source officielle (étape 7) |
| Critiquer, adapter, vérifier (fiche-outil 04) | M02-S2 | La liste des informations factuelles devient le point de départ (étape 2) |
| La fiche contexte du client (fiche-outil 03) | M02-S1 | Les informations du client viennent du client (étape 10) |

## Je vous montre

### Les trois questions avant d'utiliser une information

| Question | Pourquoi | Exemple |
|---|---|---|
| 1. Est-ce un fait ? | Les chiffres, prix, dates, noms et règles peuvent être faux | « Les inscriptions ferment le 15 » |
| 2. Qui peut le confirmer ? | Une source officielle, ou le client lui-même | Le site du ministère, le directeur de l'école |
| 3. L'ai-je vérifié ? | Seulement oui ou non, avec la source | « Oui, site officiel, consulté aujourd'hui » |

### Le cas des prix

Un institut de formation demande à Claude : « Donne le coût de chaque étape d'une démarche administrative pour partir étudier à l'étranger. » Claude répond avec un tableau propre et des montants précis. Le tableau a l'air sérieux. Mais d'où viennent ces chiffres ? Ils peuvent être anciens, approximatifs ou inventés.

La règle du prestataire : **les prix viennent du client ou de l'organisme officiel, jamais de Claude.** Claude peut préparer le tableau vide et la liste des questions à poser. Le client remplit les montants.

## Nous faisons ensemble

**Étape 1 : nouvelle conversation.** Touchez **Nouvelle conversation**. Renommez-la « Vérifier · client pilote ».

**Étape 2 : faire lister les faits.** Collez un texte que Claude a écrit pour votre client pilote, puis envoyez :

::: prompt
Voici un texte que tu as écrit. Fais la liste de toutes les informations factuelles : chiffres, prix, dates, horaires, noms, lieux, règles. Pour chacune, dis si elle vient de ce que je t'ai donné ou si tu l'as ajoutée. Ne réécris pas le texte.
:::

![Étape 2 : la liste des informations factuelles](captures/etape-2.png)

**Étape 3 : marquer.** Dans vos notes, recopiez la liste. Devant chaque information, écrivez qui peut la confirmer : « client », « site officiel », « document du client ».

**Étape 4 : supprimer ce qui est ajouté.** Une information que Claude a ajoutée et que personne ne confirme ? Envoyez :

::: prompt
Retire du texte les informations que tu as ajoutées et que je ne t'ai pas données. Remplace-les par [À CONFIRMER]. Montre-moi le texte corrigé.
:::

**Étape 5 : le message viral.** Copiez ce message, ou un vrai message transféré que vous avez reçu, dans une nouvelle conversation nommée « Vérifier · message viral » :

::: prompt
Voici un message qui circule sur WhatsApp : « URGENT. Le gouvernement offre une aide de cinquante mille francs à chaque famille. Inscrivez-vous avant minuit sur ce lien et partagez à dix contacts, sinon votre inscription sera annulée. » Ce message est-il fiable ? Cherche sur le web les sources officielles. Donne-moi : ce qui est vrai, ce qui est faux, les signes d'arnaque, et le lien de chaque source avec le nom de l'organisme.
:::

**Étape 6 : activer la recherche web.** Si Claude répond sans source, vérifiez que la **recherche web** est activée : dans la zone de saisie, ouvrez le menu des outils et activez **Recherche web** (en anglais : *Web search*). Renvoyez la consigne.

![Étape 6 : la recherche web activée](captures/etape-6.png)

**Étape 7 : ouvrir la source.** Touchez un lien cité par Claude. Vérifiez trois points : qui publie la page (un ministère, un organisme officiel, un média connu), la date de la page, et si la page dit bien ce que Claude a résumé.

**Étape 8 : noter.** Dans vos notes : la question, la réponse de Claude en une phrase, la source (organisme et lien), la date de consultation, et votre conclusion : vrai, faux ou non confirmé.

Un message qui demande d'agir vite, de partager à dix personnes ou de cliquer sur un lien pour recevoir de l'argent est presque toujours une arnaque. Ne cliquez jamais sur le lien pour « vérifier ».

## Un geste, trois contextes

Le geste de cette séance est le même partout : demander la source, puis vérifier à l'original. Vous l'appliquez trois fois :

| Contexte | Ce que vous faites | Où |
|---|---|---|
| Guidé | Le message viral vérifié avec des sources officielles | Étapes 5 à 8 |
| Transfert | Une information publique utile à un autre métier : calendrier scolaire, campagne de santé, règle d'un marché | Étape 9 |
| Client pilote | Les informations de votre client, confirmées par lui | Étapes 10 à 12 |

Un commerce vérifie le prix de son fournisseur. Une école vérifie le calendrier officiel. Un centre de santé vérifie la date d'une campagne. Le geste ne change pas.

## Vous faites avec appui

**Étape 9 : une information publique.** Choisissez une information officielle utile à votre client pilote : une date de rentrée, une date d'examen, une campagne de santé, une règle administrative. Envoyez :

::: prompt
Cherche sur le web [l'information]. Donne la réponse en une phrase, puis la source officielle : nom de l'organisme, lien, date de la page. Si tu ne trouves pas de source officielle, dis-le clairement et ne devine pas.
:::

Ouvrez la source et comparez. Un écart ? Signalez-le à Claude dans la même conversation :

::: prompt
La source dit [ce que dit la source], pas [ce que tu as écrit]. Corrige ta réponse et garde seulement ce que dit la source.
:::

**Étape 10 : les informations que seul le client connaît.** Prix, horaires, services, conditions : ce sont les informations de votre client. Préparez le message pour les lui demander :

::: prompt
Je prépare une page et des messages pour [client pilote]. Écris un message WhatsApp court et poli pour lui demander de confirmer ces informations : [liste : prix, horaires, services, contact]. Ne propose aucun chiffre. Laisse une ligne vide après chaque point pour sa réponse.
:::

**Étape 11 : envoyer.** Relisez le message : aucun chiffre ne vient de Claude. Envoyez-le à votre client pilote, ou, pour votre propre structure, à la personne qui détient l'information.

**Étape 12 : corriger le texte.** Quand le client répond, remplacez chaque [À CONFIRMER] par sa réponse. Notez la date de sa confirmation.

Vérifiez votre travail :

- [ ] Au moins trois informations du texte sont marquées avec qui peut les confirmer
- [ ] L'information publique a une source officielle, avec son organisme, son lien et la date
- [ ] Tout écart a été signalé à Claude et corrigé
- [ ] Le message au client ne contient aucun chiffre proposé par Claude
- [ ] Aucune donnée sensible dans vos conversations

::: coup-de-pouce
1. **Indice.** Une information est à vérifier si elle contient un chiffre, une date, un nom propre ou le mot « obligatoire ».
2. **Solution partielle.** Demandez à Claude : « Dans ta réponse, quelles informations pourraient être fausses ou anciennes ? Classe-les de la plus risquée à la moins risquée. »
3. **Solution complète.** Liste marquée : « Inscriptions jusqu'au 15 : à confirmer par le directeur » · « Frais d'inscription : à confirmer par le directeur, Claude n'a pas de source » · « Rentrée le premier lundi du mois : site officiel du ministère, consulté aujourd'hui ».
:::

::: defi
**La source contre la source.** Pour votre information publique, demandez à Claude deux sources différentes. Si elles ne disent pas la même chose, laquelle croyez-vous, et pourquoi ? Écrivez votre réponse en deux phrases dans votre livrable.
:::

## Pour votre client pilote

Cette séance produit la **page 4 de votre Dossier client pilote** : une information vérifiée avec sa source.

1. Ouvrez votre **Dossier client pilote** dans votre portfolio.
2. Page 4 : l'information, qui l'a confirmée (le client ou l'organisme), la source et la date, ce que Claude avait écrit de faux, où l'information est utilisée (par exemple sur la page web de la page 3).
3. Si votre page web contenait une information non confirmée, corrigez-la et publiez une nouvelle version.

::: structure
Pour votre propre structure, l'information officielle vient de la hiérarchie ou de l'autorité compétente : calendrier, campagne, règlement. Notez qui l'a validée.
:::

## Vous faites seul

Avant la prochaine séance :

1. Vérifiez **un vrai message transféré** que vous avez reçu, avec la recherche web et une source officielle.
2. Vérifiez **une information de votre client pilote** auprès de lui, avec le message de l'étape 10.
3. Relisez **votre page web** avec les trois questions et corrigez ce qui doit l'être.

Critères de qualité :

- Chaque information vérifiée a sa source : organisme ou personne, lien ou date.
- Aucune information n'est « vraie parce que Claude l'a dit ».
- Aucun prix ou chiffre du client ne vient de Claude.

## Votre fiche-outil

**Fiche-outil 06 · Trois questions avant d'utiliser une information.** À garder sur votre téléphone.

1. Est-ce un fait : chiffre, prix, date, nom, règle ?
2. Qui peut le confirmer : le client, ou l'organisme qui publie l'information ?
3. L'ai-je vérifié, avec la source et la date ?

Pour faire lister les faits :

::: prompt
Fais la liste de toutes les informations factuelles de ce texte. Pour chacune, dis si elle vient de ce que je t'ai donné ou si tu l'as ajoutée.
:::

Pour chercher une source :

::: prompt
Cherche sur le web [l'information]. Donne la source officielle : organisme, lien, date. Si tu ne trouves pas, dis-le et ne devine pas.
:::

La règle : les prix et les informations du client viennent du client, jamais de Claude.

## Cas fil rouge

M. Essomba dirige une école primaire publique à Obala. Il demande à Claude un message aux parents sur la date des examens de fin de trimestre. Claude écrit une date précise. Avec la consigne de l'étape 2, M. Essomba voit que la date a été ajoutée : il ne l'avait pas donnée. Il demande une recherche web : Claude trouve un calendrier, mais celui de l'année précédente. M. Essomba compare avec la note officielle reçue de sa hiérarchie, corrige la date et l'indique comme source. Le message part avec la bonne date. Sans vérification, deux cents familles auraient reçu une date fausse.

## Erreurs fréquentes

- **Croire un texte parce qu'il est bien écrit.** Claude écrit aussi bien une date fausse qu'une date juste.
- **Demander à Claude « es-tu sûr ? ».** Il peut répondre oui et se tromper. Demandez la source, puis ouvrez-la.
- **Prendre un blog ou un message transféré pour une source.** La source, c'est l'organisme qui publie l'information.
- **Faire inventer les prix du client.** Les prix viennent du client. Claude prépare seulement les questions.
- **Cliquer sur le lien d'un message douteux pour vérifier.** Ne cliquez pas. Cherchez l'information sur le site officiel.

## Vérifiez vos acquis

Cochez seulement ce que vous venez de faire vous-même, sans aide.

- [ ] Vous avez marqué au moins trois informations à vérifier dans un texte de Claude, avec qui peut les confirmer. Sinon : étapes 2 et 3.
- [ ] Vous avez vérifié une information avec une source officielle, son lien et la date. Sinon : étapes 6 à 9.
- [ ] Vous avez envoyé à votre client un message de confirmation sans aucun chiffre de Claude. Sinon : étapes 10 et 11.
- [ ] Quiz S03-2 : au moins 6 bonnes réponses sur 8.

## Votre livrable

Un document nommé **S03-2_Prenom** (par exemple S03-2_Aicha), dans votre portfolio, avant la prochaine séance. Chaque élément prouve une compétence :

1. **Informations marquées :** la capture de la liste des informations factuelles et vos marques « qui peut confirmer ».
2. **Vérification d'un message viral :** la question, la réponse de Claude, la source officielle avec son lien, la date de consultation et votre conclusion.
3. **Confirmation du client :** la capture du message envoyé à votre client pilote et, si elle est arrivée, sa réponse.

Et dans votre **Dossier client pilote**, la page 4 remplie.

### Comment votre livrable est évalué

| Niveau | Ce que montre votre livrable |
|---|---|
| 1 · Découverte | Des vérifications existent, mais sans source nommée ou sans date. |
| 2 · Application guidée | Les trois éléments sont présents, chaque source est nommée. |
| 3 · Autonomie | Niveau 2, avec un vrai message transféré vérifié et la page 4 du Dossier client pilote remplie. |
| 4 · Transfert | Niveau 3, et une information fausse a été corrigée sur un livrable du client pilote (page web, message), avec la source. |

La séance est validée au niveau 3. Le jalon J1 demande au moins le niveau 2 à chaque livrable.

## Kit NotebookLM

Ajoutez cette fiche à votre notebook « Parcours Claude Pro ». Les sources et consignes de la semaine se trouvent dans le dossier « 03 · Réviser avec NotebookLM ».

## Mots-clés

Hallucination · Vérification des faits · Source officielle · Recherche web · Message viral · Prix du client · Information à confirmer

---

Une formation OKOHO Consulting GmbH · Formateur : Dr. Bertrand Toumi
Claude est une marque d'Anthropic. Le Parcours Claude Pro est une formation indépendante proposée par OKOHO Consulting GmbH, sans partenariat avec Anthropic. Reproduction et diffusion interdites sans autorisation écrite d'OKOHO Consulting GmbH.
Version 1.0 · Fonctions vérifiées le 15.11.2026 (claude.com) · Captures d'écran réalisées le — · © 2026 OKOHO Consulting GmbH
