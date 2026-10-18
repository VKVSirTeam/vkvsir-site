/* =====================================================================
   VKVSIR.COM — SHARED CONTENT (header, menu, footer for every page)
   ===================================================================== */
const OLD = 'https://www.vkvsir.com';            // existing Wix site (members area & blog posts live there for now)
const SITE = {
  name: 'Prof. Vinod Kumar Verma',
  dept: 'Department of Mechanical Engineering<br>Engineering College Ajmer, Rajasthan, India',
  logo: 'https://static.wixstatic.com/media/b90d41_2891d42aeac74eb783f9e95cded38f1e~mv2.png',
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
  menu: [
    ['Home','./'],['Courses','courses'],['About','about'],
    ['R&D, Projects & Innovation', OLD + '/research-project-innovation'],
    ['Media','media'],['Test and Analysis','test-and-analysis'],
    ['Blog & Linkedin','blog'],['FAQ','faq'],['Contact','contact'],
    ['Members Area ▾', OLD + '/members',[
      ['Automobile Engineering', OLD + '/automobile-engineering'],
      ['Hybrid and Electric Vehicles', OLD + '/hev'],
      ['Workshop Practice', OLD + '/workshop-practice'],
      ['Quiz', OLD + '/quiz'],
      ['New Product Design & Launching', OLD + '/pdl'],
      ['Join membership – free', OLD + '/apply']]]
  ],
  footer: '©2026 Website created & handled by Reeva Verma'
};

(function render(){
  const here = (location.pathname.split('/').pop() || '').replace('.html','') || './';
  const media = i => `https://static.wixstatic.com/media/${i}`;
  const isCur = u => (u === here) || (u === './' && (here === './' || here === 'index'));
  const menu = SITE.menu.map(([t,u,sub]) => `<li><a href="${u}"${isCur(u)?' aria-current="page"':''}>${t}</a>${sub?`<div class="sub">${sub.map(([st,su])=>`<a href="${su}">${st}</a>`).join('')}</div>`:''}</li>`).join('');
  const soc = SITE.socials.map(([n,u,i])=>`<a href="${u}" target="_blank" rel="noopener" aria-label="${n}"><img src="${media(i)}" alt="${n}" width="28" height="28"></a>`).join('');
  document.getElementById('site-header').innerHTML = `
  <header class="site-header"><div class="head-row">
    <a class="logo" href="./"><img src="${SITE.logo}" alt="Logo of vkvsir"></a>
    <div class="titles"><a class="name" href="./">${SITE.name}</a><p class="dept">${SITE.dept}</p></div>
    <div class="head-side"><a class="login" href="${SITE.joinUrl}">Log In / Join</a><div class="socials">${soc}</div></div>
  </div></header>
  <nav class="nav" id="nav" aria-label="Main"><button class="menu-toggle" aria-expanded="false">☰ Menu</button><ul>${menu}</ul></nav>`;
  const members = SITE.menu[9][2];
  document.getElementById('site-footer').innerHTML = `
  <footer><div class="wrap"><div class="foot-grid">
    <div><h3>${SITE.name}</h3><p>${SITE.address}</p><p><a href="mailto:${SITE.email}">${SITE.email}</a></p><div class="foot-socials">${soc}</div></div>
    <div><h3>Explore</h3><ul>${[1,2,4,5,6,7,8].map(k=>`<li><a href="${SITE.menu[k][1]}">${SITE.menu[k][0]}</a></li>`).join('')}</ul></div>
    <div><h3>Members area</h3><ul>${members.map(([t,u])=>`<li><a href="${u}">${t}</a></li>`).join('')}</ul></div>
  </div><p class="copy">${SITE.footer} · <a href="${OLD}/post/privacy-policy">Privacy Policy</a></p></div></footer>`;
  const nav = document.getElementById('nav');
  nav.querySelector('.menu-toggle').addEventListener('click', e => { const o = nav.classList.toggle('open'); e.currentTarget.setAttribute('aria-expanded', o); });
})();

/* Lightbox for any image gallery marked data-gallery */
function lightbox(selector){
  const imgs = [...document.querySelectorAll(selector)]; if (!imgs.length) return;
  const box = document.createElement('div'); box.className = 'lightbox'; box.setAttribute('role','dialog');
  box.innerHTML = '<button class="lb-close" aria-label="Close">×</button><button class="lb-prev" aria-label="Previous">‹</button><img alt=""><button class="lb-next" aria-label="Next">›</button>';
  document.body.appendChild(box);
  const big = box.querySelector('img'); let i = 0;
  const show = n => { i = (n + imgs.length) % imgs.length; big.src = imgs[i].dataset.full; big.alt = imgs[i].alt; };
  imgs.forEach((im, n) => { im.style.cursor = 'zoom-in'; im.tabIndex = 0; const open = () => { show(n); box.classList.add('open'); }; im.addEventListener('click', open); im.addEventListener('keydown', e => e.key === 'Enter' && open()); });
  box.querySelector('.lb-close').onclick = () => box.classList.remove('open');
  box.querySelector('.lb-prev').onclick = () => show(i - 1);
  box.querySelector('.lb-next').onclick = () => show(i + 1);
  box.addEventListener('click', e => { if (e.target === box) box.classList.remove('open'); });
  document.addEventListener('keydown', e => { if (!box.classList.contains('open')) return; if (e.key === 'Escape') box.classList.remove('open'); if (e.key === 'ArrowLeft') show(i - 1); if (e.key === 'ArrowRight') show(i + 1); });
}
