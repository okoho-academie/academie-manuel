#!/usr/bin/env python3
"""Assemble le script Google Apps Script unique de l'Académie : synchronisation Drive + formulaires.
Usage : python3 tools/build_appscript.py <ID_racine_privée> <ID_dossier_semaine> [cohorte-1] [S00]
Sortie : out/appscript/OKOHO_Academie.gs
"""
import subprocess, sys
from common import ROOT, OUT

def main():
    racine, dossier = sys.argv[1], sys.argv[2]
    cohorte = sys.argv[3] if len(sys.argv) > 3 else "cohorte-1"
    semaine = sys.argv[4] if len(sys.argv) > 4 else "S00"
    sync = (ROOT / "tools" / "appscript" / "synchro.gs").read_text(encoding="utf-8")
    sync = sync.replace("{{RACINE_ID}}", racine).replace("{{COHORTE}}", cohorte)
    subprocess.run([sys.executable, str(ROOT / "tools" / "build_forms.py"), dossier, semaine], check=True,
                   stdout=subprocess.DEVNULL)
    forms = (OUT / "forms" / f"creer_formulaires_{semaine}.gs").read_text(encoding="utf-8")
    forms = forms.replace("function creer()", f"function creerFormulaires{semaine}()")
    dest = OUT / "appscript"
    dest.mkdir(parents=True, exist_ok=True)
    p = dest / "OKOHO_Academie.gs"
    p.write_text(sync + "\n\n" + forms, encoding="utf-8")
    print(f"appscript : {p}")

if __name__ == "__main__":
    main()
