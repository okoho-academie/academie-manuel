#!/usr/bin/env python3
"""PDF d'une présentation Claude Slides (copie dans formateur/presentations/<NOM>/) · OKOHO Académie.
Une page 1920×1080 par diapositive, dans l'ordre de deck.json. Notes du présentateur (<aside>) en page de notes.
Usage : python3 tools/build_slides_pdf.py formateur/presentations/A00-lancement sortie.pdf
"""
import json, re, sys
from pathlib import Path
from common import ROOT

BLOBS = {"484c4cd918cc7131a5e0b404692476bf": "academie-logo-A-weiss.png",
         "1aef23d7f7b59c4c19477ad9dc2fd221": "academie-zeichen-weiss.png"}

def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    deck = json.loads((src / "deck.json").read_text(encoding="utf-8"))
    logos, fonts = (ROOT / "design" / "logos").as_uri(), (ROOT / "design" / "fonts").as_uri()
    css = f"""
@font-face{{font-family:'Montserrat';src:url('{fonts}/Montserrat-Variable.ttf');font-weight:100 900}}
@font-face{{font-family:'Open Sans';src:url('{fonts}/OpenSans-Variable.ttf');font-weight:300 800}}
@page{{size:1920px 1080px;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
section{{width:1920px;height:1080px;position:relative;overflow:hidden;page-break-after:always}}
section aside{{display:none}}
section ul,section ol{{padding-left:1.2em}}
.notes{{width:1920px;height:1080px;padding:120px;background:#F5F5F5;color:#333;font-family:'Open Sans';page-break-after:always}}
.notes h2{{font-family:'Montserrat';color:#2C5697;font-size:44px;margin-bottom:40px}}
.notes p{{font-size:34px;line-height:1.5}}
"""
    pages = []
    for i, sid in enumerate(deck["order"], 1):
        h = (src / "slides" / f"{sid}.html").read_text(encoding="utf-8")
        for b, f in BLOBS.items():
            h = h.replace(f"/_blob/{b}", f"{logos}/{f}")
        pages.append(h)
        m = re.search(r"<aside>(.*?)</aside>", h, re.S)
        if m and "--notes" in sys.argv:
            pages.append(f'<div class="notes"><h2>Notes · diapositive {i}</h2><p>{m.group(1)}</p></div>')
    html = f"<!doctype html><html lang='fr'><meta charset='utf-8'><style>{css}</style><body>{''.join(pages)}</body></html>"
    tmp = out.with_suffix(".html")
    tmp.write_text(html, encoding="utf-8")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1920, "height": 1080})
        pg.goto(tmp.as_uri()); pg.wait_for_timeout(800)
        pg.pdf(path=str(out), width="1920px", height="1080px", print_background=True)
        b.close()
    tmp.unlink()
    print(f"slides : {out}")

if __name__ == "__main__":
    main()
