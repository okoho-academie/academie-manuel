// OKOHO Académie · Types TypeScript v2
// Généré pour correspondre au schéma Supabase après migration 001_schema_v2.sql

// ─────────────────────────────────────────────
// Enums
// ─────────────────────────────────────────────

export type RoleAcademie = 'administrateur' | 'formateur' | 'assistant' | 'apprenant' | 'responsable_entreprise';
export type RoleCohorte  = 'administrateur' | 'formateur' | 'assistant' | 'apprenant';
export type EtatRegle    = 'libre' | 'verrouille' | 'programme' | 'prerequis' | 'jalon' | 'manuel';
export type JalonCode    = 'J1' | 'J2' | 'J3' | 'J4' | 'J5';
export type StatutRendu  = 'depose' | 'en_correction' | 'corrige';
export type StatutDevoir = 'brouillon' | 'publie' | 'archive';
export type StatutEvaluation = 'en_attente' | 'en_cours' | 'terminee';
export type TypeRendu    = 'lien' | 'fichier' | 'texte' | 'artefact';
export type TypeAnnonce  = 'info' | 'devoir' | 'jalon' | 'urgence';
export type StatutNotification = 'non_lue' | 'lue' | 'archivee';

// ─────────────────────────────────────────────
// Type Database (Supabase générique)
// ─────────────────────────────────────────────

export type Database = {
  public: {
    Tables: {
      organisations: {
        Row: {
          id: string;
          nom: string;
          slug: string;
          logo_url: string | null;
          cree_le: string;
        };
        Insert: Omit<Database['public']['Tables']['organisations']['Row'], 'id' | 'cree_le'> & {
          id?: string;
          cree_le?: string;
        };
        Update: Partial<Database['public']['Tables']['organisations']['Insert']>;
      };
      cohortes: {
        Row: {
          id: string;
          organisation_id: string | null;
          nom: string;
          type: string;
          entreprise: string | null;
          jour: string | null;
          heure: string | null;
          fuseau: string;
          lien_visio: string | null;
          calendrier: Record<string, unknown>[] | null;
          cree_le: string;
        };
        Insert: Omit<Database['public']['Tables']['cohortes']['Row'], 'id' | 'cree_le'> & {
          id?: string;
          cree_le?: string;
        };
        Update: Partial<Database['public']['Tables']['cohortes']['Insert']>;
      };
      profiles: {
        Row: {
          id: string;
          prenom: string;
          nom: string | null;
          role: RoleAcademie;
          entreprise: string | null;
          telephone: string | null;
          langue: string;
          notif_email: boolean;
          notif_push: boolean;
          cree_le: string;
        };
        Insert: Omit<Database['public']['Tables']['profiles']['Row'], 'cree_le'> & {
          cree_le?: string;
        };
        Update: Partial<Database['public']['Tables']['profiles']['Insert']>;
      };
      membres: {
        Row: {
          groupe_id: string;
          cohorte_id: string | null;
          personne_id: string;
          role_dans_groupe: RoleAcademie;
          role_cohorte: RoleCohorte;
        };
        Insert: Database['public']['Tables']['membres']['Row'];
        Update: Partial<Database['public']['Tables']['membres']['Row']>;
      };
      regles_acces: {
        Row: {
          id: string;
          seance_code: string;
          groupe_id: string | null;
          cohorte_id: string | null;
          personne_id: string | null;
          etat: EtatRegle;
          date: string | null;
          prerequis: string[];
          jalon: JalonCode | null;
          ouvert: boolean;
          modifie_par: string | null;
          modifie_le: string;
        };
        Insert: Omit<Database['public']['Tables']['regles_acces']['Row'], 'id' | 'modifie_le'> & {
          id?: string;
          modifie_le?: string;
        };
        Update: Partial<Database['public']['Tables']['regles_acces']['Insert']>;
      };
      devoirs: {
        Row: {
          id: string;
          cohorte_id: string;
          seance_code: string;
          titre: string;
          consigne: string | null;
          statut: StatutDevoir;
          date_limite: string | null;
          cree_par: string | null;
          cree_le: string;
        };
        Insert: Omit<Database['public']['Tables']['devoirs']['Row'], 'id' | 'cree_le'> & {
          id?: string;
          cree_le?: string;
        };
        Update: Partial<Database['public']['Tables']['devoirs']['Insert']>;
      };
      rendus: {
        Row: {
          id: string;
          personne_id: string;
          seance_code: string;
          devoir_id: string | null;
          lien: string | null;
          prompts: string | null;
          reflexion: string | null;
          statut: StatutRendu;
          retour: string | null;
          niveau: number | null;
          corrige_par: string | null;
          storage_path: string | null;
          type_rendu: TypeRendu;
          galerie_consentement: boolean;
          depose_le: string;
        };
        Insert: Omit<Database['public']['Tables']['rendus']['Row'], 'id' | 'depose_le'> & {
          id?: string;
          depose_le?: string;
        };
        Update: Partial<Database['public']['Tables']['rendus']['Insert']>;
      };
      evaluations: {
        Row: {
          id: string;
          rendu_id: string;
          evaluateur_id: string;
          statut: StatutEvaluation;
          note: number | null;
          commentaire: string | null;
          grille: Record<string, unknown> | null;
          cree_le: string;
          modifie_le: string;
        };
        Insert: Omit<Database['public']['Tables']['evaluations']['Row'], 'id' | 'cree_le' | 'modifie_le'> & {
          id?: string;
          cree_le?: string;
          modifie_le?: string;
        };
        Update: Partial<Database['public']['Tables']['evaluations']['Insert']>;
      };
      quiz_tentatives: {
        Row: {
          id: string;
          personne_id: string;
          seance_code: string;
          cohorte_id: string | null;
          reponses: Record<string, unknown>;
          score: number | null;
          duree_secondes: number | null;
          tentee_le: string;
        };
        Insert: Omit<Database['public']['Tables']['quiz_tentatives']['Row'], 'id' | 'tentee_le'> & {
          id?: string;
          tentee_le?: string;
        };
        Update: Partial<Database['public']['Tables']['quiz_tentatives']['Insert']>;
      };
      annonces: {
        Row: {
          id: string;
          cohorte_id: string;
          auteur_id: string;
          type: TypeAnnonce;
          titre: string;
          corps: string | null;
          publie_le: string | null;
          expire_le: string | null;
          cree_le: string;
        };
        Insert: Omit<Database['public']['Tables']['annonces']['Row'], 'id' | 'cree_le'> & {
          id?: string;
          cree_le?: string;
        };
        Update: Partial<Database['public']['Tables']['annonces']['Insert']>;
      };
      questions: {
        Row: {
          id: string;
          cohorte_id: string;
          auteur_id: string;
          seance_code: string | null;
          titre: string;
          corps: string | null;
          resolu: boolean;
          cree_le: string;
        };
        Insert: Omit<Database['public']['Tables']['questions']['Row'], 'id' | 'cree_le'> & {
          id?: string;
          cree_le?: string;
        };
        Update: Partial<Database['public']['Tables']['questions']['Insert']>;
      };
      reponses: {
        Row: {
          id: string;
          question_id: string;
          auteur_id: string;
          corps: string;
          acceptee: boolean;
          cree_le: string;
        };
        Insert: Omit<Database['public']['Tables']['reponses']['Row'], 'id' | 'cree_le'> & {
          id?: string;
          cree_le?: string;
        };
        Update: Partial<Database['public']['Tables']['reponses']['Insert']>;
      };
      brouillons_a_valider: {
        Row: {
          id: string;
          cohorte_id: string;
          auteur_id: string;
          table_cible: string;
          objet_id: string | null;
          donnees: Record<string, unknown>;
          valide_par: string | null;
          valide_le: string | null;
          rejete_le: string | null;
          motif_rejet: string | null;
          cree_le: string;
        };
        Insert: Omit<Database['public']['Tables']['brouillons_a_valider']['Row'], 'id' | 'cree_le'> & {
          id?: string;
          cree_le?: string;
        };
        Update: Partial<Database['public']['Tables']['brouillons_a_valider']['Insert']>;
      };
      notifications: {
        Row: {
          id: string;
          destinataire_id: string;
          type: string;
          titre: string;
          corps: string | null;
          lien: string | null;
          statut: StatutNotification;
          cree_le: string;
        };
        Insert: Omit<Database['public']['Tables']['notifications']['Row'], 'id' | 'cree_le'> & {
          id?: string;
          cree_le?: string;
        };
        Update: Partial<Database['public']['Tables']['notifications']['Insert']>;
      };
      push_abonnements: {
        Row: {
          id: string;
          personne_id: string;
          endpoint: string;
          cles: { p256dh: string; auth: string };
          agent: string | null;
          cree_le: string;
        };
        Insert: Omit<Database['public']['Tables']['push_abonnements']['Row'], 'id' | 'cree_le'> & {
          id?: string;
          cree_le?: string;
        };
        Update: Partial<Database['public']['Tables']['push_abonnements']['Insert']>;
      };
      jalons: {
        Row: {
          personne_id: string;
          jalon: JalonCode;
          valide_par: string | null;
          valide_le: string;
          attestation_url: string | null;
        };
        Insert: Database['public']['Tables']['jalons']['Row'];
        Update: Partial<Database['public']['Tables']['jalons']['Row']>;
      };
      jalons_conditions: {
        Row: {
          jalon: JalonCode;
          seance_code: string;
          niveau_min: number;
        };
        Insert: Database['public']['Tables']['jalons_conditions']['Row'];
        Update: Partial<Database['public']['Tables']['jalons_conditions']['Row']>;
      };
      attestations: {
        Row: {
          id: string;
          personne_id: string;
          cohorte_id: string | null;
          jalon: JalonCode | null;
          storage_path: string;
          url_publique: string | null;
          emise_par: string | null;
          emise_le: string;
        };
        Insert: Omit<Database['public']['Tables']['attestations']['Row'], 'id' | 'emise_le'> & {
          id?: string;
          emise_le?: string;
        };
        Update: Partial<Database['public']['Tables']['attestations']['Insert']>;
      };
      progression: {
        Row: {
          personne_id: string;
          seance_code: string;
          niveau: number | null;
          quiz_score: number | null;
          terminee_le: string | null;
        };
        Insert: Database['public']['Tables']['progression']['Row'];
        Update: Partial<Database['public']['Tables']['progression']['Row']>;
      };
      journal: {
        Row: {
          id: string;
          acteur_id: string | null;
          action: string;
          table_cible: string | null;
          objet_id: string | null;
          details: Record<string, unknown> | null;
          ip: string | null;
          enregistre_le: string;
        };
        Insert: Omit<Database['public']['Tables']['journal']['Row'], 'id' | 'enregistre_le'> & {
          id?: string;
          enregistre_le?: string;
        };
        Update: Partial<Database['public']['Tables']['journal']['Insert']>;
      };
    };
    Functions: {
      mon_role: { Args: Record<never, never>; Returns: RoleAcademie };
      est_equipe: { Args: Record<never, never>; Returns: boolean };
      est_admin: { Args: Record<never, never>; Returns: boolean };
      mon_role_dans_cohorte: { Args: { cohorte_id: string }; Returns: RoleCohorte | null };
      est_equipe_cohorte: { Args: { cohorte_id: string }; Returns: boolean };
      est_formateur_ou_admin: { Args: { cohorte_id: string }; Returns: boolean };
    };
  };
};

// ─────────────────────────────────────────────
// Types domaine (raccourcis pratiques)
// ─────────────────────────────────────────────

export type Organisation = Database['public']['Tables']['organisations']['Row'];
export type Profile      = Database['public']['Tables']['profiles']['Row'];
export type Membre       = Database['public']['Tables']['membres']['Row'];
export type RegleAcces   = Database['public']['Tables']['regles_acces']['Row'];
export type Progression  = Database['public']['Tables']['progression']['Row'];
export type Jalon        = Database['public']['Tables']['jalons']['Row'];

export type Cohorte = Database['public']['Tables']['cohortes']['Row'] & {
  /** Membres chargés en option via jointure */
  membres?: Membre[];
};

export type Devoir = Database['public']['Tables']['devoirs']['Row'] & {
  /** Rendus associés (optionnel, via jointure) */
  rendus?: Rendu[];
};

export type Rendu = Database['public']['Tables']['rendus']['Row'] & {
  /** Évaluations associées (optionnel, via jointure) */
  evaluations?: Evaluation[];
};

export type Evaluation = Database['public']['Tables']['evaluations']['Row'];

export type QuizTentative = Database['public']['Tables']['quiz_tentatives']['Row'];

export type Annonce = Database['public']['Tables']['annonces']['Row'];

export type Question = Database['public']['Tables']['questions']['Row'] & {
  /** Réponses associées (optionnel, via jointure) */
  reponses?: Reponse[];
};

export type Reponse = Database['public']['Tables']['reponses']['Row'];

export type Attestation = Database['public']['Tables']['attestations']['Row'];

export type Notification = Database['public']['Tables']['notifications']['Row'];

// ─────────────────────────────────────────────
// Helpers
// ─────────────────────────────────────────────

/** Vrai si le rôle permet de gérer la cohorte */
export function estEquipe(role: RoleCohorte): boolean {
  return role === 'administrateur' || role === 'formateur' || role === 'assistant';
}

/** Vrai si le rôle permet de valider les rendus */
export function estFormateurOuAdmin(role: RoleCohorte): boolean {
  return role === 'administrateur' || role === 'formateur';
}
