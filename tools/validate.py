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
    if isinstance(value, list):
        if len(value) < sch.get("minItems", 0): errs.append(f"{path} : au moins {sch['minItems']} élément(s)")
        if "maxItems" in sch and len(value) > sch["maxItems"]: errs.append(f"{path} : au plus {sch['maxItems']} élément(s)")
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

def jalon_competences():
    """Codes des compétences de jalon (manuel/jalons.yaml)."""
    f = ROOT / "manuel" / "jalons.yaml"
    if not f.is_file():
        return {}
    return {c["code"]: j["code"] for j in load_yaml(f)["jalons"] for c in j["competences"]}

def trois_questions(meta, body):
    """Règle de planification : chaque séance montre ce que l'apprenant sait faire, comment il le prouve,
    à quoi on le reconnaît. Contrôle la présence visible de ces réponses dans la fiche."""
    errs = []
    comp = meta.get("competences") or []
    jc = jalon_competences()
    plat = re.sub(r"\s+", " ", body)
    for c in comp:
        if not isinstance(c, dict):
            continue
        if jc and c.get("jalon") not in jc:
            errs.append(f"compétence {c.get('code')} : jalon « {c.get('jalon')} » absent de manuel/jalons.yaml")
        elif jc and meta.get("jalon") and jc.get(c.get("jalon")) != meta["jalon"]:
            errs.append(f"compétence {c.get('code')} : {c.get('jalon')} n'appartient pas au jalon {meta['jalon']}")
        for champ in ("savoir_faire", "preuve", "reussi_si"):
            v = re.sub(r"\s+", " ", str(c.get(champ, ""))).strip()
            if v and v not in plat:
                errs.append(f"compétence {c.get('code')} : « {champ} » doit figurer mot pour mot dans la fiche (tableau « Ce que vous saurez faire »)")
    q = ROOT / "quiz" / f"{meta.get('code')}.yaml"
    if not q.is_file():
        errs.append(f"quiz/{meta.get('code')}.yaml absent : chaque séance a un quiz")
    else:
        d = load_yaml(q)
        tags = {x.get("competence") for x in d.get("questions", [])}
        for c in comp:
            if isinstance(c, dict) and c.get("code") not in tags:
                errs.append(f"compétence {c.get('code')} : aucune question du quiz ne la vérifie (champ « competence »)")
        if "reussite" not in d:
            errs.append(f"quiz/{meta.get('code')}.yaml : seuil « reussite » absent")
    if meta.get("type") == "direct":
        dram = [f for f in (ROOT / "formateur").glob("*.md")
                if f.name.startswith((str(meta.get("code")), str(meta.get("module")) + "-dramaturgie"))]
        if not dram:
            errs.append("séance en direct sans dramaturgie (formateur/<MODULE>-dramaturgie.md)")
        else:
            txt = dram[0].read_text(encoding="utf-8")
            for h in ("Grille d'observation", "Contrôle de sortie"):
                if h not in txt:
                    errs.append(f"{dram[0].name} : « {h} » absent")
    for h in ("Vérifiez vos acquis",):
        if f"## {h}" not in body:
            errs.append(f"section obligatoire « {h} » absente")
    return errs

def fil_client():
    """Étapes du fil du client pilote (manuel/fil-client-pilote.yaml), par code de séance."""
    f = ROOT / "manuel" / "fil-client-pilote.yaml"
    return {e["seance"]: e for e in load_yaml(f)["etapes"]} if f.is_file() else {}

SECTIONS_FIL = ("Un geste, trois contextes", "Pour votre client pilote", "Votre fiche-outil")

def regle_fil(meta, body, fil):
    """Règle du client pilote : chaque séance du fil produit une page du Dossier client pilote,
    applique le geste dans trois contextes et laisse une fiche-outil réutilisable."""
    e = fil.get(meta.get("code"))
    if not e:
        return []
    errs = []
    fc = meta.get("fil_client")
    if not fc:
        errs.append("métadonnée « fil_client » absente (séance du fil du client pilote)")
    elif fc.get("page_dossier") != e["page"]:
        errs.append(f"fil_client.page_dossier {fc.get('page_dossier')} ≠ {e['page']} (manuel/fil-client-pilote.yaml)")
    for h in SECTIONS_FIL:
        if f"## {h}" not in body:
            errs.append(f"section obligatoire « {h} » absente (fil du client pilote)")
    # Le parcours construit sur l'acquis : une séance avec prérequis dit quels gestes elle réutilise
    if meta.get("prerequis") and "## Ce que vous réutilisez" not in body:
        errs.append("section obligatoire « Ce que vous réutilisez » absente (séance avec prérequis)")
    if meta.get("prerequis") and not re.search(r"## Ce que vous réutilisez.*?(" + "|".join(map(re.escape, meta["prerequis"])) + ")", body, re.S):
        errs.append("« Ce que vous réutilisez » ne cite aucun prérequis")
    return errs

def main():
    _, struct = structure()
    gloss = {t["terme"] for t in load_yaml(ROOT / "glossaire" / "glossaire.yaml")["termes"]}
    files = seance_files()
    fil = fil_client()
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
        errs += trois_questions(meta, body)
        errs += regle_fil(meta, body, fil)
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
