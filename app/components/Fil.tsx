import type { Jalon } from '@/lib/acces';

const JALONS: Jalon[] = ['J1', 'J2', 'J3', 'J4', 'J5'];

/** Fil de progression : acquis en bleu clair, en cours en orange, à venir en contour. */
export function Fil({ actuel }: { actuel: Jalon }) {
  const idx = JALONS.indexOf(actuel);
  return (
    <div className="fil" role="img" aria-label={`Jalon ${actuel} en cours`}>
      <div className="fil-ligne">
        {JALONS.map((j, i) => (
          <span key={j} className="fil-cellule">
            {i > 0 && <span className={`fil-seg${i <= idx ? ' fait' : ''}`} />}
            <span className={`fil-pt ${i < idx ? 'acquis' : i === idx ? 'encours' : 'avenir'}`} />
          </span>
        ))}
      </div>
      <div className="fil-labels">
        {JALONS.map((j) => (
          <span key={j}>{j}</span>
        ))}
      </div>
    </div>
  );
}
