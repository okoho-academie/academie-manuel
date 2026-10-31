import { Download, QrCode } from 'lucide-react';
import { PERSONNE_DEMO } from '@/lib/demo';

export const metadata = { title: 'Mon portfolio' };

// Types locaux
interface Rendu {
  seanceCode: string;
  seanceTitre: string;
  statut: 'déposé' | 'en correction' | 'corrigé';
  niveau?: 1 | 2 | 3 | 4; // niveau d'évaluation (si corrigé)
  dateDepot: string; // AAAA-MM-JJ
}

interface AttestationJalon {
  code: string;
  titre: string;
  dateValidation: string; // AAAA-MM-JJ
  downloadUrl: string;
  qrUrl: string;
}

// Données de démonstration
const RENDUS_DEMO: Rendu[] = [
  {
    seanceCode: 'M01-S1',
    seanceTitre: 'Prendre en main Claude',
    statut: 'corrigé',
    niveau: 3,
    dateDepot: '2026-11-08',
  },
  {
    seanceCode: 'M01-S2',
    seanceTitre: 'Écrire une consigne claire',
    statut: 'corrigé',
    niveau: 2,
    dateDepot: '2026-11-09',
  },
  {
    seanceCode: 'M02-S1',
    seanceTitre: "Les cinq éléments d'une bonne consigne",
    statut: 'en correction',
    dateDepot: '2026-11-15',
  },
  {
    seanceCode: 'M02-S2',
    seanceTitre: 'Améliorer un texte professionnel',
    statut: 'déposé',
    dateDepot: '2026-11-21',
  },
];

const ATTESTATIONS_DEMO: AttestationJalon[] = [
  {
    code: 'J1',
    titre: 'Communicant autonome avec Claude',
    dateValidation: '2026-11-22',
    downloadUrl: '/attestations/J1-demo.pdf',
    qrUrl: 'https://academie.okoho.de/verifier/J1-demo',
  },
];

// Regrouper les rendus par séance
function regrouperParSeance(rendus: Rendu[]): Map<string, Rendu[]> {
  const map = new Map<string, Rendu[]>();
  for (const r of rendus) {
    const cle = `${r.seanceCode}||${r.seanceTitre}`;
    if (!map.has(cle)) map.set(cle, []);
    map.get(cle)!.push(r);
  }
  return map;
}

function badgeStatut(statut: Rendu['statut'], niveau?: number) {
  if (statut === 'corrigé') {
    return (
      <span
        style={{
          background: '#D1FAE5',
          color: '#065F46',
          borderRadius: '999px',
          padding: '2px 10px',
          fontSize: '0.75rem',
          fontWeight: 600,
        }}
      >
        Corrigé · Niveau {niveau}/4
      </span>
    );
  }
  if (statut === 'en correction') {
    return (
      <span
        style={{
          background: '#FEF3C7',
          color: '#92400E',
          borderRadius: '999px',
          padding: '2px 10px',
          fontSize: '0.75rem',
          fontWeight: 600,
        }}
      >
        En correction
      </span>
    );
  }
  return (
    <span
      style={{
        background: '#F3F4F6',
        color: '#374151',
        borderRadius: '999px',
        padding: '2px 10px',
        fontSize: '0.75rem',
        fontWeight: 600,
      }}
    >
      Déposé
    </span>
  );
}

export default function Portfolio() {
  const personne = PERSONNE_DEMO;
  const rendus = RENDUS_DEMO;
  const attestations = ATTESTATIONS_DEMO;
  const groupes = regrouperParSeance(rendus);

  return (
    <div className="conteneur">
      <div style={{ display: 'grid', gap: 'var(--space-3)', marginBottom: 'var(--space-4)' }}>
        <span className="label">Portfolio · {personne.prenom}</span>
        <h1>Mon portfolio</h1>
        <p style={{ color: 'var(--gris-fonce, #6B7280)' }}>
          Retrouvez ici tous vos rendus et vos attestations de compétences validées.
        </p>
      </div>

      {/* Section attestations */}
      {attestations.length > 0 && (
        <section style={{ marginBottom: 'var(--space-5)' }}>
          <h2 style={{ marginBottom: 'var(--space-3)' }}>Attestations de compétences</h2>
          <div style={{ display: 'grid', gap: 'var(--space-3)' }}>
            {attestations.map((att) => (
              <div
                key={att.code}
                className="carte"
                style={{
                  background: 'var(--academie-tint, #FFF4E8)',
                  borderLeft: '4px solid var(--orange)',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: 'var(--space-2)' }}>
                  <div>
                    <span className="label label-orange">{att.code}</span>
                    <h3 style={{ marginTop: 'var(--space-1)' }}>{att.titre}</h3>
                    <p style={{ fontSize: '0.85rem', color: 'var(--gris-fonce, #6B7280)', marginTop: 4 }}>
                      Validé le{' '}
                      {new Date(att.dateValidation).toLocaleDateString('fr-FR', {
                        day: 'numeric',
                        month: 'long',
                        year: 'numeric',
                      })}
                    </p>
                  </div>
                  <div style={{ display: 'flex', gap: 'var(--space-2)', alignItems: 'center' }}>
                    <a
                      href={att.downloadUrl}
                      className="bouton bouton-secondaire"
                      style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: '0.85rem' }}
                      download
                    >
                      <Download size={15} aria-hidden="true" />
                      Télécharger le PDF
                    </a>
                    <a
                      href={att.qrUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bouton bouton-secondaire"
                      style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: '0.85rem' }}
                      title="Vérifier en ligne"
                    >
                      <QrCode size={15} aria-hidden="true" />
                      Vérifier
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Section rendus */}
      <section>
        <h2 style={{ marginBottom: 'var(--space-3)' }}>Mes rendus</h2>
        {rendus.length === 0 ? (
          <p style={{ color: 'var(--gris-fonce, #6B7280)' }}>
            Vous n'avez pas encore déposé de rendu. Commencez par votre première séance !
          </p>
        ) : (
          <div style={{ display: 'grid', gap: 'var(--space-3)' }}>
            {Array.from(groupes.entries()).map(([cle, liste]) => {
              const [code, titre] = cle.split('||');
              return (
                <div key={cle} className="carte">
                  <div style={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: 'var(--space-2)', marginBottom: 'var(--space-2)' }}>
                    <div>
                      <span className="seance-code">{code}</span>
                      <h3 style={{ marginTop: 4 }}>{titre}</h3>
                    </div>
                  </div>
                  <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'grid', gap: 8 }}>
                    {liste.map((r, i) => (
                      <li
                        key={i}
                        style={{
                          display: 'flex',
                          justifyContent: 'space-between',
                          alignItems: 'center',
                          flexWrap: 'wrap',
                          gap: 8,
                          paddingTop: i > 0 ? 8 : 0,
                          borderTop: i > 0 ? '1px solid var(--gris-clair, #E5E7EB)' : 'none',
                        }}
                      >
                        <span style={{ fontSize: '0.85rem', color: 'var(--gris-fonce, #6B7280)' }}>
                          Déposé le{' '}
                          {new Date(r.dateDepot).toLocaleDateString('fr-FR', {
                            day: 'numeric',
                            month: 'long',
                            year: 'numeric',
                          })}
                        </span>
                        {badgeStatut(r.statut, r.niveau)}
                      </li>
                    ))}
                  </ul>
                </div>
              );
            })}
          </div>
        )}
      </section>
    </div>
  );
}
