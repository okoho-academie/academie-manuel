import { createClient, type SupabaseClient } from '@supabase/supabase-js';

const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
const cle = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

/** Sans variables d'environnement, l'application reste en mode démo. */
export const modeDemo = !url || !cle;

let client: SupabaseClient | null = null;
export function supabase(): SupabaseClient | null {
  if (modeDemo) return null;
  if (!client) client = createClient(url!, cle!);
  return client;
}
