#!/usr/bin/env python3
"""Sortie Google Drive d'une cohorte · OKOHO Académie.

1. Génère les PDF datés de la cohorte (tools/build_pdf.py --cohorte=…) dans out/pdf/<cohorte>/.
2. Les copie dans out/drive/<cohorte>/ avec des noms lisibles par les apprenants.
3. Écrit les textes Google Docs (programme, « Commencez ici ») dans out/drive/<cohorte>/_google_docs/.
4. Écrit manifest.json (dossier, nom, source) pour le chargement dans Drive.
Les sources restent sans date : seule la sortie porte les dates de la cohorte.

Règle de nommage (source : parcours/cohorte-N.yaml) :
  Dossier : "Semaine NN · JJ.MM.AAAA · <titre>"
  Fichier : "SNN-<ordre> · <Type> · <Code séance> <Titre>.pdf"
  Pas de « : » dans les noms (interdit sous Windows) : remplacé par « , ».
Usage : python3 tools/build_drive.py [cohorte-1]
"""
import json, shutil, subprocess, sys
from datetime import date
from common import ROOT, OUT, load_yaml, read_seance, resolve

def clean(s):
    return s.replace(" : ", ", ").replace(":", ",").replace("/", "-").strip()

def source_of(code):
    p = ROOT / ("accueil" if code.startswith("A00") else "seances") / code
    f = p / ("document.md" if code.startswith("A00") else "seance.md")
    if not f.is_file():
        return None, None
    meta, _ = read_seance(f)
    typ = "Guide" if code.startswith("A00") else "Fiche"
    return meta, (typ, str(meta.get("version", "0.1")))

def folder_name(s):
    d = date.fromisoformat(s["date"]).strftime("%d.%m.%Y")
    return f"Semaine {s['n']:02d} · {d} · {s['titre']}"

def file_name(s, i, item, meta):
    code = item["code"]
    titre = meta["titre"]
    label = titre if code.startswith("A00") else f"{code} {titre}"
    return clean(f"S{s['n']:02d}-{i} · {item['type']} · {label}")

def gdoc_md(src, cal, titre=None):
    """Markdown pour Google Docs : encadrés ::: en titres, sans images ni en-tête YAML."""
    import re
    t = src.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?", t, re.S)
    if m:
        t = t[m.end():]
    lab = {"objectifs": "Ce que vous saurez faire", "livrable": "Votre livrable", "prompt": "Consigne à copier",
           "fil-rouge": "Cas fil rouge", "erreurs": "Erreurs fréquentes", "coup-de-pouce": "Coup de pouce"}
    out = [f"# {titre}", ""] if titre else []
    for l in resolve(t, cal).splitlines():
        mm = re.match(r"^::: ?([\w-]+)\s*$", l)
        if mm:
            out += [f"### {lab.get(mm.group(1), mm.group(1))}", ""]; continue
        if l.strip() == ":::" or l.startswith("!["):
            continue
        out.append(l)
    if titre:
        out[2:2] = ["*Une formation OKOHO Consulting GmbH · Formateur : Dr. Bertrand Toumi*", ""]
        out += ["", "---", "", f"© {date.today().year} OKOHO Consulting GmbH · okoho.de · info@okoho.de · +49 5231 5682750", "",
                "Claude est une marque d'Anthropic. Le Parcours Claude Pro est une formation indépendante proposée par "
                "OKOHO Consulting GmbH, sans partenariat avec Anthropic."]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"

def main():
    nom = sys.argv[1] if len(sys.argv) > 1 else "cohorte-1"
    cal = load_yaml(ROOT / "parcours" / f"{nom}.yaml")
    codes = [it["code"] for s in cal["semaines"] for it in s.get("items", [])] + [cal.get("programme", {}).get("code", "A00-00")]
    existants = [c for c in codes if source_of(c)[0]]
    subprocess.run([sys.executable, str(ROOT / "tools" / "build_pdf.py"), *existants, f"--cohorte={nom}"], check=True)
    dest = OUT / "drive" / nom
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    manifest, manquants = [], []
    for s in cal["semaines"]:
        dossier = "02 · Séances semaine par semaine/" + folder_name(s)
        for i, item in enumerate(s.get("items", []), 1):
            meta, info = source_of(item["code"])
            if meta and meta.get("status") == "brouillon":
                manquants.append(item["code"]); continue
            pdf = OUT / "pdf" / nom / f"OKOHO_PCP_{item['code']}_{info[0]}_v{info[1]}.pdf" if meta else None
            if not meta or not pdf.is_file():
                manquants.append(item["code"]); continue
            nomf = file_name(s, i, item, meta)
            (dest / dossier).mkdir(parents=True, exist_ok=True)
            cible = dest / dossier / f"{nomf}.pdf"
            if shutil.which("qpdf"):
                subprocess.run(["qpdf", "--recompress-flate", "--compression-level=9",
                                "--object-streams=generate", str(pdf), str(cible)], check=True)
            else:
                shutil.copy(pdf, cible)
            manifest.append({"semaine": s["n"], "dossier": dossier, "fichier": f"{nomf}.pdf",
                             "code": item["code"], "version": str(meta.get("version")),
                             "livrable": f"S{s['n']:02d}-{i}_Prenom"})
            print(f"drive : {dossier} / {nomf}.pdf")
    # Tout document au design Académie : PDF pour les apprenants, Word (.docx) en version modifiable
    from build_docx import build as build_docx
    word = dest / "_word"
    word.mkdir()
    prog = cal.get("programme", {})
    nom_prog = prog.get("nom_drive", "Programme et calendrier")
    (dest / "01 · Programme et calendrier").mkdir()
    src_prog = OUT / "pdf" / nom / f"OKOHO_PCP_{prog.get('code', 'A00-00')}_Guide_v{source_of(prog.get('code', 'A00-00'))[1][1]}.pdf"
    shutil.copy(src_prog, dest / "01 · Programme et calendrier" / f"{clean(nom_prog)}.pdf")
    build_docx(ROOT / "accueil" / prog.get("code", "A00-00") / "document.md", cal, word / f"{clean(nom_prog)}.docx")
    build_docx(ROOT / "accueil" / "A00-02" / "document.md", cal, word / "S00-2 · Diagnostic d'entrée · Prénom Nom.docx")
    ci = build_docx(ROOT / "parcours" / "drive" / "commencez-ici.md", cal, word / "00 · COMMENCEZ ICI.docx", label="BIENVENUE")
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(dest), str(ci)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    (dest / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"build_drive : {len(manifest)} fichier(s) prêts dans out/drive/{nom}, {len(manquants)} séance(s) pas encore validée(s)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
