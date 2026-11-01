#!/usr/bin/env python3
"""Build complet du Manuel : validate → index → sorties (PDF, Drive, vidéo).
Usage : python3 tools/build.py [CODE]"""
import subprocess, sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent

def run(script, *args):
    r = subprocess.run([sys.executable, str(TOOLS / script), *args])
    if r.returncode:
        sys.exit(f"build : arrêt, {script} a échoué")

def hook(nom, detail):
    print(f"TODO {nom:6} : {detail}")

def main():
    code = sys.argv[1] if len(sys.argv) > 1 else None
    run("validate.py")
    run("build_index.py")
    run("couverture.py")
    cible = code or "toutes les séances"
    run("build_pdf.py", *([code] if code else []))
    run("build_drive.py", "cohorte-1")
    hook("drive", "chargement de out/drive/cohorte-1 dans Google Drive (manifest.json, connecteur ou dépôt manuel)")
    hook("video", f"tutoriel, vitrine, shorts pour {cible} (ffmpeg + voix, agent 4)")
    hook("app", "l'application academie.okoho.de lit seances/ et out/ (dossier app/)")
    print("build : terminé")

if __name__ == "__main__":
    main()
