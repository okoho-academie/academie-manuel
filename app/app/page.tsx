import Link from 'next/link';
import { ArrowRight } from 'lucide-react';
import { Orbit } from '@/components/Orbit';
import { lireStructure } from '@/lib/structure';

export default function Accueil() {
  const { parties } = lireStructure();
  const nbSeances = parties.reduce((n, p) => n + p.modules.reduce((m, mo) => m + mo.seances.length, 0), 0);
  return (
    <>
      <section className="hero">
        <div className="hero-inner">
          <Orbit className="orbit" />
          <span className="label">Parcours Claude Pro</span>
          <h1>De l'idée au service digital vendu, avec Claude.</h1>
          <Link href="/parcours" className="bouton bouton-clair">
            Parcours Démarrage <ArrowRight size={18} aria-hidden="true" />
          </Link>
        </div>
      </section>
      <div className="conteneur">
        <div className="trois">
          <div className="carte">
            <span className="label label-orange">Accès libre</span>
            <h3>Parcours Démarrage</h3>
            <p>La Partie I est ouverte à tous : créer son compte, écrire de bonnes consignes, vérifier les réponses.</p>
          </div>
          <div className="carte">
            <span className="label">Le manuel</span>
            <h3>{parties.length} parties, {nbSeances} séances</h3>
            <p>Chaque séance se termine par un livrable concret, utilisable pour un vrai client.</p>
          </div>
          <div className="carte">
            <span className="label">Votre rythme</span>
            <h3>Rendez-vous fixes, rythme libre</h3>
            <p>Les séances s'ouvrent selon le calendrier, vos acquis et les jalons validés par le formateur.</p>
          </div>
        </div>
      </div>
    </>
  );
}
