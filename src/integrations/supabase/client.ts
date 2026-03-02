import { createClient } from "@supabase/supabase-js";
import type { Database } from "./types";
const FALLBACK_PROJECT_ID = "lnxstnhlyloqqawytqqk";
const FALLBACK_URL = `https://${FALLBACK_PROJECT_ID}.supabase.co`;
const FALLBACK_PUBLISHABLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxueHN0bmhseWxvcXFhd3l0cXFrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIzNjc1MzksImV4cCI6MjA4Nzk0MzUzOX0.3vB0LSpN5wbc4W4qjykLyUXhPig6Zgm4_NYlYB_U1rA";
const supabaseUrl =
  import.meta.env.VITE_SUPABASE_URL ||
  (import.meta.env.VITE_SUPABASE_PROJECT_ID
    ? `https://${import.meta.env.VITE_SUPABASE_PROJECT_ID}.supabase.co`
    : FALLBACK_URL);
const supabasePublishableKey =
  import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY || FALLBACK_PUBLISHABLE_KEY;
export const supabase = createClient<Database>(supabaseUrl, supabasePublishableKey, {
  auth: {
    storage: typeof window !== "undefined" ? window.localStorage : undefined,
    persistSession: true,
    autoRefreshToken: true,
  },
});
