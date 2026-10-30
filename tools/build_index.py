#!/usr/bin/env python3
"""Génère out/table-des-matieres.md, out/glossaire.md et out/index.md.
Sources : manuel/structure.yaml, seances/*/seance.md (métadonnées), glossaire/glossaire.yaml.
Index : un terme de l'en-tête d'une séance = occurrence principale (en gras) ;
les références du glossaire = occurrences secondaires."""
import sys
from collections import defaultdict
from datetime import date
from common import ROOT, OUT, load_yaml, read_seance, seance_files, structure, sort_key, initial, code_key

STATUT = {"valide": "validée", "relecture": "en relecture", "brouillon": "brouillon"}
PIED = "\n---\n\nUne formation OKOHO Consulting GmbH · Formateur : Dr. Bertrand Toumi · généré le {d} · © 2026 OKOHO Consulting GmbH\n"

def metas():
    out = {}
    for f in seance_files():
        try:
            m, _ = read_seance(f)
            out[m["code"]] = m
        except Exception:
            pass
    return out

def toc(s, ms):
    L = ["# Table des matières · Parcours Claude Pro", "", "OKOHO Académie · Manuel", ""]
    n_tot = n_pres = 0
    for p in s["parties"]:
        L += [f"## Partie {p['code']} · {p['titre']}", "", f"*{p['pole']}* · échafaudage {p['echafaudage']}", ""]
        for m in p["modules"]:
            L += [f"### {m['code']} · {m['titre']}", "", "| Code | Séance | Livrable | Outil | Statut |", "|---|---|---|---|---|"]
            for se in m["seances"]:
                n_tot += 1
                st = ms.get(se["code"], {}).get("status")
                if st: n_pres += 1
                L.append(f"| {se['code']} | {se['titre']} | {se['livrable']} | {se['outil']} | {STATUT.get(st, 'à produire')} |")
            L.append("")
    L.insert(4, f"{n_pres} séance(s) sur {n_tot} en cours ou produites.\n")
    return "\n".join(L)

def glossaire(gl, ms):
    known = {t["terme"] for t in gl}
    L = ["# Glossaire · Parcours Claude Pro", ""]
    cur = None
    for t in sorted(gl, key=lambda x: sort_key(x["terme"])):
        i = initial(t["terme"])
        if i != cur:
            L += ["", f"## {i}", ""]; cur = i
        refs = ", ".join(sorted(t["seances"], key=code_key))
        L.append(f"**{t['terme']}** · {t['definition']} *({refs})*  ")
    missing = sorted({g for m in ms.values() for g in (m.get("glossaire") or []) if g not in known}, key=sort_key)
    if missing:
        L += ["", "## À définir", "", *[f"- {g}" for g in missing]]
    return "\n".join(L)

def index(gl, ms, struct):
    occ = defaultdict(dict)  # terme -> code -> principal(bool)
    for code, m in ms.items():
        for t in (m.get("index") or []):
            occ[t][code] = True
        for t in (m.get("glossaire") or []):
            occ[t].setdefault(code, False)
    for t in gl:
        for c in t["seances"]:
            if c in struct: occ[t["terme"]].setdefault(c, False)
    L = ["# Index · Parcours Claude Pro", "", "Code en **gras** : occurrence principale.", ""]
    cur = None
    for term in sorted(occ, key=sort_key):
        i = initial(term)
        if i != cur:
            L += ["", f"## {i}", ""]; cur = i
        refs = ", ".join((f"**{c}**" if main else c) for c, main in sorted(occ[term].items(), key=lambda x: code_key(x[0])))
        L.append(f"- {term} → {refs}")
    return "\n".join(L)

def main():
    s, struct = structure()
    gl = load_yaml(ROOT / "glossaire" / "glossaire.yaml")["termes"]
    ms = metas()
    OUT.mkdir(exist_ok=True)
    pied = PIED.format(d=date.today().isoformat())
    for name, content in (("table-des-matieres.md", toc(s, ms)), ("glossaire.md", glossaire(gl, ms)), ("index.md", index(gl, ms, struct))):
        (OUT / name).write_text(content + pied, encoding="utf-8")
        print(f"build_index : out/{name}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
