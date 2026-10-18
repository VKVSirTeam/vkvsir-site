/* Membership: Google sign-in (Supabase) + YouTube check (server function verify-member) */
const sb = window.supabase ? window.supabase.createClient(DB.url, DB.key, { auth: { persistSession: true, detectSessionInUrl: true, flowType: 'pkce' } }) : { auth: { getSession: async () => ({ data: { session: null } }), signInWithOAuth: async () => alert('Sign-in is loading, please try again in a moment.'), signOut: async () => {} }, rpc: async () => ({ data: null, error: new Error('offline') }), functions: { invoke: async () => ({ error: new Error('offline') }) } };
const YT_SCOPE = 'https://www.googleapis.com/auth/youtube.readonly';
async function joinWithGoogle(){
  await sb.auth.signInWithOAuth({ provider: 'google', options: {
    scopes: YT_SCOPE, redirectTo: new URL('join?check=1', location.href).href,
    queryParams: { access_type: 'offline', prompt: 'consent' } } });
}
async function membership(){
  try { const { data } = await sb.rpc('my_membership'); return data || {}; } catch(e) { return {}; }
}
async function signOut(){ await sb.auth.signOut(); location.reload(); }
/* header: show account state */
(async () => {
  const { data: { session } } = await sb.auth.getSession();
  const cta = document.querySelector('.menu .cta');
  if (session && cta) {
    const m = await membership();
    cta.textContent = m.member ? 'My membership' : 'Finish joining';
    cta.href = m.member ? 'members' : 'join';
    const li = document.createElement('li'); li.innerHTML = '<a href="#" id="so">Sign out</a>';
    cta.parentElement.after(li); document.getElementById('so').onclick = e => { e.preventDefault(); signOut(); };
  }
})();
/* join page: after Google returns, run the YouTube check */
async function runJoinCheck(box){
  const q = new URLSearchParams(location.search);
  if (!q.has('check')) return;
  box.hidden = false; box.innerHTML = '<p>Checking your YouTube account… please wait a few seconds.</p>';
  const { data: { session } } = await sb.auth.getSession();
  if (!session) { box.innerHTML = '<p>Sign-in was not completed. Please click "Join now" again.</p>'; return; }
  try {
    const { data, error } = await sb.functions.invoke('verify-member', { body: { provider_token: session.provider_token || null } });
    if (error) throw error;
    if (data.status === 'approved') { box.innerHTML = '<p>✅ Welcome! Your membership is active. Opening the members area…</p>'; setTimeout(() => location.href = 'members', 1200); return; }
    box.innerHTML = `<p>⏳ <b>Almost there.</b> ${esc(data.message || '')}</p>
      <p style="display:flex;gap:10px;flex-wrap:wrap;margin-top:12px"><a class="btn btn-yt" href="https://www.youtube.com/@vkvsirdotcom?sub_confirmation=1" target="_blank" rel="noopener">▶ Subscribe on YouTube</a>
      <button class="btn btn-primary" onclick="joinWithGoogle()">Check again</button></p>`;
  } catch (e) { box.innerHTML = '<p>We could not complete the check. Please try again in a minute.</p><p><button class="btn btn-primary" onclick="joinWithGoogle()">Try again</button></p>'; }
}
