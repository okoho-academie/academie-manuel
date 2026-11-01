---
code: M01-S2
partie: I
module: M01
titre: Fichiers, images et application mobile
type: autonomie
outil: Claude Chat
appareil: smartphone
duree: {seance: 60, devoir: 30}
prerequis: [M01-S1]
echafaudage: 1
acces_defaut: programme
jalon: J1
livrable: Analyse d'une photo ou d'un document du quotidien
competences:
  - code: M01-S2-C1
    jalon: J1-C1
    savoir_faire: Vous faites lire une photo de document par Claude et obtenez un tableau.
    preuve: Vous photographiez un document papier du quotidien et demandez un tableau de ses informations principales.
    reussi_si: Le tableau reprend la date, l'émetteur, les montants et le total du document.
  - code: M01-S2-C2
    jalon: J1-C4
    savoir_faire: Vous vérifiez une réponse de Claude avant de l'utiliser.
    preuve: Vous comparez deux valeurs du tableau avec le document original et notez le résultat.
    reussi_si: Deux valeurs sont comparées ; chaque écart est signalé à Claude et corrigé dans la conversation.
  - code: M01-S2-C3
    jalon: J1-C4
    savoir_faire: Vous choisissez ce que vous envoyez à Claude sans exposer de données sensibles.
    preuve: Vous choisissez votre document vous-même et citez trois types de documents que vous n'envoyez jamais.
    reussi_si: Aucune pièce d'identité, donnée bancaire, code ou donnée de santé dans vos captures ; les trois types cités sont justes.
glossaire: [Pièce jointe, Mode tuteur, Hallucination]
index: [Pièce jointe, Images (analyser), Fichiers (envoyer à Claude), Mobile (application Claude), Mode tuteur, Vérification des faits]
videos: {tutoriel: true, vitrine: false, shorts: 0, signature: false}
verifie: "2026-10-31"
version: "1.1"
captures: null
status: relecture
---

# M01-S2 · Fichiers, images et application mobile

## Ce que vous saurez faire

| Vous savez… | Vous le prouvez… | C'est réussi si… |
|---|---|---|
| Vous faites lire une photo de document par Claude et obtenez un tableau. | Vous photographiez un document papier du quotidien et demandez un tableau de ses informations principales. | Le tableau reprend la date, l'émetteur, les montants et le total du document. |
| Vous vérifiez une réponse de Claude avant de l'utiliser. | Vous comparez deux valeurs du tableau avec le document original et notez le résultat. | Deux valeurs sont comparées ; chaque écart est signalé à Claude et corrigé dans la conversation. |
| Vous choisissez ce que vous envoyez à Claude sans exposer de données sensibles. | Vous choisissez votre document vous-même et citez trois types de documents que vous n'envoyez jamais. | Aucune pièce d'identité, donnée bancaire, code ou donnée de santé dans vos captures ; les trois types cités sont justes. |

Ces trois compétences comptent pour le jalon **J1 · Utilisateur autonome**. En chemin, vous découvrez aussi l'envoi d'un document PDF ou Word et le mode tuteur.

## Pourquoi c'est utile

Votre téléphone devient un scanner intelligent. Une facture, un reçu, une étiquette, un tableau affiché au mur : Claude les lit, les résume et en tire un tableau en quelques secondes. Demain, vous ferez le même travail pour un client qui croule sous les papiers.

Durée : 60 minutes, en autonomie. Appareil : téléphone avec l'application Claude.

**Deux pistes, les mêmes compétences.** Suivez la fiche pas à pas. Si vous êtes à l'aise, faites aussi les encadrés **Piste Défi**.

## Avant de commencer

- [ ] L'application Claude est installée sur votre téléphone, éditeur Anthropic, et vous êtes connecté.
- [ ] Vous avez sous la main un document papier du quotidien : reçu de caisse, facture, étiquette de produit, bon de livraison.
- [ ] Ce document ne contient aucune pièce d'identité, aucun numéro de compte bancaire, aucun code secret, aucune donnée de santé.

Règle d'or : ce que vous ne montreriez pas à un inconnu, vous ne l'envoyez pas à une IA.

## Je vous montre

### Envoyer une photo ou un fichier

1. Dans une conversation, touchez le bouton **+** à gauche de la zone de saisie.
2. Choisissez l'appareil photo pour photographier, la galerie pour une photo existante, ou les fichiers pour un PDF ou un document Word.
3. La pièce jointe apparaît au-dessus de la zone de saisie. Écrivez votre consigne, puis envoyez.

![Étape 1 : le bouton + et ses choix sur téléphone](captures/etape-1.png)

Ce que Claude accepte (vérifié sur support.claude.com, date en bas de la fiche) : images JPEG, PNG, GIF et WebP ; documents PDF, DOCX, TXT, CSV et d'autres formats texte. Jusqu'à 20 fichiers par conversation.

### Exemple complet

Photo d'un reçu de supermarché, puis cette consigne : « Lis ce reçu. Fais un tableau avec trois colonnes : produit, quantité, prix. Donne le total à la fin et dis-moi si le total calculé correspond au total imprimé. »

Claude répond avec un tableau. Vous comparez deux lignes avec le papier : elles sont justes. Le tutoriel vidéo de la séance montre ce geste du début à la fin.

## Nous faisons ensemble

Suivez les étapes avec votre propre document.

**Étape 2 : photographier.** Posez le document à plat, dans un endroit bien éclairé. Touchez **+**, puis l'appareil photo. Cadrez tout le document, sans votre main.

![Étape 2 : photo d'un reçu cadrée correctement](captures/etape-2.png)

**Étape 3 : demander une lecture.** Copiez cette consigne et envoyez-la avec la photo.

::: prompt
Lis ce document. Dis-moi en deux phrases de quoi il s'agit. Ensuite, fais un tableau avec les informations principales : date, émetteur, articles ou prestations, montants, total.
:::

![Étape 3 : la réponse de Claude avec le tableau](captures/etape-3.png)

**Étape 4 : vérifier deux valeurs.** Choisissez deux chiffres du tableau et comparez-les avec le papier. Notez-les.

**Étape 5 : demander une action.** Dans la même conversation, envoyez :

::: prompt
Merci. À partir de ce document, écris-moi un rappel court de ce que je dois faire : payer, garder le reçu, contacter quelqu'un, ou rien. Une liste de trois points maximum.
:::

**Étape 6 : renommer.** Donnez un nom clair à la conversation, par exemple « Reçu courses ».

## Vous faites avec appui

Cette fois, envoyez un **document** (PDF ou Word) : une notice, un règlement, une lettre reçue, un programme. Le téléphone suffit : le bouton **+** ouvre aussi vos fichiers.

**Étape 7 : envoyer le document.** Touchez **+**, choisissez le fichier, puis copiez cette consigne en remplaçant les crochets.

::: prompt
Voici [type de document, par exemple : le règlement de mon association]. Résume-le en cinq points simples. Ensuite, réponds à cette question : [votre question, par exemple : quelles sont les obligations des membres ?]. Indique à quel endroit du document tu as trouvé la réponse.
:::

**Étape 8 : demander le mode tuteur.** Pour mieux comprendre le document, envoyez :

::: prompt
Passe en mode tuteur. Ne me donne pas les réponses. Pose-moi trois questions, une à la fois, pour vérifier que j'ai compris ce document. Après chacune de mes réponses, dis-moi si c'est juste et explique en une phrase.
:::

Vérifiez votre travail :

- [ ] Le résumé correspond vraiment au document (relisez un passage)
- [ ] Claude indique où il a trouvé la réponse
- [ ] Vous avez répondu aux trois questions du mode tuteur

::: coup-de-pouce
1. **Indice.** Claude ne lit pas bien la photo ? Reprenez-la avec plus de lumière, sans reflet, le document bien à plat.
2. **Solution partielle.** Claude invente une information absente du document ? Écrivez : « Réponds uniquement avec ce qui est écrit dans le document. Si l'information n'y est pas, dis-le. »
3. **Solution complète.** « Voici la notice de mon nouveau fer à repasser. Résume-la en cinq points simples. Ensuite, réponds à cette question : comment le nettoyer sans l'abîmer ? Indique à quel endroit du document tu as trouvé la réponse. Réponds uniquement avec ce qui est écrit dans le document. »
:::

::: defi
**Photo ou fichier : qui gagne ?** Envoyez le même document deux fois dans deux conversations : une fois en photo, une fois en PDF. Demandez le même tableau. Comparez : quelle version contient le moins d'erreurs ? Notez votre conclusion en une phrase.

**Piéger Claude, pour apprendre.** Posez une question dont la réponse n'est pas dans le document. Claude reconnaît-il qu'il ne sait pas, ou invente-t-il ? Une réponse inventée avec assurance s'appelle une **hallucination**. Elle se vérifie toujours.
:::

## Vous faites seul

Choisissez une photo ou un document utile pour vous ou un proche. Aucune consigne n'est fournie : vous écrivez vous-même votre demande.

Critères de qualité :

- Le document ne contient aucune donnée sensible.
- La demande précise le résultat attendu (tableau, résumé, liste d'actions).
- Deux valeurs de la réponse sont vérifiées sur l'original.
- Vous gardez une trace : la conversation porte un nom clair.

## Cas fil rouge

Aïcha, couturière à Bonamoussadi, reçoit la facture de son fournisseur de tissus au marché Sandaga. Elle la photographie, demande un tableau des pagnes achetés avec les prix au mètre, et vérifie deux lignes : une erreur de quantité apparaît, la photo était floue. Elle reprend la photo, tout est juste. Ensuite, elle demande à Claude un rappel : payer le solde avant la fin du mois.

## Erreurs fréquentes

- **Envoyer une pièce d'identité ou un relevé bancaire.** Jamais. Masquez ou choisissez un autre document.
- **Croire la réponse sans vérifier.** Une photo floue ou un document mal cadré donne des chiffres faux. Vérifiez toujours deux valeurs.
- **Envoyer la photo sans consigne.** Claude décrit l'image, sans plus. Dites ce que vous voulez obtenir.
- **Photographier de travers, à contre-jour.** Document à plat, bonne lumière, cadre complet.

## Vérifiez vos acquis

Cochez seulement ce que vous avez fait vous-même, sans aide.

- [ ] Claude a lu votre photo et rendu un tableau avec date, émetteur, montants et total. Sinon : étapes 2 et 3.
- [ ] Vous avez comparé deux valeurs avec l'original et corrigé les écarts. Sinon : étape 4.
- [ ] Vous citez sans regarder trois types de documents que vous n'envoyez jamais. Sinon : « Avant de commencer ».
- [ ] Quiz S01-2 : au moins 5 bonnes réponses sur 6.

## Votre livrable

Un document Google Docs nommé **S01-2_Prenom**, créé dans votre portfolio, avant la prochaine séance. Chaque élément prouve une compétence :

1. **Capture 1 :** la photo envoyée (document entier, lisible) et le tableau rendu par Claude.
2. **Capture 2 :** votre message à Claude qui signale un écart, ou la phrase « Les deux valeurs vérifiées sont justes : … ».
3. **Cinq lignes :** le document choisi, la demande, les deux valeurs vérifiées, ce que vous en faites, les trois types de documents que vous n'envoyez jamais.

Piste Défi : ajoutez votre conclusion « photo ou fichier » et le résultat de votre test d'hallucination.

### Comment votre livrable est évalué

| Niveau | Ce que montre votre livrable |
|---|---|
| 1 · Découverte | Une photo envoyée, mais le tableau manque ou aucune valeur n'est vérifiée. |
| 2 · Application guidée | Tableau complet avec la consigne de la fiche, deux valeurs comparées. |
| 3 · Autonomie | Un document choisi par vous, une demande écrite par vous, deux valeurs vérifiées, écarts corrigés, aucune donnée sensible. |
| 4 · Transfert | Niveau 3, et le résultat sert à quelqu'un : un rappel de paiement, un tableau de dépenses partagé. Ou, piste Défi : la comparaison photo et fichier est argumentée. |

La séance est validée au niveau 3. Le jalon J1 demande au moins le niveau 2 à chaque livrable.

## Kit NotebookLM

Ajoutez cette fiche à votre notebook « Parcours Claude Pro ». Les sources et consignes de la semaine se trouvent dans le dossier « 03 · Réviser avec NotebookLM ».

## Mots-clés

Pièce jointe · Images (analyser) · Fichiers (envoyer à Claude) · Mobile (application Claude) · Mode tuteur · Vérification des faits

---

Une formation OKOHO Consulting GmbH · Formateur : Dr. Bertrand Toumi
Claude est une marque d'Anthropic. Le Parcours Claude Pro est une formation indépendante proposée par OKOHO Consulting GmbH, sans partenariat avec Anthropic. Reproduction et diffusion interdites sans autorisation écrite d'OKOHO Consulting GmbH.
Version 1.1 · Fonctions vérifiées le 31.10.2026 (support.claude.com) · Captures d'écran réalisées le — · © 2026 OKOHO Consulting GmbH
