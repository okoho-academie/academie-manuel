-- OKOHO Académie · schéma Supabase (Postgres). À exécuter dans l'éditeur SQL du projet Supabase.
-- Rôles : administrateur, formateur, apprenant, responsable_entreprise.

create type role_academie as enum ('administrateur', 'formateur', 'apprenant', 'responsable_entreprise');
create type etat_regle as enum ('libre', 'verrouille', 'programme', 'prerequis', 'jalon', 'manuel');
create type jalon_code as enum ('J1', 'J2', 'J3', 'J4', 'J5');
create type statut_rendu as enum ('depose', 'en_correction', 'corrige');

create table profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  prenom text not null,
  nom text,
  role role_academie not null default 'apprenant',
  entreprise text,                       -- pour responsable_entreprise et ses membres
  cree_le timestamptz not null default now()
);

create table groupes (
  id uuid primary key default gen_random_uuid(),
  nom text not null,                     -- Cohorte 1, Autonomie, Accompagné, Entreprise X
  type text not null default 'cohorte',  -- cohorte | autonomie | accompagne | entreprise
  entreprise text,
  cree_le timestamptz not null default now()
);

create table membres (
  groupe_id uuid not null references groupes (id) on delete cascade,
  personne_id uuid not null references profiles (id) on delete cascade,
  role_dans_groupe role_academie not null default 'apprenant',
  primary key (groupe_id, personne_id)
);

create table regles_acces (
  id uuid primary key default gen_random_uuid(),
  seance_code text not null check (seance_code ~ '^M[0-9]{2}-S[0-9]$'),
  groupe_id uuid references groupes (id) on delete cascade,
  personne_id uuid references profiles (id) on delete cascade,  -- règle individuelle, prioritaire
  etat etat_regle not null,
  date date,                             -- pour « programme » (ouverture 00:00 heure de Douala)
  prerequis text[] not null default '{}',
  jalon jalon_code,
  ouvert boolean not null default false, -- pour « manuel »
  modifie_par uuid references profiles (id),
  modifie_le timestamptz not null default now(),
  check (groupe_id is not null or personne_id is not null)
);
create unique index regles_unique on regles_acces (seance_code, coalesce(groupe_id, '00000000-0000-0000-0000-000000000000'), coalesce(personne_id, '00000000-0000-0000-0000-000000000000'));

create table progression (
  personne_id uuid not null references profiles (id) on delete cascade,
  seance_code text not null,
  niveau smallint check (niveau between 1 and 4),
  quiz_score smallint,
  terminee_le timestamptz,
  primary key (personne_id, seance_code)
);

create table rendus (
  id uuid primary key default gen_random_uuid(),
  personne_id uuid not null references profiles (id) on delete cascade,
  seance_code text not null,
  lien text,                              -- lien vers le livrable (Drive, artefact, site)
  prompts text,
  reflexion text,
  statut statut_rendu not null default 'depose',
  retour text,                            -- Point fort · À améliorer · Prochaine étape
  niveau smallint check (niveau between 1 and 4),
  corrige_par uuid references profiles (id),
  depose_le timestamptz not null default now()
);

create table jalons (
  personne_id uuid not null references profiles (id) on delete cascade,
  jalon jalon_code not null,
  valide_par uuid references profiles (id),
  valide_le timestamptz not null default now(),
  attestation_url text,
  primary key (personne_id, jalon)
);

-- Fonctions d'aide pour les règles de sécurité
create or replace function mon_role() returns role_academie language sql stable security definer set search_path = public as
$$ select role from profiles where id = auth.uid() $$;

create or replace function est_equipe() returns boolean language sql stable security definer set search_path = public as
$$ select coalesce(mon_role() in ('administrateur', 'formateur'), false) $$;

create or replace function meme_entreprise(cible uuid) returns boolean language sql stable security definer set search_path = public as
$$ select exists (
     select 1 from profiles moi join profiles autre on autre.entreprise = moi.entreprise
     where moi.id = auth.uid() and moi.role = 'responsable_entreprise' and autre.id = cible and moi.entreprise is not null) $$;

alter table profiles enable row level security;
alter table groupes enable row level security;
alter table membres enable row level security;
alter table regles_acces enable row level security;
alter table progression enable row level security;
alter table rendus enable row level security;
alter table jalons enable row level security;

-- profiles : chacun se voit ; l'équipe voit tout ; le responsable voit son entreprise ; seul l'administrateur change les rôles.
create policy profils_lecture on profiles for select using (id = auth.uid() or est_equipe() or meme_entreprise(id));
create policy profils_maj_soi on profiles for update using (id = auth.uid()) with check (id = auth.uid() and role = mon_role());
create policy profils_admin on profiles for all using (mon_role() = 'administrateur') with check (mon_role() = 'administrateur');

-- groupes et membres : lecture par les membres, gestion par l'équipe.
create policy groupes_lecture on groupes for select using (est_equipe() or exists (select 1 from membres m where m.groupe_id = id and m.personne_id = auth.uid()));
create policy groupes_equipe on groupes for all using (est_equipe()) with check (est_equipe());
create policy membres_lecture on membres for select using (personne_id = auth.uid() or est_equipe());
create policy membres_equipe on membres for all using (est_equipe()) with check (est_equipe());

-- règles d'accès : l'apprenant lit celles de ses groupes et les siennes ; l'équipe les gère.
create policy regles_lecture on regles_acces for select using (
  est_equipe() or personne_id = auth.uid()
  or exists (select 1 from membres m where m.groupe_id = regles_acces.groupe_id and m.personne_id = auth.uid()));
create policy regles_equipe on regles_acces for all using (est_equipe()) with check (est_equipe());

-- progression : l'apprenant lit la sienne ; l'équipe écrit ; le responsable lit son entreprise.
create policy progression_lecture on progression for select using (personne_id = auth.uid() or est_equipe() or meme_entreprise(personne_id));
create policy progression_equipe on progression for all using (est_equipe()) with check (est_equipe());

-- rendus : l'apprenant dépose et lit les siens ; l'équipe corrige.
create policy rendus_lecture on rendus for select using (personne_id = auth.uid() or est_equipe() or meme_entreprise(personne_id));
create policy rendus_depot on rendus for insert with check (personne_id = auth.uid() and statut = 'depose');
create policy rendus_equipe on rendus for update using (est_equipe()) with check (est_equipe());

-- jalons : validés par l'équipe uniquement.
create policy jalons_lecture on jalons for select using (personne_id = auth.uid() or est_equipe() or meme_entreprise(personne_id));
create policy jalons_equipe on jalons for all using (est_equipe()) with check (est_equipe());
