---
code: M02-S2
partie: I
module: M02
titre: Itérer et affiner
type: autonomie
outil: Claude Chat
appareil: smartphone
duree: {seance: 60, devoir: 45}
prerequis: [M02-S1]
echafaudage: 1
acces_defaut: programme
jalon: J1
livrable: Avant-après d'un texte professionnel
competences:
  - code: M02-S2-C1
    jalon: J1-C2
    savoir_faire: Vous faites critiquer un texte par Claude selon trois critères, puis vous le faites réécrire.
    preuve: Votre livrable montre la critique et la réécriture dans la même conversation.
    reussi_si: La critique cite trois points précis et la réécriture traite chacun d'eux.
  - code: M02-S2-C2
    jalon: J1-C2
    savoir_faire: Vous adaptez un texte de votre client pilote à deux canaux.
    preuve: Votre livrable montre deux versions du même texte, par exemple un message WhatsApp et une affiche.
    reussi_si: La longueur, le ton et l'appel à l'action diffèrent selon le canal.
  - code: M02-S2-C3
    jalon: J1-C4
    savoir_faire: Vous vérifiez le texte final avant de l'envoyer.
    preuve: Votre livrable liste trois contrôles faits, dates et lieux, noms, prix ou chiffres.
    reussi_si: Chaque contrôle nomme sa source, et aucune information inventée ne reste dans le texte.
fil_client: {produit: "Texte de présentation critiqué, adapté à deux canaux et vérifié", page_dossier: 2}
glossaire: [Itération, Critique (consigne de), Canal, Hallucination, Fiche-outil]
index: [Itération, Critique d'un texte, Réécriture, Canal de communication, Appel à l'action, Vérification des faits, Avant-après, Affiche]
videos: {tutoriel: false, vitrine: false, shorts: 0, signature: false}
verifie: "2026-11-08"
version: "1.0"
captures: null
status: relecture
---

# M02-S2 · Itérer et affiner

## Ce que vous saurez faire

| Vous savez… | Vous le prouvez… | C'est réussi si… |
|---|---|---|
| Vous faites critiquer un texte par Claude selon trois critères, puis vous le faites réécrire. | Votre livrable montre la critique et la réécriture dans la même conversation. | La critique cite trois points précis et la réécriture traite chacun d'eux. |
| Vous adaptez un texte de votre client pilote à deux canaux. | Votre livrable montre deux versions du même texte, par exemple un message WhatsApp et une affiche. | La longueur, le ton et l'appel à l'action diffèrent selon le canal. |
| Vous vérifiez le texte final avant de l'envoyer. | Votre livrable liste trois contrôles faits, dates et lieux, noms, prix ou chiffres. | Chaque contrôle nomme sa source, et aucune information inventée ne reste dans le texte. |

Ces trois compétences comptent pour le jalon **J1 · Utilisateur autonome** : J1-C2 (améliorer une réponse par itération) et J1-C4 (vérifier les informations produites). Votre livrable est la pièce que vous montrerez au Démo Day J1 : une conversation pour votre client pilote, de la première consigne à la version finale.

## Pourquoi c'est utile

Un client ne paie pas une première version. Il paie un texte qui règle son problème : moins de questions répétées, plus de commandes, des parents qui viennent à la réunion. Un texte juste, adapté à ses publics, sans erreur. Trois gestes font cette différence : faire critiquer avant de réécrire, adapter au canal, vérifier chaque information. Ils servent pour chaque texte, chaque client.

Durée : 60 minutes de séance en autonomie, 45 minutes de travail personnel. Appareil : téléphone.

**Deux pistes, les mêmes compétences.** Piste Découverte : suivez les consignes à copier. Piste Défi : faites les encadrés **Piste Défi**.

## Avant de commencer

- [ ] Vous avez la **fiche contexte** de votre client pilote (séance M02-S1).
- [ ] Vous avez choisi **un texte réel** de votre client pilote à améliorer : sa présentation, une annonce, un message qu'il envoie souvent. S'il n'existe pas encore, écrivez une première version en deux phrases.
- [ ] Vous avez sous la main **la source** de ses informations : liste de prix, calendrier, horaires, numéro de contact.

## Ce que vous réutilisez

Cette séance s'appuie sur ce que vous savez déjà faire. Gardez votre **Kit du prestataire** ouvert.

| Geste déjà appris | Séance | Où il sert aujourd'hui |
|---|---|---|
| La fiche contexte et la grille R-T-C-F-C (fiche-outil 03) | M02-S1 | Vous collez la fiche avant chaque critique (étape 9) |
| Faire lire une photo de document et comparer deux valeurs (fiche-outil 02) | M01-S2 | Vous photographiez la source du client pour vérifier le texte (étape 13) |
| Préciser et transformer (fiche-outil 01) | M01-S1 | L'adaptation à deux canaux est une transformation guidée (étape 12) |
| Renommer une conversation | M01-S1 | « [client pilote] · présentation » : votre pièce du Démo Day se retrouve en secondes |

## Je vous montre

Un exemple complet, en quatre tours, dans une seule conversation.

**Tour 1 · Le texte de départ.** Une petite boutique a ce texte dans son profil : « Boutique ouverte tous les jours, on a de tout, venez nombreux. »

**Tour 2 · La critique.**

::: prompt
Voici le texte de présentation d'une boutique de quartier : « Boutique ouverte tous les jours, on a de tout, venez nombreux. » Critique ce texte selon trois critères : 1. clarté pour un nouveau client, 2. appel à l'action, 3. confiance. Pour chaque critère, une note sur 5 et une amélioration précise. Ne réécris pas encore le texte.
:::

Claude répond par exemple : clarté 2 sur 5, on ne sait pas ce qui est vendu ; appel à l'action 1 sur 5, aucun moyen de commander ; confiance 2 sur 5, pas d'adresse ni d'horaires.

**Tour 3 · La réécriture.**

::: prompt
Réécris le texte en appliquant tes trois améliorations. Utilise seulement ces informations : produits du quotidien et produits frais, ouvert de 7 h à 21 h, livraison dans le quartier, commande par WhatsApp. N'ajoute aucune information.
:::

**Tour 4 · La vérification.**

::: prompt
Liste toutes les informations factuelles de ton texte : dates, heures, lieux, noms, prix, chiffres, contacts. Pour chacune, indique si elle vient de ma consigne ou si tu l'as ajoutée.
:::

Claude signale ce qu'il a ajouté. Vous supprimez ou corrigez tout ce qui ne vient pas de vos informations. C'est le geste le plus important de la séance : Claude peut inventer un prix, une date ou un service qui n'existe pas.

![Étape 1 : la critique en trois critères](captures/etape-1.png)

![Étape 2 : la liste des informations factuelles](captures/etape-2.png)

## Nous faisons ensemble

Suivez les étapes avec le texte d'exemple. Les consignes sont complètes : copiez-les.

**Étape 3 : ouvrir une conversation.** Nouvelle conversation, nommée « Itérer · exemple ».

**Étape 4 : critiquer.** Envoyez :

::: prompt
Voici une annonce : « Réunion importante samedi, tout le monde doit venir. » Critique-la selon trois critères : 1. informations pratiques (jour, heure, lieu), 2. raison de venir, 3. ton. Pour chaque critère, une note sur 5 et une amélioration précise. Ne réécris pas encore.
:::

**Étape 5 : réécrire avec vos informations.**

::: prompt
Réécris l'annonce en appliquant tes trois améliorations. Informations : réunion le samedi à 10 h, dans la grande salle, pour présenter le programme du trimestre, durée une heure. N'ajoute aucune autre information.
:::

**Étape 6 : adapter à deux canaux.**

::: prompt
Adapte ce texte à deux canaux. 1. Un message WhatsApp de cinq lignes au maximum, ton chaleureux, qui demande de répondre « Présent ». 2. Une affiche A4 : un titre court en majuscules, trois informations, une phrase d'appel en bas. Pour chaque canal, change la longueur, le ton et l'appel à l'action.
:::

![Étape 6 : un texte, deux canaux](captures/etape-6.png)

**Étape 7 : vérifier.**

::: prompt
Liste toutes les informations factuelles de tes deux versions : dates, heures, lieux, noms, chiffres, contacts. Pour chacune, indique si elle vient de mes messages ou si tu l'as ajoutée.
:::

Comparez avec vos informations de l'étape 5. Tout ce qui a été ajouté est supprimé ou corrigé.

::: defi
**Choisir ses propres critères.** Les critères changent selon le public. Pour une annonce destinée à des personnes âgées : lisibilité, politesse, numéro à appeler. Pour des jeunes clients : rapidité de lecture, émojis, lien de commande. Refaites l'étape 4 avec trois critères que vous choisissez pour un public précis, et comparez les deux critiques.
:::

## Un geste, trois contextes

Le geste de cette séance : critiquer, adapter, vérifier. Vous l'appliquez trois fois :

| Contexte | Ce que vous faites | Où |
|---|---|---|
| Guidé | L'annonce de réunion | Étapes 3 à 7 |
| Transfert | Le texte de la boutique, adapté à un autre secteur | Étape 8 |
| Client pilote | Un texte réel de votre client pilote | Étapes 9 à 13 |

**Étape 8 : transfert.** Prenez le texte de la boutique (« Je vous montre ») et changez de secteur : un atelier de couture, une école ou un centre de santé. Refaites seulement le tour 2, la critique, avec trois critères adaptés à ce secteur. Notez les trois critères choisis.

## Vous faites avec appui

Maintenant, le texte réel de votre client pilote.

**Étape 9 : ouvrir une conversation.** Nommez-la « [client pilote] · présentation ». Collez d'abord votre fiche contexte, puis le texte de départ.

**Étape 10 : critiquer.** Copiez et complétez :

::: prompt
Voici la fiche contexte de mon client pilote : [fiche contexte]. Voici son texte actuel : « [texte] ». Critique ce texte selon trois critères : 1. [critère, par exemple : le texte aide-t-il à réduire le blocage de la fiche ?], 2. [critère], 3. [critère]. Pour chaque critère, une note sur 5 et une amélioration précise. Ne réécris pas encore.
:::

**Étape 11 : réécrire.**

::: prompt
Réécris le texte en appliquant tes trois améliorations. Utilise seulement ces informations : [informations exactes : services, horaires, prix, contact]. N'ajoute aucune information.
:::

**Étape 12 : adapter à deux canaux.** Choisissez les deux canaux que votre client pilote utilise vraiment (questionnaire S02-0).

::: prompt
Adapte ce texte à deux canaux : 1. [canal 1, forme et longueur], 2. [canal 2, forme et longueur]. Pour chaque canal, change la longueur, le ton et l'appel à l'action.
:::

**Étape 13 : vérifier.** Envoyez la consigne de vérification de l'étape 7. Puis photographiez la source de votre client (liste de prix, calendrier, carte de visite) et faites-en un tableau avec la fiche-outil 02. Comparez trois informations du texte avec ce tableau et avec la photo elle-même. Notez chaque contrôle sur une ligne : information, source, résultat.

Vérifiez votre travail :

- [ ] La critique donne trois points précis
- [ ] La réécriture traite chacun des trois points
- [ ] Les deux versions diffèrent par la longueur, le ton et l'appel à l'action
- [ ] Trois contrôles notés, chacun avec sa source
- [ ] Aucune information ajoutée par Claude ne reste dans le texte final

::: coup-de-pouce
1. **Indice.** Vous ne savez pas quels critères choisir ? Demandez-vous ce que les publics de votre client doivent comprendre, ressentir et faire après avoir lu le texte. Trois questions, trois critères.
2. **Solution partielle.** Critères qui marchent presque toujours : le texte réduit-il le blocage du client, clarté pour le public, appel à l'action, confiance (adresse, horaires, contact). Pour un canal : WhatsApp court et direct ; affiche lisible de loin ; Facebook avec une phrase d'accroche.
3. **Solution complète.** « Voici la fiche contexte de mon client pilote : atelier de couture à Bafoussam, clientes femmes actives, blocage : peu de commandes de fin d'année, deux semaines sans travail, ton chaleureux, contact WhatsApp de l'atelier. Voici son texte actuel : « Couture tous modèles. » Critique ce texte selon trois critères : 1. clarté pour une nouvelle cliente, 2. envie de commander, 3. confiance. Pour chaque critère, une note sur 5 et une amélioration précise. Ne réécris pas encore. »
:::

::: structure
Votre texte est souvent un message aux parents, aux patients, aux membres ou au personnel, et une affiche. Avant l'envoi, faites valider la version finale par la personne qui en a le droit. Dans la vérification, contrôlez en priorité les dates, les heures et les lieux avec le document officiel : calendrier scolaire, planning du centre, convocation signée.
:::

::: defi
**Trois variantes, une version finale.** Avant l'étape 11, demandez : « Propose trois réécritures différentes : une courte, une chaleureuse, une très professionnelle. » Choisissez la meilleure, expliquez votre choix en une phrase, puis demandez une version finale qui reprend un élément d'une autre variante. Aidez ensuite un binôme à faire la même chose.
:::

## Pour votre client pilote

Cette séance produit la **page 2 de votre Dossier client pilote** : un texte de présentation critiqué, adapté à deux canaux et vérifié.

1. Page 2 : collez le texte de départ, la critique, la version finale de chaque canal et vos trois contrôles.
2. Montrez les deux versions à votre client pilote, ou à la personne qui valide dans votre structure. Notez sa réaction en une phrase.
3. Une fois validées, publiez-les : description WhatsApp Business, publication Facebook, message, affiche.
4. Gardez ce texte : il servira de base à la page web de votre client pilote (séance M05-S1).

## Vous faites seul

Avant la prochaine séance, appliquez les trois gestes à **un deuxième texte** de votre client pilote, sans consigne à copier : une réponse aux questions fréquentes, un message de rappel, une annonce.

Critères de qualité :

- Vous choisissez vous-même les trois critères de la critique.
- Les deux canaux sont ceux que votre client utilise vraiment.
- Trois contrôles sont notés avec leur source.
- Le texte est validé par votre client pilote ou par la personne qui valide dans votre structure.

Piste Défi : faites la même chose pour une personne d'un autre secteur que votre client pilote, et notez ce qui a changé dans vos critères.

## Votre fiche-outil

**Fiche-outil 04 · Critiquer, adapter, vérifier.** À garder sur votre téléphone : copiez les trois consignes dans vos notes.

::: prompt
1 · Critiquer. Critique ce texte selon trois critères : 1. [critère], 2. [critère], 3. [critère]. Pour chaque critère, une note sur 5 et une amélioration précise. Ne réécris pas encore.
:::

::: prompt
2 · Adapter. Réécris le texte en appliquant tes améliorations, avec seulement ces informations : [informations exactes]. Puis adapte-le à deux canaux : 1. [canal, forme, longueur], 2. [canal, forme, longueur]. Change la longueur, le ton et l'appel à l'action.
:::

::: prompt
3 · Vérifier. Liste toutes les informations factuelles de ton texte : dates, heures, lieux, noms, prix, chiffres, contacts. Pour chacune, indique si elle vient de mes messages ou si tu l'as ajoutée.
:::

Puis contrôlez trois informations avec la source du client, avant tout envoi.

## Cas fil rouge

M. Essomba dirige une école primaire publique à Obala. Son annonce habituelle : « Réunion APEE samedi, présence obligatoire. » Critique selon trois critères (informations pratiques, raison de venir, respect des parents) : 1, 1 et 2 sur 5. Réécriture avec ses informations : samedi à 9 h, dans la cour de l'école, présentation des résultats du premier trimestre. Deux canaux : un message pour le groupe WhatsApp des parents, qui demande de répondre « Présent », et une affiche au portail, lisible de loin. Vérification : Claude avait ajouté « collation offerte ». M. Essomba le supprime : rien n'était prévu. Il compare l'heure avec la convocation signée, puis envoie. Ce message lui prenait d'habitude une demi-heure à écrire ; cette fois, dix minutes.

## Erreurs fréquentes

- **Réécrire sans critique.** « Améliore ce texte » donne une version différente, pas forcément meilleure. Demandez d'abord la critique, avec vos critères.
- **Une seule version pour tous les canaux.** Une affiche n'est pas un message WhatsApp. Changez la longueur, le ton et l'appel à l'action.
- **Laisser des informations inventées.** Claude ajoute parfois un service, un prix ou une promesse. Demandez toujours la liste des informations factuelles, puis contrôlez avec la source.
- **Envoyer sans validation.** Le client ou la personne qui valide dans votre structure voit le texte avant sa publication.

## Vérifiez vos acquis

Cochez seulement ce que vous venez de faire vous-même, sans aide.

- [ ] Vous avez une critique en trois points et une réécriture qui traite chacun d'eux. Sinon : étapes 10 et 11.
- [ ] Vous avez deux versions pour deux canaux, différentes par la longueur, le ton et l'appel à l'action. Sinon : étape 12.
- [ ] Vous avez trois contrôles notés avec leur source. Sinon : étape 13.
- [ ] Quiz S02-2 : au moins 6 bonnes réponses sur 8.

## Votre livrable

Un document nommé **S02-2_Prenom** (par exemple S02-2_Aicha), créé dans votre portfolio. C'est votre pièce J1-C2 pour le Démo Day. Chaque élément prouve une compétence :

1. **Critique et réécriture :** captures de la critique et de la réécriture, dans la même conversation.
2. **Deux canaux :** les deux versions du texte de votre client pilote.
3. **Vérification :** vos trois contrôles, une ligne chacun : information, source, résultat.
4. **Avant-après :** le texte de départ et le texte final, côte à côte, avec deux améliorations que vous nommez vous-même.
5. **Trois phrases :** le blocage que ce texte doit réduire et ce que vous observerez pour savoir s'il marche, la réaction de votre client pilote, ce que vous ferez autrement.

Et dans votre **Dossier client pilote**, la page 2 remplie.

### Comment votre livrable est évalué

| Niveau | Ce que montre votre livrable |
|---|---|
| 1 · Découverte | Une réécriture existe, mais sans critique, sans deuxième canal ou sans contrôle. |
| 2 · Application guidée | Les étapes de la fiche sont faites sur le texte d'exemple, avec les consignes à copier. |
| 3 · Autonomie | Le texte réel du client pilote est critiqué selon vos critères, adapté à ses deux canaux et vérifié avec sa source ; la page 2 du Dossier est remplie. |
| 4 · Transfert | Niveau 3, et le texte est validé et publié par votre client pilote, avec sa réaction notée. Ou, piste Défi : trois variantes comparées et une version finale justifiée. |

La séance est validée au niveau 3. Le jalon J1 demande au moins le niveau 2 à chaque livrable.

## Kit NotebookLM

Ajoutez cette fiche à votre notebook « Parcours Claude Pro ». Les sources et consignes de la semaine se trouvent dans le dossier « 03 · Réviser avec NotebookLM ».

## Mots-clés

Itération · Critique d'un texte · Réécriture · Canal de communication · Appel à l'action · Vérification des faits · Avant-après · Affiche

---

Une formation OKOHO Consulting GmbH · Formateur : Dr. Bertrand Toumi
Claude est une marque d'Anthropic. Le Parcours Claude Pro est une formation indépendante proposée par OKOHO Consulting GmbH, sans partenariat avec Anthropic. Reproduction et diffusion interdites sans autorisation écrite d'OKOHO Consulting GmbH.
Version 1.0 · Fonctions vérifiées le 08.11.2026 (support.claude.com) · Captures d'écran réalisées le — · © 2026 OKOHO Consulting GmbH
