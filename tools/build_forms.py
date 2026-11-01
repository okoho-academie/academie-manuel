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
    lines.append(f"  liens.push([{js(nom)}, f.getPublishedUrl()]);")
    return lines

def form_js(d):
    lines = [f"  // {d['titre']}", f"  var f = nouveau({js(d['titre'])}, {js(d['description'])});",
             "  f.setProgressBar(true);"]
    first = True
    for sec in d["sections"]:
        if not first:
            lines.append(f"  f.addPageBreakItem().setTitle({js(sec['titre'])});")
        else:
            lines.append(f"  f.addSectionHeaderItem().setTitle({js(sec['titre'])});")
        first = False
        if sec.get("texte"):
            lines.append(f"  f.addSectionHeaderItem().setHelpText({js(sec['texte'])});")
        for c in sec["champs"]:
            req = "true" if c.get("obligatoire") else "false"
            aide = f".setHelpText({js(c['aide'])})" if c.get("aide") else ""
            t = c["type"]
            if t == "texte":
                lines.append(f"  f.addTextItem().setTitle({js(c['q'])}){aide}.setRequired({req});")
            elif t == "paragraphe":
                lines.append(f"  f.addParagraphTextItem().setTitle({js(c['q'])}){aide}.setRequired({req});")
            elif t == "choix":
                lines.append(f"  f.addMultipleChoiceItem().setTitle({js(c['q'])}){aide}.setChoiceValues({js(c['choix'])}).setRequired({req});")
            elif t == "cases":
                lines.append(f"  f.addCheckboxItem().setTitle({js(c['q'])}){aide}.setChoiceValues({js(c['choix'])}).setRequired({req});")
            elif t == "echelle":
                lines.append(f"  f.addScaleItem().setTitle({js(c['q'])}).setBounds({c['min']}, {c['max']}).setLabels({js(c['bas'])}, {js(c['haut'])}).setRequired({req});")
            elif t == "grille":
                lines.append(f"  f.addGridItem().setTitle({js(c['q'])}).setRows({js(c['lignes'])}).setColumns({js(c['colonnes'])}).setRequired({req});")
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
           f" * Utilisation : script.google.com › Nouveau projet › coller ce code › Enregistrer › Exécuter « creerFormulaires{semaine} » (ou « creer »).",
           " * Autoriser l'accès au compte de l'Académie. Les liens à partager s'affichent dans le journal d'exécution.",
           " * Une formation OKOHO Consulting GmbH · Formateur : Dr. Bertrand Toumi",
           " */",
           f"var DOSSIER_ID = {js(dossier)};",
           f"var LOGO_B64 = {js(logo_b64)};",
           "",
           "// DOSSIER_ID : identifiant du dossier Drive, ou « nom:<nom exact du dossier> » (le premier dossier de ce nom est utilisé).",
           "function dossier() {",
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
           "  DriveApp.getFileById(f.getId()).moveTo(dossier());",
           "  return f;",
           "}",
           "",
           f"function creerFormulaires{semaine}() {{",
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
    out += ["  liens.forEach(function (l) { Logger.log(l[0] + ' : ' + l[1]); });", "}", "",
            "// Raccourci identique au nom historique", f"function creer() {{ creerFormulaires{semaine}(); }}"]
    dest = OUT / "forms"
    dest.mkdir(parents=True, exist_ok=True)
    p = dest / f"creer_formulaires_{semaine}.gs"
    p.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"forms : {p}")

if __name__ == "__main__":
    main()
