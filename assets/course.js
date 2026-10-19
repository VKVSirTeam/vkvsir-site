/* Renders lecture plans live from the shared Test Lab database (table: library).
   Edit links in Supabase → Table editor → library. No website change needed. */
const yt = u => u ? `<a class="lk v" href="${esc(u)}" target="_blank" rel="noopener" title="Watch video">▶ Video</a>` : '<span class="na">–</span>';
const tl = u => u ? `<a class="lk t" href="${esc(u)}" target="_blank" rel="noopener" title="Topic quiz on Test Lab">✎ Quiz</a>` : '<span class="na">–</span>';
const dl = u => u ? `<a class="lk d" href="${esc(u)}" target="_blank" rel="noopener" title="PPT / PDF">⬇ Notes</a>` : '<span class="na">–</span>';
const qz = u => u ? `<a class="lk q" href="${esc(u)}" target="_blank" rel="noopener" title="Quiz">✎ Quiz</a>` : '<span class="na">–</span>';
function fmtDur(d){ if(!d) return '–'; const p=String(d).split('.'); if(p.length===1) return p[0]+' min'; const pad=x=>(x+'0').slice(0,2); return p.length===3 ? `${p[0]}:${p[1].padStart(2,'0')}:${pad(p[2])}` : `${p[0]}:${pad(p[1])}`; }
function mins(d){ if(!d) return 0; const p = String(d).split('.').map(Number); if (p.length===3) return p[0]*60+p[1]+p[2]/60; return p[0]+(p[1]||0)/60; }
async function loadOutline(course){
  try { const { data, error } = await sb.rpc('library_outline', { p_course: course }); if (error) throw error; return data || []; } catch(e) { return window.LIB_FALLBACK || []; }
}
async function loadMember(course){
  const { data, error } = await sb.rpc('library_member', { p_course: course });
  if (error) throw error; return data || [];
}
function groupUnits(rows){ const m = new Map(); rows.forEach(r => { const k = r.unit || 'Lectures'; if(!m.has(k)) m.set(k, []); m.get(k).push(r); }); return [...m]; }

/* Public course page: syllabus outline + stats, links locked */
async function renderPublic(course, el, statsEl){
  try {
    const rows = (await loadOutline(course)).filter(r => r.item_type === 'lecture');
    if (!rows.length) { el.innerHTML = '<p class="muted">The detailed lecture plan for this course is being prepared. Join free to be notified when it goes live.</p>'; return; }
    const units = groupUnits(rows), hrs = rows.reduce((a,r)=>a+mins(r.duration),0)/60;
    if (statsEl) statsEl.innerHTML = `<div><b>${units.length}</b><span>units</span></div><div><b>${plus(rows.length)}</b><span>lectures</span></div><div><b>${plus(Math.round(hrs))}</b><span>hours of learning</span></div><div><b>${rows.some(r=>r.ppt_url||r.has_ppt)?plus(rows.filter(r=>r.ppt_url||r.has_ppt).length):'Many'}</b><span>notes &amp; quizzes</span></div>`;
    el.innerHTML = units.map(([u, ls], n) => `<details class="unit"${n===0?' open':''}><summary><span>${esc(u)}</span><em>${ls.length} lectures</em></summary><ol>${ls.map(l=>`<li><b>${esc(l.lecture||'')}</b> ${esc(l.topic)} ${l.url?`<a class="lk v sm" href="${esc(l.url)}" target="_blank" rel="noopener">▶ Video</a>`:''} <span class="lock" title="Members only">🔒 notes · quiz</span></li>`).join('')}</ol></details>`).join('');
  } catch(e) { el.innerHTML = '<p class="muted">Syllabus could not be loaded right now. Please refresh in a moment.</p>'; }
}

/* Members page: full lecture plan with links */
async function renderMembers(course, el, statsEl, searchEl){
  const m = await membership();
  if (!m.member) {
    const rows = (await loadOutline(course)).filter(r => r.item_type === 'lecture');
    document.querySelectorAll('.members-only').forEach(x => x.hidden = true);
    el.innerHTML = `<div class="free" style="margin-bottom:24px"><div><span class="kicker">🔒 Members only · free forever</span><h2>${m.signed_in ? 'Finish your free membership' : 'Sign in to open this page'}</h2><p>${m.signed_in ? esc(m.reason==='not_subscribed'?'Subscribe to our YouTube channel with the same Google account, then check again.':'Complete the YouTube check to unlock notes and quizzes.') : 'Lecture videos are free for everyone. PPT/PDF notes, Test Lab quizzes and books open after a one-time, 30-second sign-up.'}</p></div><div class="actions"><button class="btn btn-gold" onclick="joinWithGoogle()">${m.signed_in ? 'Check again' : 'Join free with Google'}</button><a class="btn btn-light" href="join">How it works</a></div></div>`
      + groupUnits(rows).map(([u, ls], n) => `<details class="unit"${n===0?' open':''}><summary><span>${esc(u)}</span><em>${ls.length} lectures</em></summary><ol>${ls.map(l=>`<li><b>${esc(l.lecture||'')}</b> ${esc(l.topic)} ${l.url?`<a class="lk v sm" href="${esc(l.url)}" target="_blank" rel="noopener">▶ Video</a>`:''} <span class="lock">🔒 notes · quiz</span></li>`).join('')}</ol></details>`).join('');
    if (statsEl) statsEl.innerHTML = `<div><b>${plus(rows.length)}</b><span>lectures</span></div><div><b>▶</b><span>videos free</span></div><div><b>🔒</b><span>notes</span></div><div><b>🔒</b><span>quizzes</span></div>`;
    if (searchEl) searchEl.hidden = true;
    return;
  }
  document.querySelectorAll('.members-only').forEach(x => x.hidden = false);
  try {
    const rows = (await loadMember(course)).filter(r => r.item_type === 'lecture');
    if (!rows.length) { el.innerHTML = '<p class="muted">Lecture videos, notes and quizzes for this course are being added. Check back soon.</p>'; return; }
    const units = groupUnits(rows), hrs = rows.reduce((a,r)=>a+mins(r.duration),0)/60;
    if (statsEl) statsEl.innerHTML = `<div><b>${plus(rows.length)}</b><span>lectures</span></div><div><b>${plus(Math.round(hrs))}</b><span>hours</span></div><div><b>${rows.some(r=>r.ppt_url||r.has_ppt)?plus(rows.filter(r=>r.ppt_url||r.has_ppt).length):'Soon'}</b><span>notes</span></div><div><b>Unit-wise</b><span>Test Lab quizzes</span></div>`;
    el.innerHTML = units.map(([u, ls], n) => `<details class="unit" open><summary><span>${esc(u)}</span><em>${ls.length} lectures</em></summary><div class="tbl"><table><thead><tr><th>Lecture</th><th>Topic</th><th>Duration</th><th style="text-align:center">Video</th><th style="text-align:center">PPT / PDF</th><th style="text-align:center">Test Lab quiz</th></tr></thead><tbody>${ls.map(l=>`<tr data-q="${esc((l.lecture+' '+l.topic).toLowerCase())}"><td class="lec">${esc(l.lecture||'')}</td><td class="top">${esc(l.topic)}${(l.extra_videos||[]).map((v,i)=>` <a class="lk v sm" href="${esc(v)}" target="_blank" rel="noopener">▶ Part ${i+2}</a>`).join('')}</td><td class="dur">${fmtDur(l.duration)}</td><td class="c3">${yt(l.url)}</td><td class="c3">${dl(l.ppt_url)}</td><td class="c3">${tl(l.test_url)}</td></tr>`).join('')}</tbody></table></div></details>`).join('');
    if (searchEl) searchEl.oninput = () => { const q = searchEl.value.trim().toLowerCase(); el.querySelectorAll('tbody tr').forEach(tr => tr.hidden = q && !tr.dataset.q.includes(q)); el.querySelectorAll('details').forEach(d => { d.hidden = q && ![...d.querySelectorAll('tbody tr')].some(tr => !tr.hidden); if (q) d.open = true; }); };
  } catch(e) { el.innerHTML = '<p class="muted">Lecture plan could not be loaded right now. Please refresh in a moment.</p>'; }
}

/* one-time hints on course pages */
setTimeout(() => { const s = document.querySelector('#plan details summary, #syl details summary'); if (s && window.siteGuide) siteGuide(s, 'Tap a unit to see its lectures. Videos are free to watch'); }, 1500);
