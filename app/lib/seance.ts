import 'server-only';
import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';
import { marked } from 'marked';
import type { Jalon } from './acces';

const RACINE = path.resolve(process.cwd(), '..');
const CODE = /^M\d{2}-S\d$/;

export interface SeanceMeta {
  code: string;
  partie?: string;
  module?: string;
  titre: string;
  type?: 'direct' | 'autonomie';
  outil?: string;
  appareil?: string;
  duree?: { seance: number; devoir: number };
  echafaudage?: number;
  jalon?: Jalon;
  livrable?: string;
  status?: string;
  version?: string;
}

export interface SeanceDoc {
  meta: SeanceMeta;
  html: string;
  objectifsHtml: string | null;
}

/** Lit seances/<code>/seance.md. Le code est validé pour empêcher toute sortie du dossier. */
export function lireSeance(code: string): SeanceDoc | null {
  if (!CODE.test(code)) return null;
  const fichier = path.join(RACINE, 'seances', code, 'seance.md');
  if (!fs.existsSync(fichier)) return null;
  const { data, content } = matter(fs.readFileSync(fichier, 'utf8'));
  // Le bloc « Ce que vous saurez faire » est extrait pour être affiché dans son encadré.
  const sections = content.split(/^## /m);
  let objectifs: string | null = null;
  const reste: string[] = [];
  sections.forEach((s, i) => {
    if (i > 0 && /^Ce que vous saurez faire/i.test(s)) {
      objectifs = s.replace(/^Ce que vous saurez faire\s*/i, '').trim();
    } else reste.push(i === 0 ? s : '## ' + s);
  });
  const corps = reste.join('').replace(/^# .*$/m, '').replace(/<!--[\s\S]*?-->/g, '');
  return {
    meta: data as SeanceMeta,
    html: marked.parse(corps, { async: false }) as string,
    objectifsHtml: objectifs ? (marked.parse(objectifs, { async: false }) as string) : null,
  };
}

export function seancesDisponibles(): string[] {
  const dossier = path.join(RACINE, 'seances');
  try {
    return fs.readdirSync(dossier).filter((d) => CODE.test(d) && fs.existsSync(path.join(dossier, d, 'seance.md')));
  } catch {
    return [];
  }
}
