// Règles d'accès aux séances (Cockpit 07, section 8). Fonction pure, sans dépendance.

export type EtatRegle = 'libre' | 'verrouille' | 'programme' | 'prerequis' | 'jalon' | 'manuel';
export type Jalon = 'J1' | 'J2' | 'J3' | 'J4' | 'J5';

export interface SeanceAcces {
  code: string;
  acces_defaut?: EtatRegle;
  date?: string; // AAAA-MM-JJ, ouverture à 00:00 heure de Douala
  prerequis?: string[];
  jalon?: Jalon;
}
export interface Regle {
  seanceCode: string;
  groupeId?: string | null;
  personneId?: string | null; // règle individuelle, prioritaire
  etat: EtatRegle;
  date?: string;
  prerequis?: string[];
  jalon?: Jalon;
  ouvert?: boolean; // pour « manuel »
}
export interface Groupe {
  id: string;
  regles: Regle[];
}
export interface Personne {
  id: string;
  terminees: string[];
  jalonsAcquis: Jalon[];
}

export type EtatAffiche = 'terminee' | 'libre' | 'ouverte' | 'verrouillee';
export type Raison = 'date' | 'prerequis' | 'jalon' | 'formateur' | null;

export interface ResultatAcces {
  etat: EtatAffiche;
  raison: Raison;
  libelle: string; // toujours un mot, jamais la couleur seule
}

const FUSEAU_DOUALA = '+01:00';

export function formaterDate(date: string): string {
  const [a, m, j] = date.split('-');
  return `${j}.${m}.${a}`;
}

function ouvertureDate(date: string): Date {
  return new Date(`${date}T00:00:00${FUSEAU_DOUALA}`);
}

/** Choisit la règle applicable : personne > groupe > défaut de la séance. */
export function regleApplicable(seance: SeanceAcces, groupe: Groupe | null, personne: Personne | null): Regle {
  const regles = groupe?.regles.filter((r) => r.seanceCode === seance.code) ?? [];
  const individuelle = personne ? regles.find((r) => r.personneId === personne.id) : undefined;
  if (individuelle) return individuelle;
  const collective = regles.find((r) => !r.personneId);
  if (collective) return collective;
  return {
    seanceCode: seance.code,
    etat: seance.acces_defaut ?? 'verrouille',
    date: seance.date,
    prerequis: seance.prerequis,
    jalon: seance.jalon,
  };
}

export function etatSeance(
  seance: SeanceAcces,
  groupe: Groupe | null,
  personne: Personne | null,
  maintenant: Date,
): ResultatAcces {
  if (personne?.terminees.includes(seance.code)) {
    return { etat: 'terminee', raison: null, libelle: 'Terminée' };
  }
  const r = regleApplicable(seance, groupe, personne);
  switch (r.etat) {
    case 'libre':
      return { etat: 'libre', raison: null, libelle: 'Accès libre' };
    case 'verrouille':
      return { etat: 'verrouillee', raison: 'formateur', libelle: 'Ouverture par le formateur' };
    case 'manuel':
      return r.ouvert
        ? { etat: 'ouverte', raison: null, libelle: 'Ouverte' }
        : { etat: 'verrouillee', raison: 'formateur', libelle: 'Ouverture par le formateur' };
    case 'programme': {
      if (!r.date) return { etat: 'verrouillee', raison: 'formateur', libelle: 'Date à venir' };
      return maintenant >= ouvertureDate(r.date)
        ? { etat: 'ouverte', raison: null, libelle: 'Ouverte' }
        : { etat: 'verrouillee', raison: 'date', libelle: `Disponible le ${formaterDate(r.date)}` };
    }
    case 'prerequis': {
      const manquants = (r.prerequis ?? []).filter((c) => !personne?.terminees.includes(c));
      return manquants.length === 0
        ? { etat: 'ouverte', raison: null, libelle: 'Ouverte' }
        : { etat: 'verrouillee', raison: 'prerequis', libelle: `Après ${manquants.join(', ')}` };
    }
    case 'jalon': {
      if (!r.jalon) return { etat: 'verrouillee', raison: 'formateur', libelle: 'Ouverture par le formateur' };
      return personne?.jalonsAcquis.includes(r.jalon)
        ? { etat: 'ouverte', raison: null, libelle: 'Ouverte' }
        : { etat: 'verrouillee', raison: 'jalon', libelle: `Après le Jalon ${r.jalon}` };
    }
  }
}
