import { Etat } from '@/components/Etat';
import { etatSeance } from '@/lib/acces';
import { GROUPES_DEMO, MAINTENANT_DEMO, seanceAcces } from '@/lib/demo';
import { toutesLesSeances } from '@/lib/structure';

export const metadata = { title: 'Formateur' };

export default function Formateur() {
  const seances = toutesLesSeances().filter((s) => s.partie === 'I' || s.partie === 'II');
  return (
    <div className="conteneur">
      <div style={{ display: 'grid', gap: 'var(--space-2)' }}>
        <span className="label">Espace formateur · démo</span>
        <h1>Ouvertures par groupe</h1>
        <p>
          Chaque cellule montre l'état d'une séance pour un groupe. Ouvrir ou fermer se fera ici d'un clic, ou depuis Claude
          avec « Libérer [code] pour [groupe] ».
        </p>
      </div>
      <div className="tableau-conteneur">
        <table>
          <thead>
            <tr>
              <th scope="col">Séance</th>
              {GROUPES_DEMO.map((g) => <th key={g.id} scope="col">{g.nom}</th>)}
            </tr>
          </thead>
          <tbody>
            {seances.map((s) => (
              <tr key={s.code}>
                <td title={s.titre}>{s.code}</td>
                {GROUPES_DEMO.map((g) => (
                  <td key={g.id}>
                    <Etat r={etatSeance(seanceAcces(s.code, s.partie), g, null, MAINTENANT_DEMO)} />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="label">Parties I et II affichées · données d'exemple au {MAINTENANT_DEMO.toLocaleDateString('fr-FR')}</p>
    </div>
  );
}
