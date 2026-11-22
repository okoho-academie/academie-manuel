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
import json, re, shutil, subprocess, sys
from pathlib import Path
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
           "fil-rouge": "Cas fil rouge", "erreurs": "Erreurs fréquentes", "coup-de-pouce": "Coup de pouce", "defi": "Piste Défi", "acquis": "Vérifiez vos acquis", "structure": "Si votre client pilote est votre propre structure"}
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

def sha(p):
    """Empreinte du contenu. Les dates et identifiants que Chromium et LibreOffice écrivent à chaque build sont retirés :
    un fichier inchangé garde la même empreinte, « synchroniser » ne le remplace pas et son lien Drive reste valable."""
    import hashlib
    b = Path(p).read_bytes()
    if str(p).endswith(".pdf") and shutil.which("qpdf"):
        # Flux décompressés : les dates cachées dans les flux d'objets deviennent visibles et sont retirées ci-dessous.
        r = subprocess.run(["qpdf", "--qdf", "--object-streams=disable", "--deterministic-id", str(p), "-"], capture_output=True)
        if r.returncode in (0, 3) and r.stdout:
            b = r.stdout
    if str(p).endswith(".pdf"):
        for motif in (rb"/(?:CreationDate|ModDate)\s*\([^)]*\)", rb"/ID\s*\[\s*<[0-9A-Fa-f]*>\s*<[0-9A-Fa-f]*>\s*\]",
                      rb"/DocChecksum\s*/[0-9A-Fa-f]+", rb"<xmp:\w*Date>[^<]*</xmp:\w*Date>",
                      rb"<xmpMM:(?:DocumentID|InstanceID)>[^<]*</xmpMM:(?:DocumentID|InstanceID)>"):
            b = re.sub(motif, b"", b)
    elif str(p).endswith(".docx"):
        import zipfile, io
        z = zipfile.ZipFile(io.BytesIO(b))
        b = b"".join(n.encode() + (re.sub(rb"<dcterms:(?:created|modified)[^>]*>[^<]*</dcterms:(?:created|modified)>", b"", z.read(n)))
                     for n in sorted(z.namelist()))
    return hashlib.sha256(b).hexdigest()[:16]

def main():
    nom = sys.argv[1] if len(sys.argv) > 1 else "cohorte-1"
    cal = load_yaml(ROOT / "parcours" / f"{nom}.yaml")
    codes = [it["code"] for s in cal["semaines"] for it in s.get("items", [])] + [cal.get("programme", {}).get("code", "A00-00")]
    ressources = [c for c in cal.get("ressources", []) if source_of(c)[0]]
    existants = [c for c in codes + ressources if source_of(c)[0]]
    subprocess.run([sys.executable, str(ROOT / "tools" / "build_pdf.py"), *existants, f"--cohorte={nom}"], check=True)
    dest = OUT / "drive" / nom
    if dest.exists():
        shutil.rmtree(dest)
    espace = f"{cal['nom']} · Espace participants"
    formateur = "Formateur (privé)"
    (dest / espace).mkdir(parents=True)
    manquants = []
    for s in cal["semaines"]:
        dossier = f"{espace}/02 · Séances semaine par semaine/" + folder_name(s)
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
            print(f"drive : {dossier} / {nomf}.pdf")
    from build_docx import build as build_docx
    tmp = OUT / "docx" / nom
    tmp.mkdir(parents=True, exist_ok=True)
    def docx_pdf(src, cible, label=None, lang="fr"):
        d = build_docx(src, cal, tmp / (Path(cible).stem + ".docx"), label=label, lang=lang)
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(tmp), str(d)],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        Path(cible).parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(tmp / (Path(cible).stem + ".pdf")), cible)
    prog = cal.get("programme", {})
    nom_prog = clean(prog.get("nom_drive", "Programme et calendrier"))
    (dest / espace / "01 · Programme et calendrier").mkdir(parents=True)
    src_prog = OUT / "pdf" / nom / f"OKOHO_PCP_{prog.get('code', 'A00-00')}_Guide_v{source_of(prog.get('code', 'A00-00'))[1][1]}.pdf"
    shutil.copy(src_prog, dest / espace / "01 · Programme et calendrier" / f"{nom_prog}.pdf")
    docx_pdf(ROOT / "parcours" / "drive" / "commencez-ici.md", dest / espace / "00 · COMMENCEZ ICI.pdf", label="BIENVENUE")
    # Kit du prestataire (PDF) et Dossier client pilote (Word à remplir) : 05 · Ressources et liens utiles
    subprocess.run([sys.executable, str(ROOT / "tools" / "build_kit.py")], check=True, stdout=subprocess.DEVNULL)
    res = dest / espace / "05 · Ressources et liens utiles"
    docx_pdf(OUT / "kit" / "kit-du-prestataire.md", res / "Kit du prestataire · fiches-outils.pdf", label="KIT")
    res.mkdir(parents=True, exist_ok=True)
    build_docx(OUT / "kit" / "dossier-client-pilote.md", cal, res / "Dossier client pilote · à copier dans votre portfolio.docx", label="À REMPLIR")
    print("drive : 05 · Ressources et liens utiles / Kit du prestataire, Dossier client pilote")
    # Guides d'accueil complémentaires (portfolio, passerelle) : 05 · Ressources et liens utiles
    for c in ressources:
        meta, info = source_of(c)
        pdf = OUT / "pdf" / nom / f"OKOHO_PCP_{c}_{info[0]}_v{info[1]}.pdf"
        if pdf.is_file():
            shutil.copy(pdf, res / f"{c} · Guide · {clean(meta['titre'])}.pdf")
            print(f"drive : 05 · Ressources et liens utiles / {c} {meta['titre']}")
    # Quiz et questionnaires de la semaine : une fiche avec les liens à remplir (/viewform),
    # jamais le fichier du formulaire (il ouvrirait l'éditeur et montrerait les réponses).
    liens = cal.get("formulaires", {}) or {}
    for s in cal["semaines"]:
        fl = liens.get(s["n"]) or []
        if not fl:
            continue
        for f in fl:
            if "/viewform" not in f["url"] or "/edit" in f["url"]:
                sys.exit(f"build_drive : lien non publié pour {f['code']} : {f['url']}")
        md = tmp / f"liens-s{s['n']:02d}.md"
        lignes = ["---", f"titre: \"Quiz de la semaine {s['n']:02d}\"", "---", "",
                  "::: objectifs",
                  "- Touchez le titre en gras ou l'adresse d'un quiz : il s'ouvre, prêt à remplir.",
                  "- Votre score s'affiche à la fin, avec l'explication de chaque réponse.",
                  "- Vous pouvez refaire chaque quiz autant de fois que vous voulez.",
                  ":::", "", "## Les liens à remplir", ""]
        for f in fl:
            lignes += [f"**[{f['code']} · {f['titre']}]({f['url']})**", "", f"<{f['url']}>", ""]
        lignes += ["## Comment faire", "",
                   "1. Touchez le lien. Le formulaire s'ouvre dans votre navigateur.",
                   "2. Écrivez votre prénom, puis répondez.",
                   "3. Touchez **Envoyer**, puis **Afficher le score**.",
                   "4. Pour recommencer, touchez à nouveau le lien.", "",
                   "Le lien ne s'ouvre pas ? Copiez l'adresse sous le titre dans votre navigateur, ou demandez le lien dans le groupe WhatsApp."]
        md.write_text("\n".join(lignes) + "\n", encoding="utf-8")
        nomq = clean(f"S{s['n']:02d}-0 · À remplir · Quiz de la semaine, liens à ouvrir")
        cible_q = dest / espace / "02 · Séances semaine par semaine" / folder_name(s) / f"{nomq}.pdf"
        docx_pdf(md, cible_q, label="À REMPLIR")
        print(f"drive : {folder_name(s)} / {nomq}.pdf")
    # Dramaturgies du formateur (formateur/*.md) : privé
    for f in sorted((ROOT / "formateur").glob("*.md")):
        meta, _ = read_seance(f)
        docx_pdf(f, dest / formateur / "Dramaturgies" / f"{clean(meta['titre'])}.pdf", label="FORMATEUR")
        print(f"drive : {formateur} / Dramaturgies / {meta['titre']}")
    # NotebookLM : consigne et sources de chaque semaine (parcours/drive/notebooklm-sNN.md)
    nb = ROOT / "parcours" / "drive" / "notebooklm-s00.md"
    nb_pdf = {}
    for s in cal["semaines"]:
        src = ROOT / "parcours" / "drive" / f"notebooklm-s{s['n']:02d}.md"
        if not src.is_file():
            continue
        nom_nb = "S00 · Votre premier notebook NotebookLM" if s["n"] == 0 else clean(f"S{s['n']:02d} · Réviser avec NotebookLM · {s['titre']}")
        nb_pdf[s["n"]] = dest / espace / "03 · Réviser avec NotebookLM" / f"{nom_nb}.pdf"
        docx_pdf(src, nb_pdf[s["n"]], label="NOTEBOOKLM")
        print(f"drive : 03 · Réviser avec NotebookLM / {nom_nb}.pdf")
    # Formateur (privé) : tout le matériel d'une semaine au même endroit
    # (présentation, présentation avec notes, dramaturgie, documents des participants)
    for s in cal["semaines"]:
        codes_s = [it["code"] for it in s.get("items", [])]
        pres = [d for d in sorted((ROOT / "formateur" / "presentations").glob("*"))
                if d.is_dir() and (d.name in codes_s or (d.name.startswith("A00-") and s["n"] == 0))]
        # Correspondance exacte : un deck « M02-S1 » ne va qu'à la semaine de M02-S1 (avant : préfixe « M02 », decks copiés dans d'autres semaines)
        espace_s = dest / espace / "02 · Séances semaine par semaine" / folder_name(s)
        if not pres and not espace_s.exists():
            continue
        cible = dest / formateur / f"Semaine {s['n']:02d} · {s['titre']}"
        cible.mkdir(parents=True, exist_ok=True)
        for d in pres:
            nom_p = f"Présentation · {s['titre']}"
            subprocess.run([sys.executable, str(ROOT / "tools" / "build_slides_pdf.py"), str(d), str(cible / f"{nom_p}.pdf")], check=True)
            subprocess.run([sys.executable, str(ROOT / "tools" / "build_slides_pdf.py"), str(d), str(cible / f"{nom_p} · avec notes.pdf"), "--notes"], check=True)
        if espace_s.exists():
            for f in sorted(espace_s.glob("*.pdf")):
                shutil.copy(f, cible / f.name)
        for f in (dest / formateur / "Dramaturgies").glob("*.pdf"):
            if s["titre"] in f.name:
                shutil.copy(f, cible / f.name)
        if s["n"] in nb_pdf:
            shutil.copy(nb_pdf[s["n"]], cible)
        quiz = [c for c in codes_s if (ROOT / "quiz" / f"{c}.yaml").is_file() and not c.startswith("A00")]
        if quiz:
            # Les formulaires sont créés dans le dossier privé du formateur ; les participants ne reçoivent que les liens /viewform.
            subprocess.run([sys.executable, str(ROOT / "tools" / "build_forms.py"), f"chemin:OKOHO Académie · Parcours Claude Pro/{formateur}/Semaine {s['n']:02d} · {s['titre']}",
                            f"S{s['n']:02d}", *quiz], check=True, stdout=subprocess.DEVNULL)
        gs = OUT / "forms" / f"creer_formulaires_S{s['n']:02d}.gs"
        if gs.is_file():
            shutil.copy(gs, cible / f"S{s['n']:02d} · Script des formulaires (Apps Script).txt")
        print(f"drive : {formateur} / {cible.name}")
    fichiers = sorted(p for p in dest.rglob("*") if p.is_file())
    manifest = {"cohorte": nom, "racine": "OKOHO Académie · Parcours Claude Pro",
                "fichiers": [{"chemin": str(p.relative_to(dest)), "sha": sha(p)} for p in fichiers]}
    (dest / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"build_drive : {len(fichiers)} fichier(s) dans out/drive/{nom}, {len(manquants)} séance(s) pas encore validée(s)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
