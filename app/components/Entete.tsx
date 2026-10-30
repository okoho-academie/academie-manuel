import Link from 'next/link';
import { Logo } from './Logo';
import { modeDemo } from '@/lib/supabase';

export function Entete() {
  return (
    <header className="entete">
      <div className="entete-inner">
        <Link href="/" className="entete-logo" aria-label="Accueil OKOHO Académie">
          <Logo largeur={150} />
        </Link>
        <nav aria-label="Navigation principale">
          <Link href="/ma-semaine">Ma semaine</Link>
          <Link href="/parcours">Parcours</Link>
          <Link href="/formateur">Formateur</Link>
        </nav>
      </div>
      {modeDemo && <p className="bandeau-demo">Mode démo : données d'exemple</p>}
    </header>
  );
}
