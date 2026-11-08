#!/usr/bin/env python3
"""Kit du prestataire et Dossier client pilote · OKOHO Académie.

Deux documents générés, jamais écrits à la main :
  out/kit/kit-du-prestataire.md     : toutes les sections « ## Votre fiche-outil » des séances, dans l'ordre du Manuel.
                                      Les outils servent pour n'importe quel client (PDF à garder).
  out/kit/dossier-client-pilote.md  : modèle à remplir (Word), une page par étape de manuel/fil-client-pilote.yaml.
                                      Les produits d'un seul client, réunis séance après séance.
build_drive.py les place dans « 05 · Ressources et liens utiles ». Usage : python3 tools/build_kit.py
"""
import re, sys
from common import ROOT, OUT, load_yaml, read_seance, seance_files, structure

MENTION = ("Une formation OKOHO Consulting GmbH · Formateur : Dr. Bertrand Toumi\n"
           "Claude est une marque d'Anthropic. Le Parcours Claude Pro est une formation indépendante proposée par "
           "OKOHO Consulting GmbH, sans partenariat avec Anthropic.")

def section(body, titre):
    m = re.search(rf"^## {re.escape(titre)}\n(.*?)(?=^## |\n-{{3,}}\n|\Z)", body, re.S | re.M)
    return m.group(1).strip() if m else None

def kit():
    _, struct = structure()
    ordre = list(struct)
    fiches = []
    for f in seance_files():
        meta, body = read_seance(f)
        s = section(body, "Votre fiche-outil")
        if not s or meta.get("status") == "brouillon":
            continue
        m = re.match(r"\*\*(Fiche-outil [^*]+?)\.?\*\*\s*(.*)", s, re.S)
        titre, texte = (m.group(1), m.group(2)) if m else (f"Fiche-outil · {meta['titre']}", s)
        fiches.append((ordre.index(meta["code"]) if meta["code"] in ordre else 999, meta["code"], titre, texte.strip()))
    fiches.sort()
    out = ["# Kit du prestataire", "",
           "::: objectifs",
           "- Les outils de chaque séance, réunis dans un seul document à garder sur votre téléphone.",
           "- Chaque fiche sert pour n'importe quel client : vous changez seulement le contexte.",
           "- Le kit grandit à chaque séance. Téléchargez la nouvelle version chaque semaine.",
           ":::", "",
           "## Comment utiliser ce kit", "",
           "Copiez les consignes à trous dans les notes de votre téléphone. Pour un nouveau client : écrivez d'abord sa fiche contexte (fiche-outil 03), puis collez-la dans la partie « Contexte » de chaque consigne. "
           "Ce kit deviendra votre bibliothèque de consignes (séance M02-S3), puis les connaissances de votre projet Claude (séance M04-S2).", "",
           "| N° | Fiche-outil | Séance |", "|---|---|---|"]
    out += [f"| {i} | {t.split('·', 1)[-1].strip()} | {c} |" for i, (_, c, t, _) in enumerate(fiches, 1)]
    out.append("")
    for _, code, titre, texte in fiches:
        out += [f"## {titre}", "", f"*Séance {code}*", "", texte, ""]
    out += ["---", "", MENTION]
    return "\n".join(out) + "\n", len(fiches)

def dossier():
    d = load_yaml(ROOT / "manuel" / "fil-client-pilote.yaml")
    _, struct = structure()
    r = d["regles"]
    out = ["# Dossier client pilote", "",
           "::: objectifs",
           "- Un seul document pour votre client pilote : chaque séance y ajoute une page, un produit réel.",
           "- À chaque Démo Day, vous présentez ce dossier : ce que vous avez produit, ce que votre client en a fait.",
           "- À la fin du parcours, vous remettez le dossier complet à votre client pilote.",
           ":::", "",
           "## Avant de commencer", "",
           "1. Copiez ce document dans votre portfolio et renommez-le **Dossier_client_pilote_Prenom**.",
           "2. Votre client pilote : une personne, une entreprise ou votre propre structure (école, centre de santé, commerce, association).",
           "3. Remplissez une page à la fin de chaque séance indiquée ci-dessous.", "",
           "| Votre client pilote | Votre réponse |", "|---|---|",
           "| Activité ou structure (sans nom de famille) | |",
           "| Type | Externe (personne de mon entourage) / Interne (ma propre structure) |",
           "| Accord obtenu le (externe) ou personne qui valide (interne) | |",
           "| Tâches qui prennent le plus de temps, heures par semaine au départ | |", "",
           "## Les règles", "",
           f"- **Données.** {r['donnees']}",
           f"- **Publication.** {r['publication_interne']}",
           f"- **Valeur.** {r['valeur']}", "",
           "## Feuille de route", "",
           "| Page | Séance | Produit | Jalon |", "|---|---|---|---|"]
    for e in d["etapes"]:
        out.append(f"| {e['page']} | {e['seance']} | {e['produit']} | {e['jalon']} |")
    out.append("")
    for e in d["etapes"]:
        titre = struct.get(e["seance"], {}).get("titre", "")
        out += [f"## Page {e['page']} · {e['produit']}", "",
                f"*Séance {e['seance']} · {titre} · jalon {e['jalon']}*", ""]
        ex = [f"Exemple externe : {e['externe']}." if e.get("externe") else "",
              f"Exemple interne : {e['interne']}." if e.get("interne") else ""]
        ex = " ".join(x for x in ex if x)
        if ex:
            out += [ex, ""]
        out += ["| Rubrique | Votre réponse |", "|---|---|",
                "| Ce que j'ai produit | |",
                "| Consigne principale utilisée | |",
                "| Résultat (texte, capture ou lien) | |",
                "| Réaction du client ou validation (date) | |",
                "| Utilisé ou publié ? Où ? | |",
                "| Temps gagné (interne) ou résultat obtenu (externe) | |", ""]
    out += ["---", "", MENTION]
    return "\n".join(out) + "\n"

def main():
    dest = OUT / "kit"
    dest.mkdir(parents=True, exist_ok=True)
    k, n = kit()
    (dest / "kit-du-prestataire.md").write_text(k, encoding="utf-8")
    (dest / "dossier-client-pilote.md").write_text(dossier(), encoding="utf-8")
    print(f"kit : {n} fiche(s)-outil, dossier client pilote généré dans out/kit/")
    return 0

if __name__ == "__main__":
    sys.exit(main())
