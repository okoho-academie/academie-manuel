import { test } from 'node:test';
import assert from 'node:assert/strict';
import { etatSeance, type Groupe, type Personne } from '../lib/acces.ts';

const awa: Personne = { id: 'awa', terminees: ['M01-S1'], jalonsAcquis: [] };
const g: Groupe = {
  id: 'cohorte-1',
  regles: [
    { seanceCode: 'M02-S1', etat: 'programme', date: '2026-11-13' },
    { seanceCode: 'M02-S3', etat: 'prerequis', prerequis: ['M02-S2'] },
    { seanceCode: 'M04-S1', etat: 'jalon', jalon: 'J1' },
    { seanceCode: 'M05-S1', etat: 'manuel', ouvert: false },
    { seanceCode: 'M05-S1', personneId: 'awa', etat: 'manuel', ouvert: true },
  ],
};
const avant = new Date('2026-11-12T22:59:00Z'); // 23:59 à Douala le 12.11.
const apres = new Date('2026-11-12T23:00:00Z'); // 00:00 à Douala le 13.11.

test('terminée prime sur tout', () => {
  assert.equal(etatSeance({ code: 'M01-S1' }, g, awa, avant).etat, 'terminee');
});
test('libre par défaut de la séance', () => {
  const r = etatSeance({ code: 'M01-S2', acces_defaut: 'libre' }, g, awa, avant);
  assert.equal(r.etat, 'libre');
});
test('programmé : fermé avant, ouvert à minuit heure de Douala', () => {
  const r1 = etatSeance({ code: 'M02-S1' }, g, awa, avant);
  assert.equal(r1.etat, 'verrouillee');
  assert.equal(r1.libelle, 'Disponible le 13.11.2026');
  assert.equal(etatSeance({ code: 'M02-S1' }, g, awa, apres).etat, 'ouverte');
});
test('prérequis manquant puis rempli', () => {
  assert.equal(etatSeance({ code: 'M02-S3' }, g, awa, apres).libelle, 'Après M02-S2');
  const awa2 = { ...awa, terminees: [...awa.terminees, 'M02-S2'] };
  assert.equal(etatSeance({ code: 'M02-S3' }, g, awa2, apres).etat, 'ouverte');
});
test('jalon', () => {
  assert.equal(etatSeance({ code: 'M04-S1' }, g, awa, apres).libelle, 'Après le Jalon J1');
  assert.equal(etatSeance({ code: 'M04-S1' }, g, { ...awa, jalonsAcquis: ['J1'] }, apres).etat, 'ouverte');
});
test('règle individuelle prioritaire sur la règle du groupe', () => {
  assert.equal(etatSeance({ code: 'M05-S1' }, g, awa, apres).etat, 'ouverte');
  const autre: Personne = { id: 'paul', terminees: [], jalonsAcquis: [] };
  assert.equal(etatSeance({ code: 'M05-S1' }, g, autre, apres).etat, 'verrouillee');
});
test('sans règle ni défaut : verrouillée avec un mot', () => {
  const r = etatSeance({ code: 'M18-S4' }, g, awa, apres);
  assert.equal(r.etat, 'verrouillee');
  assert.ok(r.libelle.length > 0);
});
