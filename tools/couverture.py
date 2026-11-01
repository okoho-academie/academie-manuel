#!/usr/bin/env python3
"""Couverture des compétences de jalon par les séances · OKOHO Académie.

Lit manuel/jalons.yaml et les métadonnées « competences » des séances.
Affiche, pour chaque compétence de jalon, les séances qui la construisent et l'état de ces séances.
Écrit out/couverture.md (lu par le formateur et par Claude pour planifier).
Usage : python3 tools/couverture.py [J1]
"""
import sys
from common import ROOT, OUT, load_yaml, read_seance, seance_files

def main():
    cible = sys.argv[1] if len(sys.argv) > 1 else None
    jalons = load_yaml(ROOT / "manuel" / "jalons.yaml")["jalons"]
    seances = {}
    for f in seance_files():
        meta, _ = read_seance(f)
        seances[meta["code"]] = meta
    lignes = ["# Couverture des compétences de jalon", "",
              "Généré par tools/couverture.py. Ne pas modifier à la main.", ""]
    manque = 0
    for j in jalons:
        if cible and j["code"] != cible:
            continue
        lignes += [f"## {j['code']} · {j['titre']}", "",
                   "| Compétence de jalon | Séances qui la construisent | Séances prévues, pas encore écrites |", "|---|---|---|"]
        for c in j["competences"]:
            faites = [f"{s} ({m.get('status', '?')})" for s, m in seances.items()
                      for x in m.get("competences") or [] if x.get("jalon") == c["code"]]
            prevues = [s for s in j["seances"] if s not in seances]
            if not faites:
                manque += 1
            lignes.append(f"| {c['code']} · {c['intitule']} | {', '.join(sorted(set(faites))) or '**aucune**'} | {', '.join(prevues) or '—'} |")
        lignes.append("")
    OUT.mkdir(exist_ok=True)
    (OUT / "couverture.md").write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print("\n".join(lignes))
    print(f"couverture : {manque} compétence(s) de jalon sans séance écrite")
    return 0

if __name__ == "__main__":
    sys.exit(main())
