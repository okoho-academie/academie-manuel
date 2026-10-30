import Link from 'next/link';
import { Etat } from '@/components/Etat';
import { etatSeance } from '@/lib/acces';
import { GROUPES_DEMO, MAINTENANT_DEMO, PERSONNE_DEMO, seanceAcces } from '@/lib/demo';
import { lireStructure } from '@/lib/structure';

export const metadata = { title: 'Parcours' };

export default function Parcours() {
  const { parties } = lireStructure();
  const groupe = GROUPES_DEMO.find((g) => g.id === PERSONNE_DEMO.groupe) ?? null;
  return (
    <div className="conteneur">
      <div style={{ display: 'grid', gap: 'var(--space-2)' }}>
        <span className="label">Parcours Claude Pro</span>
        <h1>Tout le parcours, étape par étape</h1>
        <p>Les séances fermées restent visibles. Chaque carte indique quand et comment elle s'ouvre.</p>
      </div>
      {parties.map((p) => (
        <section key={p.num} className="partie" aria-labelledby={`partie-${p.num}`}>
          <div className="partie-tete">
            <div className="nb">{p.num}</div>
            <div>
              <span className="label">Partie {p.num}</span>
              <h2 id={`partie-${p.num}`}>{p.titre}</h2>
            </div>
          </div>
          {p.modules.map((m) => (
            <div key={m.code} style={{ display: 'grid', gap: 'var(--space-2)' }}>
              <span className="module-titre">{m.code} · {m.titre}</span>
              <div className="grille">
                {m.seances.map((s) => {
                  const r = etatSeance(seanceAcces(s.code, p.num), groupe, PERSONNE_DEMO, MAINTENANT_DEMO);
                  const ouverte = r.etat !== 'verrouillee';
                  const contenu = (
                    <>
                      <span className="seance-code">{s.code}</span>
                      <span className="seance-titre">{s.titre}</span>
                      <Etat r={r} />
                    </>
                  );
                  return ouverte ? (
                    <Link key={s.code} href={`/seance/${s.code}`} className="seance-carte">{contenu}</Link>
                  ) : (
                    <div key={s.code} className="seance-carte verrouillee" aria-disabled="true">{contenu}</div>
                  );
                })}
              </div>
            </div>
          ))}
        </section>
      ))}
    </div>
  );
}
