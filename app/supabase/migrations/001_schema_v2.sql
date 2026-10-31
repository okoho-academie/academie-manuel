-- OKOHO Académie · Migration v2
-- Passe du schéma initial (schema.sql) au modèle complet décrit dans HANDOFF_v1.md §3.
-- À appliquer dans l'éditeur SQL Supabase APRÈS schema.sql.

-- ─────────────────────────────────────────────
-- 1. Nouveaux types énumérés
-- ─────────────────────────────────────────────

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'role_cohorte') THEN
    CREATE TYPE role_cohorte AS ENUM ('administrateur', 'formateur', 'assistant', 'apprenant');
  END IF;
END $$;

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'statut_devoir') THEN
    CREATE TYPE statut_devoir AS ENUM ('brouillon', 'publie', 'archive');
  END IF;
END $$;

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'statut_evaluation') THEN
    CREATE TYPE statut_evaluation AS ENUM ('en_attente', 'en_cours', 'terminee');
  END IF;
END $$;

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'type_rendu') THEN
    CREATE TYPE type_rendu AS ENUM ('lien', 'fichier', 'texte', 'artefact');
  END IF;
END $$;

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'type_annonce') THEN
    CREATE TYPE type_annonce AS ENUM ('info', 'devoir', 'jalon', 'urgence');
  END IF;
END $$;

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'statut_notification') THEN
    CREATE TYPE statut_notification AS ENUM ('non_lue', 'lue', 'archivee');
  END IF;
END $$;

-- Étendre l'enum role_academie existant avec 'assistant'
DO $$ BEGIN
  ALTER TYPE role_academie ADD VALUE IF NOT EXISTS 'assistant';
END $$;

-- ─────────────────────────────────────────────
-- 2. Étendre profiles
-- ─────────────────────────────────────────────

ALTER TABLE profiles
  ADD COLUMN IF NOT EXISTS telephone     text,
  ADD COLUMN IF NOT EXISTS langue        text NOT NULL DEFAULT 'fr',
  ADD COLUMN IF NOT EXISTS notif_email   boolean NOT NULL DEFAULT true,
  ADD COLUMN IF NOT EXISTS notif_push    boolean NOT NULL DEFAULT true;

-- ─────────────────────────────────────────────
-- 3. organisations (nouvelle table)
-- ─────────────────────────────────────────────

CREATE TABLE organisations (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  nom         text NOT NULL,
  slug        text UNIQUE NOT NULL,
  logo_url    text,
  cree_le     timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE organisations ENABLE ROW LEVEL SECURITY;

-- ─────────────────────────────────────────────
-- 4. cohortes (renomme groupes + colonnes supplémentaires)
-- ─────────────────────────────────────────────

-- On crée cohortes avec toutes les colonnes ; membres pointera dessus.
CREATE TABLE cohortes (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organisation_id uuid REFERENCES organisations (id) ON DELETE SET NULL,
  nom             text NOT NULL,
  type            text NOT NULL DEFAULT 'cohorte',   -- cohorte | autonomie | accompagne | entreprise
  entreprise      text,
  jour            text,                              -- ex : 'samedi'
  heure           time,                              -- ex : '09:00'
  fuseau          text NOT NULL DEFAULT 'Africa/Douala',
  lien_visio      text,
  calendrier      jsonb,                             -- [{"date":"2026-11-07","seance":"S01"}, …]
  cree_le         timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE cohortes ENABLE ROW LEVEL SECURITY;

-- Migrer les données depuis groupes vers cohortes
INSERT INTO cohortes (id, nom, type, entreprise, cree_le)
SELECT id, nom, type, entreprise, cree_le FROM groupes
ON CONFLICT (id) DO NOTHING;

-- ─────────────────────────────────────────────
-- 5. membres : remplacer groupe_id → cohorte_id
-- ─────────────────────────────────────────────

-- Ajouter colonne cohorte_id et role_cohorte
ALTER TABLE membres
  ADD COLUMN IF NOT EXISTS cohorte_id    uuid REFERENCES cohortes (id) ON DELETE CASCADE,
  ADD COLUMN IF NOT EXISTS role_cohorte  role_cohorte NOT NULL DEFAULT 'apprenant';

-- Copier les valeurs depuis groupe_id
UPDATE membres SET cohorte_id = groupe_id WHERE cohorte_id IS NULL;

-- Copier les rôles
UPDATE membres SET role_cohorte = role_dans_groupe::text::role_cohorte
  WHERE role_dans_groupe::text IN ('administrateur','formateur','assistant','apprenant');

-- regles_acces : ajouter colonne cohorte_id
ALTER TABLE regles_acces
  ADD COLUMN IF NOT EXISTS cohorte_id uuid REFERENCES cohortes (id) ON DELETE CASCADE;

UPDATE regles_acces SET cohorte_id = groupe_id WHERE cohorte_id IS NULL;

-- ─────────────────────────────────────────────
-- 6. devoirs
-- ─────────────────────────────────────────────

CREATE TABLE devoirs (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  cohorte_id      uuid NOT NULL REFERENCES cohortes (id) ON DELETE CASCADE,
  seance_code     text NOT NULL,
  titre           text NOT NULL,
  consigne        text,
  statut          statut_devoir NOT NULL DEFAULT 'brouillon',
  date_limite     timestamptz,
  cree_par        uuid REFERENCES profiles (id),
  cree_le         timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE devoirs ENABLE ROW LEVEL SECURITY;

-- ─────────────────────────────────────────────
-- 7. rendus : étendre + colonnes v2
-- ─────────────────────────────────────────────

ALTER TABLE rendus
  ADD COLUMN IF NOT EXISTS devoir_id             uuid REFERENCES devoirs (id) ON DELETE SET NULL,
  ADD COLUMN IF NOT EXISTS storage_path          text,
  ADD COLUMN IF NOT EXISTS type_rendu            type_rendu NOT NULL DEFAULT 'lien',
  ADD COLUMN IF NOT EXISTS galerie_consentement  boolean NOT NULL DEFAULT false;

-- ─────────────────────────────────────────────
-- 8. evaluations
-- ─────────────────────────────────────────────

CREATE TABLE evaluations (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  rendu_id        uuid NOT NULL REFERENCES rendus (id) ON DELETE CASCADE,
  evaluateur_id   uuid NOT NULL REFERENCES profiles (id),
  statut          statut_evaluation NOT NULL DEFAULT 'en_attente',
  note            smallint CHECK (note BETWEEN 0 AND 100),
  commentaire     text,
  grille          jsonb,        -- critères détaillés
  cree_le         timestamptz NOT NULL DEFAULT now(),
  modifie_le      timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE evaluations ENABLE ROW LEVEL SECURITY;

-- ─────────────────────────────────────────────
-- 9. quiz_tentatives
-- ─────────────────────────────────────────────

CREATE TABLE quiz_tentatives (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  personne_id     uuid NOT NULL REFERENCES profiles (id) ON DELETE CASCADE,
  seance_code     text NOT NULL,
  cohorte_id      uuid REFERENCES cohortes (id) ON DELETE SET NULL,
  reponses        jsonb NOT NULL DEFAULT '{}',
  score           smallint,
  duree_secondes  integer,
  tentee_le       timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE quiz_tentatives ENABLE ROW LEVEL SECURITY;

-- ─────────────────────────────────────────────
-- 10. annonces
-- ─────────────────────────────────────────────

CREATE TABLE annonces (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  cohorte_id      uuid NOT NULL REFERENCES cohortes (id) ON DELETE CASCADE,
  auteur_id       uuid NOT NULL REFERENCES profiles (id),
  type            type_annonce NOT NULL DEFAULT 'info',
  titre           text NOT NULL,
  corps           text,
  publie_le       timestamptz,
  expire_le       timestamptz,
  cree_le         timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE annonces ENABLE ROW LEVEL SECURITY;

-- ─────────────────────────────────────────────
-- 11. questions / réponses
-- ─────────────────────────────────────────────

CREATE TABLE questions (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  cohorte_id      uuid NOT NULL REFERENCES cohortes (id) ON DELETE CASCADE,
  auteur_id       uuid NOT NULL REFERENCES profiles (id),
  seance_code     text,
  titre           text NOT NULL,
  corps           text,
  resolu          boolean NOT NULL DEFAULT false,
  cree_le         timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE questions ENABLE ROW LEVEL SECURITY;

CREATE TABLE reponses (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  question_id     uuid NOT NULL REFERENCES questions (id) ON DELETE CASCADE,
  auteur_id       uuid NOT NULL REFERENCES profiles (id),
  corps           text NOT NULL,
  acceptee        boolean NOT NULL DEFAULT false,
  cree_le         timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE reponses ENABLE ROW LEVEL SECURITY;

-- ─────────────────────────────────────────────
-- 12. brouillons_a_valider
-- ─────────────────────────────────────────────

CREATE TABLE brouillons_a_valider (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  cohorte_id      uuid NOT NULL REFERENCES cohortes (id) ON DELETE CASCADE,
  auteur_id       uuid NOT NULL REFERENCES profiles (id),
  table_cible     text NOT NULL,       -- nom de la table concernée
  objet_id        uuid,                -- identifiant de l'objet à valider
  donnees         jsonb NOT NULL,
  valide_par      uuid REFERENCES profiles (id),
  valide_le       timestamptz,
  rejete_le       timestamptz,
  motif_rejet     text,
  cree_le         timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE brouillons_a_valider ENABLE ROW LEVEL SECURITY;

-- ─────────────────────────────────────────────
-- 13. notifications + push_abonnements
-- ─────────────────────────────────────────────

CREATE TABLE notifications (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  destinataire_id uuid NOT NULL REFERENCES profiles (id) ON DELETE CASCADE,
  type            text NOT NULL,
  titre           text NOT NULL,
  corps           text,
  lien            text,
  statut          statut_notification NOT NULL DEFAULT 'non_lue',
  cree_le         timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;

CREATE TABLE push_abonnements (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  personne_id     uuid NOT NULL REFERENCES profiles (id) ON DELETE CASCADE,
  endpoint        text NOT NULL UNIQUE,
  cles            jsonb NOT NULL,     -- {p256dh, auth}
  agent           text,
  cree_le         timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE push_abonnements ENABLE ROW LEVEL SECURITY;

-- ─────────────────────────────────────────────
-- 14. jalons_conditions (complète jalons)
-- ─────────────────────────────────────────────

CREATE TABLE jalons_conditions (
  jalon           jalon_code NOT NULL,
  seance_code     text NOT NULL,
  niveau_min      smallint NOT NULL DEFAULT 1 CHECK (niveau_min BETWEEN 1 AND 4),
  PRIMARY KEY (jalon, seance_code)
);

ALTER TABLE jalons_conditions ENABLE ROW LEVEL SECURITY;

-- ─────────────────────────────────────────────
-- 15. attestations
-- ─────────────────────────────────────────────

CREATE TABLE attestations (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  personne_id     uuid NOT NULL REFERENCES profiles (id) ON DELETE CASCADE,
  cohorte_id      uuid REFERENCES cohortes (id) ON DELETE SET NULL,
  jalon           jalon_code,
  storage_path    text NOT NULL,     -- chemin dans Supabase Storage
  url_publique    text,
  emise_par       uuid REFERENCES profiles (id),
  emise_le        timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE attestations ENABLE ROW LEVEL SECURITY;

-- ─────────────────────────────────────────────
-- 16. journal (audit log)
-- ─────────────────────────────────────────────

CREATE TABLE journal (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  acteur_id       uuid REFERENCES profiles (id),
  action          text NOT NULL,
  table_cible     text,
  objet_id        uuid,
  details         jsonb,
  ip              inet,
  enregistre_le   timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE journal ENABLE ROW LEVEL SECURITY;

-- ─────────────────────────────────────────────
-- 17. Fonctions d'aide par cohorte
-- ─────────────────────────────────────────────

-- Renvoie le rôle de l'utilisateur courant dans une cohorte donnée
CREATE OR REPLACE FUNCTION mon_role_dans_cohorte(cohorte_id uuid)
  RETURNS role_cohorte
  LANGUAGE sql STABLE SECURITY DEFINER
  SET search_path = public
AS $$
  SELECT role_cohorte
  FROM membres
  WHERE membres.cohorte_id = mon_role_dans_cohorte.cohorte_id
    AND membres.personne_id = auth.uid()
  LIMIT 1
$$;

-- Vrai si l'utilisateur est formateur, assistant ou administrateur dans la cohorte
CREATE OR REPLACE FUNCTION est_equipe_cohorte(cohorte_id uuid)
  RETURNS boolean
  LANGUAGE sql STABLE SECURITY DEFINER
  SET search_path = public
AS $$
  SELECT COALESCE(
    mon_role_dans_cohorte(cohorte_id) IN ('administrateur', 'formateur', 'assistant'),
    false
  )
$$;

-- Vrai si l'utilisateur est administrateur (global)
CREATE OR REPLACE FUNCTION est_admin()
  RETURNS boolean
  LANGUAGE sql STABLE SECURITY DEFINER
  SET search_path = public
AS $$
  SELECT COALESCE(mon_role() = 'administrateur', false)
$$;

-- Vrai si l'utilisateur est formateur ou administrateur dans la cohorte
CREATE OR REPLACE FUNCTION est_formateur_ou_admin(cohorte_id uuid)
  RETURNS boolean
  LANGUAGE sql STABLE SECURITY DEFINER
  SET search_path = public
AS $$
  SELECT COALESCE(
    mon_role_dans_cohorte(cohorte_id) IN ('administrateur', 'formateur'),
    false
  )
$$;

-- ─────────────────────────────────────────────
-- 18. Politiques RLS — nouvelles tables
-- ─────────────────────────────────────────────

-- organisations
CREATE POLICY orga_lecture ON organisations FOR SELECT USING (est_admin() OR true);
CREATE POLICY orga_admin   ON organisations FOR ALL USING (est_admin()) WITH CHECK (est_admin());

-- cohortes
CREATE POLICY cohortes_lecture ON cohortes FOR SELECT
  USING (est_admin() OR EXISTS (
    SELECT 1 FROM membres m WHERE m.cohorte_id = cohortes.id AND m.personne_id = auth.uid()
  ));
CREATE POLICY cohortes_admin ON cohortes FOR ALL USING (est_admin()) WITH CHECK (est_admin());

-- devoirs : l'apprenant lit les devoirs de ses cohortes ; l'équipe gère
CREATE POLICY devoirs_lecture ON devoirs FOR SELECT
  USING (est_equipe_cohorte(cohorte_id) OR EXISTS (
    SELECT 1 FROM membres m WHERE m.cohorte_id = devoirs.cohorte_id AND m.personne_id = auth.uid()
  ));
CREATE POLICY devoirs_equipe ON devoirs FOR ALL
  USING (est_equipe_cohorte(cohorte_id)) WITH CHECK (est_equipe_cohorte(cohorte_id));

-- evaluations : l'apprenant lit ses évaluations ; l'équipe gère
CREATE POLICY evaluations_lecture ON evaluations FOR SELECT
  USING (est_admin() OR evaluateur_id = auth.uid() OR EXISTS (
    SELECT 1 FROM rendus r WHERE r.id = evaluations.rendu_id AND r.personne_id = auth.uid()
  ));
CREATE POLICY evaluations_equipe ON evaluations FOR ALL
  USING (est_admin()) WITH CHECK (est_admin());

-- quiz_tentatives : chacun lit les siennes ; l'équipe lit tout
CREATE POLICY quiz_lecture ON quiz_tentatives FOR SELECT
  USING (personne_id = auth.uid() OR est_equipe_cohorte(cohorte_id));
CREATE POLICY quiz_depot   ON quiz_tentatives FOR INSERT
  WITH CHECK (personne_id = auth.uid());

-- annonces : membres en lecture ; équipe en écriture
CREATE POLICY annonces_lecture ON annonces FOR SELECT
  USING (est_equipe_cohorte(cohorte_id) OR EXISTS (
    SELECT 1 FROM membres m WHERE m.cohorte_id = annonces.cohorte_id AND m.personne_id = auth.uid()
  ));
CREATE POLICY annonces_equipe ON annonces FOR ALL
  USING (est_equipe_cohorte(cohorte_id)) WITH CHECK (est_equipe_cohorte(cohorte_id));

-- questions / réponses : membres lisent ; auteur modifie le sien ; équipe gère
CREATE POLICY questions_lecture ON questions FOR SELECT
  USING (est_equipe_cohorte(cohorte_id) OR EXISTS (
    SELECT 1 FROM membres m WHERE m.cohorte_id = questions.cohorte_id AND m.personne_id = auth.uid()
  ));
CREATE POLICY questions_depot ON questions FOR INSERT
  WITH CHECK (auteur_id = auth.uid());
CREATE POLICY questions_equipe ON questions FOR ALL
  USING (est_equipe_cohorte(cohorte_id)) WITH CHECK (est_equipe_cohorte(cohorte_id));

CREATE POLICY reponses_lecture ON reponses FOR SELECT
  USING (EXISTS (
    SELECT 1 FROM questions q
    JOIN membres m ON m.cohorte_id = q.cohorte_id
    WHERE q.id = reponses.question_id AND m.personne_id = auth.uid()
  ) OR est_admin());
CREATE POLICY reponses_depot ON reponses FOR INSERT
  WITH CHECK (auteur_id = auth.uid());

-- brouillons_a_valider
CREATE POLICY brouillons_lecture ON brouillons_a_valider FOR SELECT
  USING (auteur_id = auth.uid() OR est_equipe_cohorte(cohorte_id));
CREATE POLICY brouillons_depot ON brouillons_a_valider FOR INSERT
  WITH CHECK (auteur_id = auth.uid());
CREATE POLICY brouillons_equipe ON brouillons_a_valider FOR UPDATE
  USING (est_equipe_cohorte(cohorte_id)) WITH CHECK (est_equipe_cohorte(cohorte_id));

-- notifications : chacun lit et gère les siennes
CREATE POLICY notifs_lecture ON notifications FOR SELECT
  USING (destinataire_id = auth.uid());
CREATE POLICY notifs_maj ON notifications FOR UPDATE
  USING (destinataire_id = auth.uid()) WITH CHECK (destinataire_id = auth.uid());
CREATE POLICY notifs_admin ON notifications FOR ALL
  USING (est_admin()) WITH CHECK (est_admin());

-- push_abonnements
CREATE POLICY push_lecture ON push_abonnements FOR SELECT
  USING (personne_id = auth.uid());
CREATE POLICY push_depot ON push_abonnements FOR INSERT
  WITH CHECK (personne_id = auth.uid());
CREATE POLICY push_suppression ON push_abonnements FOR DELETE
  USING (personne_id = auth.uid());

-- jalons_conditions : lecture publique, écriture admin
CREATE POLICY jalons_cond_lecture ON jalons_conditions FOR SELECT USING (true);
CREATE POLICY jalons_cond_admin ON jalons_conditions FOR ALL
  USING (est_admin()) WITH CHECK (est_admin());

-- attestations
CREATE POLICY attestations_lecture ON attestations FOR SELECT
  USING (personne_id = auth.uid() OR est_admin());
CREATE POLICY attestations_admin ON attestations FOR ALL
  USING (est_admin()) WITH CHECK (est_admin());

-- journal : lecture et écriture admin uniquement
CREATE POLICY journal_admin ON journal FOR ALL
  USING (est_admin()) WITH CHECK (est_admin());
