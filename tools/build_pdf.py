#!/usr/bin/env python3
"""PDF du Manuel · OKOHO Académie.

Génère out/pdf/OKOHO_PCP_<CODE>_<Type>_v<version>.pdf à partir de
  seances/<CODE>/seance.md   (Type : Fiche)
  accueil/<CODE>/document.md (Type : Guide)
Usage : python3 tools/build_pdf.py [CODE ...] [--fixtures]
Conventions de rédaction : tools/README_PDF.md
"""
import base64, html, re, sys
from pathlib import Path
from common import ROOT, OUT, read_seance, structure, load_yaml

try:
    import markdown
except ImportError:
    sys.exit("markdown manquant : pip install markdown")

DESIGN = ROOT / "design"
FONTS = DESIGN / "fonts"
PDF_DIR = OUT / "pdf"
WARNINGS = []

BOXES = {
    "objectifs": ("CE QUE VOUS SAUREZ FAIRE", "box-aca"),
    "livrable": ("VOTRE LIVRABLE", "box-aca"),
    "fil-rouge": ("CAS FIL ROUGE", "box-tint"),
    "erreurs": ("ERREURS FRÉQUENTES", "box-alert"),
    "coup-de-pouce": ("COUPS DE POUCE", "box-pouce"),
    "prompt": ("CONSIGNE À COPIER", "box-prompt"),
}
# Titres de section transformés en encadrés (séances)
HEADING_BOXES = {"Ce que vous saurez faire": "objectifs", "Votre livrable": "livrable",
                 "Cas fil rouge": "fil-rouge", "Erreurs fréquentes": "erreurs"}
JALONS = ["J1", "J2", "J3", "J4", "J5"]


def md_to_html(text):
    return markdown.markdown(text, extensions=["tables", "sane_lists", "attr_list"], output_format="html5")


def data_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def strip_doc_chrome(body):
    """Retire le titre H1 et le bloc de mentions final : le gabarit les produit lui-même."""
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    body = re.sub(r"^\s*# [^\n]*\n", "", body, count=1)
    parts = re.split(r"\n-{3,}\s*\n", body)
    if len(parts) > 1 and "Une formation OKOHO Consulting GmbH" in parts[-1]:
        body = "\n---\n".join(parts[:-1])
    return body


def split_divs(text):
    """Découpe le texte en segments (nom_de_bloc|None, contenu). Blocs ::: nom … ::: non imbriqués."""
    out, cur, name = [], [], None
    for line in text.split("\n"):
        m = re.match(r"^:::\s*([\w-]+)\s*$", line)
        if m and name is None:
            out.append((None, "\n".join(cur))); cur, name = [], m.group(1)
        elif re.match(r"^:::\s*$", line) and name is not None:
            out.append((name, "\n".join(cur))); cur, name = [], None
        else:
            cur.append(line)
    out.append((name, "\n".join(cur)))
    if name is not None:
        WARNINGS.append(f"bloc ::: {name} non fermé")
    return out


def heading_boxes(text):
    """Dans une séance, '## Ce que vous saurez faire' etc. deviennent des blocs encadrés."""
    lines, res, i = text.split("\n"), [], 0
    while i < len(lines):
        m = re.match(r"^##\s+(.+?)\s*$", lines[i])
        if m and m.group(1) in HEADING_BOXES:
            j = i + 1
            while j < len(lines) and not re.match(r"^#{1,2}\s", lines[j]):
                j += 1
            res += [f"::: {HEADING_BOXES[m.group(1)]}", *lines[i + 1:j], ":::"]
            i = j
        else:
            res.append(lines[i]); i += 1
    return "\n".join(res)


def render_body(text, base_dir):
    chunks = []
    for name, content in split_divs(text):
        inner = md_to_html(content) if content.strip() else ""
        if name is None:
            chunks.append(inner)
            continue
        if name not in BOXES:
            WARNINGS.append(f"bloc inconnu ::: {name}")
            chunks.append(inner); continue
        label, cls = BOXES[name]
        if name == "coup-de-pouce":
            inner = inner.replace("<ol>", '<ol class="pouce">', 1)
        if not content.strip():
            inner = '<p class="vide">À compléter.</p>'
        chunks.append(f'<section class="box {cls}"><div class="box-label">{label}</div>{inner}</section>')
    out = "\n".join(chunks)
    out = postprocess(out, base_dir)
    return out


def postprocess(h, base_dir):
    # Checklists
    h = re.sub(r"<li>\s*\[ \]\s*", '<li class="check"><span class="cb"></span>', h)
    h = re.sub(r"<li>\s*\[[xX]\]\s*", '<li class="check"><span class="cb on">✓</span>', h)
    h = re.sub(r"<ul>(\s*<li class=\"check\")", r'<ul class="checklist">\1', h)

    # Images -> figures avec légende, ou emplacement « Capture à venir »
    def fig(m):
        attrs = m.group(1)
        src = re.search(r'src="([^"]*)"', attrs).group(1)
        alt_m = re.search(r'alt="([^"]*)"', attrs)
        alt = alt_m.group(1) if alt_m else ""
        p = (base_dir / html.unescape(src)).resolve()
        if src.startswith(("http://", "https://", "data:")):
            img = f'<img src="{src}" alt="{alt}">'
        elif p.is_file():
            mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "svg": "image/svg+xml", "webp": "image/webp"}.get(p.suffix[1:].lower(), "image/png")
            img = f'<img src="{data_uri(p, mime)}" alt="{alt}">'
        else:
            WARNINGS.append(f"capture manquante : {src}")
            return f'<figure class="capture missing"><div class="placeholder">Capture à venir : {alt or src}</div></figure>'
        return f'<figure class="capture">{img}<figcaption>{alt}</figcaption></figure>'
    h = re.sub(r"<p>\s*<img ([^>]*?)/?>\s*</p>", fig, h)
    h = re.sub(r"<img ((?![^>]*(?:data:|https?:))[^>]*?)/?>", fig, h)

    # Chapitres numérotés (h2) avec bloc numéro
    n = [0]
    def chap(m):
        n[0] += 1
        return f'<h2 class="chap"><span class="nb">{n[0]:02d}</span><span class="t">{m.group(1)}</span></h2>'
    h = re.sub(r"<h2>(.*?)</h2>", chap, h)
    return h


def fil_svg(jalon, width=150):
    """Fil de progression : J1–J5, acquis / en cours / à venir."""
    if jalon not in JALONS:
        return ""
    k = JALONS.index(jalon)
    step, r, y = 32, 5, 8
    x0 = 8
    parts = []
    for i in range(4):
        col = "#FFA142" if i < k else "#D5DCE6"
        parts.append(f'<line x1="{x0+i*step}" y1="{y}" x2="{x0+(i+1)*step}" y2="{y}" stroke="{col}" stroke-width="2"/>')
    for i, j in enumerate(JALONS):
        cx = x0 + i * step
        if i < k:
            parts.append(f'<circle cx="{cx}" cy="{y}" r="{r}" fill="#6B9CD1"/>')
        elif i == k:
            parts.append(f'<circle cx="{cx}" cy="{y}" r="{r+1}" fill="#FFA142"/>')
        else:
            parts.append(f'<circle cx="{cx}" cy="{y}" r="{r-0.75}" fill="#FFFFFF" stroke="#2C5697" stroke-width="1.5"/>')
        parts.append(f'<text x="{cx}" y="{y+16}" text-anchor="middle" font-family="Montserrat, Arial" font-size="7" font-weight="600" fill="#5C5C5C">{j}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="26" viewBox="0 0 {x0*2+4*step} 26" '
            f'role="img" aria-label="Fil de progression : jalon {jalon} en cours">' + "".join(parts) + "</svg>")


def css():
    fonts = ""
    # Polices statiques : PDF nettement plus légers que les polices variables (Type 3).
    for fam, base in (("Montserrat", "Montserrat"), ("Open Sans", "OpenSans")):
        for w, style in ((400, "Regular"), (600, "SemiBold"), (700, "Bold")):
            p = FONTS / f"{base}-{style}.ttf"
            if p.is_file():
                fonts += f'@font-face{{font-family:"{fam}";src:url("{p.as_uri()}");font-weight:{w};}}\n'
    tokens = (DESIGN / "tokens.css").read_text(encoding="utf-8")
    return tokens + fonts + r"""
@page{size:A4;margin:30mm 20mm 20mm 25mm;}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact;}
body{font-family:var(--font-body);font-size:10.5pt;line-height:1.55;color:var(--ink);margin:0;}
.cover{margin-bottom:8mm;}
.cover .label{font-family:var(--font-display);font-weight:700;font-size:8pt;letter-spacing:.15em;text-transform:uppercase;color:var(--orange-text);}
.cover h1{font-family:var(--font-display);font-weight:700;font-size:24pt;line-height:1.2;color:var(--blue-primary);margin:3mm 0 3mm;}
.cover .meta{font-size:9pt;color:var(--ink-muted);display:flex;flex-wrap:wrap;gap:2mm 6mm;margin-bottom:2mm;}
.cover .mention{font-size:9pt;color:var(--ink);border-bottom:1px solid var(--line);padding-bottom:3mm;}
.cover .fil{margin:2mm 0 1mm;}
h2.chap{display:flex;align-items:center;gap:4mm;margin:9mm 0 4mm;break-after:avoid;font-family:var(--font-display);}
h2.chap .nb{flex:none;width:10mm;height:10mm;background:var(--blue-deep);color:#fff;font-weight:700;font-size:11pt;display:flex;align-items:center;justify-content:center;border-bottom:1.6pt solid var(--orange-accent);}
h2.chap .t{font-size:15pt;font-weight:700;color:var(--blue-primary);}
h3{font-family:var(--font-display);font-weight:600;font-size:12pt;color:var(--blue-primary);margin:6mm 0 2mm;break-after:avoid;}
h4{font-family:var(--font-display);font-weight:600;font-size:10.5pt;color:var(--ink);margin:4mm 0 1mm;}
p{margin:0 0 2.5mm;} ul,ol{margin:0 0 3mm;padding-left:6mm;} li{margin-bottom:1mm;}
a{color:var(--orange-text);}
strong{font-weight:600;}
.box{border-radius:8px;padding:4mm 5mm;margin:4mm 0;break-inside:avoid;}
.box p:last-child,.box ul:last-child,.box ol:last-child{margin-bottom:0;}
.box-label{font-family:var(--font-display);font-weight:700;font-size:7.5pt;letter-spacing:.15em;color:var(--orange-text);margin-bottom:2mm;}
.box-aca{background:var(--academie-tint);}
.box-tint{background:var(--blue-tint);}
.box-alert{background:#fff;border:1.5pt solid var(--orange-accent);}
.box-pouce{background:var(--surface-muted);}
.box-prompt{background:#fff;border:1pt solid var(--line-strong);}
.box-prompt p{font-family:var(--font-body);}
ol.pouce{list-style:none;counter-reset:pouce;padding-left:0;}
ol.pouce li{counter-increment:pouce;position:relative;padding-left:8mm;margin-bottom:2mm;}
ol.pouce li::before{content:counter(pouce);position:absolute;left:0;top:0;width:5.5mm;height:5.5mm;border-radius:50%;background:var(--orange-accent);color:var(--ink);font-family:var(--font-display);font-weight:700;font-size:8pt;display:flex;align-items:center;justify-content:center;}
.vide{color:var(--ink-muted);font-style:normal;}
ul.checklist{list-style:none;padding-left:0;}
li.check{display:flex;gap:2.5mm;align-items:flex-start;}
.cb{flex:none;width:3.6mm;height:3.6mm;border:1.2pt solid var(--blue-primary);border-radius:1px;margin-top:.9mm;font-size:7pt;line-height:3.6mm;text-align:center;color:var(--blue-primary);}
figure.capture{margin:4mm 0;break-inside:avoid;}
figure.capture img{max-width:100%;max-height:120mm;border:1px solid var(--line);display:block;}
figure.capture figcaption{font-size:8.5pt;color:var(--ink-muted);margin-top:1.5mm;}
figure.missing .placeholder{border:1.2pt dashed var(--line-strong);background:var(--surface-muted);color:var(--ink-muted);padding:10mm 5mm;text-align:center;font-size:9pt;}
table{border-collapse:collapse;width:100%;margin:3mm 0 4mm;font-size:9.5pt;break-inside:auto;}
thead th{background:var(--blue-deep);color:#fff;font-family:var(--font-display);font-weight:600;text-align:left;padding:2mm 3mm;}
td{padding:2mm 3mm;border-bottom:1px solid var(--line);vertical-align:top;}
tbody tr:nth-child(even) td{background:var(--surface-muted);}
hr{border:0;border-top:1px solid var(--line);margin:6mm 0;}
code{font-family:var(--font-body);background:var(--surface-muted);padding:0 1mm;border-radius:2px;}
.fin{margin-top:10mm;border-top:1px solid var(--line);padding-top:3mm;font-size:7.5pt;color:var(--ink-muted);line-height:1.5;break-inside:avoid;}
"""


def header_footer(code, titre, jalon):
    logo = data_uri(DESIGN / "logos" / "academie-logo-A.svg", "image/svg+xml")
    fil = fil_svg(jalon, 120)
    head = f"""<div style="width:100%;margin:0 20mm 0 25mm;font-family:'Open Sans',Arial,sans-serif;font-size:7pt;color:#5C5C5C;
display:flex;justify-content:space-between;align-items:flex-start;border-bottom:0.5pt solid #D5DCE6;padding:8mm 0 2mm;-webkit-print-color-adjust:exact;">
<img src="{logo}" style="height:11mm;">
<div style="text-align:right;"><div style="font-family:Montserrat,Arial,sans-serif;font-weight:600;color:#2C5697;font-size:7.5pt;">{html.escape(code)} · {html.escape(titre)}</div>
<div style="margin-top:1mm;">{fil}</div></div></div>"""
    foot = """<div style="width:100%;margin:0 20mm 0 25mm;font-family:'Open Sans',Arial,sans-serif;font-size:7pt;color:#5C5C5C;
display:flex;justify-content:space-between;border-top:0.5pt solid #D5DCE6;padding-top:2mm;">
<span>okoho.de · info@okoho.de · +49 5231 5682750</span><span class="pageNumber"></span></div>"""
    return head, foot


def build_one(kind, path, struct):
    meta, body = read_seance(path)
    code, titre = meta["code"], meta["titre"]
    version = str(meta.get("version", "0.1"))
    captures = meta.get("captures") or "—"
    if kind == "seance":
        ref = struct.get(code, {})
        label = f"PARTIE {meta.get('partie','')} · {ref.get('partie_titre','')} · MODULE {meta.get('module','')} · {ref.get('module_titre','')}"
        typ = "Fiche"
        duree = meta.get("duree") or {}
        infos = [f"{'En direct' if meta.get('type') == 'direct' else 'En autonomie'}", meta.get("outil", ""),
                 {"smartphone": "Smartphone possible", "laptop-recommande": "Ordinateur portable recommandé",
                  "laptop-obligatoire": "Ordinateur portable obligatoire"}.get(meta.get("appareil"), meta.get("appareil", "")),
                 f"Séance {duree.get('seance','–')} min · devoir {duree.get('devoir','–')} min",
                 f"Échafaudage niveau {meta.get('echafaudage','–')}"]
        body = heading_boxes(strip_doc_chrome(body))
    else:
        label = "ACCUEIL"
        typ = "Guide"
        infos = ["Public : " + ("apprenants" if meta.get("public") == "apprenants" else "formateur")]
        body = strip_doc_chrome(body)
    jalon = meta.get("jalon")
    content = render_body(body, path.parent)
    fil = fil_svg(jalon, 190)
    cover = f"""<header class="cover"><div class="label">{html.escape(label)}</div>
<h1>{html.escape(titre)}</h1>
<div class="meta">{''.join(f'<span>{html.escape(str(i))}</span>' for i in infos if i)}</div>
{f'<div class="fil">{fil}</div>' if fil else ''}
<div class="mention">Une formation OKOHO Consulting GmbH · Formateur : Dr. Bertrand Toumi</div></header>"""
    fin = f"""<div class="fin">Claude est une marque d'Anthropic. Le Parcours Claude Pro est une formation indépendante proposée par
OKOHO Consulting GmbH, sans partenariat avec Anthropic. Reproduction et diffusion interdites sans autorisation écrite
d'OKOHO Consulting GmbH.<br>Version {html.escape(version)} · Captures d'écran réalisées le {html.escape(str(captures))} · © 2026 OKOHO Consulting GmbH</div>"""
    doc = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{html.escape(code)} · {html.escape(titre)}</title>
<style>{css()}</style></head><body>{cover}{content}{fin}</body></html>"""
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    out = PDF_DIR / f"OKOHO_PCP_{code}_{typ}_v{version}.pdf"
    head, foot = header_footer(code, titre, jalon)
    return doc, out, head, foot


def render(jobs):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        for doc, out, head, foot in jobs:
            tmp = OUT / "pdf" / (out.stem + ".html")
            tmp.write_text(doc, encoding="utf-8")
            pg.goto(tmp.as_uri())
            pg.wait_for_load_state("networkidle")
            pg.evaluate("document.fonts.ready")
            pg.pdf(path=str(out), format="A4", print_background=True, display_header_footer=True,
                   header_template=head, footer_template=foot, prefer_css_page_size=True)
            tmp.unlink()
            print(f"pdf : {out.relative_to(ROOT)}")
        b.close()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    fixtures = "--fixtures" in sys.argv
    _, struct = structure()
    sources = [("seance", f) for f in sorted((ROOT / "seances").glob("*/seance.md"))]
    sources += [("document", f) for f in sorted((ROOT / "accueil").glob("*/document.md"))]
    if fixtures:
        sources += [("document", f) for f in sorted((ROOT / "tests" / "fixtures").glob("*/document.md"))]
    if args:
        sources = [s for s in sources if s[1].parent.name in args]
    jobs = []
    for kind, f in sources:
        try:
            jobs.append(build_one(kind, f, struct))
        except Exception as e:
            print(f"ERREUR pdf {f.relative_to(ROOT)} : {e}"); return 1
    if jobs:
        render(jobs)
    for w in WARNINGS:
        print(f"AVERT.  pdf : {w}")
    print(f"build_pdf : {len(jobs)} PDF, {len(WARNINGS)} avertissement(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
