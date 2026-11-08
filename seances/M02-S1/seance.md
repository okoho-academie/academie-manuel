---
code: M02-S1
partie: I
module: M02
titre: Les cinq éléments d'une bonne consigne
type: direct
outil: Claude Chat
appareil: smartphone
duree: {seance: 90, devoir: 60}
prerequis: [M01-S1]
echafaudage: 1
acces_defaut: programme
jalon: J1
livrable: Cinq tâches du quotidien résolues
competences:
  - code: M02-S1-C1
    jalon: J1-C2
    savoir_faire: Vous rédigez une consigne qui contient les cinq éléments, rôle, tâche, contexte, format et contraintes.
    preuve: Vous postez dans le chat de la séance la consigne écrite pour votre client pilote, chaque élément marqué R, T, C, F, C.
    reussi_si: Les cinq éléments sont repérables et Claude rend un texte utilisable sans retouche.
  - code: M02-S1-C2
    jalon: J1-C2
    savoir_faire: Vous adaptez une consigne à un autre contexte.
    preuve: Vous tirez une carte contexte et adaptez en direct la consigne de l'exercice commun.
    reussi_si: Le rôle, le contexte et le format sont changés et le résultat convient au nouveau contexte.
  - code: M02-S1-C3
    jalon: J1-C2
    savoir_faire: Vous rédigez la fiche contexte de votre client pilote.
    preuve: Vous collez dans le chat de la séance la fiche contexte de votre client pilote, en cinq lignes.
    reussi_si: La fiche nomme l'activité ou la mission, les publics, le besoin, le ton et le contact, sans aucune donnée de patient, d'élève ou de client nommé.
fil_client: {produit: "Fiche contexte et premier message prêt à envoyer", page_dossier: 1}
glossaire: [Consigne (prompt), Contexte, Client pilote, Fiche contexte, Fiche-outil, Dossier client pilote, Mode tuteur]
index: [Consigne (cinq éléments), Grille R-T-C-F-C, Rôle, Format, Contraintes, Fiche contexte, Client pilote, Transfert, Carte contexte, Mode tuteur]
videos: {tutoriel: true, vitrine: false, shorts: 3, signature: false}
verifie: "2026-11-08"
version: "1.0"
captures: null
status: relecture
---

# M02-S1 · Les cinq éléments d'une bonne consigne

## Ce que vous saurez faire

| Vous savez… | Vous le prouvez… | C'est réussi si… |
|---|---|---|
| Vous rédigez une consigne qui contient les cinq éléments, rôle, tâche, contexte, format et contraintes. | Vous postez dans le chat de la séance la consigne écrite pour votre client pilote, chaque élément marqué R, T, C, F, C. | Les cinq éléments sont repérables et Claude rend un texte utilisable sans retouche. |
| Vous adaptez une consigne à un autre contexte. | Vous tirez une carte contexte et adaptez en direct la consigne de l'exercice commun. | Le rôle, le contexte et le format sont changés et le résultat convient au nouveau contexte. |
| Vous rédigez la fiche contexte de votre client pilote. | Vous collez dans le chat de la séance la fiche contexte de votre client pilote, en cinq lignes. | La fiche nomme l'activité ou la mission, les publics, le besoin, le ton et le contact, sans aucune donnée de patient, d'élève ou de client nommé. |

Ces trois compétences comptent pour le jalon **J1 · Utilisateur autonome** (compétence J1-C2 : formuler des consignes structurées).

## Pourquoi c'est utile

Une consigne vague donne une réponse moyenne, qu'il faut corriger trois fois. Une consigne complète donne en une fois un texte que vous pouvez envoyer. Avec un client, c'est la différence entre une heure de travail et dix minutes. Et une bonne consigne se réutilise : vous changez le contexte, elle sert pour un autre client.

Durée : 90 minutes en direct, 60 minutes de travail personnel. Appareil : téléphone.

**Deux pistes, les mêmes compétences.** Vous découvrez l'IA ? Suivez la fiche pas à pas et utilisez le mode tuteur. Vous utilisez déjà ChatGPT, Gemini ou DeepSeek ? Faites les mêmes étapes, puis les encadrés **Piste Défi**.

## Avant de commencer

- [ ] Votre téléphone est chargé, l'application Claude est ouverte.
- [ ] Vous avez rempli le questionnaire **S02-0 · Votre client pilote et vos contextes**.
- [ ] Vous savez qui est votre **client pilote** : une personne, une entreprise ou votre propre structure (école, centre de santé, commerce, association).
- [ ] Vous avez noté **une tâche réelle** de votre client pilote : un message, une annonce, une lettre à écrire cette semaine.

**Votre client pilote est votre propre structure ?** Vous n'avez pas d'accord à demander. Notez seulement qui valide une publication officielle et quelles informations ne sortent jamais de la structure.

**Votre client pilote est une personne de votre entourage ?** Demandez son accord avant de travailler avec ses informations. Message à adapter :

::: prompt
Bonjour [prénom]. Je suis une formation pour créer des services digitaux avec l'intelligence artificielle. J'aimerais t'aider gratuitement pendant quelques mois : messages, page web, documents pour [ton activité]. Je n'utiliserai que les informations que tu me donnes pour ça, jamais de données personnelles de tes clients. Es-tu d'accord ?
:::

## Je vous montre

### La même tâche, deux consignes

Consigne vague :

::: prompt
Écris un message pour dire que les horaires changent.
:::

Claude répond avec un texte général : pas de nom, pas de dates, un ton au hasard. Il faut tout corriger.

Consigne complète :

::: prompt
Tu es le responsable de la communication d'une petite structure de quartier. Écris un message pour annoncer à nos clients que nous ouvrons désormais de 7 h à 18 h du lundi au samedi, au lieu de 8 h à 17 h. Nos clients sont des habitants du quartier, ils lisent nos messages sur WhatsApp. Format : un message WhatsApp de cinq lignes au maximum, avec un émoji au début. Contraintes : ton chaleureux, phrases courtes, termine par le numéro de contact, pas de majuscules partout.
:::

Le texte est prêt à envoyer. La différence ne vient pas de Claude : elle vient des cinq éléments de la consigne.

### La grille R-T-C-F-C

| Lettre | Élément | La question à vous poser | Exemple |
|---|---|---|---|
| R | Rôle | Qui doit écrire ? | « Tu es le responsable de la communication… » |
| T | Tâche | Qu'est-ce que je veux obtenir ? | « Écris un message pour annoncer… » |
| C | Contexte | Pour qui, pourquoi, avec quelles informations ? | « Nos clients sont des habitants du quartier… » |
| F | Format | Sous quelle forme ? | « Un message WhatsApp de cinq lignes… » |
| C | Contraintes | Ce qu'il faut respecter ou éviter ? | « Ton chaleureux, termine par le numéro… » |

Le contexte est l'élément le plus souvent oublié. C'est aussi celui qui change le plus le résultat. Le tutoriel vidéo de la séance montre les deux consignes sur téléphone.

![Étape 1 : la consigne vague et sa réponse](captures/etape-1.png)

![Étape 2 : la consigne complète et sa réponse](captures/etape-2.png)

## Nous faisons ensemble

Tout le monde construit la même consigne, élément par élément. La tâche : une structure change ses horaires et doit prévenir ses publics.

**Étape 3 : ouvrir une nouvelle conversation.** Touchez **Nouvelle conversation**. Renommez-la tout de suite « Grille horaires ».

**Étape 4 : écrire R et T.** Dans la zone de saisie, écrivez sans envoyer :

::: prompt
Tu es le responsable de la communication d'une petite structure. Écris un message pour annoncer nos nouveaux horaires.
:::

**Étape 5 : ajouter C.** À la suite, ajoutez les informations : qui lit le message, les anciens et les nouveaux horaires, la raison si elle est utile.

::: prompt
Nos publics sont des habitants du quartier. Nous ouvrons désormais de 7 h à 18 h du lundi au samedi, au lieu de 8 h à 17 h, pour mieux servir les personnes qui travaillent.
:::

**Étape 6 : ajouter F et C.** Terminez par la forme et les règles, puis envoyez le tout en un seul message.

::: prompt
Format : un message WhatsApp de cinq lignes au maximum. Contraintes : ton chaleureux, phrases courtes, termine par « Pour toute question : » suivi d'un numéro que j'ajouterai.
:::

![Étape 6 : la consigne complète envoyée](captures/etape-6.png)

**Étape 7 : vérifier avec la grille.** Relisez votre consigne et marquez chaque élément : R, T, C, F, C. Un élément manque ? Ajoutez-le et utilisez l'icône **crayon** sur votre message pour l'envoyer à nouveau.

**Étape 8 : la carte contexte (transfert).** Le formateur fait tirer une carte à chacun. Adaptez la consigne de l'étape 6 à ce nouveau contexte : changez le rôle, le contexte et le format. Postez le résultat dans le chat de la séance.

| Carte | Contexte |
|---|---|
| 1 | Une boutique de quartier qui livre maintenant à domicile |
| 2 | Un restaurant qui ouvre aussi le dimanche |
| 3 | Un atelier de couture qui prend les commandes de fin d'année |
| 4 | Une école primaire qui convoque les parents à une réunion |
| 5 | Un centre de santé qui annonce de nouveaux horaires de consultation |
| 6 | Une association qui invite ses membres à l'assemblée générale |
| 7 | Un groupement agricole qui annonce un jour de vente au marché |
| 8 | Une agence de transport qui change l'heure de départ d'un bus |

::: defi
**Une consigne, trois publics.** Gardez la tâche de l'étape 6 et écrivez trois consignes pour trois publics différents : des clients, le personnel, une autorité qui doit être informée. Notez ce qui change à chaque fois dans R, C, F et C. La tâche reste la même : seul le reste change.
:::

## Un geste, trois contextes

Le geste de cette séance est le même partout : écrire une consigne complète avec la grille R-T-C-F-C. Vous l'appliquez trois fois :

| Contexte | Ce que vous faites | Où |
|---|---|---|
| Guidé | La consigne des horaires, construite ensemble | Étapes 3 à 7 |
| Transfert | La même consigne adaptée à une carte contexte | Étape 8 |
| Client pilote | Une consigne pour une tâche réelle de votre client pilote | Étapes 9 à 12 |

Un prestataire digital ne connaît jamais tous les métiers à l'avance. Il sait poser les mêmes cinq questions à chaque nouveau client.

## Vous faites avec appui

### La fiche contexte de votre client pilote

**Étape 9 : écrire la fiche contexte.** Copiez ce modèle dans une nouvelle conversation nommée « Client pilote · fiche », puis remplissez les crochets. Ne l'envoyez pas encore à Claude.

::: prompt
Fiche contexte · [activité ou structure, sans nom de famille]
Activité ou mission : [ce que fait votre client pilote, où]
Publics : [à qui il s'adresse : clients, parents, patients, membres…]
Besoin : [ce qui lui prend du temps ou lui manque]
Ton : [chaleureux, formel, simple…]
Contact : [comment le joindre : numéro professionnel, adresse, horaires]
:::

Postez la fiche dans le chat de la séance. C'est le **C** de toutes vos prochaines consignes pour ce client : vous la collerez à chaque fois.

![Étape 9 : la fiche contexte remplie](captures/etape-9.png)

::: structure
Ajoutez une sixième ligne : « Validation : [qui valide une publication officielle] ». Dans « Publics », écrivez des groupes, jamais des personnes : « les parents d'élèves », « les patients du centre ». Aucun nom d'élève, aucun dossier de patient, aucun salaire.
:::

### La consigne pour votre client pilote

**Étape 10 : construire la consigne.** Choisissez la tâche réelle notée avant la séance. Copiez cette consigne à trous et remplacez les crochets :

::: prompt
Tu es [rôle : la personne qui devrait écrire ce texte].
Écris [tâche : le texte à produire].
Contexte : [collez votre fiche contexte].
Format : [forme et longueur : message WhatsApp de cinq lignes, affiche, lettre d'une page…].
Contraintes : [ce qu'il faut respecter ou éviter].
:::

**Étape 11 : marquer et envoyer.** Avant d'envoyer, vérifiez chaque élément. Postez votre consigne dans le chat de la séance avec les lettres R, T, C, F, C devant chaque partie.

**Étape 12 : juger le résultat.** Le texte peut-il partir tel quel ? Si non, l'élément qui manquait dans votre consigne est presque toujours le contexte ou le format. Complétez la consigne, pas seulement la réponse.

Vérifiez votre travail :

- [ ] Les cinq éléments sont présents et marqués
- [ ] La fiche contexte est collée dans la partie C
- [ ] Le format dit la forme et la longueur
- [ ] Le texte de Claude peut être envoyé sans retouche
- [ ] Aucune donnée personnelle sensible dans votre consigne

::: coup-de-pouce
1. **Indice.** Lisez votre consigne comme si vous étiez Claude et que vous ne connaissiez pas votre client. Quelle information vous manquerait pour écrire juste ?
2. **Solution partielle.** Si vous bloquez, utilisez le mode tuteur : « Tu es mon tuteur. Je veux écrire une consigne pour [tâche]. Pose-moi une question à la fois pour remplir les cinq éléments : rôle, tâche, contexte, format, contraintes. N'écris pas la consigne à ma place. À la fin, montre-moi ma consigne complète et ce que je peux encore améliorer. »
3. **Solution complète.** « Tu es la gérante d'un petit restaurant. Écris un message pour annoncer que nous prenons maintenant les commandes la veille. Contexte : restaurant de quartier, clients qui travaillent dans les bureaux voisins, ils commandent sur WhatsApp ; nous voulons moins d'attente à midi ; ton chaleureux ; contact : numéro WhatsApp du restaurant. Format : message WhatsApp de cinq lignes au maximum. Contraintes : phrases courtes, un seul émoji, termine par l'heure limite de commande, 20 h. »
:::

::: defi
**La consigne critiquée.** Écrivez votre consigne sans le modèle à trous. Puis envoyez à Claude : « Voici ma consigne. Vérifie-la avec la grille rôle, tâche, contexte, format, contraintes. Dis-moi ce qui manque, sans réécrire le texte final. » Corrigez vous-même, puis aidez un binôme à faire la même chose.
:::

## Pour votre client pilote

Cette séance produit la **page 1 de votre Dossier client pilote** : la fiche contexte et un premier message prêt à envoyer.

1. Ouvrez votre **Dossier client pilote** (document Word dans « 05 · Ressources et liens utiles », copié dans votre portfolio).
2. Page 1 : collez la fiche contexte, la consigne de l'étape 10 et le texte final de Claude.
3. Montrez le message à votre client pilote ou, si c'est votre structure, à la personne qui valide. Notez sa réaction en une phrase.
4. Si le message est validé, envoyez-le. Notez la date d'envoi.

::: structure
Votre premier message est souvent une note à votre équipe, un message aux parents ou aux patients, ou une affiche. Notez aussi le temps que cette tâche vous prenait avant, et le temps qu'elle vous a pris avec Claude. C'est votre premier « temps gagné ».
:::

## Vous faites seul

Avant la prochaine séance, résolvez **cinq tâches dans cinq contextes différents** avec la grille R-T-C-F-C. Aucune consigne n'est fournie.

| N° | Contexte | Exemple |
|---|---|---|
| 1 | Votre vie personnelle | Une invitation, une demande à un propriétaire |
| 2 | Votre vie personnelle | Un message difficile à écrire |
| 3 | Votre client pilote | Une deuxième tâche réelle, différente de l'étape 10 |
| 4 | Une carte contexte que vous n'avez pas tirée | La carte suivante de la liste |
| 5 | Libre | Une tâche d'une personne de votre entourage |

Critères de qualité :

- Chaque consigne contient les cinq éléments, marqués R, T, C, F, C.
- Les cinq contextes sont différents.
- Au moins trois résultats peuvent partir tels quels.
- Pour la tâche 3, vous réutilisez votre fiche contexte.

Piste Défi : pour la tâche 3, demandez à Claude de critiquer votre consigne avec la grille avant de l'envoyer, puis comparez les deux résultats.

## Votre fiche-outil

**Fiche-outil 03 · La consigne R-T-C-F-C.** À garder sur votre téléphone : copiez la consigne à trous dans vos notes. Elle sert pour chaque client, chaque tâche.

| Élément | Question |
|---|---|
| R · Rôle | Qui doit écrire ? |
| T · Tâche | Qu'est-ce que je veux obtenir ? |
| C · Contexte | Pour qui, pourquoi, avec quelles informations ? Collez la fiche contexte du client. |
| F · Format | Quelle forme, quelle longueur ? |
| C · Contraintes | Ton, mots à éviter, éléments obligatoires ? |

Pour chaque nouveau client, écrivez d'abord sa fiche contexte, une fois :

::: prompt
Fiche contexte · [activité ou structure, sans nom de famille]
Activité ou mission : […]
Publics : […]
Besoin : […]
Ton : […]
Contact : […]
Validation (propre structure) : […]
:::

Puis, pour chaque tâche :

::: prompt
Tu es [rôle].
Écris [tâche].
Contexte : [fiche contexte du client].
Format : [forme et longueur].
Contraintes : [à respecter, à éviter].
:::

Avant d'envoyer : les cinq éléments sont là ? Aucune donnée sensible ? Avant d'utiliser : le texte peut partir tel quel ? Les noms, dates et chiffres sont justes ?

## Cas fil rouge

Mama Ngono vend des beignets-haricots à Mvog-Mbi, à Yaoundé. Sa première consigne : « Fais un message pour mes clients. » Claude répond avec un texte général. Avec la grille : « Tu es une vendeuse de beignets-haricots. Écris un message pour annoncer que je prends maintenant les commandes la veille. Contexte : mes clients sont des travailleurs du quartier qui passent le matin ; je veux moins d'attente à 7 h ; ton chaleureux. Format : message WhatsApp de quatre lignes. Contraintes : prix du jour inchangé, 25 FCFA le beignet (exemple), commande avant 21 h. » Elle envoie le message à son groupe de clients le soir même. Le lendemain, douze commandes l'attendent.

## Erreurs fréquentes

- **Oublier le contexte.** Claude ne connaît ni votre client ni votre ville. Sans contexte, le texte reste général. Collez toujours la fiche contexte.
- **Mettre des données sensibles dans la consigne.** Noms de patients, notes d'élèves, numéros de compte : jamais. Écrivez des groupes (« les parents ») et des informations publiques.
- **Corriger la réponse au lieu de la consigne.** Si le résultat est faux, c'est souvent la consigne qui manquait d'un élément. Complétez-la avec l'icône crayon.
- **Un format flou.** « Un petit texte » ne suffit pas. Dites la forme et la longueur : « message WhatsApp de cinq lignes ».

## Vérifiez vos acquis

Cochez seulement ce que vous venez de faire vous-même, sans aide.

- [ ] Votre consigne pour le client pilote contient les cinq éléments marqués, et le texte est utilisable sans retouche. Sinon : étapes 10 à 12.
- [ ] Vous avez adapté la consigne commune à une carte contexte. Sinon : étape 8.
- [ ] Votre fiche contexte tient en cinq lignes, sans donnée sensible. Sinon : étape 9.
- [ ] Quiz S02-1 : au moins 6 bonnes réponses sur 8.

## Votre livrable

Un document nommé **S02-1_Prenom** (par exemple S02-1_Aicha), créé dans votre portfolio, avant la prochaine séance. Chaque élément prouve une compétence :

1. **Consigne du client pilote :** la consigne marquée R, T, C, F, C et le texte final de Claude.
2. **Transfert :** la capture de la consigne adaptée à votre carte contexte et de la réponse.
3. **Fiche contexte :** la fiche de votre client pilote, en cinq lignes.
4. **Les cinq tâches :** pour chacune, le contexte en une ligne, la consigne et une capture du résultat.
5. **Trois phrases :** ce qui a changé entre votre consigne du questionnaire S02-0 et votre consigne de fin de séance, ce qui a le mieux marché, ce que vous ferez autrement.

Et dans votre **Dossier client pilote**, la page 1 remplie.

### Comment votre livrable est évalué

| Niveau | Ce que montre votre livrable |
|---|---|
| 1 · Découverte | Des consignes existent, mais il manque des éléments de la grille ou des captures. |
| 2 · Application guidée | Les consignes de la fiche sont complètes, la fiche contexte est remplie. |
| 3 · Autonomie | Cinq tâches dans cinq contextes, écrites par vous, avec les cinq éléments ; la page 1 du Dossier client pilote est remplie. |
| 4 · Transfert | Niveau 3, et le message du client pilote a été envoyé ou validé, avec sa réaction notée. Ou, piste Défi : la consigne critiquée et comparée. |

La séance est validée au niveau 3. Le jalon J1 demande au moins le niveau 2 à chaque livrable.

## Kit NotebookLM

Ajoutez cette fiche à votre notebook « Parcours Claude Pro ». Les sources et consignes de la semaine se trouvent dans le dossier « 03 · Réviser avec NotebookLM ».

## Mots-clés

Consigne (cinq éléments) · Grille R-T-C-F-C · Rôle · Format · Contraintes · Fiche contexte · Client pilote · Transfert · Carte contexte · Mode tuteur

---

Une formation OKOHO Consulting GmbH · Formateur : Dr. Bertrand Toumi
Claude est une marque d'Anthropic. Le Parcours Claude Pro est une formation indépendante proposée par OKOHO Consulting GmbH, sans partenariat avec Anthropic. Reproduction et diffusion interdites sans autorisation écrite d'OKOHO Consulting GmbH.
Version 1.0 · Fonctions vérifiées le 08.11.2026 (support.claude.com) · Captures d'écran réalisées le — · © 2026 OKOHO Consulting GmbH
