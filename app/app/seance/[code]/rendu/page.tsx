'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { supabase, modeDemo } from '@/lib/supabase';

const BLEU = '#2C5697';
const ORANGE = '#FFA142';
const TINT = '#FFF4E8';
const MAX_BYTES = 10 * 1024 * 1024;

export default function RenduPage() {
  const params = useParams();
  const code = params.code as string;
  const router = useRouter();

  const [texte, setTexte] = useState('');
  const [fichier, setFichier] = useState<File | null>(null);
  const [chargement, setChargement] = useState(false);
  const [envoye, setEnvoye] = useState(false);
  const [erreur, setErreur] = useState('');
  const [dejaDepose, setDejaDepose] = useState(false);

  useEffect(() => {
    async function chargerExistant() {
      // Vérifier si un rendu existe déjà
      if (modeDemo) {
        try {
          const val = localStorage.getItem(`rendu_${code}`);
          if (val) {
            const d = JSON.parse(val);
            setTexte(d.texte ?? '');
            setDejaDepose(true);
          }
        } catch (_) {}
        return;
      }
      const sb = supabase();
      if (!sb) return;
      const { data: userData } = await sb.auth.getUser();
      if (!userData?.user) return;
      const { data } = await sb.from('rendus').select('texte').eq('personne_id', userData.user.id).eq('seance_code', code).maybeSingle();
      if (data) {
        setTexte(data.texte ?? '');
        setDejaDepose(true);
      }
    }
    chargerExistant();
  }, [code]);

  async function soumettre(e: React.FormEvent) {
    e.preventDefault();
    setErreur('');
    if (fichier && fichier.size > MAX_BYTES) {
      setErreur('Le fichier dépasse la limite de 10 Mo.');
      return;
    }
    setChargement(true);

    if (modeDemo) {
      try { localStorage.setItem(`rendu_${code}`, JSON.stringify({ texte, fichier: fichier?.name })); } catch (_) {}
      setEnvoye(true);
      setChargement(false);
      return;
    }

    const sb = supabase();
    if (!sb) { setChargement(false); return; }
    const { data: userData } = await sb.auth.getUser();
    const userId = userData?.user?.id;

    let cheminFichier: string | null = null;
    if (fichier && userId) {
      const chemin = `rendus/${userId}/${code}/${fichier.name}`;
      const { error: uploadErr } = await sb.storage.from('rendus').upload(chemin, fichier, { upsert: true });
      if (uploadErr) { setErreur(uploadErr.message); setChargement(false); return; }
      cheminFichier = chemin;
    }

    const { error: dbErr } = await sb.from('rendus').upsert({
      personne_id: userId,
      seance_code: code,
      texte,
      fichier_path: cheminFichier,
      depose_le: new Date().toISOString(),
    }, { onConflict: 'personne_id,seance_code' });

    if (dbErr) { setErreur(dbErr.message); } else { setEnvoye(true); }
    setChargement(false);
  }

  if (envoye) {
    return (
      <div className="conteneur" style={{ paddingTop: '2rem' }}>
        <div style={{ maxWidth: 600, margin: '0 auto', background: '#f0fff4', borderRadius: 12, padding: '2rem', borderLeft: '4px solid #6c6', textAlign: 'center' }}>
          <p style={{ fontSize: '1.5rem', margin: 0 }}>✅</p>
          <h2 style={{ color: '#2a6', fontFamily: 'var(--font-display)' }}>Rendu déposé</h2>
          <p style={{ color: '#444' }}>Votre travail pour la séance <strong>{code}</strong> a bien été enregistré.</p>
          <button onClick={() => router.push(`/seance/${code}`)} style={{ marginTop: '1rem', padding: '.75rem 1.5rem', borderRadius: 8, background: BLEU, color: '#fff', border: 'none', cursor: 'pointer', fontFamily: 'var(--font-display)', fontWeight: 600 }}>
            Retour à la séance
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="conteneur" style={{ paddingTop: '2rem', paddingBottom: '4rem' }}>
      <div style={{ maxWidth: 600, margin: '0 auto' }}>
        <h1 style={{ color: BLEU, fontFamily: 'var(--font-display)', fontSize: '1.4rem' }}>
          {dejaDepose ? 'Remplacer mon rendu' : 'Déposer mon rendu'} · {code}
        </h1>
        {dejaDepose && (
          <div style={{ background: TINT, border: `1px solid ${ORANGE}`, borderRadius: 8, padding: '.75rem', marginBottom: '1rem', fontSize: '.9rem', color: '#555' }}>
            Vous avez déjà déposé un rendu pour cette séance. Vous pouvez le modifier ci-dessous.
          </div>
        )}

        {erreur && (
          <div style={{ background: '#fff0f0', border: '1px solid #f88', borderRadius: 8, padding: '.75rem', marginBottom: '1rem', color: '#c00', fontSize: '.9rem' }}>
            {erreur}
          </div>
        )}

        <form onSubmit={soumettre} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <div>
            <label style={{ display: 'block', fontWeight: 600, color: BLEU, marginBottom: '.5rem' }}>
              Votre réflexion / texte de livrable
            </label>
            <textarea
              value={texte}
              onChange={e => setTexte(e.target.value)}
              rows={6}
              placeholder="Décrivez ce que vous avez réalisé, vos apprentissages, vos questions…"
              style={{ width: '100%', padding: '.75rem', borderRadius: 8, border: '1.5px solid #ddd', fontSize: '.95rem', fontFamily: 'var(--font-body)', boxSizing: 'border-box', resize: 'vertical' }}
            />
          </div>

          <div>
            <label style={{ display: 'block', fontWeight: 600, color: BLEU, marginBottom: '.5rem' }}>
              Joindre un fichier (photo ou PDF, max 10 Mo) — facultatif
            </label>
            <input
              type="file"
              accept="image/*,.pdf"
              onChange={e => setFichier(e.target.files?.[0] ?? null)}
              style={{ fontSize: '.95rem' }}
            />
          </div>

          <button
            type="submit"
            disabled={chargement || (!texte.trim() && !fichier)}
            style={{ padding: '.875rem', borderRadius: 8, background: ORANGE, color: '#fff', border: 'none', fontFamily: 'var(--font-display)', fontWeight: 600, fontSize: '1rem', cursor: 'pointer', opacity: (!texte.trim() && !fichier) ? .5 : 1 }}
          >
            {chargement ? 'Envoi en cours…' : (dejaDepose ? 'Remplacer mon rendu' : 'Déposer mon rendu')}
          </button>
        </form>
      </div>
    </div>
  );
}
