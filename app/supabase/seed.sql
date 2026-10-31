-- OKOHO Académie · Données de test (seed.sql)
-- Utilisé pour les tests L1. Aucune donnée personnelle réelle.
-- Adresses : *@example.com uniquement.

-- ─────────────────────────────────────────────
-- Nettoyage (ordre inverse des dépendances)
-- ─────────────────────────────────────────────

TRUNCATE TABLE
  journal, attestations, jalons_conditions, push_abonnements, notifications,
  brouillons_a_valider, reponses, questions, annonces, quiz_tentatives,
  evaluations, rendus, devoirs, regles_acces, jalons, progression,
  membres, cohortes, profiles, organisations
CASCADE;

-- ─────────────────────────────────────────────
-- Organisation
-- ─────────────────────────────────────────────

INSERT INTO organisations (id, nom, slug) VALUES
  ('00000000-0000-0000-0000-000000000001', 'OKOHO Consulting GmbH', 'okoho');

-- ─────────────────────────────────────────────
-- Profiles (utilisateurs de test)
-- Les UUID doivent correspondre à des entrées dans auth.users.
-- En local (Supabase CLI) : créer les users via la CLI puis copier les UUID.
-- Pour les tests automatisés, ces UUID sont des valeurs fictives cohérentes.
-- ─────────────────────────────────────────────

-- Admin
INSERT INTO profiles (id, prenom, nom, role, langue) VALUES
  ('10000000-0000-0000-0000-000000000001', 'Admin', 'Test', 'administrateur', 'fr');

-- Formateur
INSERT INTO profiles (id, prenom, nom, role, langue) VALUES
  ('10000000-0000-0000-0000-000000000002', 'Formateur', 'Test', 'formateur', 'fr');

-- Apprenants
INSERT INTO profiles (id, prenom, nom, role, langue) VALUES
  ('10000000-0000-0000-0000-000000000003', 'Apprenant', 'Alpha', 'apprenant', 'fr'),
  ('10000000-0000-0000-0000-000000000004', 'Apprenant', 'Bêta',  'apprenant', 'fr');

-- ─────────────────────────────────────────────
-- Cohorte 1
-- ─────────────────────────────────────────────

INSERT INTO cohortes (id, organisation_id, nom, type, jour, heure, fuseau) VALUES
  (
    '20000000-0000-0000-0000-000000000001',
    '00000000-0000-0000-0000-000000000001',
    'OKOHO Parcours Claude Pro · Cohorte 1',
    'cohorte',
    'samedi',
    '09:00',
    'Africa/Douala'
  );

-- ─────────────────────────────────────────────
-- Membres de la cohorte 1
-- ─────────────────────────────────────────────

INSERT INTO membres (groupe_id, cohorte_id, personne_id, role_dans_groupe, role_cohorte) VALUES
  ('20000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001',
   '10000000-0000-0000-0000-000000000001', 'administrateur', 'administrateur'),
  ('20000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001',
   '10000000-0000-0000-0000-000000000002', 'formateur', 'formateur'),
  ('20000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001',
   '10000000-0000-0000-0000-000000000003', 'apprenant', 'apprenant'),
  ('20000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001',
   '10000000-0000-0000-0000-000000000004', 'apprenant', 'apprenant');

-- ─────────────────────────────────────────────
-- Règles d'accès
-- S00 : libre pour toute la cohorte
-- S01 : programmé au 2026-11-06 (vendredi avant la première séance en direct)
-- ─────────────────────────────────────────────

INSERT INTO regles_acces (seance_code, groupe_id, cohorte_id, etat, prerequis) VALUES
  ('M01-S0', '20000000-0000-0000-0000-000000000001',
   '20000000-0000-0000-0000-000000000001', 'libre', '{}');

INSERT INTO regles_acces (seance_code, groupe_id, cohorte_id, etat, date, prerequis) VALUES
  ('M01-S1', '20000000-0000-0000-0000-000000000001',
   '20000000-0000-0000-0000-000000000001', 'programme', '2026-11-06', '{}');

-- ─────────────────────────────────────────────
-- Conditions de jalon J1 (exemple)
-- ─────────────────────────────────────────────

INSERT INTO jalons_conditions (jalon, seance_code, niveau_min) VALUES
  ('J1', 'M01-S0', 2),
  ('J1', 'M01-S1', 2),
  ('J1', 'M01-S2', 2);
