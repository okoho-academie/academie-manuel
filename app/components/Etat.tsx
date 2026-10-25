import { CalendarDays, Check, Flag, Lock, LockOpen, Unlock } from 'lucide-react';
import type { ResultatAcces } from '@/lib/acces';

/** Statut toujours avec icône et mot, jamais la couleur seule. */
export function Etat({ r }: { r: ResultatAcces }) {
  const Icone =
    r.etat === 'terminee' ? Check
    : r.etat === 'libre' ? Unlock
    : r.etat === 'ouverte' ? LockOpen
    : r.raison === 'date' ? CalendarDays
    : r.raison === 'jalon' ? Flag
    : Lock;
  return (
    <span className={`etat etat-${r.etat}`}>
      <Icone size={16} strokeWidth={2} aria-hidden="true" />
      {r.libelle}
    </span>
  );
}
