# OKOHO Académie · App academie.okoho.de

Application d'apprentissage du Parcours Claude Pro. Next.js 14 (App Router), Supabase, hébergement Vercel.
Design : OKOHO Design System 2.2, mode Académie (document 02 v3.0).

## Démarrer en local

```bash
cd app
npm install
npm run dev      # http://localhost:3000
npm test         # règles d'accès (lib/acces.ts)
npm run build
```

Sans variables d'environnement, l'application tourne en **mode démo** avec des données d'exemple (bandeau en haut de page).

## Contenus

- `../manuel/structure.yaml` : parties, modules, séances (sinon `lib/demo-structure.ts`).
- `../seances/<CODE>/seance.md` : contenu d'une séance (front matter selon `../schema/seance.schema.json`).
  La section `## Ce que vous saurez faire` s'affiche dans l'encadré academie-tint.

L'application ne modifie jamais ces fichiers ; elle les lit au moment du build.

## Pages

| Page | Rôle |
|---|---|
| `/` | Accueil, Académie-Orbit, promesse, accès au Parcours Démarrage |
| `/ma-semaine` | Séance de la semaine, devoir et échéance, prochaine séance en direct, fil de progression |
| `/parcours` | Toutes les parties et séances, état d'ouverture avec mot et icône |
| `/seance/[code]` | Contenu d'une séance |
| `/formateur` | Matrice groupes × séances (démo, lecture seule) |

## Règles d'accès

`lib/acces.ts` → `etatSeance(seance, groupe, personne, maintenant)`.
Ordre : terminée > règle individuelle > règle du groupe > accès par défaut de la séance.
États : libre, verrouillé, programmé (ouverture 00:00 heure de Douala), prérequis, jalon, manuel.

## Variables d'environnement

| Variable | Où la trouver |
|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase → Project Settings → API |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase → Project Settings → API (clé publique) |

Copier `.env.example` en `.env.local` pour le développement.

## Base de données

Exécuter `supabase/schema.sql` dans l'éditeur SQL de Supabase. Tables : profiles, groupes, membres, regles_acces,
progression, rendus, jalons. Row Level Security active : l'apprenant voit ses données, l'équipe (administrateur,
formateur) gère, le responsable d'entreprise lit la progression de son entreprise.

## Déploiement Vercel

1. Importer le dépôt `academie-manuel` dans Vercel.
2. **Root Directory** : `app`. Activer « Include files outside of the Root Directory » (lecture de `../seances` et `../manuel`).
3. Renseigner les deux variables d'environnement.
4. Domaine : `academie.okoho.de` (enregistrement CNAME chez l'hébergeur DNS d'okoho.de).

## Polices

Montserrat et Open Sans sont embarquées (`fonts/`, licence OFL) via `next/font/local`, pour un build sans accès à Google Fonts.

## Dépannage

Page sans styles ou « Application error » après `next start` : le serveur sert une ancienne compilation
alors que `.next/` a été reconstruit entre-temps (les fichiers CSS et JS changent de nom à chaque build).
Arrêter le serveur, puis `rm -rf .next && npm run build && npm start`. Ne jamais lancer `npm run build`
pendant qu'un `next start` tourne sur le même dossier.
