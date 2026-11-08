#!/usr/bin/env python3
"""Formulaires Google (diagnostic, quiz) · OKOHO Académie.

Lit quiz/*.yaml et écrit un script Google Apps Script prêt à coller :
  out/forms/creer_formulaires_<semaine>.gs
Le formateur l'exécute une fois sur script.google.com (compte de l'Académie) :
il crée les formulaires dans le dossier Drive de la semaine, avec logo, couleur Académie,
correction automatique des quiz, et écrit les liens à partager dans le journal d'exécution.
Usage : python3 tools/build_forms.py <ID_dossier_Drive | nom:Nom du dossier> [S00] [A00-02-formulaire A00-01 A00-03]
"""
import base64, json, sys
from common import ROOT, OUT, load_yaml

LOGO = ROOT / "design" / "logos" / "academie-logo-A-docx.png"

def js(s):
    return json.dumps(s, ensure_ascii=False)

def quiz_js(d, nom):
    desc = d["description"]
    if "reussite" in d:
        desc += f" Objectif : au moins {d['reussite']} bonnes réponses sur {len(d['questions'])}."
    lines = [f"  // {d['titre']}",
             f"  var f = nouveau({js(nom)}, {js(desc)});",
             "  f.setIsQuiz(true);",
             "  f.setShuffleQuestions(false);",
             "  f.addTextItem().setTitle('Prénom').setRequired(true);"]
    for q in d["questions"]:
        lines.append("  var it = f.addMultipleChoiceItem().setTitle(" + js(q["q"]) + ").setRequired(true).setPoints(1);")
        ch = ", ".join(f"it.createChoice({js(c)}, {'true' if i == q['bonne'] else 'false'})" for i, c in enumerate(q["choix"]))
        lines.append(f"  it.setChoices([{ch}]);")
        fb = js(q["explication"])
        lines.append(f"  it.setFeedbackForCorrect(FormApp.createFeedback().setText({fb}).build());")
        lines.append(f"  it.setFeedbackForIncorrect(FormApp.createFeedback().setText({fb}).build());")
    if d.get("pouls"):
        lines.append("  f.addPageBreakItem().setTitle('Pouls de la semaine (non noté)')"
                     ".setHelpText('Trois questions pour adapter le parcours à votre situation. Elles ne comptent pas dans votre score.');")
        for c in POULS:
            lines.append(champ_js(c))
    lines.append(f"  liens.push([{js(nom)}, f.getPublishedUrl()]);")
    return lines

# Trois questions non notées en fin de quiz (« pouls: true » dans quiz/<CODE>.yaml)
POULS = [
    {"type": "choix", "q": "Temps passé cette semaine sur le parcours, hors séance en direct",
     "choix": ["Moins d'une heure", "1 à 2 heures", "2 à 4 heures", "Plus de 4 heures"], "obligatoire": True},
    {"type": "paragraphe", "q": "Ce qui vous a bloqué cette semaine (une phrase suffit)", "obligatoire": False},
    {"type": "paragraphe", "q": "Où en est votre client pilote ? Qu'avez-vous produit pour lui cette semaine ?", "obligatoire": False},
]

def champ_js(c, var=None):
    """Une question de formulaire. var : nom de variable JavaScript si la question sert à un aiguillage."""
    req = "true" if c.get("obligatoire") else "false"
    aide = f".setHelpText({js(c['aide'])})" if c.get("aide") else ""
    pre = f"  var {var} = " if var else "  "
    t = c["type"]
    if t == "texte":
        val = ""
        if c.get("format") == "gmail":
            val = (".setValidation(FormApp.createTextValidation()"
                   ".setHelpText('Indiquez une adresse qui se termine par @gmail.com.')"
                   ".requireTextMatchesPattern('^[A-Za-z0-9._%+-]+@gmail[.]com$').build())")
        return f"{pre}f.addTextItem().setTitle({js(c['q'])}){aide}{val}.setRequired({req});"
    if t == "paragraphe":
        return f"{pre}f.addParagraphTextItem().setTitle({js(c['q'])}){aide}.setRequired({req});"
    if t == "choix":
        if var:
            return f"{pre}f.addMultipleChoiceItem().setTitle({js(c['q'])}){aide}.setRequired({req});"
        return f"{pre}f.addMultipleChoiceItem().setTitle({js(c['q'])}){aide}.setChoiceValues({js(c['choix'])}).setRequired({req});"
    if t == "cases":
        return f"{pre}f.addCheckboxItem().setTitle({js(c['q'])}){aide}.setChoiceValues({js(c['choix'])}).setRequired({req});"
    if t == "echelle":
        return f"{pre}f.addScaleItem().setTitle({js(c['q'])}){aide}.setBounds({c['min']}, {c['max']}).setLabels({js(c['bas'])}, {js(c['haut'])}).setRequired({req});"
    if t == "grille":
        return f"{pre}f.addGridItem().setTitle({js(c['q'])}){aide}.setRows({js(c['lignes'])}).setColumns({js(c['colonnes'])}).setRequired({req});"
    raise ValueError(f"type de champ inconnu : {t}")

def form_js(d):
    """Formulaire non noté. Aiguillage :
    - section « id » : identifiant de la section ;
    - champ choix avec « aller_a » {choix: id_section} : la réponse mène à cette section ;
    - section « suite » : id de la section où l'on va après celle-ci (au lieu de la suivante)."""
    lines = [f"  // {d['titre']}", f"  var f = nouveau({js(d['titre'])}, {js(d['description'])});",
             "  f.setProgressBar(true);", "  var sec = {};"]
    aiguillages, suites = [], []
    for n, sec in enumerate(d["sections"]):
        sid = sec.get("id", f"s{n}")
        if n:
            lines.append(f"  sec[{js(sid)}] = f.addPageBreakItem().setTitle({js(sec['titre'])});")
            if sec.get("suite"):
                suites.append((n, sec["suite"]))
        else:
            lines.append(f"  f.addSectionHeaderItem().setTitle({js(sec['titre'])});")
        if sec.get("texte"):
            lines.append(f"  f.addSectionHeaderItem().setHelpText({js(sec['texte'])});")
        for k, c in enumerate(sec["champs"]):
            if c.get("aller_a"):
                var = f"aig{n}_{k}"
                lines.append(champ_js(c, var))
                aiguillages.append((var, c))
            else:
                lines.append(champ_js(c))
    for var, c in aiguillages:
        ch = ", ".join(f"{var}.createChoice({js(v)}, sec[{js(c['aller_a'][v])}])" for v in c["choix"])
        lines.append(f"  {var}.setChoices([{ch}]);")
    # « suite » : la section n se termine sur la section cible. Google Forms règle ce saut
    # sur le saut de page qui SUIT la section n.
    ids = [s_.get("id", f"s{i}") for i, s_ in enumerate(d["sections"])]
    for n, cible in suites:
        if n + 1 < len(ids):
            lines.append(f"  sec[{js(ids[n + 1])}].setGoToPage(sec[{js(cible)}]);")
    lines.append(f"  liens.push([{js(d['titre'])}, f.getPublishedUrl()]);")
    return lines

def ordre(code, cohorte="cohorte-1"):
    """Position du code dans sa semaine (S01-1 → « 1 »), lue dans parcours/<cohorte>.yaml."""
    f = ROOT / "parcours" / f"{cohorte}.yaml"
    if f.is_file():
        for s in load_yaml(f)["semaines"]:
            for i, it in enumerate(s.get("items", []), 1):
                if it["code"] == code:
                    return str(i)
    return ""

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    dossier = sys.argv[1]
    semaine = sys.argv[2] if len(sys.argv) > 2 else "S00"
    noms = sys.argv[3:] or ["A00-02-formulaire", "A00-01", "A00-03"]
    logo_b64 = base64.b64encode(LOGO.read_bytes()).decode()
    out = ["/**",
           f" * OKOHO Académie · Formulaires de la semaine {semaine} · généré par tools/build_forms.py",
           f" * Utilisation : projet Apps Script OKOHO_Academie.gs (déjà autorisé) › Fichiers › + › Script « Formulaires_{semaine} » › coller › Enregistrer › Exécuter « creerFormulaires{semaine} ».",
           " * Autoriser l'accès au compte de l'Académie. Les liens à partager s'affichent dans le journal d'exécution.",
           " * OBLIGATOIRE après exécution, pour chaque quiz (Apps Script ne peut pas le régler) :",
           " *   Paramètres › Quiz › Publier la note : « Immédiatement après chaque envoi »,",
           " *   puis activer Questions manquées, Bonnes réponses, Valeur en points.",
           " *   Sinon le quiz reste sur « Plus tard » sans collecte d'e-mails et les réponses ne s'envoient pas.",
           " * Une formation OKOHO Consulting GmbH · Formateur : Dr. Bertrand Toumi",
           " */",
           f"function creerFormulaires{semaine}() {{",
           "  // Tout est encapsulé : le code peut être ajouté au projet OKOHO_Academie.gs sans écraser d'autres fonctions.",
           f"var DOSSIER_ID = {js(dossier)};",
           f"var LOGO_B64 = {js(logo_b64)};",
           "",
           "// DOSSIER_ID : identifiant du dossier Drive, « nom:<nom exact du dossier> » (premier dossier de ce nom)",
           "// ou « chemin:<racine>/<sous-dossier>/… » (dossiers créés s'ils manquent, mêmes noms que « synchroniser »).",
           "function dossier() {",
           "  if (DOSSIER_ID.indexOf('chemin:') === 0) {",
           "    var parts = DOSSIER_ID.slice(7).split('/'), r = DriveApp.getFoldersByName(parts[0]);",
           "    if (!r.hasNext()) throw new Error('Racine introuvable : ' + parts[0]);",
           "    var d = r.next();",
           "    parts.slice(1).forEach(function (p) { var it = d.getFoldersByName(p); d = it.hasNext() ? it.next() : d.createFolder(p); });",
           "    return d;",
           "  }",
           "  if (DOSSIER_ID.indexOf('nom:') !== 0) return DriveApp.getFolderById(DOSSIER_ID);",
           "  var it = DriveApp.getFoldersByName(DOSSIER_ID.slice(4));",
           "  if (!it.hasNext()) throw new Error('Dossier introuvable : ' + DOSSIER_ID.slice(4) + '. Lancez d\\'abord « synchroniser ».');",
           "  return it.next();",
           "}",
           "",
           "function nouveau(titre, description) {",
           "  var f = FormApp.create(titre);",
           "  f.setTitle(titre).setDescription(description + '\\n\\nUne formation OKOHO Consulting GmbH · Formateur : Dr. Bertrand Toumi · okoho.de');",
           "  f.setConfirmationMessage('Merci. Vos réponses sont enregistrées. OKOHO Académie · Parcours Claude Pro');",
           "  f.addImageItem().setImage(Utilities.newBlob(Utilities.base64Decode(LOGO_B64), 'image/png', 'logo.png')).setWidth(220);",
           "  try { f.setPublished(true); } catch (e) {}",
           "  var fichier = DriveApp.getFileById(f.getId());",
           "  fichier.moveTo(dossier());",
           "  fichier.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);  // jamais Éditeur",
           "  return f;",
           "}",
           "",
           "  var liens = [];"]
    for n in noms:
        d = load_yaml(ROOT / "quiz" / f"{n}.yaml")
        code = d["code"]
        num = {"A00-01": "1", "A00-02": "2", "A00-03": "3"}.get(code) or ordre(code)
        if "sections" in d:
            out += form_js(d)
        else:
            out += quiz_js(d, f"{semaine}-{num} · {d['titre']}")
        out.append("")
    out += ["  liens.forEach(function (l) { Logger.log(l[0] + ' : ' + l[1]); });",
            "  Logger.log('À FAIRE pour chaque quiz : Paramètres › Quiz › Publier la note « Immédiatement après chaque envoi ».');", "}", "",
            ]
    dest = OUT / "forms"
    dest.mkdir(parents=True, exist_ok=True)
    p = dest / f"creer_formulaires_{semaine}.gs"
    p.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"forms : {p}")

if __name__ == "__main__":
    main()
