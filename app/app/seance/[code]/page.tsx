import { notFound } from 'next/navigation';
import Link from 'next/link';
import { Fil } from '@/components/Fil';
import { lireSeance, seancesDisponibles } from '@/lib/seance';
import { toutesLesSeances } from '@/lib/structure';
import type { Jalon } from '@/lib/acces';
import QuestionModal from './QuestionModal';

const APPAREIL: Record<string, string> = {
  smartphone: 'Smartphone possible',
  'laptop-recommande': 'Ordinateur recommandé',
  'laptop-obligatoire': 'Ordinateur obligatoire',
};

export function generateStaticParams() {
  return toutesLesSeances().map((s) => ({ code: s.code }));
}

export function generateMetadata({ params }: { params: { code: string } }) {
  return { title: params.code };
}

export default function Seance({ params }: { params: { code: string } }) {
  const ref = toutesLesSeances().find((s) => s.code === params.code);
  if (!ref) notFound();
  const doc = seancesDisponibles().includes(params.code) ? lireSeance(params.code) : null;
  const m = doc?.meta;
  const jalon: Jalon = (m?.jalon as Jalon) ?? 'J1';
  return (
    <>
      <div className="seance-tete">
        <div className="conteneur">
          <span className="label">Partie {ref.partie} · {ref.module} · {ref.moduleTitre}</span>
          <h1>{ref.titre}</h1>
          <Fil actuel={jalon} />
          <div className="meta">
            <span>{ref.code}</span>
            {m?.type && <span>{m.type === 'direct' ? 'En direct' : 'En autonomie'}</span>}
            {(m?.outil ?? ref.outil) && <span>{m?.outil ?? ref.outil}</span>}
            {(m?.appareil ?? ref.appareil) && <span>{APPAREIL[(m?.appareil ?? ref.appareil) as string] ?? m?.appareil}</span>}
            {m?.duree && <span>{m.duree.seance} min · devoir {Math.round(m.duree.devoir / 60)} h</span>}
          </div>
        </div>
      </div>
      <div className="conteneur">
        <div className="encadre">
          <span className="label label-orange">Ce que vous saurez faire</span>
          {doc?.objectifsHtml ? (
            <div dangerouslySetInnerHTML={{ __html: doc.objectifsHtml }} />
          ) : (
            <p>{ref.livrable ? `Livrable : ${ref.livrable}.` : 'Les objectifs de cette séance seront publiés avec son contenu.'}</p>
          )}
        </div>
        {doc ? (
          <article className="contenu" dangerouslySetInnerHTML={{ __html: doc.html }} />
        ) : (
          <div className="carte"><p>Le contenu de cette séance est en préparation.</p></div>
        )}
        {(ref.livrable ?? m?.livrable) && (
          <div className="encadre">
            <span className="label label-orange">Votre livrable</span>
            <p>{m?.livrable ?? ref.livrable}</p>
          </div>
        )}
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginTop: '2rem' }}>
          <Link
            href={`/seance/${params.code}/rendu`}
            style={{ padding: '.75rem 1.5rem', borderRadius: 8, background: '#2C5697', color: '#fff', textDecoration: 'none', fontFamily: 'var(--font-display)', fontWeight: 600, fontSize: '.95rem', display: 'inline-block' }}
          >
            📤 Déposer mon rendu
          </Link>
          <Link
            href={`/quiz/${params.code}`}
            style={{ padding: '.75rem 1.5rem', borderRadius: 8, background: '#FFF4E8', color: '#2C5697', border: '1.5px solid #2C5697', textDecoration: 'none', fontFamily: 'var(--font-display)', fontWeight: 600, fontSize: '.95rem', display: 'inline-block' }}
          >
            🧩 Quiz de la séance
          </Link>
        </div>
        <QuestionModal seanceCode={params.code} />
      </div>
    </>
  );
}
