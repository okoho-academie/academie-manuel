import 'server-only';
import fs from 'node:fs';
import path from 'node:path';
import yaml from 'js-yaml';
import type { Partie } from './types';
import { DEMO_STRUCTURE } from './demo-structure';

const RACINE = path.resolve(process.cwd(), '..');

interface YamlStructure {
  parties?: { code: string; titre: string; modules?: Partie['modules'] }[];
}

/** Lit manuel/structure.yaml du dépôt ; sinon la structure de démonstration. */
export function lireStructure(): { parties: Partie[]; source: 'depot' | 'demo' } {
  const fichier = path.join(RACINE, 'manuel', 'structure.yaml');
  try {
    const brut = yaml.load(fs.readFileSync(fichier, 'utf8')) as YamlStructure;
    if (brut?.parties?.length) {
      return {
        source: 'depot',
        parties: brut.parties.map((p) => ({ num: p.code, titre: p.titre, modules: p.modules ?? [] })),
      };
    }
  } catch {
    /* pas de fichier : mode démo */
  }
  return { parties: DEMO_STRUCTURE, source: 'demo' };
}

export function toutesLesSeances() {
  return lireStructure().parties.flatMap((p) =>
    p.modules.flatMap((m) => m.seances.map((s) => ({ ...s, partie: p.num, module: m.code, moduleTitre: m.titre }))),
  );
}
