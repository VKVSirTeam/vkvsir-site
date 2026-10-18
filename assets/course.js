/* Renders lecture plans live from the shared Test Lab database (table: library).
   Edit links in Supabase → Table editor → library. No website change needed. */
const yt = u => u ? `<a class="lk v" href="${esc(u)}" target="_blank" rel="noopener" title="Watch video">▶ Video</a>` : '<span class="na">–</span>';
const dl = u => u ? `<a class="lk d" href="${esc(u)}" target="_blank" rel="noopener" title="PPT / PDF">⬇ Notes</a>` : '<span class="na">–</span>';
const qz = u => u ? `<a class="lk q" href="${esc(u)}" target="_blank" rel="noopener" title="Quiz">✎ Quiz</a>` : '<span class="na">–</span>';
function mins(d){ if(!d) return 0; const p = String(d).split('.').map(Number); if (p.length===3) return p[0]*60+p[1]+p[2]/60; return p[0]+(p[1]||0)/60; }
async function loadCourse(course){
  try { const r = await dbGet('library?select=*&active=eq.true&course=eq.' + encodeURIComponent(course) + '&order=sort_order.asc'); return r.length ? r : (window.LIB_FALLBACK || []); } catch(e) { return window.LIB_FALLBACK || []; }
}
function groupUnits(rows){ const m = new Map(); rows.forEach(r => { const k = r.unit || 'Lectures'; if(!m.has(k)) m.set(k, []); m.get(k).push(r); }); return [...m]; }

/* Public course page: syllabus outline + stats, links locked */
async function renderPublic(course, el, statsEl){
  try {
    const rows = (await loadCourse(course)).filter(r => r.item_type === 'lecture');
    if (!rows.length) { el.innerHTML = '<p class="muted">The detailed lecture plan for this course is being prepared. Join free to be notified when it goes live.</p>'; return; }
    const units = groupUnits(rows), hrs = rows.reduce((a,r)=>a+mins(r.duration),0)/60;
    if (statsEl) statsEl.innerHTML = `<div><b>${units.length}</b><span>units</span></div><div><b>${rows.length}</b><span>lectures</span></div><div><b>${Math.round(hrs)}+</b><span>hours of video</span></div><div><b>${rows.filter(r=>r.ppt_url).length}</b><span>PPT/PDF notes</span></div>`;
    el.innerHTML = units.map(([u, ls], n) => `<details class="unit"${n===0?' open':''}><summary><span>${esc(u)}</span><em>${ls.length} lectures</em></summary><ol>${ls.map(l=>`<li><b>${esc(l.lecture||'')}</b> ${esc(l.topic)} <span class="lock" title="Members only">🔒 video · notes · quiz</span></li>`).join('')}</ol></details>`).join('');
  } catch(e) { el.innerHTML = '<p class="muted">Syllabus could not be loaded right now. Please refresh in a moment.</p>'; }
}

/* Members page: full lecture plan with links */
async function renderMembers(course, el, statsEl, searchEl){
  try {
    const rows = (await loadCourse(course)).filter(r => r.item_type === 'lecture');
    if (!rows.length) { el.innerHTML = '<p class="muted">Lecture videos, notes and quizzes for this course are being added. Check back soon.</p>'; return; }
    const units = groupUnits(rows), hrs = rows.reduce((a,r)=>a+mins(r.duration),0)/60;
    if (statsEl) statsEl.innerHTML = `<div><b>${rows.length}</b><span>lectures</span></div><div><b>${Math.round(hrs)}+</b><span>hours</span></div><div><b>${rows.filter(r=>r.ppt_url).length}</b><span>notes</span></div><div><b>${rows.filter(r=>r.quiz_url).length}</b><span>quizzes</span></div>`;
    el.innerHTML = units.map(([u, ls], n) => `<details class="unit" open><summary><span>${esc(u)}</span><em>${ls.length} lectures</em></summary><div class="tbl"><table><thead><tr><th>Lecture</th><th>Topic</th><th>Duration</th><th>Video</th><th>PPT / PDF</th><th>Quiz</th><th>Test Lab</th></tr></thead><tbody>${ls.map(l=>`<tr data-q="${esc((l.lecture+' '+l.topic).toLowerCase())}"><td class="lec">${esc(l.lecture||'')}</td><td>${esc(l.topic)}${(l.extra_videos||[]).map((v,i)=>` <a class="lk v sm" href="${esc(v)}" target="_blank" rel="noopener">▶ Part ${i+2}</a>`).join('')}</td><td class="dur">${esc(l.duration||'')}</td><td>${yt(l.url)}</td><td>${dl(l.ppt_url)}</td><td>${qz(l.quiz_url)}</td><td><a class="lk t" href="${esc(l.test_url || TESTLAB)}" target="_blank" rel="noopener">Practise</a></td></tr>`).join('')}</tbody></table></div></details>`).join('');
    if (searchEl) searchEl.oninput = () => { const q = searchEl.value.trim().toLowerCase(); el.querySelectorAll('tbody tr').forEach(tr => tr.hidden = q && !tr.dataset.q.includes(q)); el.querySelectorAll('details').forEach(d => { d.hidden = q && ![...d.querySelectorAll('tbody tr')].some(tr => !tr.hidden); if (q) d.open = true; }); };
  } catch(e) { el.innerHTML = '<p class="muted">Lecture plan could not be loaded right now. Please refresh in a moment.</p>'; }
}
