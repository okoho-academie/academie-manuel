#!/usr/bin/env python3
"""Word (.docx) au design OKOHO Académie · source unique : design/tokens.json.

Usage :
  python3 tools/build_docx.py <fichier.md> [--cohorte=cohorte-1] [--out=chemin.docx] [--label=ACCUEIL] [--lang=fr|de]
Accepte un document du Manuel (en-tête YAML code/titre) ou tout Markdown (titre = premier « # »).
Le .docx sert aussi de base aux Google Docs : chargé dans Drive, il est converti en conservant
styles, en-tête (logo, titre) et pied de page (contact, numéro de page).
"""
import json, re, subprocess, sys, tempfile
from datetime import date
from pathlib import Path
from common import ROOT, OUT, read_seance, resolve, load_cohorte

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

DESIGN = ROOT / "design"
TOK = {t["name"]: t["value"] for t in json.loads((DESIGN / "tokens.json").read_text(encoding="utf-8"))["color"]["tokens"]}
LOGO = DESIGN / "logos" / "academie-logo-A-docx.png"
HEAD, BODY = "Montserrat", "Open Sans"

# Encadrés : style Word, libellé, fond, bordure gauche
BOXES = {
    "objectifs": ("Encadre Objectifs", "CE QUE VOUS SAUREZ FAIRE", "academie-tint", "orange-accent"),
    "livrable": ("Encadre Livrable", "VOTRE LIVRABLE", "academie-tint", "orange-accent"),
    "fil-rouge": ("Encadre Fil rouge", "CAS FIL ROUGE", "academie-tint", "blue-light"),
    "erreurs": ("Encadre Erreurs", "ERREURS FRÉQUENTES", "surface", "orange-text"),
    "coup-de-pouce": ("Encadre Coup de pouce", "COUPS DE POUCE", "surface-muted", "blue-light"),
    "prompt": ("Encadre Consigne", "CONSIGNE À COPIER", "surface", "blue-primary"),
}

def rgb(name):
    return RGBColor.from_string(TOK[name].lstrip("#"))

def hexv(name):
    return TOK[name].lstrip("#").upper()

def logo_png():
    """Logo réduit pour l'en-tête (léger, pour Drive et WhatsApp)."""
    if not LOGO.is_file():
        from PIL import Image
        im = Image.open(DESIGN / "logos" / "academie-logo-A.png").convert("RGBA")
        im.thumbnail((330, 134))
        bg = Image.new("RGBA", im.size, (255, 255, 255, 0))
        bg.alpha_composite(im)
        bg.convert("P", palette=Image.ADAPTIVE, colors=24).save(LOGO, optimize=True)
    return LOGO

def shade(par_pr, fill):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), fill)
    par_pr.append(shd)

def border(par_pr, side, color, size=18, space=8):
    pbdr = par_pr.find(qn("w:pBdr"))
    if pbdr is None:
        pbdr = OxmlElement("w:pBdr"); par_pr.append(pbdr)
    b = OxmlElement(f"w:{side}")
    b.set(qn("w:val"), "single"); b.set(qn("w:sz"), str(size)); b.set(qn("w:space"), str(space)); b.set(qn("w:color"), color)
    pbdr.append(b)

def font(style, name, size, color, bold=False, caps=False):
    f = style.font
    f.name, f.size, f.color.rgb, f.bold, f.all_caps = name, Pt(size), color, bold, caps
    rpr = style.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts"); rpr.append(rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), name)

def reference_docx(path):
    d = Document()
    sec = d.sections[0]
    sec.page_height, sec.page_width = Mm(297), Mm(210)
    sec.top_margin, sec.bottom_margin, sec.left_margin, sec.right_margin = Mm(30), Mm(20), Mm(25), Mm(20)
    sec.header_distance, sec.footer_distance = Mm(10), Mm(10)
    st = d.styles
    font(st["Normal"], BODY, 10.5, rgb("ink"))
    st["Normal"].paragraph_format.space_after = Pt(6)
    st["Normal"].paragraph_format.line_spacing = 1.25
    font(st["Title"], HEAD, 24, rgb("blue-primary"), bold=True)
    st["Title"].paragraph_format.space_after = Pt(6)
    # Le style Title de python-docx porte une bordure basse : retirée
    ppr = st["Title"].element.get_or_add_pPr()
    for b in ppr.findall(qn("w:pBdr")):
        ppr.remove(b)
    font(st["Subtitle"], HEAD, 9, rgb("orange-text"), bold=True, caps=True)
    for lvl, size in ((1, 15), (2, 12.5), (3, 10.5)):
        s = st[f"Heading {lvl}"]
        font(s, HEAD, size, rgb("blue-primary") if lvl < 3 else rgb("orange-text"), bold=True, caps=(lvl == 3))
        s.paragraph_format.space_before, s.paragraph_format.space_after = Pt(16 if lvl == 1 else 10), Pt(6)
        s.paragraph_format.keep_with_next = True
    for name in ("Body Text", "First Paragraph", "Compact"):
        s = st[name] if name in [x.name for x in st] else st.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        s.base_style = st["Normal"]
    for key, (sname, _, fill, line) in BOXES.items():
        s = st.add_style(sname, WD_STYLE_TYPE.PARAGRAPH)
        s.base_style = st["Normal"]
        s.paragraph_format.left_indent = Mm(4)
        s.paragraph_format.space_after = Pt(3)
        p = s.element.get_or_add_pPr()
        shade(p, hexv(fill))
        border(p, "left", hexv(line), 24, 10)
        if fill == "surface":
            for side in ("top", "bottom", "right"):
                border(p, side, hexv("line"), 4, 4)
    # Prompts à copier (blocs de code) : encadré bleu, police à chasse fixe
    sc = st.add_style("Source Code", WD_STYLE_TYPE.PARAGRAPH)
    sc.base_style = st["Normal"]
    font(sc, "Roboto Mono", 9.5, rgb("blue-deep"))
    sc.paragraph_format.left_indent = Mm(4)
    sc.paragraph_format.space_after = Pt(0)
    sc.paragraph_format.line_spacing = 1.15
    pp = sc.element.get_or_add_pPr()
    shade(pp, hexv("surface-muted"))
    border(pp, "left", hexv("blue-primary"), 24, 10)
    vc = st.add_style("Verbatim Char", WD_STYLE_TYPE.CHARACTER)
    font(vc, "Roboto Mono", 9, rgb("blue-deep"))
    rpr = vc.element.get_or_add_rPr()
    shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hexv("surface-muted"))
    rpr.append(shd)
    lab = st.add_style("Encadre Libelle", WD_STYLE_TYPE.CHARACTER)
    font(lab, HEAD, 8, rgb("orange-text"), bold=True, caps=True)
    mut = st.add_style("Mentions", WD_STYLE_TYPE.PARAGRAPH)
    mut.base_style = st["Normal"]
    font(mut, BODY, 7.5, rgb("ink-muted"))
    # En-tête : logo à gauche, titre à droite (remplacé par document)
    hdr = sec.header
    hp = hdr.paragraphs[0]
    hp.paragraph_format.tab_stops.add_tab_stop(Mm(165), WD_TAB_ALIGNMENT.RIGHT)
    hp.add_run().add_picture(str(logo_png()), height=Mm(11))
    r = hp.add_run("\t{{ENTETE}}")
    r.font.name, r.font.size, r.font.bold, r.font.color.rgb = HEAD, Pt(7.5), True, rgb("blue-primary")
    border(hp._p.get_or_add_pPr(), "bottom", hexv("line"), 4, 4)
    ftr = sec.footer
    fp = ftr.paragraphs[0]
    fp.paragraph_format.tab_stops.add_tab_stop(Mm(165), WD_TAB_ALIGNMENT.RIGHT)
    r = fp.add_run("okoho.de · info@okoho.de · +49 5231 5682750\t")
    r.font.name, r.font.size, r.font.color.rgb = BODY, Pt(7), rgb("ink-muted")
    for code in ("begin", None, "end"):
        run = fp.add_run()
        run.font.size, run.font.color.rgb = Pt(7), rgb("ink-muted")
        if code is None:
            it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = "PAGE"; run._r.append(it)
        else:
            fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), code); run._r.append(fc)
    border(fp._p.get_or_add_pPr(), "top", hexv("line"), 4, 4)
    d.save(path)

def prepare_md(src, cal, label_default, lang="fr"):
    """Markdown → Markdown pandoc : variables, encadrés en custom-style, titre et mentions."""
    text = Path(src).read_text(encoding="utf-8")
    meta = {}
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    if m:
        meta, body = read_seance(src)
    else:
        body = text
    body = resolve(body, cal)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    titre = meta.get("titre")
    if not titre:
        t = re.search(r"^# (.+)$", body, re.M)
        titre = t.group(1).strip() if t else Path(src).stem
    body = re.sub(r"^# .+\n", "", body, count=1, flags=re.M)
    # bloc de mentions final retiré : régénéré
    parts = re.split(r"\n-{3,}\s*\n", body)
    if len(parts) > 1 and ("Une formation OKOHO" in parts[-1] or "© " in parts[-1] or "Quelle:" in parts[-1]):
        body = "\n\n".join(parts[:-1])
    lines, out, in_box = body.splitlines(), [], False
    for l in lines:
        mm = re.match(r"^::: ?([\w-]+)\s*$", l)
        if mm and mm.group(1) in BOXES:
            sname, lab, _, _ = BOXES[mm.group(1)]
            out += [f'::: {{custom-style="{sname}"}}', f'[{lab}]{{custom-style="Encadre Libelle"}}', ""]
            in_box = True
            continue
        if in_box and l.strip() == ":::":
            in_box = False
        elif in_box:
            # Dans un encadré : listes converties en paragraphes pour garder fond et bordure
            l = re.sub(r"^\s*[-*] (\[ \] )?", lambda x: "☐ " if x.group(1) else "• ", l)
            l = re.sub(r"^(\d+)\. ", r"\1\\. ", l)
            if l.strip():
                out += [l, ""]; continue
        out.append(l.replace("- [ ] ", "- ☐ "))
    body = "\n".join(out)
    # Images : largeur téléphone ; capture absente → mention « Capture à venir »
    base = Path(src).parent
    def img(m):
        alt, path = m.group(1), m.group(2)
        if (base / path).is_file():
            return f"![{alt}]({path}){{width=60mm}}"
        return f"*Capture à venir : {alt}*"
    body = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", img, body)
    # « ## » devient Titre 1, « ### » Titre 2
    body = re.sub(r"^(#{2,6}) ", lambda x: "#" * (len(x.group(1)) - 1) + " ", body, flags=re.M)
    code = meta.get("code", "")
    label = label_default or ("ACCUEIL" if code.startswith("A00") else (f"SÉANCE {code}" if code else "OKOHO ACADÉMIE"))
    entete = f"{code} · {titre}" if code else titre
    fr = ("Une formation OKOHO Consulting GmbH · Formateur : Dr. Bertrand Toumi" if lang == "fr"
          else "Interne Arbeitsunterlage der OKOHO Consulting GmbH · Dr. Bertrand Toumi · vertraulich")
    version = meta.get("version")
    capt = meta.get("captures")
    if lang != "fr":
        fin = (f"Claude ist eine Marke von Anthropic. OKOHO Académie ist eine Marke der OKOHO Consulting GmbH, ohne Partnerschaft "
               f"mit Anthropic." + (f" Version {version}." if version else "") + f" © {date.today().year} OKOHO Consulting GmbH")
    else:
      fin = (f"Claude est une marque d'Anthropic. Le Parcours Claude Pro est une formation indépendante proposée par OKOHO "
           f"Consulting GmbH, sans partenariat avec Anthropic. Reproduction et diffusion interdites sans autorisation écrite "
           f"d'OKOHO Consulting GmbH." + (f" Version {version}." if version else "") +
           (f" Captures d'écran réalisées le {capt}." if capt else "") + f" © {date.today().year} OKOHO Consulting GmbH")
    head = f'::: {{custom-style="Subtitle"}}\n{label}\n:::\n\n::: {{custom-style="Title"}}\n{titre}\n:::\n\n*{fr}*\n\n'
    tail = f'\n\n::: {{custom-style="Mentions"}}\n{fin}\n:::\n'
    return head + body + tail, entete, titre

def style_tables(doc):
    for t in doc.tables:
        tbl_pr = t._tbl.tblPr
        borders = OxmlElement("w:tblBorders")
        for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
            b = OxmlElement(f"w:{side}")
            b.set(qn("w:val"), "single"); b.set(qn("w:sz"), "4"); b.set(qn("w:color"), hexv("line"))
            borders.append(b)
        tbl_pr.append(borders)
        for i, row in enumerate(t.rows):
            for cell in row.cells:
                tc = cell._tc.get_or_add_tcPr()
                if i == 0 or i % 2 == 0:
                    shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto")
                    shd.set(qn("w:fill"), hexv("blue-deep") if i == 0 else hexv("surface-muted")); tc.append(shd)
                for p in cell.paragraphs:
                    p.paragraph_format.space_after = Pt(2)
                    for r in p.runs:
                        r.font.size = Pt(9)
                        if i == 0:
                            r.font.bold = True; r.font.color.rgb = rgb("surface")

def build(src, cal=None, out=None, label=None, lang="fr"):
    md, entete, titre = prepare_md(src, cal, label, lang)
    with tempfile.TemporaryDirectory() as tmp:
        ref = Path(tmp) / "reference.docx"
        reference_docx(ref)
        mdf = Path(tmp) / "doc.md"
        mdf.write_text(md, encoding="utf-8")
        out = Path(out) if out else OUT / "docx" / (Path(src).parent.name + ".docx")
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["pandoc", str(mdf), "-f", "markdown+fenced_divs+bracketed_spans+pipe_tables",
                        "-t", "docx", "--reference-doc", str(ref), "--resource-path", str(Path(src).parent),
                        "-o", str(out)], check=True)
    doc = Document(out)
    for p in doc.sections[0].header.paragraphs:
        for r in p.runs:
            if "{{ENTETE}}" in r.text:
                r.text = r.text.replace("{{ENTETE}}", entete)
    style_tables(doc)
    doc.core_properties.title = titre
    doc.core_properties.author = "OKOHO Consulting GmbH · Dr. Bertrand Toumi"
    # Allègement (Drive, WhatsApp) : styles latents et styles inutilisés retirés
    st_el = doc.styles.element
    for ls in st_el.findall(qn("w:latentStyles")):
        st_el.remove(ls)
    body_xml = doc.element.xml + "".join(s_.part.element.xml for s_ in [doc.sections[0].header, doc.sections[0].footer])
    used = set(re.findall(r'w:(?:pStyle|rStyle|tblStyle) w:val="([^"]+)"', body_xml))
    keep = {"Normal", "DefaultParagraphFont", "TableNormal", "NoList"}
    for el in list(st_el.findall(qn("w:style"))):
        sid = el.get(qn("w:styleId"))
        based = el.find(qn("w:basedOn"))
        if sid not in used and sid not in keep and not el.get(qn("w:default")):
            # garder les styles de base des styles utilisés
            if not any(x.find(qn("w:basedOn")) is not None and x.find(qn("w:basedOn")).get(qn("w:val")) == sid
                       for x in st_el.findall(qn("w:style")) if x.get(qn("w:styleId")) in used):
                st_el.remove(el)
    doc.save(out)
    print(f"docx : {out}")
    return out

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opt = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
    if not args:
        sys.exit(__doc__)
    build(args[0], load_cohorte(opt.get("cohorte")), opt.get("out"), opt.get("label"), opt.get("lang", "fr"))

if __name__ == "__main__":
    main()
