#!/usr/bin/env python3
"""Sortie Google Drive d'une cohorte · OKOHO Académie.

Copie les PDF de out/pdf/ vers out/drive/<cohorte>/ avec des noms lisibles par les apprenants
et écrit out/drive/<cohorte>/manifest.json (dossier, nom, source) pour le chargement dans Drive.

Règle de nommage (source : parcours/cohorte-N.yaml) :
  Dossier : "Semaine NN · JJ.MM.AAAA · <titre>"
  Fichier : "SNN-<ordre> · <Type> · <Code séance> <Titre>.pdf"
  Pas de « : » dans les noms (interdit sous Windows) : remplacé par « , ».
Usage : python3 tools/build_drive.py [cohorte-1]
"""
import json, shutil, subprocess, sys
from datetime import date
from common import ROOT, OUT, load_yaml, read_seance

def clean(s):
    return s.replace(" : ", ", ").replace(":", ",").replace("/", "-").strip()

def source_of(code):
    p = ROOT / ("accueil" if code.startswith("A00") else "seances") / code
    f = p / ("document.md" if code.startswith("A00") else "seance.md")
    if not f.is_file():
        return None, None
    meta, _ = read_seance(f)
    typ = "Guide" if code.startswith("A00") else "Fiche"
    pdf = OUT / "pdf" / f"OKOHO_PCP_{code}_{typ}_v{meta.get('version', '0.1')}.pdf"
    return meta, pdf

def folder_name(s):
    d = date.fromisoformat(s["date"]).strftime("%d.%m.%Y")
    return f"Semaine {s['n']:02d} · {d} · {s['titre']}"

def file_name(s, i, item, meta):
    code = item["code"]
    titre = meta["titre"]
    label = titre if code.startswith("A00") else f"{code} {titre}"
    return clean(f"S{s['n']:02d}-{i} · {item['type']} · {label}")

def main():
    nom = sys.argv[1] if len(sys.argv) > 1 else "cohorte-1"
    cal = load_yaml(ROOT / "parcours" / f"{nom}.yaml")
    dest = OUT / "drive" / nom
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    manifest, manquants = [], []
    for s in cal["semaines"]:
        dossier = folder_name(s)
        for i, item in enumerate(s.get("items", []), 1):
            meta, pdf = source_of(item["code"])
            if meta and meta.get("status") == "brouillon":
                manquants.append(item["code"]); continue
            if not meta or not pdf.is_file():
                manquants.append(item["code"]); continue
            nomf = file_name(s, i, item, meta)
            (dest / dossier).mkdir(exist_ok=True)
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
    (dest / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"build_drive : {len(manifest)} fichier(s) prêts dans out/drive/{nom}, {len(manquants)} séance(s) pas encore validée(s)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
