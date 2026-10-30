/**
 * OKOHO Académie · Synchronisation Google Drive (GitHub → Drive)
 * Recopie la branche « publication » du dépôt academie-manuel dans le Drive de l'Académie.
 * Remplace les fichiers modifiés, place les anciens à la corbeille, crée les dossiers manquants.
 * Installation unique : voir « Mode d'emploi » en bas de ce fichier.
 * Une formation OKOHO Consulting GmbH · Formateur : Dr. Bertrand Toumi
 */
var CONFIG = {
  racineId: '{{RACINE_ID}}',            // dossier privé « OKOHO Académie · Parcours Claude Pro »
  depot: 'okoho-academie/academie-manuel',
  branche: 'publication',
  cohorte: '{{COHORTE}}'
};

function jeton_() {
  var t = PropertiesService.getScriptProperties().getProperty('GITHUB_TOKEN');
  if (!t) throw new Error('Propriété GITHUB_TOKEN absente : Paramètres du projet › Propriétés du script.');
  return t;
}

function github_(chemin) {
  var url = 'https://api.github.com/repos/' + CONFIG.depot + '/contents/' +
    chemin.split('/').map(encodeURIComponent).join('/') + '?ref=' + CONFIG.branche;
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
  return 'application/octet-stream';
}

function dossier_(parent, nom) {
  var it = parent.getFoldersByName(nom);
  return it.hasNext() ? it.next() : parent.createFolder(nom);
}

function synchroniser() {
  var base = 'drive/' + CONFIG.cohorte + '/';
  var manifeste = JSON.parse(github_(base + 'manifest.json').getContentText());
  var racine = DriveApp.getFolderById(CONFIG.racineId);
  var attendus = {}, dossiers = {}, nouveaux = [];
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
      var blob = github_(base + f.chemin).getBlob().setName(nom).setContentType(type_(nom));
      d.createFile(blob).setDescription('sha:' + f.sha);
      nouveaux.push(f.chemin);
    }
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
  Logger.log(nouveaux.length ? 'Mis à jour : \n' + nouveaux.join('\n') : 'Rien à mettre à jour.');
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
