/**
 * OKOHO Académie · Synchronisation Google Drive (GitHub → Drive)
 * Recopie la branche « publication » du dépôt academie-manuel dans le Drive de l'Académie.
 * Remplace les fichiers modifiés, place les anciens à la corbeille, crée les dossiers manquants.
 * Installation unique : voir « Mode d'emploi » en bas de ce fichier.
 * Une formation OKOHO Consulting GmbH · Formateur : Dr. Bertrand Toumi
 */
var CONFIG = {
  racineId: '{{RACINE_ID}}',            // dossier privé « OKOHO Académie · Parcours Claude Pro »
  cohorte: '{{COHORTE}}',
  // Deux sources : le cours (public pour les participants) et le privé du formateur (contrats, manuel).
  // La seconde exige que le jeton GITHUB_TOKEN ait aussi accès au dépôt academie-pilotage ; sinon elle est ignorée.
  sources: [
    { depot: 'okoho-academie/academie-manuel', branche: 'publication', base: 'drive/{{COHORTE}}/' },
    { depot: 'okoho-academie/academie-pilotage', branche: 'publication-prive', base: 'prive/', facultatif: true }
  ]
};

function jeton_() {
  var t = PropertiesService.getScriptProperties().getProperty('GITHUB_TOKEN');
  if (!t) throw new Error('Propriété GITHUB_TOKEN absente : Paramètres du projet › Propriétés du script.');
  return t;
}

function github_(src, chemin) {
  var url = 'https://api.github.com/repos/' + src.depot + '/contents/' +
    chemin.split('/').map(encodeURIComponent).join('/') + '?ref=' + src.branche;
  var r = UrlFetchApp.fetch(url, {
    headers: { Authorization: 'Bearer ' + jeton_(), Accept: 'application/vnd.github.raw' },
    muteHttpExceptions: true
  });
  if (r.getResponseCode() !== 200) throw new Error('GitHub ' + r.getResponseCode() + ' pour ' + chemin);
  return r;
}

// GitHub livre les fichiers en « octet-stream » : sans type explicite, Drive n'affiche pas d'aperçu.
function type_(nom) {
  if (/\.pdf$/i.test(nom)) return 'application/pdf';
  if (/\.docx$/i.test(nom)) return 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
  if (/\.txt$/i.test(nom)) return 'text/plain';   // sinon le .txt est recopié à chaque synchronisation
  return 'application/octet-stream';
}

function dossier_(parent, nom) {
  var it = parent.getFoldersByName(nom);
  return it.hasNext() ? it.next() : parent.createFolder(nom);
}

function synchroniser() {
  var racine = DriveApp.getFolderById(CONFIG.racineId);
  var attendus = {}, dossiers = {}, nouveaux = [], erreurs = [];
  CONFIG.sources.forEach(function (src) {
    var manifeste;
    try { manifeste = JSON.parse(github_(src, src.base + 'manifest.json').getContentText()); }
    catch (e) { if (src.facultatif) { erreurs.push(src.depot + ' ignoré (' + e.message + ')'); return; } throw e; }
    manifeste.fichiers.forEach(function (f) {
      var parts = f.chemin.split('/');
      var nom = parts.pop();
      var d = racine;
      parts.forEach(function (p) { d = dossier_(d, p); });
      dossiers[d.getId()] = d;
      attendus[d.getId() + '/' + nom] = true;
      var present = false, it = d.getFilesByName(nom);
      while (it.hasNext()) {
        var x = it.next();
        if (x.getDescription() === 'sha:' + f.sha && x.getMimeType() === type_(nom) && !present) { present = true; }
        else { x.setTrashed(true); }
      }
      if (!present) {
        var blob = github_(src, src.base + f.chemin).getBlob().setName(nom).setContentType(type_(nom));
        d.createFile(blob).setDescription('sha:' + f.sha);
        nouveaux.push(f.chemin);
      }
    });
  });
  // PDF et Word absents de la publication (anciennes versions, dépôts manuels) : corbeille.
  // Les formulaires et documents Google ne sont jamais touchés.
  var geres = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/octet-stream'];
  Object.keys(dossiers).forEach(function (id) {
    var it = dossiers[id].getFiles();
    while (it.hasNext()) {
      var x = it.next();
      if (geres.indexOf(x.getMimeType()) >= 0 && !attendus[id + '/' + x.getName()]) x.setTrashed(true);
    }
  });
  garderLecteur_(racine);
  Logger.log(nouveaux.length ? 'Mis à jour : \n' + nouveaux.join('\n') : 'Rien à mettre à jour.');
  if (erreurs.length) Logger.log('Remarque : ' + erreurs.join(' · '));
}

// Règle depuis le 07.11.2026 : « Espace participants » et tout son contenu (formulaires compris)
// restent en « Tous les utilisateurs disposant du lien : Lecteur ». Jamais « Éditeur ».
// Chaque synchronisation remet en Lecteur ce qui serait passé en Éditeur.
function garderLecteur_(racine) {
  function fixe(x) {
    try {
      if (x.getSharingAccess() === DriveApp.Access.ANYONE_WITH_LINK && x.getSharingPermission() === DriveApp.Permission.EDIT) {
        x.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
        Logger.log('Remis en Lecteur : ' + x.getName());
      }
    } catch (e) { Logger.log('Partage non modifiable : ' + x.getName() + ' · ' + e.message); }
  }
  function parcourir(d) {
    fixe(d);
    var f = d.getFiles(); while (f.hasNext()) fixe(f.next());
    var s = d.getFolders(); while (s.hasNext()) parcourir(s.next());
  }
  var it = racine.getFolders();
  while (it.hasNext()) { var d = it.next(); if (/Espace participants/.test(d.getName())) parcourir(d); }
}

function installer() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'synchroniser') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('synchroniser').timeBased().everyHours(1).create();
  synchroniser();
}

/* Mode d'emploi (une seule fois)
 * 1. github.com › Settings › Developer settings › Fine-grained tokens › Generate new token :
 *    Resource owner : okoho-academie · Repository access : academie-manuel · Permissions : Contents = Read-only.
 * 2. Ici : Paramètres du projet (roue dentée) › Propriétés du script › Ajouter : GITHUB_TOKEN = le jeton.
 * 3. Choisir la fonction « installer » › Exécuter › Autoriser.
 * Ensuite, la synchronisation tourne seule toutes les heures. Pour forcer : exécuter « synchroniser ».
 */
