'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { supabase, modeDemo } from '@/lib/supabase';

export default function Connexion() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [envoye, setEnvoye] = useState(false);
  const [erreur, setErreur] = useState('');
  const [chargement, setChargement] = useState(false);

  async function connecterGoogle() {
    const sb = supabase();
    if (!sb) { router.push('/ma-semaine'); return; }
    setChargement(true);
    const { error } = await sb.auth.signInWithOAuth({
      provider: 'google',
      options: { redirectTo: `${location.origin}/auth/callback` },
    });
    if (error) setErreur(error.message);
    setChargement(false);
  }

  async function envoyerLien(e: React.FormEvent) {
    e.preventDefault();
    const sb = supabase();
    if (!sb) { router.push('/ma-semaine'); return; }
    setChargement(true);
    const { error } = await sb.auth.signInWithOtp({
      email,
      options: { emailRedirectTo: `${location.origin}/auth/callback` },
    });
    if (error) {
      setErreur(error.message);
    } else {
      setEnvoye(true);
    }
    setChargement(false);
  }

  return (
    <div style={{ minHeight: '100vh', background: '#FFF4E8', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '1rem' }}>
      <div style={{ background: '#fff', borderRadius: 12, boxShadow: '0 2px 16px rgba(44,86,151,.1)', padding: '2rem', maxWidth: 420, width: '100%' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/icons/icon-192.png" alt="OKOHO Académie" style={{ height: 64, marginBottom: '1rem' }} />
          <h1 style={{ fontFamily: 'var(--font-display)', color: '#2C5697', fontSize: '1.5rem', margin: 0 }}>OKOHO Académie</h1>
          <p style={{ color: '#555', marginTop: '.5rem', fontSize: '.95rem' }}>Connectez-vous pour accéder à votre parcours.</p>
        </div>

        {erreur && (
          <div style={{ background: '#fff0f0', border: '1px solid #f88', borderRadius: 8, padding: '.75rem', marginBottom: '1rem', color: '#c00', fontSize: '.9rem' }}>
            {erreur}
          </div>
        )}

        {envoye ? (
          <div style={{ background: '#f0fff4', border: '1px solid #6c6', borderRadius: 8, padding: '1rem', textAlign: 'center', color: '#2a6' }}>
            <p style={{ margin: 0 }}>✉️ Un lien de connexion a été envoyé à <strong>{email}</strong>. Vérifiez votre boîte mail.</p>
          </div>
        ) : (
          <>
            <button
              onClick={connecterGoogle}
              disabled={chargement}
              style={{ width: '100%', padding: '.875rem', borderRadius: 8, border: '1.5px solid #2C5697', background: '#2C5697', color: '#fff', fontFamily: 'var(--font-display)', fontWeight: 600, fontSize: '1rem', cursor: 'pointer', marginBottom: '1rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '.5rem' }}
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>
              Se connecter avec Google
            </button>

            <div style={{ textAlign: 'center', color: '#aaa', marginBottom: '1rem', fontSize: '.9rem' }}>ou</div>

            <form onSubmit={envoyerLien}>
              <label style={{ display: 'block', fontWeight: 600, color: '#2C5697', marginBottom: '.5rem', fontSize: '.9rem' }}>
                Recevoir un lien par e-mail
              </label>
              <input
                type="email"
                required
                value={email}
                onChange={e => setEmail(e.target.value)}
                placeholder="votre@email.com"
                style={{ width: '100%', padding: '.75rem', borderRadius: 8, border: '1.5px solid #ddd', fontSize: '1rem', marginBottom: '.75rem', boxSizing: 'border-box' }}
              />
              <button
                type="submit"
                disabled={chargement}
                style={{ width: '100%', padding: '.875rem', borderRadius: 8, border: '1.5px solid #FFA142', background: '#FFA142', color: '#fff', fontFamily: 'var(--font-display)', fontWeight: 600, fontSize: '1rem', cursor: 'pointer' }}
              >
                Envoyer le lien
              </button>
            </form>

            <hr style={{ margin: '1.5rem 0', borderColor: '#eee' }} />

            <button
              onClick={() => router.push('/ma-semaine')}
              style={{ width: '100%', padding: '.75rem', borderRadius: 8, border: '1.5px solid #ddd', background: 'transparent', color: '#666', fontSize: '.95rem', cursor: 'pointer' }}
            >
              Continuer en mode démo
            </button>
          </>
        )}
      </div>
      <p style={{ marginTop: '1.5rem', fontSize: '.75rem', color: '#aaa', textAlign: 'center' }}>
        Une formation OKOHO Consulting GmbH · Formateur : Dr. Bertrand Toumi
      </p>
    </div>
  );
}
