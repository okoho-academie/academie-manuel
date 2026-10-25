import Link from 'next/link';
export default function Introuvable() {
  return (
    <div className="conteneur">
      <h1>Page introuvable</h1>
      <p>Cette séance ou cette page n'existe pas. <Link href="/parcours">Revenir au parcours</Link></p>
    </div>
  );
}
