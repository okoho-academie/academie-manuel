'use client';

import { CheckCircle, Circle, Clock } from 'lucide-react';

interface BarreJalonProps {
  jalon: string;
  livrables: number;
  livrablesFaits: number;
  quizScore: number;
  quizMin: number;
}

type EtatCondition = 'accompli' | 'partiel' | 'attente';

function iconCondition(etat: EtatCondition) {
  if (etat === 'accompli') return <CheckCircle size={18} style={{ color: 'var(--vert)' }} aria-hidden="true" />;
  if (etat === 'partiel') return <Clock size={18} style={{ color: 'var(--orange)' }} aria-hidden="true" />;
  return <Circle size={18} style={{ color: 'var(--gris)' }} aria-hidden="true" />;
}

export function BarreJalon({ jalon, livrables, livrablesFaits, quizScore, quizMin }: BarreJalonProps) {
  const etatLivrables: EtatCondition =
    livrablesFaits >= livrables ? 'accompli' : livrablesFaits > 0 ? 'partiel' : 'attente';
  const etatQuiz: EtatCondition = quizScore >= quizMin ? 'accompli' : quizScore > 0 ? 'partiel' : 'attente';
  // Demo Day : non connu côté client, toujours en attente
  const etatDemo: EtatCondition = 'attente';

  const nbAccomplis = [etatLivrables, etatQuiz, etatDemo].filter((e) => e === 'accompli').length;
  const progression = Math.round((nbAccomplis / 3) * 100);

  const couleurBarre =
    progression === 100 ? 'var(--vert)' : progression > 0 ? 'var(--orange)' : 'var(--gris-clair)';

  return (
    <div
      style={{
        background: 'var(--academie-tint, #FFF4E8)',
        border: '2px solid var(--orange)',
        borderRadius: 'var(--radius)',
        padding: 'var(--space-3)',
        display: 'flex',
        flexDirection: 'column',
        gap: 'var(--space-2)',
      }}
    >
      <span className="label label-orange">Progression vers {jalon}</span>

      {/* Barre de progression */}
      <div
        role="progressbar"
        aria-valuenow={progression}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={`Progression vers ${jalon} : ${progression}%`}
        style={{
          background: 'var(--gris-clair, #E5E7EB)',
          borderRadius: '999px',
          height: '10px',
          overflow: 'hidden',
        }}
      >
        <div
          style={{
            width: `${progression}%`,
            height: '100%',
            background: couleurBarre,
            transition: 'width 0.4s ease',
            borderRadius: '999px',
          }}
        />
      </div>
      <span style={{ fontSize: '0.75rem', color: 'var(--gris-fonce, #6B7280)' }}>{progression}% accompli</span>

      {/* Conditions */}
      <ul style={{ listStyle: 'none', margin: 0, padding: 0, display: 'flex', flexDirection: 'column', gap: 'var(--space-1)' }}>
        <li style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-1)' }}>
          {iconCondition(etatLivrables)}
          <span>
            Livrables : {livrablesFaits}/{livrables} au niveau requis
          </span>
        </li>
        <li style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-1)' }}>
          {iconCondition(etatQuiz)}
          <span>
            Quiz : {quizScore > 0 ? `${quizScore}%` : 'non passé'} (minimum {quizMin}%)
          </span>
        </li>
        <li style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-1)' }}>
          {iconCondition(etatDemo)}
          <span>Démo Day : à confirmer par le formateur</span>
        </li>
      </ul>
    </div>
  );
}
