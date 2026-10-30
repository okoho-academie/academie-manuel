// Données d'exemple, utilisées tant que Supabase n'est pas configuré.
import type { Groupe, Personne, Regle, SeanceAcces, Jalon } from './acces';

export const MAINTENANT_DEMO = new Date('2026-11-16T09:00:00+01:00');

export const PERSONNE_DEMO: Personne & { prenom: string; groupe: string } = {
  id: 'demo-apprenant',
  prenom: 'Exemple',
  groupe: 'cohorte-1',
  terminees: ['M01-S1', 'M01-S2'],
  jalonsAcquis: [],
};

// Calendrier Cohorte 1 : ouverture le vendredi avant la séance du samedi.
const programme: [string, string][] = [
  ['M01-S1', '2026-11-06'], ['M01-S2', '2026-11-06'],
  ['M02-S1', '2026-11-13'], ['M02-S2', '2026-11-13'],
  ['M05-S1', '2026-11-20'], ['M03-S1', '2026-11-20'],
  ['M02-S3', '2026-11-27'], ['M03-S2', '2026-11-27'],
];
const reglesCohorte1: Regle[] = [
  ...programme.map(([c, d]) => ({ seanceCode: c, etat: 'programme' as const, date: d })),
  { seanceCode: 'M04-S1', etat: 'jalon', jalon: 'J1' },
  { seanceCode: 'M04-S2', etat: 'prerequis', prerequis: ['M04-S1'] },
];
const reglesAutonomie: Regle[] = [
  { seanceCode: 'M01-S1', etat: 'libre' }, { seanceCode: 'M01-S2', etat: 'libre' },
  { seanceCode: 'M02-S1', etat: 'libre' }, { seanceCode: 'M02-S2', etat: 'prerequis', prerequis: ['M02-S1'] },
  { seanceCode: 'M02-S3', etat: 'prerequis', prerequis: ['M02-S2'] },
];

export const GROUPES_DEMO: (Groupe & { nom: string })[] = [
  { id: 'cohorte-1', nom: 'Cohorte 1', regles: reglesCohorte1 },
  { id: 'autonomie', nom: 'Autonomie', regles: reglesAutonomie },
  { id: 'accompagne', nom: 'Accompagné', regles: [] },
];

/** Accès par défaut : Partie I libre (Parcours Démarrage), le reste verrouillé. */
export function seanceAcces(code: string, partie: string): SeanceAcces {
  return { code, acces_defaut: partie === 'I' ? 'libre' : 'verrouille' };
}

export const SEMAINE_DEMO = {
  semaine: 2,
  seance: { code: 'M02-S1', titre: "Les cinq éléments d'une bonne consigne" },
  devoir: { titre: 'Cinq tâches du quotidien résolues avec Claude', echeance: '2026-11-20' },
  live: { titre: 'Séance en direct · M05-S1', date: '2026-11-21', heure: '10:00', fuseau: 'Douala' },
  jalonActuel: 'J1' as Jalon,
};
