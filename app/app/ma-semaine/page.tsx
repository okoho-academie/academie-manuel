import Link from 'next/link';
import { CalendarDays, ClipboardList, Video, ArrowRight } from 'lucide-react';
import { Fil } from '@/components/Fil';
import { formaterDate } from '@/lib/acces';
import { PERSONNE_DEMO, SEMAINE_DEMO } from '@/lib/demo';
import { prochainPas } from '@/lib/prochain-pas';

export const metadata = { title: 'Ma semaine' };

export default function MaSemaine() {
  const s = SEMAINE_DEMO;
  const pas = prochainPas({
    seanceOuverte: s.seance.code,
    devoirEcheance: s.devoir.echeance,
    devoirRendu: false,
  });
  return (
    <div className="conteneur">
      <div style={{ display: 'grid', gap: 'var(--space-3)' }}>
        <span className="label">Semaine {s.semaine} · Bonjour {PERSONNE_DEMO.prenom}</span>
        <h1>Ma semaine</h1>
        <Fil actuel={s.jalonActuel} />
      </div>

      {/* Mon prochain pas */}
      <div style={{ margin: 'var(--space-3) 0' }}>
        <Link
          href={pas.href}
          className={`bouton${pas.urgent ? ' bouton-urgent' : ''}`}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 8,
            background: pas.urgent ? 'var(--rouge, #DC2626)' : 'var(--blue-deep, #1E3A8A)',
            color: '#fff',
            padding: '10px 20px',
            borderRadius: 'var(--radius)',
            textDecoration: 'none',
            fontFamily: 'var(--font-titre, Montserrat, sans-serif)',
            fontWeight: 700,
            fontSize: '1rem',
          }}
        >
          <ArrowRight size={18} aria-hidden="true" />
          {pas.label}
        </Link>
      </div>
      <div className="trois">
        <Link href={`/seance/${s.seance.code}`} className="carte" style={{ textDecoration: 'none', color: 'inherit' }}>
          <span className="label label-orange"><ClipboardList size={14} aria-hidden="true" /> Séance de la semaine</span>
          <span className="seance-code">{s.seance.code}</span>
          <h3>{s.seance.titre}</h3>
        </Link>
        <div className="carte">
          <span className="label">Devoir</span>
          <h3>{s.devoir.titre}</h3>
          <p className="etat"><CalendarDays size={16} aria-hidden="true" /> À rendre le {formaterDate(s.devoir.echeance)}</p>
        </div>
        <div className="carte">
          <span className="label"><Video size={14} aria-hidden="true" /> Prochaine séance en direct</span>
          <h3>{s.live.titre}</h3>
          <p className="etat"><CalendarDays size={16} aria-hidden="true" /> Samedi {formaterDate(s.live.date)} · {s.live.heure} (heure de {s.live.fuseau})</p>
        </div>
      </div>
    </div>
  );
}
