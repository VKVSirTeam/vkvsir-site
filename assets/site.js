/* =====================================================================
   VKVSIR.COM — SHARED HEADER, MENU, FOOTER & EFFECTS
   ===================================================================== */
const OLD = 'https://www.vkvsir.com';
const TESTLAB = 'https://test.vkvsir.com';
/* Shared data source (Test Lab database). Same for GitHub and Wix, so links never break. */
const DB = { url: 'https://thrpqwnjwewhdhimmgpu.supabase.co', key: 'sb_publishable_EgH3u5RbDFJPMH7svguFaQ_zuGZ2zVJ' };
async function dbGet(path){ const r = await fetch(DB.url + '/rest/v1/' + path, { headers: { apikey: DB.key, Authorization: 'Bearer ' + DB.key } }); if (!r.ok) throw new Error(r.status); return r.json(); }
async function dbRpc(fn){ const r = await fetch(DB.url + '/rest/v1/rpc/' + fn, { method: 'POST', headers: { apikey: DB.key, Authorization: 'Bearer ' + DB.key, 'Content-Type': 'application/json' }, body: '{}' }); if (!r.ok) throw new Error(r.status); return r.json(); }
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const SITE = {
  name: 'Dr. Vinod Kumar Verma',
  short: 'Mechanical Engg. · Engineering College Ajmer',
  logo: 'https://static.wixstatic.com/media/b90d41_2891d42aeac74eb783f9e95cded38f1e~mv2.png/v1/fit/w_120,h_120,q_90/logo.png',
  joinUrl: OLD + '/apply',
  email: 'vinodvermavkvsir@gmail.com',
  address: 'NB-202, New Building, Engineering College Ajmer, Rajasthan, India – 305025',
  socials: [
    ['YouTube','https://www.youtube.com/@vkvsirdotcom?sub_confirmation=1','a1b09fe8b7f04378a9fe076748ad4a6a.png'],
    ['LinkedIn','https://www.linkedin.com/in/vkvsir','48a2a42b19814efaa824450f23e8a253.png'],
    ['Facebook','https://www.facebook.com/vkvsir','e316f544f9094143b9eac01f1f19e697.png'],
    ['Twitter','https://www.twitter.com/vkvsir','9c4b521dd2404cd5a05ed6115f3a0dc8.png'],
    ['Instagram','https://www.instagram.com/vkvsir','8d6893330740455c96d218258a458aa4.png'],
    ['Telegram','https://t.me/vkvsir','11062b_e98838ff3ed04690a4d6de29d5936f77~mv2.png']
  ],
  courses: [
    ['Automobile Engineering','course-automobile-engineering'],
    ['Hybrid & Electric Vehicles','course-hev'],
    ['Workshop Practice','course-workshop-practice'],
    ['Machine Drawing','course-machine-drawing'],
    ['Casting Process','course-casting-process'],
    ['New Product Design & Launching','course-pdl']
  ],
  members: [
    ['Lecture plans & videos','members#lectures'],
    ['Notes & PPT/PDF downloads','members#downloads'],
    ['Quizzes & practice tests','members#quizzes'],
    ['Project & innovation ideas','members#projects']
  ],
  menu: [
    ['Home','./'],['About','about'],['Courses',null,'courses'],['Test Lab','test-lab'],
    ['R&D','research-project-innovation'],['Media','media'],['Blog','blog'],['Members',null,'members']
  ],
  footer: '©2026 Website created & handled by Reeva Verma'
};

(function render(){
  const here = (location.pathname.split('/').pop() || '').replace('.html','') || './';
  const cur = u => u === here || (u === './' && (here === './' || here === 'index'));
  const ext = u => /^https?:/.test(u) && !u.startsWith(location.origin);
  const A = (t,u) => `<a href="${u}"${cur(u)?' aria-current="page"':''}${ext(u)&&u.startsWith(TESTLAB)?' target="_blank" rel="noopener"':''}>${t}</a>`;
  const items = SITE.menu.map(([t,u,sub]) => {
    if (!sub) return `<li>${A(t,u)}</li>`;
    const list = sub === 'members' ? [['Members home','members'], ...SITE.members, ['Join membership – free', SITE.joinUrl]] : sub === 'courses' ? [['All courses','courses'], ...SITE.courses] : sub;
    return `<li><button aria-expanded="false" aria-haspopup="true">${t} <svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true"><path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" stroke-width="2"/></svg></button><ul class="drop">${list.map(([a,b])=>`<li>${A(a,b)}</li>`).join('')}</ul></li>`;
  }).join('');
  const soc = SITE.socials.map(([n,u,i])=>`<a href="${u}" target="_blank" rel="noopener" aria-label="${n}"><img src="https://static.wixstatic.com/media/${i}/v1/fit/w_44,h_44/s.png" alt="" width="22" height="22" loading="lazy"></a>`).join('');
  const brand = `<a class="brand" href="./" aria-label="Home – ${SITE.name}"><img src="${SITE.logo}" alt="VKVSir logo" width="46" height="39"><span><b>${SITE.name}</b><small>${SITE.short}</small></span></a>`;
  document.getElementById('site-header').outerHTML = `
  <a class="skip" href="#main">Skip to content</a>
  <header class="hdr" id="hdr"><div class="wrap hdr-in">${brand}
    <button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="menu"><span></span></button>
    <ul class="menu" id="menu">${items}<li><a class="cta" href="${SITE.joinUrl}">Join free</a></li></ul>
  </div></header><div class="scrim" id="scrim"></div>`;
  document.getElementById('site-footer').outerHTML = `
  <footer class="ftr"><div class="wrap"><div class="ftr-grid" style="grid-template-columns:1.3fr 1fr 1.2fr 1fr">
    <div>${brand}<p style="margin-top:16px">${SITE.address}</p><p><a href="mailto:${SITE.email}">${SITE.email}</a></p><div class="soc">${soc}</div></div>
    <div><h3>Explore</h3><ul><li><a href="about">About</a></li><li><a href="research-project-innovation">R&amp;D &amp; Consultancy</a></li><li><a href="media">Media</a></li><li><a href="blog">Blog</a></li><li><a href="test-lab">Test Lab</a></li></ul></div>
    <div><h3>Courses</h3><ul>${SITE.courses.map(([t,u])=>`<li><a href="${u}">${t}</a></li>`).join('')}</ul></div>
    <div><h3>Help</h3><ul><li><a href="${SITE.joinUrl}">Join membership – free</a></li><li><a href="members">Members area</a></li><li><a href="faq">FAQ</a></li><li><a href="contact">Contact</a></li><li><a href="${OLD}/post/privacy-policy">Privacy policy</a></li></ul></div>
  </div><div class="copy"><span>${SITE.footer}</span><span>Learning with VKVSir is fun.</span></div></div></footer>`;

  const body = document.body, burger = document.querySelector('.burger');
  const setNav = o => { body.classList.toggle('nav-open', o); burger.setAttribute('aria-expanded', o); };
  burger.onclick = () => setNav(!body.classList.contains('nav-open'));
  document.getElementById('scrim').onclick = () => setNav(false);
  document.addEventListener('keydown', e => e.key === 'Escape' && setNav(false));
  document.querySelectorAll('.menu > li > button').forEach(b => b.onclick = () => { const li = b.parentElement; const o = li.classList.toggle('open'); b.setAttribute('aria-expanded', o); });
  const hdr = document.getElementById('hdr');
  const onScroll = () => hdr.classList.toggle('scrolled', scrollY > 8);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* reveal on scroll */
  const els = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px' });
    els.forEach(el => io.observe(el));
  } else els.forEach(el => el.classList.add('in'));
})();

/* Lightbox for galleries: lightbox('selector') — images need data-full */
function lightbox(selector){
  const imgs = [...document.querySelectorAll(selector)]; if (!imgs.length) return;
  const box = document.createElement('div'); box.className = 'lightbox'; box.setAttribute('role','dialog'); box.setAttribute('aria-modal','true');
  box.innerHTML = '<button class="lb-close" aria-label="Close">×</button><button class="lb-prev" aria-label="Previous">‹</button><img alt=""><button class="lb-next" aria-label="Next">›</button><p class="lb-cap"></p>';
  document.body.appendChild(box);
  const big = box.querySelector('img'), cap = box.querySelector('.lb-cap'); let i = 0;
  const show = n => { i = (n + imgs.length) % imgs.length; big.src = imgs[i].dataset.full; big.alt = imgs[i].alt; cap.textContent = imgs[i].alt + '  ·  ' + (i + 1) + ' / ' + imgs.length; };
  const close = () => box.classList.remove('open');
  imgs.forEach((im, n) => { im.style.cursor = 'zoom-in'; im.tabIndex = 0; const open = () => { show(n); box.classList.add('open'); }; im.onclick = open; im.onkeydown = e => e.key === 'Enter' && open(); });
  box.querySelector('.lb-close').onclick = close;
  box.querySelector('.lb-prev').onclick = () => show(i - 1);
  box.querySelector('.lb-next').onclick = () => show(i + 1);
  box.onclick = e => { if (e.target === box) close(); };
  document.addEventListener('keydown', e => { if (!box.classList.contains('open')) return; if (e.key === 'Escape') close(); if (e.key === 'ArrowLeft') show(i - 1); if (e.key === 'ArrowRight') show(i + 1); });
}
