'use client';

import { useState } from 'react';
import { supabase, modeDemo } from '@/lib/supabase';

const BLEU = '#2C5697';
const ORANGE = '#FFA142';

export default function QuestionModal({ seanceCode }: { seanceCode: string }) {
  const [ouvert, setOuvert] = useState(false);
  const [question, setQuestion] = useState('');
  const [partager, setPartager] = useState(false);
  const [envoye, setEnvoye] = useState(false);
  const [chargement, setChargement] = useState(false);
  const [erreur, setErreur] = useState('');

  async function soumettre(e: React.FormEvent) {
    e.preventDefault();
    if (!question.trim()) return;
    setChargement(true);
    setErreur('');

    if (modeDemo) {
      try {
        const questions = JSON.parse(localStorage.getItem(`questions_${seanceCode}`) ?? '[]');
        questions.push({ question, partager, date: new Date().toISOString() });
        localStorage.setItem(`questions_${seanceCode}`, JSON.stringify(questions));
      } catch (_) {}
      setEnvoye(true);
      setChargement(false);
      return;
    }

    const sb = supabase();
    if (!sb) { setChargement(false); return; }
    const { data: userData } = await sb.auth.getUser();

    const { error } = await sb.from('questions').insert({
      personne_id: userData?.user?.id ?? null,
      seance_code: seanceCode,
      texte: question,
      partager_cohorte: partager,
      posee_le: new Date().toISOString(),
    });

    if (error) { setErreur(error.message); } else { setEnvoye(true); }
    setChargement(false);
  }

  function fermer() {
    setOuvert(false);
    setQuestion('');
    setPartager(false);
    setEnvoye(false);
    setErreur('');
  }

  return (
    <>
      <div style={{ marginTop: '2.5rem', paddingTop: '2rem', borderTop: '1px solid #eee' }}>
        <button
          onClick={() => setOuvert(true)}
          style={{ padding: '.75rem 1.5rem', borderRadius: 8, background: 'transparent', border: `1.5px solid ${BLEU}`, color: BLEU, fontFamily: 'var(--font-display)', fontWeight: 600, fontSize: '.95rem', cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: '.5rem' }}
        >
          ❓ Poser une question
        </button>
      </div>

      {ouvert && (
        <div
          role="dialog"
          aria-modal="true"
          style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,.5)', zIndex: 1000, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '1rem' }}
          onClick={e => { if (e.target === e.currentTarget) fermer(); }}
        >
          <div style={{ background: '#fff', borderRadius: 12, padding: '1.5rem', maxWidth: 500, width: '100%', boxShadow: '0 8px 32px rgba(0,0,0,.2)' }}>
            <h2 style={{ color: BLEU, fontFamily: 'var(--font-display)', marginTop: 0, fontSize: '1.2rem' }}>
              Poser une question · {seanceCode}
            </h2>

            {envoye ? (
              <div style={{ textAlign: 'center', padding: '1rem 0' }}>
                <p style={{ fontSize: '1.5rem', margin: '0 0 .5rem' }}>✅</p>
                <p style={{ color: '#2a6', fontWeight: 600 }}>Votre question a bien été envoyée.</p>
                <button onClick={fermer} style={{ marginTop: '1rem', padding: '.75rem 1.5rem', borderRadius: 8, background: BLEU, color: '#fff', border: 'none', cursor: 'pointer', fontFamily: 'var(--font-display)', fontWeight: 600 }}>
                  Fermer
                </button>
              </div>
            ) : (
              <form onSubmit={soumettre} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {erreur && (
                  <div style={{ background: '#fff0f0', border: '1px solid #f88', borderRadius: 8, padding: '.75rem', color: '#c00', fontSize: '.9rem' }}>
                    {erreur}
                  </div>
                )}
                <div>
                  <label style={{ display: 'block', fontWeight: 600, color: BLEU, marginBottom: '.5rem', fontSize: '.9rem' }}>
                    Votre question
                  </label>
                  <textarea
                    required
                    value={question}
                    onChange={e => setQuestion(e.target.value)}
                    rows={4}
                    placeholder="Posez votre question ici…"
                    autoFocus
                    style={{ width: '100%', padding: '.75rem', borderRadius: 8, border: '1.5px solid #ddd', fontSize: '.95rem', fontFamily: 'var(--font-body)', boxSizing: 'border-box', resize: 'vertical' }}
                  />
                </div>
                <label style={{ display: 'flex', alignItems: 'flex-start', gap: '.75rem', cursor: 'pointer', fontSize: '.9rem', color: '#444' }}>
                  <input
                    type="checkbox"
                    checked={partager}
                    onChange={e => setPartager(e.target.checked)}
                    style={{ marginTop: 2, accentColor: ORANGE }}
                  />
                  <span>Partager avec la cohorte (FAQ de la séance)</span>
                </label>
                <div style={{ display: 'flex', gap: '.75rem', justifyContent: 'flex-end' }}>
                  <button type="button" onClick={fermer} style={{ padding: '.75rem 1.25rem', borderRadius: 8, border: '1px solid #ddd', background: '#fff', cursor: 'pointer', fontSize: '.9rem' }}>
                    Annuler
                  </button>
                  <button
                    type="submit"
                    disabled={chargement}
                    style={{ padding: '.75rem 1.5rem', borderRadius: 8, background: ORANGE, color: '#fff', border: 'none', cursor: 'pointer', fontFamily: 'var(--font-display)', fontWeight: 600, fontSize: '.95rem' }}
                  >
                    {chargement ? 'Envoi…' : 'Envoyer'}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </>
  );
}
