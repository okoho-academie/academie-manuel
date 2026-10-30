#!/usr/bin/env python3
"""Valide toutes les séances contre schema/seance.schema.json et manuel/structure.yaml.
Sortie : 0 si aucune erreur (les avertissements n'arrêtent pas le build)."""
import json, re, sys
from common import ROOT, read_seance, seance_files, structure, load_yaml, resolve

SCHEMA = json.loads((ROOT / "schema" / "seance.schema.json").read_text(encoding="utf-8"))
SCHEMA_DOC = json.loads((ROOT / "schema" / "document.schema.json").read_text(encoding="utf-8"))
TYPES = {"string": str, "integer": int, "boolean": bool, "array": list, "object": dict, "null": type(None)}

def check(value, sch, path, errs):
    """Sous-ensemble de JSON Schema utilisé par seance.schema.json."""
    t = sch.get("type")
    if t:
        ts = t if isinstance(t, list) else [t]
        ok = any(isinstance(value, TYPES[x]) and not (x == "integer" and isinstance(value, bool)) for x in ts)
        if not ok:
            errs.append(f"{path} : type attendu {t}, reçu {type(value).__name__}"); return
    if value is None:
        return
    if "enum" in sch and value not in sch["enum"]:
        errs.append(f"{path} : « {value} » hors liste {sch['enum']}")
    if isinstance(value, str):
        if "pattern" in sch and not re.search(sch["pattern"], value):
            errs.append(f"{path} : « {value} » ne respecte pas {sch['pattern']}")
        if len(value) < sch.get("minLength", 0):
            errs.append(f"{path} : trop court")
    if isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in sch and value < sch["minimum"]: errs.append(f"{path} : < {sch['minimum']}")
        if "maximum" in sch and value > sch["maximum"]: errs.append(f"{path} : > {sch['maximum']}")
    if isinstance(value, list) and "items" in sch:
        for i, v in enumerate(value):
            check(v, sch["items"], f"{path}[{i}]", errs)
    if isinstance(value, dict):
        props = sch.get("properties", {})
        for r in sch.get("required", []):
            if r not in value: errs.append(f"{path}.{r} : obligatoire")
        for k, v in value.items():
            if k in props: check(v, props[k], f"{path}.{k}", errs)
            elif sch.get("additionalProperties") is False: errs.append(f"{path}.{k} : champ inconnu")

# Règle de réutilisation : aucune date ni nom de cohorte dans les sources (voir parcours/*.yaml et {{variables}}).
DATE_RE = re.compile(r"\b\d{1,2}\.\d{1,2}\.(\d{2,4})?(?!\d)|\b(19|20)\d{2}\b|\b\d{1,2}(er)? (janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\b|\bcohorte \d", re.I)

def dates_interdites(body):
    """Signale les dates et noms de cohorte écrits en dur (hors commentaires et mentions finales)."""
    b = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    parts = re.split(r"\n-{3,}\s*\n", b)
    if len(parts) > 1 and "Une formation OKOHO Consulting GmbH" in parts[-1]:
        b = "\n".join(parts[:-1])
    errs = []
    try:
        resolve(b, None)
    except Exception as e:
        errs.append(f"variable invalide : {e}")
    return errs + [f"date ou cohorte en dur « {m.group(0)} » : utiliser une variable {{{{date:SNN}}}}, {{{{cohorte}}}}…"
            for m in DATE_RE.finditer(b)]

def main():
    _, struct = structure()
    gloss = {t["terme"] for t in load_yaml(ROOT / "glossaire" / "glossaire.yaml")["termes"]}
    files = seance_files()
    n_err = n_warn = 0
    for f in files:
        rel = f.relative_to(ROOT)
        errs, warns = [], []
        try:
            meta, body = read_seance(f)
        except Exception as e:
            print(f"ERREUR {rel} : {e}"); n_err += 1; continue
        check(meta, SCHEMA, "meta", errs)
        code = meta.get("code")
        if code and f.parent.name != code:
            errs.append(f"dossier « {f.parent.name} » différent du code « {code} »")
        ref = struct.get(code)
        if code and not ref:
            errs.append(f"code « {code} » absent de manuel/structure.yaml")
        if ref:
            for k in ("titre", "partie", "module"):
                if meta.get(k) != ref[k]: errs.append(f"{k} « {meta.get(k)} » ≠ structure « {ref[k]} »")
            for k in ("livrable", "outil", "appareil", "echafaudage"):
                if meta.get(k) != ref[k]: warns.append(f"{k} « {meta.get(k)} » ≠ structure « {ref[k]} »")
        for p in meta.get("prerequis") or []:
            if p not in struct: errs.append(f"prérequis inconnu « {p} »")
        for g in meta.get("glossaire") or []:
            if g not in gloss: warns.append(f"terme « {g} » absent de glossaire/glossaire.yaml")
        errs += dates_interdites(body)
        for h in ("Ce que vous saurez faire", "Votre livrable"):
            if f"## {h}" not in body: errs.append(f"section obligatoire « {h} » absente")
        if "Une formation OKOHO Consulting GmbH · Formateur : Dr. Bertrand Toumi" not in body:
            errs.append("mention obligatoire OKOHO absente")
        for e in errs: print(f"ERREUR  {rel} : {e}")
        for w in warns: print(f"AVERT.  {rel} : {w}")
        n_err += len(errs); n_warn += len(warns)
    docs = sorted((ROOT / "accueil").glob("*/document.md"))
    for f in docs:
        rel = f.relative_to(ROOT)
        errs = []
        try:
            meta, body = read_seance(f)
        except Exception as e:
            print(f"ERREUR {rel} : {e}"); n_err += 1; continue
        check(meta, SCHEMA_DOC, "meta", errs)
        errs += dates_interdites(body)
        if meta.get("code") and f.parent.name != meta["code"]:
            errs.append(f"dossier « {f.parent.name} » différent du code « {meta['code']} »")
        for e in errs: print(f"ERREUR  {rel} : {e}")
        n_err += len(errs)
    for f in sorted((ROOT / "parcours" / "drive").glob("*.md")) + sorted((ROOT / "formateur").glob("*.md")):
        for e in dates_interdites(f.read_text(encoding="utf-8")):
            print(f"ERREUR  {f.relative_to(ROOT)} : {e}"); n_err += 1
    print(f"validate : {len(files)} séance(s), {len(docs)} document(s) d'accueil, {n_err} erreur(s), {n_warn} avertissement(s)")
    return 1 if n_err else 0

if __name__ == "__main__":
    sys.exit(main())
