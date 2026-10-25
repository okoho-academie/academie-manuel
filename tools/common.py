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
