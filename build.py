import json, html
W = lambda i, w=600, h=None: f"https://static.wixstatic.com/media/{i}/v1/fill/w_{w},h_{h or int(w*0.66)},al_c,q_85/img.jpg"
FIT = lambda i, w=1600: f"https://static.wixstatic.com/media/{i}/v1/fit/w_{w},h_{w},q_90/img.jpg"
OLD = "https://www.vkvsir.com"

def page(fname, title, desc, body, script=""):
    open(fname, "w").write(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="https://static.wixstatic.com/media/b90d41_c42d4694683b4a9b8599e2321e7a0d1f~mv2.jpg">
<meta name="google-site-verification" content="6SKN6jL13ZKnwFayefSH5_D0gb4olI3XBhQWLGzdgRY">
<link rel="icon" href="https://static.wixstatic.com/media/b90d41_2891d42aeac74eb783f9e95cded38f1e~mv2.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800&family=Oswald:wght@400;500&family=Lora:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<div id="site-header"></div>
<main>
{body}
</main>
<div id="site-footer"></div>
<script src="assets/site.js"></script>
{script}
</body>
</html>
""")

def banner(title, sub=""):
    return f'<section class="banner"><div class="wrap"><p class="crumbs"><a href="./">Home</a> › {title}</p><h1>{title}</h1>{f"<p>{sub}</p>" if sub else ""}</div></section>'

# ---------------- BLOG DATA (from Wix blog) ----------------
from posts import POSTS
posts=[dict(title=t,url=OLD+"/post/"+sl,date=d,img=im,kind=k,excerpt=ex) for t,sl,d,im,k,ex in POSTS]

def post_cards(items):
    out = []
    for p in items:
        from datetime import date
        d = date.fromisoformat(p["date"]).strftime("%d %b %Y")
        im = f'<img loading="lazy" src="{p["img"]}" alt="{html.escape(p["title"])}">' if p["img"] else '<img alt="" style="background:linear-gradient(135deg,#f5c242,#e8742b)">'
        ex = f'<span class="m">{html.escape(p["excerpt"][:110])}{"…" if len(p["excerpt"])>110 else ""}</span>' if p["excerpt"] else ""
        out.append(f'<a class="card" href="{p["url"]}" data-year="{p["date"][:4]}">{im}<div class="body"><span class="tag">{p["kind"]} · {d}</span><span class="t">{html.escape(p["title"])}</span>{ex}</div></a>')
    return "\n".join(out)

# ---------------- HOME ----------------
media_home = ["b90d41_f8d7b46bf8ef4e02a2f843e58c2fdf16~mv2.jpg","b90d41_ae1e83e73dd6481598341637786512d7~mv2.jpg","b90d41_f092db602bf744719a308a9403cb38a4~mv2.jpg","b90d41_de1bdfb6fbee45d48ef1c051f74ae05e~mv2.jpeg","b90d41_37ebd5a8adc548abab515507462c8ccb~mv2.jpeg","b90d41_1fb7211d22994a669b0071c450a3e3ed~mv2.jpg","b90d41_3092ac066fe54b44a1a853116385b953~mv2.jpg","b90d41_b3fa9e02c8af40e6bd557244e44df2ef~mv2.jpg","b90d41_13e95f61ad114a59b38860e2a7316532~mv2.jpg","b90d41_0504ef60c2e14cea83781638f9bac1de~mv2.jpeg"]
views = ["b90d41_4b0b2e74e44241968531a826ee177608~mv2.png","b90d41_1eceb170101d4e18a61b447ab23b4892~mv2.png","b90d41_883c935dac5a4542a30294f91f8fb922~mv2.png","b90d41_d75231deb0d84b6caa5cd3ff86bd9cd5~mv2.png","b90d41_b13b4fe9d1964223a95e5da29c2073a3~mv2.png","b90d41_e2e15e52de6e4d9f9c2342a5dfd74afa~mv2.png","b90d41_6cc1a4a2b7cd432bb5fd1d633638432d~mv2.png","b90d41_142d5d1f99f6466bba10646d3e681be9~mv2.png"]
home_courses = [("Automobile Engineering",f"{OLD}/automobile-engineering","11062b_42b9ecea6a1540668defdedea80d1a9d~mv2.jpg"),("Workshop Practice",f"{OLD}/workshop-practice","e592d5b87e234c849e8363ee949932a0.jpg"),("Hybrid & Electric Vehicles",f"{OLD}/hev","nsplsh_7d668a14fefe4074a5acad37439a215e~mv2.jpg")]
home_css = """<style>
.hero{background:radial-gradient(circle at 80% 40%,#1a5a4c 0,var(--hero-bg) 55%);color:var(--hero-text);overflow:hidden}
.hero .wrap{display:grid;grid-template-columns:1.1fr .9fr;gap:30px;align-items:center;padding-top:50px;padding-bottom:50px}
.rule{display:block;width:90px;height:4px;border-radius:2px;background:var(--gold);margin-bottom:18px}
.hero h1{font-family:var(--font-title);color:var(--gold);font-size:clamp(34px,5vw,58px);margin:0 0 10px}
.hero .he{font-size:20px;margin:0 0 6px;font-style:italic}
.hero .lines p{margin:2px 0;font-size:clamp(18px,2vw,23px)}
.hero blockquote{margin:22px 0 0;font-style:italic;color:var(--gold);font-size:18px}
.hero-photo{justify-self:center;max-width:420px;filter:drop-shadow(0 18px 30px rgba(0,0,0,.45))}
.media-strip{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}
.media-strip img{width:100%;height:150px;object-fit:cover;border-radius:6px}
.slider{position:relative;max-width:440px;margin:0 auto;aspect-ratio:503/671;overflow:hidden;border-radius:14px;background:#f3f6f4;box-shadow:0 10px 30px rgba(14,58,54,.18)}
.slider img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;opacity:0;transition:opacity .8s}
.slider img.on{opacity:1}
.slide-nav{position:absolute;top:50%;transform:translateY(-50%);width:40px;height:40px;border-radius:50%;border:0;background:rgba(255,255,255,.9);color:var(--title);font-size:22px;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.2);z-index:2}
.slide-nav.prev{left:10px}.slide-nav.next{right:10px}
.dots{display:flex;justify-content:center;gap:8px;margin-top:14px}
.dots button{width:11px;height:11px;border-radius:50%;border:0;background:#b9c9c4;cursor:pointer;padding:0}
.dots button.on{background:var(--accent)}
.fun{position:relative;color:#fff;text-align:center;padding:110px 20px;background:center/cover no-repeat}
.fun::before{content:"";position:absolute;inset:0;background:rgba(10,40,35,.55)}
.fun>*{position:relative}.fun h2{font-family:var(--font-title);font-size:clamp(30px,5vw,54px);margin:0 0 20px;color:#fff}
.join{background:var(--hero-bg);color:var(--hero-text);text-align:center;padding:60px 20px}
.join h2{font-family:var(--font-title);color:var(--gold);margin:0 0 8px;font-size:clamp(24px,3vw,34px)}
.join p{margin:0 auto 22px;max-width:620px}
@media (max-width:860px){.hero .wrap{grid-template-columns:1fr;text-align:center}.rule{margin:0 auto 18px}}
</style>"""
lines = ["a professor by profession,","an innovator by intelligence,","a motivator by mood,","brilliant with brain &amp;","humble with heart."]
home = home_css + f"""
<section class="hero"><div class="wrap">
  <div><span class="rule" aria-hidden="true"></span><h1>Vinod Kr. Verma</h1><p class="he">He is</p>
    <div class="lines">{''.join(f'<p>{l}</p>' for l in lines)}</div>
    <blockquote>"In today's era, there is nothing better than human networking!!" … VKVSir</blockquote>
    <p style="margin-top:26px"><a class="btn gold" href="about">Know more about him</a></p></div>
  <img class="hero-photo" src="https://static.wixstatic.com/media/b90d41_0e9d277a56394502abc7bd99cb2779c1~mv2.png/v1/crop/x_110,y_0,w_1074,h_1296/fill/w_433,h_519,al_c,q_85/vinod3_edited.png" alt="Prof. Vinod Kumar Verma">
</div></section>
<section class="block"><div class="wrap"><h2>Media Appearances of VKVSir</h2><p class="lead">This is a section showing the media appearances of VKV sir.</p>
  <div class="media-strip">{''.join(f'<img loading="lazy" src="{W(i,400,300)}" data-full="{FIT(i)}" alt="Media appearance of VKV Sir" class="g">' for i in media_home)}</div>
  <div class="center"><a class="btn" href="media">View More Media</a></div></div></section>
<section class="block alt"><div class="wrap"><h2>Courses Conducted</h2>
  <p class="lead">He loves to teach his students by meeting them at their level. Once the students feel comfortable with him, they begin to ask questions and engage fully in VKV Sir's class. VKV Sir believes in his students and allows them to make their own choices, whether right or wrong.</p>
  <div class="grid">{''.join(f'<a class="card" href="{u}"><img loading="lazy" src="{W(i)}" alt="{t}"><div class="body"><span class="t" style="text-align:center">{t}</span></div></a>' for t,u,i in home_courses)}</div>
  <div class="center"><a class="btn ghost" href="courses">See all courses</a></div></div></section>
<section class="block"><div class="wrap"><h2>His Views for Teachers &amp; Students</h2>
  <div class="slider" id="slider">{''.join(f'<img src="https://static.wixstatic.com/media/{i}/v1/fit/w_880,h_1180,q_90/v.png" alt="VKV Sir\'s view {n+1}" class="{"on" if n==0 else ""}" {"loading=lazy" if n else ""}>' for n,i in enumerate(views))}<button class="slide-nav prev" aria-label="Previous view">‹</button><button class="slide-nav next" aria-label="Next view">›</button></div>
  <div class="dots" id="dots">{''.join(f'<button aria-label="Show view {n+1}" class="{"on" if n==0 else ""}"></button>' for n in range(len(views)))}</div></div></section>
<section class="fun" style="background-image:url('https://static.wixstatic.com/media/11062b_07608b0b281a42bcafaea6a99b070d47f000.jpg/v1/fill/w_1600,h_900,al_c,q_80/fun.jpg')"><h2>Learning Online is Fun</h2><a class="btn gold" href="courses">View Online Courses</a></section>
<section class="block"><div class="wrap"><h2>Posts &amp; Articles</h2>
  <p class="lead">By posting good content and information, he would like to help and update his peers so we can help each other directly or indirectly. In today's world networking is the key to success!</p>
  <div class="grid">{post_cards(posts[:3])}</div>
  <div class="center"><a class="btn" href="blog">View More Blogs</a></div></div></section>
<section class="join"><h2>Get free PDFs, MCQs &amp; full lectures</h2><p>Membership is free for our YouTube subscribers. Sign in with the Google account you use on YouTube and get access in seconds.</p><a class="btn yt" href="{OLD}/apply">Join Membership – Free</a></section>
"""
home_js = """<script>
lightbox('.media-strip img.g');
(() => { const imgs=[...document.querySelectorAll('#slider img')], dots=[...document.querySelectorAll('#dots button')]; let i=0, t;
 const show=n=>{imgs[i].classList.remove('on');dots[i].classList.remove('on');i=(n+imgs.length)%imgs.length;imgs[i].classList.add('on');dots[i].classList.add('on');};
 const start=()=>{ if(!matchMedia('(prefers-reduced-motion: reduce)').matches) t=setInterval(()=>show(i+1),4000); };
 const jump=n=>{clearInterval(t);show(n);start();};
 dots.forEach((d,n)=>d.onclick=()=>jump(n));
 document.querySelector('.slide-nav.prev').onclick=()=>jump(i-1); document.querySelector('.slide-nav.next').onclick=()=>jump(i+1); start(); })();
</script>"""
page("index.html","Academician | Vkvsir | India","Learning with vkvsir is fun. All course are in hindi & english with animations, ppt, pdf and objective question / mcq. Full course lectures of Automobile engineering, Hybrid & Electric Vehicles (HEV), Workshop, Drawing etc.",home,home_js)

# ---------------- ABOUT ----------------
about = banner("About", "Vinod Kumar Verma (Ph.D.*, M. Tech., MBA)") + """
<style>.about-grid{display:grid;grid-template-columns:.8fr 1.2fr;gap:40px;align-items:start}.about-grid img{border-radius:12px;box-shadow:var(--shadow)}
.facts{display:grid;gap:14px}.fact{background:var(--card);border-left:4px solid var(--gold);padding:14px 18px;border-radius:8px;box-shadow:var(--shadow)}.fact b{font-family:var(--font-nav);font-weight:500;color:var(--title);font-size:18px;display:block}
.sanskrit{text-align:center;font-size:20px;color:var(--title);margin-top:26px}
@media(max-width:860px){.about-grid{grid-template-columns:1fr}}</style>
<section class="block"><div class="wrap about-grid">
 <img src="https://static.wixstatic.com/media/19fa25ac40be44df99cd64854ce1ee7e.jpg/v1/crop/x_0,y_0,w_1366,h_1080/fill/w_779,h_612,al_c,q_85/Contractors.jpg" alt="Engineering at work">
 <div class="facts">
  <div class="fact"><b>Bio</b>Mr. Vinod Kr. Verma is a faculty in the Department of Mechanical Engineering at Engineering College Ajmer, since 2008. He is known for his excellence in the field of Automobile Engineering, Renewable Energy, Marketing, and New Product Design &amp; Launching.</div>
  <div class="fact"><b>Education</b>He was a Topper in Diploma (Govt. Polytechnic Kota), B.E (MBM Jodhpur), M. Tech (IIT Jodhpur), Ph.D.* and MBA-Marketing (Symbiosis University).</div>
  <div class="fact"><b>Experience</b>He has 5 Yr+ Industrial experience (2 Yr in Dubai &amp; Afghanistan + 3 Yrs in India) &amp; 14 Yr+ Teaching experience with a goal to enhance &amp; strengthen the young generation with good quality education and to create tremendous opportunities for them.</div>
  <div class="fact"><b>Achievements</b>He received many Awards &amp; Appreciations like by Former President Late Mr. Pranab Mukharejee, MHRD Minister Mr. Satyapal Singh, Education Minister of Rajasthan, District Collector of Ajmer, and from many more dignitaries.</div>
  <div class="fact"><b>Milestones</b>He has one published patent, publications in many reputed National &amp; International Journals, SAE Founder at ECA, Participate in BAJA Main round, Organized 60+ seminar/tours/workshops for students. Delivered many lectures as an expert and keynote speaker.</div>
 </div></div>
 <p class="sanskrit">सर्वे भवन्तु सुखिनः<br>Jai Hind!</p></section>
<section class="block alt"><div class="wrap about-grid">
 <img src="https://static.wixstatic.com/media/b90d41_4866adbee9464682abf4a1dfda66fb69~mv2.png/v1/crop/x_185,y_93,w_1153,h_1407/fill/w_436,h_532,al_c,q_85/vinod1_edited.png" alt="VKV Sir">
 <div class="prose"><h2>More about VKVSir</h2>
 <p>Welcome to the official website of Prof. Vinod Kumar Verma, affectionately known as VKVSir, a distinguished figure in the realm of automobile engineering, manufacturing processes, and innovation.</p>
 <p>With over two decades of combined experience in both corporate and academic spheres, Prof. Vinod Kumar Verma brings a wealth of knowledge and expertise to the table. Having spent five years in the corporate world, including a two-year stint abroad as a project manager, he possesses invaluable insights into real-world challenges and solutions.</p>
 <p>However, it is his passion for education and innovation that truly sets him apart. With more than 17 years of teaching experience, Prof. Verma has nurtured countless young minds, guiding them towards their academic and professional aspirations. He is renowned for his dedication to fostering innovation, evident in his numerous research publications and a patented invention in his name.</p>
 <p>Beyond academia, Prof. Verma is celebrated for his role as a mentor and motivator. Students flock to him for career advice and personal guidance, drawn by his genuine desire to see them succeed. As a coordinator in the training and placement cell, he bridges the gap between academia and industry, forging partnerships with leading companies and HR professionals.</p>
 <p>Prof. Verma's academic journey is equally illustrious, with a graduation from MBM Engineering College, Jodhpur, followed by research endeavors at the prestigious Indian Institute of Technology, Jodhpur, and an MBA from Symbiosis, Pune.</p>
 <p>Always at the forefront of networking and engagement, Prof. Verma maintains an active presence on <a href="https://www.linkedin.com/in/vkvsir" target="_blank" rel="noopener">LinkedIn</a>, ensuring that his expertise and mentorship reach a global audience.</p>
 <p>Join us in exploring the multifaceted world of Prof. Vinod Kumar Verma, where education, innovation, and mentorship converge to shape the leaders of tomorrow.</p>
 <p><a class="btn" href="contact">Contact VKVSir</a></p></div></div></section>"""
page("about.html","About | vkvsir","Welcome to the official website of Prof. Vinod Kumar Verma, affectionately known as VKVSir, a distinguished figure in the realm of automobile engineering, manufacturing processes, and innovation.",about)

# ---------------- COURSES ----------------
courses = [("Automobile Engineering","11062b_42b9ecea6a1540668defdedea80d1a9d~mv2.jpg",f"{OLD}/automobile-engineering"),
 ("Machine Drawing","7fba3905ea184ee29642cf0def056821.jpg",f"{OLD}/automobile-engineering"),
 ("Workshop Practice","e592d5b87e234c849e8363ee949932a0.jpg",f"{OLD}/workshop-practice"),
 ("Casting Process","aef2ab657d574a17adc9dc6a7312c958.jpg",f"{OLD}/automobile-engineering"),
 ("Hybrid & Electric Vehicles","11062b_0d56d33639234010a96c69ca297bf60a~mv2.jpg",f"{OLD}/hev"),
 ("New Product Design","9d090cf24c96432db9c956dbdac792f6.jpg",f"{OLD}/pdl")]
cbody = banner("Courses Taught","Full course lectures in Hindi &amp; English with animations, PPTs, PDFs and MCQs. Course pages are in the free Members Area.") + f"""
<section class="block"><div class="wrap"><div class="grid">
{''.join(f'<a class="card" href="{u}"><img loading="lazy" src="{W(i)}" alt="{t}"><div class="body"><span class="t">{t}</span><span class="m">View full course →</span></div></a>' for t,i,u in courses)}
</div></div></section>
<section class="block alt"><div class="wrap" style="text-align:center"><h2>Practice sheet</h2><p class="lead">MVSI / RTO Inspector Practice Sheet 1</p><a class="btn" href="https://forms.gle/uDEB4LovbrKjtFTH9" target="_blank" rel="noopener">Open practice sheet</a>
<p class="lead" style="margin-top:30px">Course pages need free membership.</p><a class="btn yt" href="{OLD}/apply">Join Membership – Free</a></div></section>"""
page("courses.html","Courses | vkvsir","Courses by Prof. Vinod Kumar Verma: Automobile Engineering, Machine Drawing, Workshop Practice, Casting Process, Hybrid & Electric Vehicles and New Product Design.",cbody)

# ---------------- MEDIA ----------------
media = [("b90d41_92b1f87de246438386291d40d248e62b~mv2.jpg","PCRA"),("b90d41_ba9d6f25da3d449eaffd545359b5f097~mv2.jpeg","Dainik NavJyoti 23 May 2018"),("b90d41_6e032864d49c412f9950856d0d3ee018~mv2.jpg","Bhaskar & Patrika 17 Aug 2017"),("b90d41_963bdfc7ea9d4260838aaced8793fc8a~mv2.jpeg","Dainik Bhaskar 23 May 2018"),("b90d41_6f3957c5d8504c8d845fc6fc8ead26d2~mv2.jpg","Bhaskar 30 June 2017"),("b90d41_7cec79804645421a83efd91284441225~mv2.jpg","Bhaskar 19 Sep 2017"),("b90d41_2f515a0836eb4cf3b7303f9c41419bfb~mv2.jpg","Bhaskar 7 Oct 2016"),("b90d41_72163043971a4e49a9479397ab2d1168~mv2.jpg","Automatic Gear System"),("b90d41_eb2104b6597649e4a5c0b65bd44f0619~mv2.jpg","Anti-roll braking news"),("b90d41_22ccfd37e9384f73a0c6540086034ff0~mv2.jpg","Airforce seminar"),("b90d41_1323325e93a44bab99e23dcca99bb22f~mv2.jpg","Airforce seminar"),("b90d41_fabdd8eeadc5438fb668094ed3bd18e5~mv2.jpg","Bhaskar & Patrika 17 Aug 2017"),("b90d41_d2b156d8092848489d33c90634c0b568~mv2.jpg","Bhaskar 12 Aug 2016"),("b90d41_d87f56553ddc4852b747b20ab28cde90~mv2.png","Bhaskar BAJA 3 Sep 2018"),("b90d41_0a6314db80f148f2837606043d55ac01~mv2.jpg","Patrika 17 Aug 2017"),("b90d41_00ace1642c7e41c883b7f5cc13a93806~mv2.jpg","Patrika 17 Aug 2017"),("b90d41_b9aaebb9bd604fa8b5854408b7173a8b~mv2.jpg","Silicon Valley Smart Stick (Bhaskar 23 July 2018)"),("b90d41_2b0fabb766804dd18cac674d3abd6f79~mv2.jpeg","Bhaskar 16 March 2021"),("b90d41_efc2ea2689de462b91981f586dd4ba01~mv2.jpeg","Dainik NavJyoti 23 May 2018"),("b90d41_9f2ea0acbea04b7bacba6478d1de33ae~mv2.jpg","Dainik Bhaskar 23 May 2018"),("b90d41_0c3c0aba71354922833dfb52621aea4d~mv2.jpeg","Bhaskar 20 March 2021"),("b90d41_ea9d919649d64b1a8ab7028e786125ff~mv2.jpeg","Navjyoti 16 March 2021"),("b90d41_9bb6427654b3401f839048387e53d890~mv2.jpg","Dainik Navjyoti Ajmer 16 March 2021"),("b90d41_707b8c2b5b8a4269a47936ebb093cf24~mv2.jpg","Rajasthan Patrika Ajmer 16 March 2021"),("b90d41_139f4d7b832a4ca08979443334c181c7~mv2.jpg","Media appearance")] + [(i,"Media appearance of VKV Sir") for i in media_home]
mbody = banner("Media Appearances","Newspaper coverage, seminars and innovations. Tap any picture to view it large.") + f"""
<style>.masonry{{columns:4 240px;column-gap:14px}}.masonry figure{{margin:0 0 14px;break-inside:avoid;background:var(--card);border-radius:8px;overflow:hidden;box-shadow:var(--shadow)}}.masonry img{{width:100%;height:auto}}.masonry figcaption{{font-size:13.5px;color:var(--muted);padding:8px 10px}}</style>
<section class="block"><div class="wrap"><div class="masonry">
{''.join(f'<figure><img loading="lazy" src="https://static.wixstatic.com/media/{i}/v1/fit/w_500,h_900,q_85/m.jpg" data-full="{FIT(i)}" alt="{html.escape(c)}"><figcaption>{html.escape(c)}</figcaption></figure>' for i,c in media)}
</div></div></section>"""
page("media.html","Media | vkvsir","Media appearances of Prof. Vinod Kumar Verma: newspaper coverage, seminars, student innovations and awards.",mbody,"<script>lightbox('.masonry img')</script>")

# ---------------- TEST & ANALYSIS ----------------
tbody = banner("Test and Analysis","Check your understanding with quizzes and practice tests.") + f"""
<section class="block"><div class="wrap"><div class="grid">
 <a class="card" href="https://forms.gle/uDEB4LovbrKjtFTH9" target="_blank" rel="noopener"><div class="body"><span class="tag">Practice</span><span class="t">MVSI / RTO Inspector Practice Sheet 1</span><span class="m">Open in Google Forms</span></div></a>
 <a class="card" href="{OLD}/quiz"><div class="body"><span class="tag">Members</span><span class="t">Course quizzes</span><span class="m">Unit-wise quizzes in the Members Area</span></div></a>
 <a class="card" href="courses"><div class="body"><span class="tag">Courses</span><span class="t">PPTs, PDFs &amp; full lectures</span><span class="m">For more quiz and PPT/PDFs visit the Full Course pages (Membership Area)</span></div></a>
</div>
<div class="center"><a class="btn yt" href="{OLD}/apply">Join Membership – Free</a></div></div></section>"""
page("test-and-analysis.html","Test and Analysis | vkvsir","Quizzes, practice tests and analysis for automobile engineering, workshop and more by VKVSir.",tbody)

# ---------------- BLOG ----------------
years = sorted({p["date"][:4] for p in posts}, reverse=True)
bbody = banner("Blog &amp; LinkedIn","Posts, wishes, events and thoughts from VKVSir.") + f"""
<style>.filters{{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-bottom:26px}}.filters button{{font-family:var(--font-nav);font-size:15px;border:1px solid var(--accent);background:#fff;color:var(--accent);padding:6px 16px;border-radius:20px;cursor:pointer}}.filters button.on{{background:var(--accent);color:#fff}}</style>
<section class="block"><div class="wrap">
<div class="filters" role="group" aria-label="Filter by year"><button class="on" data-y="all">All</button>{''.join(f'<button data-y="{y}">{y}</button>' for y in years)}</div>
<div class="grid" id="posts">{post_cards(posts)}</div>
<div class="center"><a class="btn ghost" href="https://www.linkedin.com/in/vkvsir" target="_blank" rel="noopener">Follow on LinkedIn</a></div></div></section>"""
bjs = """<script>document.querySelectorAll('.filters button').forEach(b=>b.onclick=()=>{document.querySelectorAll('.filters button').forEach(x=>x.classList.toggle('on',x===b));document.querySelectorAll('#posts .card').forEach(c=>c.hidden=!(b.dataset.y==='all'||c.dataset.year===b.dataset.y));});</script>"""
page("blog.html","Blog & Linkedin | vkvsir","Posts and articles by Prof. Vinod Kumar Verma (VKVSir).",bbody,bjs)

# ---------------- FAQ ----------------
faqs = [
 ("What subject/topic does VKVSir like most?", 'He likes to experiment with new topics and fields especially technical stuff. He likes to work on innovations, new ideas and develop new products and solutions. His delivered major <a href="courses">courses</a> are on Automobile, Hybrid &amp; Electric Vehicles, Robotics, Renewable Energy Sources, Solar Energy, App development, IoT, Machine Learning, AI &amp; AR, etc.'),
 ("Does VKVSir take expert lectures and talks?", 'Yes, but through proper channel. Drop an <a href="mailto:vinodvermavkvsir@gmail.com">email</a> with all details.'),
 ("Does VKVSir take interns &amp; project association from other institutes or industries?", "Yes, but through proper channel."),
 ("Does VKVSir take subject tuitions?", "No."),
 ("Does VKVSir take career counseling? If yes, what are the charges?", "Yes, and it's free of cost. It is subject to the availability of his time &amp; domain."),
 ("How to contact or follow VKVSir?", 'You can visit the <a href="contact">contact page</a> of the website or message through the website chat option.'),
 ("How to get membership &amp; access to premium content on this site?", f'Premium content like PPT/PDF, objective &amp; subjective questions, etc. is absolutely FREE for all. Membership is now automatic: subscribe to our <a href="https://www.youtube.com/@vkvsirdotcom?sub_confirmation=1" target="_blank" rel="noopener">YouTube channel</a> (or comment on 5+ of our videos), then <a href="{OLD}/apply">apply here</a> with the same Google account. Your YouTube account must be at least 1 month old. Subscribers get access within seconds.'),
]
fbody = banner("Frequently Asked Questions") + f"""
<style>.faq details{{background:var(--card);border-radius:10px;box-shadow:var(--shadow);margin-bottom:12px}}.faq summary{{cursor:pointer;padding:16px 20px;font-family:var(--font-nav);font-size:19px;color:var(--title);list-style:none;display:flex;justify-content:space-between;gap:12px}}.faq summary::-webkit-details-marker{{display:none}}.faq summary::after{{content:"+";font-size:24px;line-height:1}}.faq details[open] summary::after{{content:"–"}}.faq .a{{padding:0 20px 18px}}</style>
<section class="block"><div class="wrap narrow faq">
{''.join(f'<details{" open" if n==0 else ""}><summary>{q}</summary><div class="a">{a}</div></details>' for n,(q,a) in enumerate(faqs))}
<p class="lead" style="margin-top:30px">The VKVSIR website assists students in learning about automobile engineering, manufacturing processes, machine drawing, workshop technology, AutoCAD, and various other subjects in both English &amp; Hindi. All contents are free of charge.</p>
</div></section>"""
page("faq.html","FAQ | vkvsir","Frequently asked questions about VKVSir, membership, lectures, internships and career counseling.",fbody)

# ---------------- CONTACT ----------------
contacts = [("YouTube Channel","https://www.youtube.com/@vkvsirdotcom?sub_confirmation=1","nsplsh_c92ddf0e17e64aef930643cfe2cec7f1~mv2.jpg"),("Instagram","https://www.instagram.com/vkvsir","nsplsh_27541482937644aeb058cc4998e51b0e~mv2.jpg"),("vinodvermavkvsir@gmail.com","mailto:vinodvermavkvsir@gmail.com","nsplsh_0a3bd89c78f542d3ad247cc9b6fa9efc~mv2.jpg"),("LinkedIn","https://www.linkedin.com/in/vkvsir","nsplsh_087084d9ec1f4dc7acf02f741b729a46~mv2.jpg"),("Twitter","https://www.twitter.com/vkvsir","nsplsh_3cf8ac6146fb419c9f5624a4a7a6150c~mv2.jpg"),("Telegram","https://t.me/vkvsir","nsplsh_956aa20fafab4cf9b5149b0cf8b50aff~mv2.jpg"),("Facebook","https://www.facebook.com/vkvsir","nsplsh_29e5af0fac174538ab715092c01770ed~mv2.jpg"),("Pinterest","https://www.pinterest.com/vkvsir/","11062b_f6a4cd17d3354ebaada954f7d3239380~mv2.jpg")]
ctbody = banner("Contact / Follow us at") + f"""
<style>.addr{{display:grid;grid-template-columns:1fr 1fr;gap:30px;align-items:center}}.addr iframe{{width:100%;height:280px;border:0;border-radius:10px}}@media(max-width:860px){{.addr{{grid-template-columns:1fr}}}}</style>
<section class="block"><div class="wrap"><div class="grid">
{''.join(f'<a class="card" href="{u}" {"" if u.startswith("mailto") else "target=_blank rel=noopener"}><img loading="lazy" src="{W(i,500,330)}" alt=""><div class="body"><span class="t" style="text-align:center;word-break:break-word">{t}</span></div></a>' for t,u,i in contacts)}
</div></div></section>
<section class="block alt"><div class="wrap addr">
 <div class="prose"><h2>Address</h2><p>Prof. Vinod Kumar Verma<br>NB-202, New Building,<br>Engineering College Ajmer<br>Rajasthan, India<br>305025</p><p><a class="btn" href="mailto:vinodvermavkvsir@gmail.com">Send an email</a></p></div>
 <iframe loading="lazy" title="Map of Engineering College Ajmer" src="https://www.google.com/maps?q=Government+Engineering+College+Ajmer&output=embed"></iframe>
</div></section>"""
page("contact.html","Contact | vkvsir","Contact Prof. Vinod Kumar Verma (VKVSir): YouTube, Instagram, email, LinkedIn, Twitter, Telegram, Facebook, Pinterest and address.",ctbody)

# 404 page → home
page("404.html","Page not found | vkvsir","Page not found",banner("Page not found","The page you are looking for has moved.")+'<section class="block"><div class="wrap center"><a class="btn" href="./">Go to homepage</a></div></section>')
print("built", len(posts), "posts")
