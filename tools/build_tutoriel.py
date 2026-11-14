#!/usr/bin/env python3
"""Tutoriel vidéo par IA · OKOHO Académie.

Source : formateur/videos/<CODE>/storyboard.yaml (texte dit, image de chaque plan).
Sortie : out/videos/<CODE>-tutoriel.mp4 (1920×1080, voix Piper en français, sous-titres incrustés)
         et out/videos/<CODE>-tutoriel.srt. La vidéo ne va jamais dans le dépôt.

Plans possibles (champ « image ») :
  carte:intro · carte:outro          cartes de marque générées (logo, titre, mention)
  diapo:<id>                         diapositive de formateur/presentations/<CODE>/ (rendue en 1920×1080)
  capture:<fichier>                  capture réelle de Claude, dans formateur/videos/<CODE>/captures/,
                                     posée sur fond bleu OKOHO ; « cadre » optionnel [x0, y0, x1, y1] pour recadrer
Voix : modèle Piper dans $PIPER_VOIX (défaut /home/claude/video/voix), voix nommée dans le storyboard.
Usage : python3 tools/build_tutoriel.py M02-S1
"""
import json, os, re, subprocess, sys, tempfile, wave
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from common import ROOT, OUT, load_yaml

W, H = 1920, 1080
BLEU, BLEU_FONCE, ORANGE, BLANC, CLAIR = (14, 74, 123), (10, 52, 88), (255, 161, 66), (255, 255, 255), (191, 211, 234)
FONTS = ROOT / "design" / "fonts"
LOGO = ROOT / "design" / "logos" / "academie-logo-A-weiss-600.png"
VOIX = Path(os.environ.get("PIPER_VOIX", "/home/claude/video/voix"))
MENTION = "Une formation OKOHO Consulting GmbH · Formateur : Dr. Bertrand Toumi · Claude est une marque d'Anthropic, sans partenariat"

def police(nom, taille):
    return ImageFont.truetype(str(FONTS / nom), taille)

def lignes(draw, texte, font, largeur):
    mots, out, cur = texte.split(), [], ""
    for m in mots:
        t = (cur + " " + m).strip()
        if draw.textlength(t, font=font) <= largeur:
            cur = t
        else:
            out.append(cur); cur = m
    return out + [cur] if cur else out

def carte(sb, quoi, dest):
    im = Image.new("RGB", (W, H), BLEU)
    d = ImageDraw.Draw(im)
    logo = Image.open(LOGO).convert("RGBA")
    logo.thumbnail((600, 240))
    im.paste(logo, (128, 110), logo)
    if quoi == "intro":
        d.text((128, 560), f"Tutoriel · {sb['code']}", font=police("Montserrat-SemiBold.ttf", 44), fill=ORANGE)
        y = 630
        for l in lignes(d, sb["titre"], police("Montserrat-Bold.ttf", 104), 1600):
            d.text((128, y), l, font=police("Montserrat-Bold.ttf", 104), fill=BLANC); y += 118
        d.rectangle((128, y + 20, 248, y + 28), fill=ORANGE)
        d.text((128, y + 60), sb.get("sous_titre", ""), font=police("OpenSans-Regular.ttf", 44), fill=BLANC)
    else:
        d.text((128, 470), "À vous", font=police("Montserrat-SemiBold.ttf", 44), fill=ORANGE)
        y = 540
        for l in lignes(d, sb["action"], police("Montserrat-Bold.ttf", 88), 1660):
            d.text((128, y), l, font=police("Montserrat-Bold.ttf", 88), fill=BLANC); y += 104
    d.text((128, 990), MENTION, font=police("OpenSans-Regular.ttf", 28), fill=CLAIR)
    im.save(dest)

def diapos(code, tmp):
    """Rend toutes les diapositives de la présentation en PNG 1920×1080, par id."""
    src = ROOT / "formateur" / "presentations" / code
    if not src.is_dir():
        return {}
    deck = json.loads((src / "deck.json").read_text(encoding="utf-8"))
    pdf = Path(tmp) / "diapos.pdf"
    subprocess.run([sys.executable, str(ROOT / "tools" / "build_slides_pdf.py"), str(src), str(pdf)], check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["pdftoppm", "-png", "-scale-to-x", str(W), "-scale-to-y", str(H), str(pdf), str(Path(tmp) / "d")], check=True)
    pages = sorted(Path(tmp).glob("d-*.png"))
    return {sid: pages[i] for i, sid in enumerate(deck["order"]) if i < len(pages)}

def capture(fichier, cadre, dest, legende=None):
    """Capture réelle, centrée sur fond bleu, coins arrondis, ombre ; légende orange optionnelle."""
    im = Image.new("RGB", (W, H), BLEU)
    c = Image.open(fichier).convert("RGB")
    if cadre:
        c = c.crop(tuple(cadre))
    zone_h = H - (340 if legende else 260)   # bande basse de 200 px réservée aux sous-titres
    c.thumbnail((W - 200, zone_h), Image.LANCZOS)
    if c.width < W - 200 and c.height < zone_h:
        f = min((W - 200) / c.width, zone_h / c.height)
        c = c.resize((int(c.width * f), int(c.height * f)), Image.LANCZOS)
    x, y = (W - c.width) // 2, (120 if legende else 60) + (zone_h - c.height) // 2
    ombre = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ombre).rounded_rectangle((x + 8, y + 12, x + c.width + 8, y + c.height + 12), 24, fill=(0, 0, 0, 110))
    im.paste(ombre.filter(ImageFilter.GaussianBlur(14)), (0, 0), ombre.filter(ImageFilter.GaussianBlur(14)))
    masque = Image.new("L", c.size, 0)
    ImageDraw.Draw(masque).rounded_rectangle((0, 0, c.width, c.height), 24, fill=255)
    im.paste(c, (x, y), masque)
    if legende:
        d = ImageDraw.Draw(im)
        d.text((100, 40), legende, font=police("Montserrat-SemiBold.ttf", 46), fill=ORANGE)
    im.save(dest)

def voix(texte, modele, dest):
    subprocess.run([sys.executable, "-m", "piper", "-m", str(VOIX / f"{modele}.onnx"), "-f", str(dest),
                    "--length-scale", "1.08", "--sentence-silence", "0.35"],
                   input=texte.encode("utf-8"), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with wave.open(str(dest)) as w:
        return w.getnframes() / w.getframerate()

def srt_temps(s):
    h, r = divmod(s, 3600); m, r = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(r):02d},{int((r % 1) * 1000):03d}"

def morceaux(texte, n=70):
    """Coupe le texte en sous-titres courts, aux limites de phrase puis de mots."""
    out = []
    for phrase in re.split(r"(?<=[.!?:])\s+", texte.strip()):
        mots, cur = phrase.split(), ""
        for m in mots:
            if len(cur) + len(m) + 1 > n and cur:
                out.append(cur); cur = m
            else:
                cur = (cur + " " + m).strip()
        if cur:
            out.append(cur)
    return out

def main():
    code = sys.argv[1]
    base = ROOT / "formateur" / "videos" / code
    sb = load_yaml(base / "storyboard.yaml")
    dest = OUT / "videos"
    dest.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        ds = diapos(code, tmp)
        clips, srt, t, k = [], [], 0.0, 1
        for i, seg in enumerate(sb["plans"]):
            img = tmp / f"p{i:02d}.png"
            src = seg["image"]
            if src.startswith("carte:"):
                carte(sb, src[6:], img)
            elif src.startswith("diapo:"):
                Image.open(ds[src[6:]]).convert("RGB").resize((W, H)).save(img)
            elif src.startswith("capture:"):
                capture(base / "captures" / src[8:], seg.get("cadre"), img, seg.get("legende"))
            else:
                sys.exit(f"plan inconnu : {src}")
            wav = tmp / f"p{i:02d}.wav"
            texte = seg.get("texte", "").strip()
            duree = voix(texte, sb["voix"], wav) if texte else 0.0
            duree = max(duree + 0.6, seg.get("min", 3.0))
            mp4 = tmp / f"p{i:02d}.mp4"
            zoom = "zoompan=z='min(zoom+0.0004,1.06)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=25," if seg.get("zoom") else ""
            audio = ["-i", str(wav)] if texte else ["-f", "lavfi", "-i", "anullsrc=r=22050:cl=mono"]
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(img), *audio,
                            "-filter_complex", f"[0:v]{zoom}scale=1920:1080,format=yuv420p[v];[1:a]apad,atrim=0:{duree:.2f},aresample=44100[a]",
                            "-map", "[v]", "-map", "[a]", "-t", f"{duree:.2f}", "-r", "25",
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "128k", str(mp4)], check=True)
            clips.append(mp4)
            if texte:
                parts = morceaux(texte)
                total = sum(len(p) for p in parts)
                debut = t
                for p in parts:
                    fin = debut + (duree - 0.6) * len(p) / total
                    srt.append(f"{k}\n{srt_temps(debut)} --> {srt_temps(fin)}\n{p}\n"); k += 1
                    debut = fin
            t += duree
            print(f"plan {i + 1:02d} · {src} · {duree:.1f} s")
        liste = tmp / "liste.txt"
        liste.write_text("".join(f"file '{c}'\n" for c in clips))
        brut = tmp / "brut.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(liste), "-c", "copy", str(brut)], check=True)
        srt_f = dest / f"{code}-tutoriel.srt"
        srt_f.write_text("\n".join(srt), encoding="utf-8")
        style = "FontName=Open Sans,FontSize=20,PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,BorderStyle=3,Outline=1,Shadow=0,MarginV=28"
        final = dest / f"{code}-tutoriel.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(brut),
                        "-vf", f"subtitles={srt_f}:fontsdir={FONTS}:force_style='{style}'",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-c:a", "copy", str(final)], check=True)
    print(f"tutoriel : {final} · {t / 60:.1f} min")

if __name__ == "__main__":
    main()
