"""Fonctions communes · OKOHO Académie."""
import json, re, sys, unicodedata
from pathlib import Path
try:
    import yaml
except ImportError:
    sys.exit("PyYAML manquant : pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out"

def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

def read_seance(path):
    """Retourne (métadonnées, corps) d'un fichier seance.md."""
    text = Path(path).read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        raise ValueError("en-tête YAML absent (--- … ---)")
    return yaml.safe_load(m.group(1)) or {}, m.group(2)

def seance_files():
    return sorted((ROOT / "seances").glob("*/seance.md"))

def structure():
    """Dictionnaire code -> infos de séance, avec partie, module et échafaudage attendus."""
    s = load_yaml(ROOT / "manuel" / "structure.yaml")
    out = {}
    for p in s["parties"]:
        for m in p["modules"]:
            for se in m["seances"]:
                out[se["code"]] = dict(se, partie=p["code"], partie_titre=p["titre"], module=m["code"],
                                       module_titre=m["titre"], echafaudage=m.get("echafaudage", p["echafaudage"]))
    return s, out

def sort_key(term):
    """Tri alphabétique français : accents ignorés au premier niveau."""
    base = unicodedata.normalize("NFD", term)
    base = "".join(c for c in base if unicodedata.category(c) != "Mn").casefold()
    base = re.sub(r"^[«“\"'(]+", "", base)
    return (base, term.casefold(), term)

def initial(term):
    return sort_key(term)[0][:1].upper() or "#"

def code_key(code):
    m = re.match(r"^M(\d+)-S(\d+)$", code)
    return (0, int(m.group(1)), int(m.group(2))) if m else (1, 0, 0) if code == "Parcours" else (2, 0, 0)


# ---------------------------------------------------------------------------
# Variables de cohorte · les sources restent sans date, la sortie est datée.
# ---------------------------------------------------------------------------
from datetime import date as _date

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre"]
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
VAR = re.compile(r"\{\{\s*([a-z_]+)(?::([A-Za-z0-9-]+))?\s*\}\}")

def load_cohorte(nom):
    """Charge parcours/<nom>.yaml (ex. cohorte-1). None si nom vide."""
    if not nom:
        return None
    return load_yaml(ROOT / "parcours" / f"{nom}.yaml")

def date_longue(iso):
    d = _date.fromisoformat(iso)
    return f"{JOURS[d.weekday()]} {d.day} {MOIS[d.month - 1]} {d.year}"

def date_courte(iso):
    return _date.fromisoformat(iso).strftime("%d.%m.%Y")

def _semaine(cal, ref):
    n = int(ref.lstrip("Ss"))
    for s in cal["semaines"]:
        if s["n"] == n:
            return s
    raise KeyError(f"semaine {ref} absente du calendrier")

def _titre_item(code, struct):
    if code.startswith("A00"):
        f = ROOT / "accueil" / code / "document.md"
        return read_seance(f)[0]["titre"] if f.is_file() else code
    return f"{code} {struct.get(code, {}).get('titre', '')}".strip()

def calendrier_md(cal):
    """Tableau du calendrier. Avec cohorte : dates et pauses. Sans cohorte : semaines seules."""
    s_all, struct = structure()
    lignes = []
    if cal:
        lignes += ["| Semaine | Date | Thème | Documents |", "|---|---|---|---|"]
    else:
        lignes += ["| Semaine | Thème | Documents |", "|---|---|---|"]
    base = cal or load_yaml(ROOT / "parcours" / "modele.yaml")
    cycles = base.get("cycles", {})
    semaines = base["semaines"]
    pauses = {p["apres"]: p for p in (cal or {}).get("pauses", [])}
    cycle_vu = None
    for s in semaines:
        c = s.get("cycle")
        if c and c != cycle_vu and c in cycles:
            lignes.append(f"| **Cycle {c}** | {'| ' if cal else ''}**{cycles[c]}** | |")
            cycle_vu = c
        docs = [f"S{s['n']:02d}-{i} {_titre_item(it['code'], struct)}" for i, it in enumerate(s.get("items", []), 1)]
        if s.get("note"):
            docs.append(s["note"])
        cell = " · ".join(docs) or "–"
        if cal:
            lignes.append(f"| {s['n']} | {date_courte(s['date'])} | {s['titre']} | {cell} |")
        else:
            lignes.append(f"| {s['n']} | {s['titre']} | {cell} |")
        if s["n"] in pauses:
            p = pauses[s["n"]]
            lignes.append(f"| Pause | {', '.join(date_courte(d) for d in p['dates'])} | {p['note']} | |")
    return "\n".join(lignes)

def jalons_md(cal):
    s_all, _ = structure()
    jal = s_all.get("jalons", {})
    sem = {s.get("jalon"): s for s in (cal or load_yaml(ROOT / "parcours" / "modele.yaml"))["semaines"] if s.get("jalon")}
    if cal:
        out = ["| Jalon | Date | Ce que vous savez faire |", "|---|---|---|"]
        for k, v in jal.items():
            out.append(f"| {k} {v['nom']} | {date_courte(sem[k]['date']) if k in sem else '–'} | {v['competence']} |")
    else:
        out = ["| Jalon | Semaine | Ce que vous savez faire |", "|---|---|---|"]
        for k, v in jal.items():
            out.append(f"| {k} {v['nom']} | {sem[k]['n'] if k in sem else '–'} | {v['competence']} |")
    return "\n".join(out)

def resolve(text, cal):
    """Remplace les variables {{…}}. cal = calendrier de cohorte ou None (texte neutre)."""
    def rep(m):
        k, arg = m.group(1), m.group(2)
        if k == "cohorte":
            return cal["nom"] if cal else "votre groupe"
        if k == "groupe":
            return cal.get("groupe", cal["nom"]) if cal else "Entraide"
        if k == "jour":
            return cal.get("jour", "samedi") if cal else "jour de séance"
        if k == "nb_semaines":
            return str(max(s["n"] for s in (cal or load_yaml(ROOT / "parcours" / "modele.yaml"))["semaines"]))
        if k == "debut":
            return date_longue(cal["semaines"][0]["date"]) if cal else "séance de lancement"
        if k == "fin":
            return date_longue(cal["semaines"][-1]["date"]) if cal else "Démo Day final"
        if k == "date":
            return "le " + date_longue(_semaine(cal, arg)["date"]) if cal else f"la séance de la semaine {int(arg.lstrip('Ss'))}"
        if k == "calendrier":
            return calendrier_md(cal)
        if k == "jalons":
            return jalons_md(cal)
        raise KeyError(f"variable inconnue {{{{{k}}}}}")
    return VAR.sub(rep, text)
