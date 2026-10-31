'use client';

import { useState, useEffect } from 'react';
import { supabase, modeDemo } from '@/lib/supabase';

interface QuizQuestion {
  q: string;
  choix: string[];
  bonne: number;
  explication: string;
}

interface QuizData {
  code: string;
  titre: string;
  description: string;
  questions: QuizQuestion[];
}

const BLEU = '#2C5697';
const ORANGE = '#FFA142';
const TINT = '#FFF4E8';

export default function QuizClient({ data }: { data: QuizData }) {
  const [index, setIndex] = useState(0);
  const [selectionne, setSelectionne] = useState<number | null>(null);
  const [reponsesCorrectes, setReponsesCorrectes] = useState(0);
  const [termine, setTermine] = useState(false);
  const [meilleur, setMeilleur] = useState<number | null>(null);

  const q = data.questions[index];
  const total = data.questions.length;

  useEffect(() => {
    // Charger le meilleur score (localStorage ou Supabase)
    try {
      const val = localStorage.getItem(`quiz_score_${data.code}`);
      if (val) setMeilleur(parseInt(val, 10));
    } catch (_) {}
  }, [data.code]);

  async function sauvegarderScore(score: number) {
    const pct = Math.round((score / total) * 100);
    // Sauvegarder en localStorage (toujours)
    try {
      const actuel = localStorage.getItem(`quiz_score_${data.code}`);
      if (!actuel || pct > parseInt(actuel, 10)) {
        localStorage.setItem(`quiz_score_${data.code}`, String(pct));
        setMeilleur(pct);
      }
    } catch (_) {}

    // Sauvegarder dans Supabase si connecté
    if (!modeDemo) {
      const sb = supabase();
      if (!sb) return;
      const { data: userData } = await sb.auth.getUser();
      if (!userData?.user) return;
      await sb.from('quiz_tentatives').upsert({
        personne_id: userData.user.id,
        code_quiz: data.code,
        score: pct,
        nb_bonnes: score,
        nb_questions: total,
        tente_le: new Date().toISOString(),
      }, { onConflict: 'personne_id,code_quiz', ignoreDuplicates: false });
    }
  }

  function choisir(i: number) {
    if (selectionne !== null) return;
    setSelectionne(i);
  }

  function suivant() {
    const bonneReponse = selectionne === q.bonne;
    const nouveauScore = reponsesCorrectes + (bonneReponse ? 1 : 0);

    if (index + 1 >= total) {
      setReponsesCorrectes(nouveauScore);
      sauvegarderScore(nouveauScore);
      setTermine(true);
    } else {
      setReponsesCorrectes(nouveauScore);
      setIndex(index + 1);
      setSelectionne(null);
    }
  }

  function recommencer() {
    setIndex(0);
    setSelectionne(null);
    setReponsesCorrectes(0);
    setTermine(false);
  }

  if (termine) {
    const score = reponsesCorrectes;
    const pct = Math.round((score / total) * 100);
    return (
      <div style={{ maxWidth: 600, margin: '0 auto' }}>
        <div style={{ background: TINT, borderRadius: 12, padding: '2rem', textAlign: 'center', borderLeft: `4px solid ${ORANGE}` }}>
          <h1 style={{ color: BLEU, fontFamily: 'var(--font-display)', marginTop: 0 }}>{data.titre}</h1>
          <p style={{ fontSize: '3rem', margin: '.5rem 0', fontFamily: 'var(--font-display)', color: ORANGE, fontWeight: 700 }}>{pct} %</p>
          <p style={{ color: '#333', fontSize: '1.1rem' }}>
            {score} / {total} bonnes réponses
            {meilleur !== null && meilleur >= pct && <> · meilleur : <strong>{meilleur} %</strong></>}
          </p>
          <button
            onClick={recommencer}
            style={{ marginTop: '1.5rem', padding: '.875rem 2rem', borderRadius: 8, background: BLEU, color: '#fff', border: 'none', fontFamily: 'var(--font-display)', fontWeight: 600, fontSize: '1rem', cursor: 'pointer' }}
          >
            Recommencer
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 600, margin: '0 auto' }}>
      <div style={{ marginBottom: '1.5rem' }}>
        <h1 style={{ color: BLEU, fontFamily: 'var(--font-display)', fontSize: '1.4rem', margin: 0 }}>{data.titre}</h1>
        <p style={{ color: '#666', marginTop: '.25rem' }}>{data.description}</p>
        <div style={{ display: 'flex', alignItems: 'center', gap: '.5rem', marginTop: '.75rem' }}>
          <div style={{ flex: 1, height: 6, background: '#ddd', borderRadius: 3 }}>
            <div style={{ width: `${((index) / total) * 100}%`, height: '100%', background: BLEU, borderRadius: 3, transition: 'width .3s' }} />
          </div>
          <span style={{ fontSize: '.85rem', color: '#888', whiteSpace: 'nowrap' }}>{index + 1} / {total}</span>
        </div>
      </div>

      <div style={{ background: TINT, borderRadius: 12, padding: '1.5rem', borderLeft: `4px solid ${BLEU}`, marginBottom: '1rem' }}>
        <p style={{ fontWeight: 600, fontSize: '1.05rem', color: '#222', margin: 0 }}>{q.q}</p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '.75rem', marginBottom: '1.5rem' }}>
        {q.choix.map((c, i) => {
          let bg = '#fff';
          let border = '1.5px solid #ddd';
          let color = '#333';
          if (selectionne !== null) {
            if (i === q.bonne) { bg = '#f0fff4'; border = `1.5px solid #6c6`; color = '#2a6'; }
            else if (i === selectionne) { bg = '#fff0f0'; border = `1.5px solid #f88`; color = '#c00'; }
          }
          return (
            <button
              key={i}
              onClick={() => choisir(i)}
              style={{ padding: '1rem', borderRadius: 8, background: bg, border, color, textAlign: 'left', fontSize: '1rem', cursor: selectionne === null ? 'pointer' : 'default', fontFamily: 'var(--font-body)' }}
            >
              {c}
            </button>
          );
        })}
      </div>

      {selectionne !== null && (
        <div style={{ background: '#f8f8f8', borderRadius: 8, padding: '1rem', marginBottom: '1.5rem', fontSize: '.95rem', color: '#444' }}>
          <strong>Explication :</strong> {q.explication}
        </div>
      )}

      {selectionne !== null && (
        <button
          onClick={suivant}
          style={{ width: '100%', padding: '.875rem', borderRadius: 8, background: ORANGE, color: '#fff', border: 'none', fontFamily: 'var(--font-display)', fontWeight: 600, fontSize: '1rem', cursor: 'pointer' }}
        >
          {index + 1 < total ? 'Question suivante →' : 'Voir mon score'}
        </button>
      )}
    </div>
  );
}
