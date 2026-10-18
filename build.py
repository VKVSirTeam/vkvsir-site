# Builds every page of the site. Run: python3 build.py
import json, html
from datetime import date
from posts import POSTS
E = html.escape
DOMAIN = "https://www.vkvsir.com"        # final domain (used for SEO canonical links & sitemap)
OLD = "https://www.vkvsir.com"           # Wix pages still used (members area, blog posts)
TESTLAB = "https://test.vkvsir.com"
def W(i, w=600, h=400, q=80): return f"https://static.wixstatic.com/media/{i}/v1/fill/w_{w},h_{h},al_c,q_{q},enc_auto/i.jpg"
def FIT(i, w=1600): return f"https://static.wixstatic.com/media/{i}/v1/fit/w_{w},h_{w},q_85,enc_auto/i.jpg"
def IMG(i, w, h, alt, cls="", eager=False):
    return (f'<img src="{W(i,w,h)}" srcset="{W(i,w//2,h//2)} {w//2}w, {W(i,w,h)} {w}w" sizes="(max-width:600px) 100vw, {w}px" '
            f'width="{w}" height="{h}" alt="{E(alt)}"{" class="+chr(34)+cls+chr(34) if cls else ""} {"fetchpriority=high" if eager else "loading=lazy decoding=async"}>')

PERSON = {"@type":"Person","@id":DOMAIN+"/#person","name":"Prof. Vinod Kumar Verma","alternateName":["VKVSir","Vinod Kr. Verma","VKV Sir"],
 "jobTitle":"Professor, Department of Mechanical Engineering","url":DOMAIN,"email":"mailto:vinodvermavkvsir@gmail.com",
 "image":"https://static.wixstatic.com/media/b90d41_0e9d277a56394502abc7bd99cb2779c1~mv2.png",
 "worksFor":{"@type":"CollegeOrUniversity","name":"Government Engineering College Ajmer","address":{"@type":"PostalAddress","streetAddress":"NH-8, Barliya Circle","addressLocality":"Ajmer","addressRegion":"Rajasthan","postalCode":"305025","addressCountry":"IN"}},
 "alumniOf":["MBM Engineering College, Jodhpur","Indian Institute of Technology Jodhpur","Symbiosis International University"],
 "knowsAbout":["Automobile Engineering","Hybrid and Electric Vehicles","Renewable Energy","Workshop Technology","Machine Drawing","Manufacturing Processes","New Product Design and Launching"],
 "sameAs":["https://www.youtube.com/@vkvsirdotcom","https://www.linkedin.com/in/vkvsir","https://www.facebook.com/vkvsir","https://www.instagram.com/vkvsir","https://www.twitter.com/vkvsir","https://t.me/vkvsir","https://scholar.google.com/citations?user=CDzm7o8AAAAJ"]}

def page(slug, title, desc, body, script="", extra_ld=None, crumbs=None):
    url = DOMAIN + ("/" if slug == "index" else "/" + slug)
    ld = [{"@context":"https://schema.org","@type":"WebSite","@id":DOMAIN+"/#site","name":"VKVSir","url":DOMAIN+"/","inLanguage":"en-IN","publisher":{"@id":DOMAIN+"/#person"}},
          dict({"@context":"https://schema.org"}, **PERSON)]
    if crumbs: ld.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":DOMAIN+"/"},{"@type":"ListItem","position":2,"name":crumbs,"item":url}]})
    if extra_ld: ld.append(extra_ld)
    fname = "index.html" if slug == "index" else slug + ".html"
    open(fname,"w").write(f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="Prof. Vinod Kumar Verma">
<meta name="theme-color" content="#0f3b33">
<meta property="og:type" content="website"><meta property="og:site_name" content="VKVSir">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="https://static.wixstatic.com/media/b90d41_c42d4694683b4a9b8599e2321e7a0d1f~mv2.jpg/v1/fit/w_1200,h_630,al_c/og.jpg">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:site" content="@vkvsir">
<meta name="google-site-verification" content="6SKN6jL13ZKnwFayefSH5_D0gb4olI3XBhQWLGzdgRY">
<link rel="icon" href="https://static.wixstatic.com/media/b90d41_2891d42aeac74eb783f9e95cded38f1e~mv2.png/v1/fit/w_64,h_64/f.png">
<link rel="apple-touch-icon" href="https://static.wixstatic.com/media/b90d41_2891d42aeac74eb783f9e95cded38f1e~mv2.png/v1/fit/w_180,h_180/a.png">
<link rel="preconnect" href="https://static.wixstatic.com">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Lora:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<div id="site-header"></div>
<main id="main">
{body}
</main>
<div id="site-footer"></div>
<script src="assets/site.js"></script>
{script}
</body>
</html>
""")

def banner(title, sub="", crumb=None):
    return f'<section class="banner"><div class="wrap"><p class="crumbs"><a href="./">Home</a> › {crumb or title}</p><h1>{title}</h1>{f"<p>{sub}</p>" if sub else ""}</div></section>'

posts = [dict(title=t,url=OLD+"/post/"+sl,date=d,img=im,kind=k,excerpt=ex) for t,sl,d,im,k,ex in POSTS]
def post_cards(items, reveal=False):
    out=[]
    for n,p in enumerate(items):
        d = date.fromisoformat(p["date"]).strftime("%d %b %Y")
        ph = f'<img src="{p["img"]}" alt="{E(p["title"])}" loading="lazy" decoding="async" width="600" height="400">' if p["img"] else '<div style="width:100%;height:100%;background:linear-gradient(135deg,#f5c242,#e8742b)"></div>'
        ex = f'<p>{E(p["excerpt"][:110])}{"…" if len(p["excerpt"])>110 else ""}</p>' if p["excerpt"] else ""
        rv = f' rv rv-d{n%3+1}' if reveal else ''
        out.append(f'<a class="card{rv}" href="{p["url"]}" data-year="{p["date"][:4]}"><div class="ph">{ph}</div><div class="bd"><span class="tag">{p["kind"]} · {d}</span><h3>{E(p["title"])}</h3>{ex}<span class="go link-more">Read post</span></div></a>')
    return "\n".join(out)

COURSES = [("Automobile Engineering","11062b_42b9ecea6a1540668defdedea80d1a9d~mv2.jpg",f"{OLD}/automobile-engineering","Engines, transmission, steering, brakes and vehicle systems explained with animations."),
 ("Hybrid & Electric Vehicles","11062b_0d56d33639234010a96c69ca297bf60a~mv2.jpg",f"{OLD}/hev","Batteries, motors, controllers and the technology shaping electric mobility."),
 ("Workshop Practice","e592d5b87e234c849e8363ee949932a0.jpg",f"{OLD}/workshop-practice","Welding, fitting, carpentry, smithy and safe shop-floor practice."),
 ("Machine Drawing","7fba3905ea184ee29642cf0def056821.jpg",f"{OLD}/automobile-engineering","Projections, sections, fasteners and assembly drawings, step by step."),
 ("Casting Process","aef2ab657d574a17adc9dc6a7312c958.jpg",f"{OLD}/automobile-engineering","Patterns, moulds, melting and defects in metal casting."),
 ("New Product Design & Launching","9d090cf24c96432db9c956dbdac792f6.jpg",f"{OLD}/pdl","From idea to market: design thinking, prototyping and launch strategy.")]
def course_cards(reveal=True):
    return "".join(f'<a class="card{" rv rv-d"+str(n%3+1) if reveal else ""}" href="{u}"><div class="ph">{IMG(i,600,400,t)}</div><div class="bd"><h3>{t}</h3><p>{d}</p><span class="go link-more">View full course</span></div></a>' for n,(t,i,u,d) in enumerate(COURSES))

MEDIA = [("b90d41_92b1f87de246438386291d40d248e62b~mv2.jpg","PCRA"),("b90d41_ba9d6f25da3d449eaffd545359b5f097~mv2.jpeg","Dainik NavJyoti, 23 May 2018"),("b90d41_6e032864d49c412f9950856d0d3ee018~mv2.jpg","Bhaskar & Patrika, 17 Aug 2017"),("b90d41_963bdfc7ea9d4260838aaced8793fc8a~mv2.jpeg","Dainik Bhaskar, 23 May 2018"),("b90d41_6f3957c5d8504c8d845fc6fc8ead26d2~mv2.jpg","Bhaskar, 30 June 2017"),("b90d41_7cec79804645421a83efd91284441225~mv2.jpg","Bhaskar, 19 Sep 2017"),("b90d41_2f515a0836eb4cf3b7303f9c41419bfb~mv2.jpg","Bhaskar, 7 Oct 2016"),("b90d41_72163043971a4e49a9479397ab2d1168~mv2.jpg","Automatic gear system"),("b90d41_eb2104b6597649e4a5c0b65bd44f0619~mv2.jpg","Anti-roll braking system"),("b90d41_22ccfd37e9384f73a0c6540086034ff0~mv2.jpg","Air Force seminar"),("b90d41_1323325e93a44bab99e23dcca99bb22f~mv2.jpg","Air Force seminar"),("b90d41_fabdd8eeadc5438fb668094ed3bd18e5~mv2.jpg","Bhaskar & Patrika, 17 Aug 2017"),("b90d41_d2b156d8092848489d33c90634c0b568~mv2.jpg","Bhaskar, 12 Aug 2016"),("b90d41_d87f56553ddc4852b747b20ab28cde90~mv2.png","Bhaskar – BAJA, 3 Sep 2018"),("b90d41_0a6314db80f148f2837606043d55ac01~mv2.jpg","Patrika, 17 Aug 2017"),("b90d41_00ace1642c7e41c883b7f5cc13a93806~mv2.jpg","Patrika, 17 Aug 2017"),("b90d41_b9aaebb9bd604fa8b5854408b7173a8b~mv2.jpg","Silicon Valley smart stick – Bhaskar, 23 July 2018"),("b90d41_2b0fabb766804dd18cac674d3abd6f79~mv2.jpeg","Bhaskar, 16 March 2021"),("b90d41_efc2ea2689de462b91981f586dd4ba01~mv2.jpeg","Dainik NavJyoti, 23 May 2018"),("b90d41_9f2ea0acbea04b7bacba6478d1de33ae~mv2.jpg","Dainik Bhaskar, 23 May 2018"),("b90d41_0c3c0aba71354922833dfb52621aea4d~mv2.jpeg","Bhaskar, 20 March 2021"),("b90d41_ea9d919649d64b1a8ab7028e786125ff~mv2.jpeg","Navjyoti, 16 March 2021"),("b90d41_9bb6427654b3401f839048387e53d890~mv2.jpg","Dainik Navjyoti Ajmer, 16 March 2021"),("b90d41_707b8c2b5b8a4269a47936ebb093cf24~mv2.jpg","Rajasthan Patrika Ajmer, 16 March 2021"),("b90d41_139f4d7b832a4ca08979443334c181c7~mv2.jpg","Media appearance"),
 ("b90d41_f8d7b46bf8ef4e02a2f843e58c2fdf16~mv2.jpg","Media appearance"),("b90d41_ae1e83e73dd6481598341637786512d7~mv2.jpg","Media appearance"),("b90d41_f092db602bf744719a308a9403cb38a4~mv2.jpg","Media appearance"),("b90d41_de1bdfb6fbee45d48ef1c051f74ae05e~mv2.jpeg","Media appearance"),("b90d41_37ebd5a8adc548abab515507462c8ccb~mv2.jpeg","Media appearance"),("b90d41_1fb7211d22994a669b0071c450a3e3ed~mv2.jpg","Media appearance"),("b90d41_3092ac066fe54b44a1a853116385b953~mv2.jpg","Media appearance"),("b90d41_b3fa9e02c8af40e6bd557244e44df2ef~mv2.jpg","Experimenting in lab"),("b90d41_13e95f61ad114a59b38860e2a7316532~mv2.jpg","College campus"),("b90d41_0504ef60c2e14cea83781638f9bac1de~mv2.jpeg","Students on a break")]
VIEWS = ["b90d41_4b0b2e74e44241968531a826ee177608~mv2.png","b90d41_1eceb170101d4e18a61b447ab23b4892~mv2.png","b90d41_883c935dac5a4542a30294f91f8fb922~mv2.png","b90d41_d75231deb0d84b6caa5cd3ff86bd9cd5~mv2.png","b90d41_b13b4fe9d1964223a95e5da29c2073a3~mv2.png","b90d41_e2e15e52de6e4d9f9c2342a5dfd74afa~mv2.png","b90d41_6cc1a4a2b7cd432bb5fd1d633638432d~mv2.png","b90d41_142d5d1f99f6466bba10646d3e681be9~mv2.png"]
FAQS = [
 ("What subject/topic does VKVSir like most?", 'He likes to experiment with new topics and fields, especially technical ones. He likes to work on innovations and new ideas and to develop new products and solutions. His major <a href="courses">courses</a> cover Automobile, Hybrid &amp; Electric Vehicles, Robotics, Renewable Energy Sources, Solar Energy, App development, IoT, Machine Learning, AI &amp; AR, etc.'),
 ("How do I get membership and access to premium content?", f'Premium content like PPT/PDF and objective &amp; subjective questions is absolutely free. Subscribe to our <a href="https://www.youtube.com/@vkvsirdotcom?sub_confirmation=1" target="_blank" rel="noopener">YouTube channel</a> (or comment on 5+ of our videos), then <a href="{OLD}/apply">apply here</a> with the same Google account. Your YouTube account must be at least 1 month old. Subscribers get access within seconds.'),
 ("Does VKVSir take career counseling? What are the charges?", "Yes, and it's free of cost, subject to the availability of his time &amp; domain."),
 ("Does VKVSir take expert lectures and talks?", 'Yes, but through proper channel. Drop an <a href="mailto:vinodvermavkvsir@gmail.com">email</a> with all details.'),
 ("Does VKVSir take interns &amp; project association from other institutes or industries?", "Yes, but through proper channel."),
 ("Does VKVSir take subject tuitions?", "No."),
 ("How do I contact or follow VKVSir?", 'Visit the <a href="contact">contact page</a> or message through the website chat option.')]
def faq_html(items): return "".join(f'<details class="rv"{" open" if n==0 else ""}><summary>{q}</summary><div class="a">{a}</div></details>' for n,(q,a) in enumerate(items))
FAQ_CSS = '<style>.faq details{background:#fff;border:1px solid var(--line);border-radius:var(--r);margin-bottom:12px;transition:box-shadow .2s}.faq details[open]{box-shadow:var(--sh)}.faq summary{cursor:pointer;padding:18px 22px;font-family:var(--f-head);font-weight:700;font-size:var(--step-1);color:var(--g800);list-style:none;display:flex;justify-content:space-between;gap:14px}.faq summary::-webkit-details-marker{display:none}.faq summary::after{content:"+";font-size:26px;line-height:1;color:var(--g500);transition:transform .2s}.faq details[open] summary::after{transform:rotate(45deg)}.faq .a{padding:0 22px 20px;color:var(--muted)}</style>'

# =================== HOME ===================
H_CSS = """<style>
.hero{background:radial-gradient(900px 520px at 85% 20%,#1f6253 0,transparent 62%),radial-gradient(600px 400px at 0 100%,#123f37 0,transparent 70%),var(--g900);color:#e4ece8;overflow:hidden;position:relative}
.hero .wrap:not(.stats-wrap){display:grid;grid-template-columns:1.15fr .85fr;gap:40px;align-items:center;padding:clamp(48px,7vw,90px) 0 0}
.hero h1{color:#fff;font-size:var(--step-4);margin:.1em 0 .3em}
.hero h1 span{display:block;color:var(--gold);font-size:.42em;font-weight:600;letter-spacing:.02em;margin-bottom:.4em}
.he{font-size:var(--step-1);line-height:1.6;color:#cfe0d9;margin:0 0 1.2em}
.he em{color:var(--lime);font-style:normal}
.quote{border-left:3px solid var(--gold);padding:4px 0 4px 16px;font-style:italic;color:#e9dcb8;margin:0 0 28px}
.actions{display:flex;gap:12px;flex-wrap:wrap}
.hero-ph{align-self:end;justify-self:center;position:relative;max-width:440px}
.hero-ph::before{content:"";position:absolute;inset:12% 6% 0;background:radial-gradient(circle,var(--gold) 0,transparent 68%);opacity:.28;filter:blur(10px)}
.hero-ph img{position:relative;filter:drop-shadow(0 24px 40px rgba(0,0,0,.45))}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:rgba(255,255,255,.1);border-radius:var(--r) var(--r) 0 0;overflow:hidden;margin-top:-1px}
.stats div{background:rgba(255,255,255,.04);padding:22px 18px;text-align:center}
.stats b{display:block;font-family:var(--f-head);font-size:var(--step-3);color:var(--gold);line-height:1}
.stats span{font-family:var(--f-head);font-size:14px;color:#b9cbc4}
.split{display:grid;grid-template-columns:.9fr 1.1fr;gap:clamp(30px,5vw,64px);align-items:center}
.split img{border-radius:var(--r-lg);box-shadow:var(--sh-lg);width:100%}
.ticks{list-style:none;padding:0;margin:0 0 24px;display:grid;gap:10px}
.ticks li{padding-left:30px;position:relative}
.ticks li::before{content:"";position:absolute;left:0;top:.45em;width:18px;height:18px;border-radius:50%;background:var(--g100) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3E%3Cpath d='M5 10l3 3 7-7' fill='none' stroke='%230e6b5c' stroke-width='2.5'/%3E%3C/svg%3E") center/12px no-repeat}
.lab{display:grid;grid-template-columns:1fr 1fr;gap:clamp(30px,5vw,60px);align-items:center}
.feat{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:24px 0 30px}
.feat div{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:var(--r);padding:16px}
.feat b{font-family:var(--f-head);color:#fff;display:block;margin-bottom:4px}
.feat span{font-size:14.5px;color:#a9bfb7}
.mock{background:#fff;color:var(--ink);border-radius:var(--r-lg);box-shadow:0 30px 70px rgba(0,0,0,.45);padding:22px;transform:rotate(-1.5deg)}
.mock .top{display:flex;justify-content:space-between;font-family:var(--f-head);font-size:13px;color:var(--muted);margin-bottom:12px}
.mock .bar{height:6px;background:var(--g100);border-radius:6px;margin-bottom:18px;overflow:hidden}.mock .bar i{display:block;height:100%;width:60%;background:var(--g500)}
.mock h4{font-size:18px;margin:0 0 14px;color:var(--ink)}
.opt{border:1.5px solid var(--line);border-radius:10px;padding:11px 14px;margin-bottom:9px;font-family:var(--f-head);font-size:15px;display:flex;gap:10px}
.opt.ok{border-color:#2e9d6a;background:#eaf7f0}.opt b{color:var(--g500)}
.mock .timer{display:inline-block;background:var(--gold-soft);color:#8a6a1e;font-family:var(--f-head);font-weight:700;font-size:13px;padding:4px 10px;border-radius:999px}
.rd{display:grid;grid-template-columns:1.1fr .9fr;gap:clamp(30px,5vw,60px);align-items:center}
.patent{background:#fff;border-radius:var(--r-lg);padding:28px;box-shadow:var(--sh);border-top:5px solid var(--gold)}
.patent .tag{background:var(--gold-soft);color:#8a6a1e}
.patent h3{font-size:var(--step-2);margin:.5em 0}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 26px}
.chips span{font-family:var(--f-head);font-size:14px;font-weight:600;background:#fff;border:1px solid #ecdcb3;color:#6b5418;padding:7px 14px;border-radius:999px}
.strip{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(220px,1fr);gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:10px;scrollbar-width:thin}
.strip img{scroll-snap-align:start;border-radius:var(--r);aspect-ratio:4/3;object-fit:cover;width:100%;height:auto;background:var(--g100)}
.views{display:grid;grid-template-columns:.9fr 1.1fr;gap:clamp(30px,5vw,60px);align-items:center}
.slider{position:relative;max-width:440px;width:100%;margin:0 auto;aspect-ratio:503/671;border-radius:var(--r-lg);overflow:hidden;background:#fff;box-shadow:var(--sh-lg)}
.slider img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;opacity:0;transition:opacity .8s}
.slider img.on{opacity:1}
.sbtn{position:absolute;top:50%;transform:translateY(-50%);width:42px;height:42px;border-radius:50%;border:0;background:rgba(255,255,255,.92);color:var(--g800);font-size:22px;cursor:pointer;box-shadow:var(--sh);z-index:2}
.sbtn.p{left:10px}.sbtn.n{right:10px}
.dots{display:flex;justify-content:center;gap:8px;margin-top:16px}
.dots button{width:10px;height:10px;border-radius:50%;border:0;background:#c3d3cd;cursor:pointer;padding:0;transition:width .2s}
.dots button.on{background:var(--g500);width:26px;border-radius:6px}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:30px 0}
.step{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:var(--r);padding:22px}
.step i{font-style:normal;font-family:var(--f-head);font-weight:800;color:var(--g900);background:var(--gold);width:34px;height:34px;border-radius:50%;display:grid;place-items:center;margin-bottom:12px}
.step b{font-family:var(--f-head);color:#fff;display:block;margin-bottom:6px;font-size:18px}
.step span{color:#b9cbc4;font-size:15px}
.cta-band{position:relative;color:#fff;text-align:center;padding:clamp(70px,10vw,120px) 20px;background:center/cover no-repeat}
.cta-band::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,41,36,.75),rgba(10,41,36,.85))}
.cta-band>*{position:relative}.cta-band h2{color:#fff;font-size:var(--step-4);margin-bottom:.3em}.cta-band p{color:#d5e2dd;max-width:620px;margin:0 auto 28px;font-size:var(--step-1)}
.cta-band .actions{justify-content:center}
@media (max-width:900px){.hero .wrap:not(.stats-wrap),.split,.lab,.rd,.views{grid-template-columns:1fr}.hero .wrap:not(.stats-wrap){text-align:center}.actions{justify-content:center}.quote{text-align:left}.hero-ph{max-width:320px}.stats{grid-template-columns:repeat(2,1fr)}.steps{grid-template-columns:1fr}.mock{transform:none}}
@media (max-width:520px){.feat{grid-template-columns:1fr}}
</style>"""
home = H_CSS + f"""
<section class="hero"><div class="wrap">
  <div class="rv in">
    <h1><span>Prof. Vinod Kumar Verma · VKVSir</span>Vinod Kr. Verma</h1>
    <p class="he">He is <em>a professor by profession</em>, an innovator by intelligence, a motivator by mood, brilliant with brain &amp; humble with heart.</p>
    <p class="quote">"In today's era, there is nothing better than human networking!!" … VKVSir</p>
    <div class="actions"><a class="btn btn-gold" href="courses">Explore courses</a><a class="btn btn-light" href="{TESTLAB}" target="_blank" rel="noopener">Take a free test</a></div>
  </div>
  <div class="hero-ph"><img src="https://static.wixstatic.com/media/b90d41_0e9d277a56394502abc7bd99cb2779c1~mv2.png/v1/crop/x_110,y_0,w_1074,h_1296/fill/w_440,h_531,al_c,q_85,enc_auto/vkvsir.png" width="440" height="531" alt="Prof. Vinod Kumar Verma (VKVSir), Engineering College Ajmer" fetchpriority="high"></div>
</div>
<div class="wrap stats-wrap"><div class="stats">
  <div><b>18+</b><span>years teaching</span></div><div><b>5+</b><span>years in industry</span></div><div><b>60+</b><span>seminars &amp; workshops</span></div><div><b>1</b><span>patent granted</span></div>
</div></div></section>

<section class="sec sec-white" id="about"><div class="wrap split">
  <img class="rv" src="https://static.wixstatic.com/media/b90d41_4866adbee9464682abf4a1dfda66fb69~mv2.png/v1/crop/x_185,y_93,w_1153,h_1407/fill/w_520,h_634,al_c,q_85,enc_auto/vkv.png" width="520" height="634" loading="lazy" alt="VKVSir portrait">
  <div class="rv rv-d1"><span class="kicker">About VKVSir</span><h2 style="font-size:var(--step-3)">Teacher, innovator and mentor since 2008</h2>
    <p>Faculty in the Department of Mechanical Engineering at Engineering College Ajmer, known for excellence in Automobile Engineering, Renewable Energy, Marketing and New Product Design &amp; Launching.</p>
    <ul class="ticks"><li>Topper in Diploma · B.E. MBM Jodhpur · M.Tech IIT Jodhpur · Ph.D.* · MBA Symbiosis</li><li>Appreciated by Former President Late Shri Pranab Mukherjee and many dignitaries</li><li>SAE founder at ECA, BAJA main round, free career counseling for students</li></ul>
    <a class="btn btn-primary" href="about">Know more about him</a></div>
</div></section>

<section class="sec sec-mint" id="courses"><div class="wrap">
  <div class="sec-head rv"><div><span class="kicker">Courses</span><h2>Learn in Hindi &amp; English</h2><p>Full course lectures with animations, PPTs, PDFs and MCQs, free for members.</p></div><a class="link-more" href="courses">All courses</a></div>
  <div class="grid grid-3">{course_cards()}</div>
</div></section>

<section class="sec sec-deep" id="test-lab"><div class="wrap lab">
  <div class="rv"><span class="kicker">New · VKV Sir Test Lab</span><h2 style="font-size:var(--step-3)">Practise like the real exam</h2>
    <p>Free online MCQ tests for B.Tech Mechanical subjects, built from VKVSir's own question bank, with GATE/ESE/PSU-style questions.</p>
    <div class="feat"><div><b>Topic &amp; unit tests</b><span>Pick a unit or a single topic and start in one tap.</span></div><div><b>Fair timing</b><span>Per-question timers with extra time for numericals.</span></div><div><b>Easy → hard mix</b><span>Balanced difficulty, from concepts to analytical problems.</span></div><div><b>Instant results</b><span>See your score and correct answers right away.</span></div></div>
    <div class="actions" style="justify-content:flex-start"><a class="btn btn-gold" href="{TESTLAB}" target="_blank" rel="noopener">Open Test Lab</a><a class="btn btn-light" href="test-and-analysis">More practice</a></div></div>
  <div class="mock rv rv-d2" aria-hidden="true"><div class="top"><span>Automobile Engg. · Unit 3</span><span class="timer">⏱ 00:42</span></div><div class="bar"><i></i></div>
    <h4>Q 6 / 10 · Which component converts reciprocating motion into rotary motion?</h4>
    <div class="opt"><b>A</b> Camshaft</div><div class="opt ok"><b>B</b> Crankshaft ✓</div><div class="opt"><b>C</b> Flywheel</div><div class="opt"><b>D</b> Connecting rod</div></div>
</div></section>

<section class="sec sec-gold" id="rd"><div class="wrap rd">
  <div class="rv"><span class="kicker" style="color:#8a6a1e">R&amp;D, Projects &amp; Innovation</span><h2 style="font-size:var(--step-3)">Ideas that leave the classroom</h2>
    <p>Research in renewable energy, automobile safety and electric mobility, with student projects that reached national newspapers.</p>
    <div class="chips"><span>Solar receiver glass-metal seals</span><span>Vehicle safety</span><span>Electric mobility</span><span>Auto gear shifting</span><span>Smart stick</span><span>Anti-roll braking</span></div>
    <a class="btn btn-primary" href="research-project-innovation">Explore R&amp;D</a></div>
  <div class="patent rv rv-d2"><span class="tag">Patent granted</span><h3>Automatic Fire Extinguisher and Window Breaking System for Passenger Cars</h3><p style="color:var(--muted)">Inventors: Vinod Kumar Verma, Arpit Mathur, Jaya Khatwani · Government Engineering College Ajmer</p><a class="link-more" href="research-project-innovation">Read more</a></div>
</div></section>

<section class="sec sec-white" id="media"><div class="wrap">
  <div class="sec-head rv"><div><span class="kicker">In the news</span><h2>Media appearances</h2><p>Newspaper coverage of seminars, student innovations and awards.</p></div><a class="link-more" href="media">Full gallery</a></div>
  <div class="strip rv">{''.join(f'<img src="{W(i,440,330)}" width="440" height="330" loading="lazy" decoding="async" alt="{E(c)}" data-full="{FIT(i)}" class="g">' for i,c in MEDIA[:10])}</div>
</div></section>

<section class="sec sec-paper" id="views"><div class="wrap views">
  <div class="rv"><span class="kicker">His views</span><h2 style="font-size:var(--step-3)">For teachers &amp; students</h2><p>Short thoughts from VKVSir on learning, teaching and growing together. Use the arrows or let them play.</p><a class="btn btn-ghost" href="about">More about VKVSir</a></div>
  <div class="rv rv-d1"><div class="slider" id="slider">{''.join(f'<img src="https://static.wixstatic.com/media/{i}/v1/fit/w_880,h_1180,q_85,enc_auto/v.png" alt="VKVSir view {n+1}" class="{"on" if n==0 else ""}" {"" if n==0 else "loading=lazy"} width="503" height="671">' for n,i in enumerate(VIEWS))}<button class="sbtn p" aria-label="Previous view">‹</button><button class="sbtn n" aria-label="Next view">›</button></div>
  <div class="dots" id="dots">{''.join(f'<button aria-label="Show view {n+1}" class="{"on" if n==0 else ""}"></button>' for n in range(len(VIEWS)))}</div></div>
</div></section>

<section class="sec sec-dark" id="members"><div class="wrap">
  <div class="sec-head rv"><div><span class="kicker">Members area · free</span><h2>Get every PDF, PPT &amp; MCQ</h2><p>Membership is free for our YouTube subscribers and fully automatic.</p></div></div>
  <div class="steps"><div class="step rv"><i>1</i><b>Subscribe</b><span>Subscribe to the VKVSir YouTube channel (account 1+ month old).</span></div><div class="step rv rv-d1"><i>2</i><b>Sign in with Google</b><span>Use the same Google account on the join page.</span></div><div class="step rv rv-d2"><i>3</i><b>Start learning</b><span>Access all courses, notes and quizzes instantly.</span></div></div>
  <div class="actions" style="justify-content:flex-start"><a class="btn btn-gold" href="{OLD}/apply">Join membership – free</a><a class="btn btn-light" href="https://www.youtube.com/@vkvsirdotcom?sub_confirmation=1" target="_blank" rel="noopener">Subscribe on YouTube</a></div>
</div></section>

<section class="sec sec-white" id="blog"><div class="wrap">
  <div class="sec-head rv"><div><span class="kicker">Blog &amp; LinkedIn</span><h2>Posts &amp; articles</h2><p>In today's world networking is the key to success.</p></div><a class="link-more" href="blog">All posts</a></div>
  <div class="grid grid-3">{post_cards(posts[:3], True)}</div>
</div></section>

<section class="sec sec-mint" id="faq"><div class="narrow faq">
  <div class="sec-head rv"><div><span class="kicker">FAQ</span><h2>Common questions</h2></div><a class="link-more" href="faq">All FAQs</a></div>
  {faq_html(FAQS[:3])}
</div></section>

<section class="cta-band" style="background-image:url('https://static.wixstatic.com/media/11062b_07608b0b281a42bcafaea6a99b070d47f000.jpg/v1/fill/w_1600,h_900,al_c,q_70,enc_auto/fun.jpg')">
  <h2 class="rv">Learning online is fun</h2><p class="rv rv-d1">Questions, guest lectures, internships or career advice: VKVSir is one message away.</p>
  <div class="actions rv rv-d2"><a class="btn btn-gold" href="contact">Contact VKVSir</a><a class="btn btn-light" href="courses">View online courses</a></div>
</section>
""" + FAQ_CSS
home_js = """<script>
lightbox('.strip img.g');
(()=>{const s=document.getElementById('slider');if(!s)return;const imgs=[...s.querySelectorAll('img')],dots=[...document.querySelectorAll('#dots button')];let i=0,t;
const show=n=>{imgs[i].classList.remove('on');dots[i].classList.remove('on');i=(n+imgs.length)%imgs.length;imgs[i].classList.add('on');dots[i].classList.add('on');};
const start=()=>{if(!matchMedia('(prefers-reduced-motion: reduce)').matches)t=setInterval(()=>show(i+1),4500);};
const jump=n=>{clearInterval(t);show(n);start();};
dots.forEach((d,n)=>d.onclick=()=>jump(n));s.querySelector('.p').onclick=()=>jump(i-1);s.querySelector('.n').onclick=()=>jump(i+1);
let x0=null;s.addEventListener('touchstart',e=>x0=e.touches[0].clientX,{passive:true});s.addEventListener('touchend',e=>{if(x0===null)return;const dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>40)jump(i+(dx<0?1:-1));x0=null;});
new IntersectionObserver(es=>es.forEach(e=>{clearInterval(t);if(e.isIntersecting)start();})).observe(s);})();
</script>"""
faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":html.unescape(q),"acceptedAnswer":{"@type":"Answer","text":html.unescape(a)}} for q,a in FAQS]}
page("index","VKVSir – Prof. Vinod Kumar Verma | Automobile Engineering, EV & Workshop Courses",
 "Free Automobile Engineering, Hybrid & Electric Vehicles, Workshop Practice and Machine Drawing lectures in Hindi & English by Prof. Vinod Kumar Verma (VKVSir), Engineering College Ajmer. PPTs, PDFs, MCQs and online tests.",
 home, home_js)

# =================== ABOUT ===================
about = banner("About VKVSir","Vinod Kumar Verma (Ph.D.*, M.Tech., MBA): professor, innovator and mentor at Engineering College Ajmer.","About") + """
<style>.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:18px}.fact{background:#fff;border:1px solid var(--line);border-top:4px solid var(--gold);border-radius:var(--r);padding:22px;box-shadow:var(--sh)}.fact h3{font-size:var(--step-1);margin-bottom:.4em}.fact p{margin:0;color:var(--muted)}.split{display:grid;grid-template-columns:.85fr 1.15fr;gap:clamp(30px,5vw,60px);align-items:start}.split img{border-radius:var(--r-lg);box-shadow:var(--sh-lg);position:sticky;top:calc(var(--hh) + 20px)}.sk{text-align:center;font-size:var(--step-2);font-family:var(--f-head);color:var(--g800);margin-top:40px}@media(max-width:900px){.split{grid-template-columns:1fr}.split img{position:static;max-width:420px;margin:0 auto}}</style>
<section class="sec sec-white"><div class="wrap"><div class="facts">
 <div class="fact rv"><h3>Bio</h3><p>Mr. Vinod Kr. Verma is a faculty in the Department of Mechanical Engineering at Engineering College Ajmer, since 2008. He is known for his excellence in the field of Automobile Engineering, Renewable Energy, Marketing, and New Product Design &amp; Launching.</p></div>
 <div class="fact rv rv-d1"><h3>Education</h3><p>He was a Topper in Diploma (Govt. Polytechnic Kota), B.E (MBM Jodhpur), M. Tech (IIT Jodhpur), Ph.D.* and MBA-Marketing (Symbiosis University).</p></div>
 <div class="fact rv rv-d2"><h3>Experience</h3><p>He has 5 Yr+ Industrial experience (2 Yr in Dubai &amp; Afghanistan + 3 Yrs in India) &amp; 14 Yr+ Teaching experience with a goal to enhance &amp; strengthen the young generation with good quality education and to create tremendous opportunities for them.</p></div>
 <div class="fact rv"><h3>Achievements</h3><p>He received many awards &amp; appreciations from Former President Late Mr. Pranab Mukherjee, MHRD Minister Mr. Satyapal Singh, the Education Minister of Rajasthan, the District Collector of Ajmer, and many more dignitaries.</p></div>
 <div class="fact rv rv-d1"><h3>Milestones</h3><p>One patent, publications in many reputed National &amp; International Journals, SAE Founder at ECA, participation in BAJA main round, 60+ seminars/tours/workshops organized for students, and many lectures delivered as an expert and keynote speaker.</p></div>
 <div class="fact rv rv-d2"><h3>Beyond the classroom</h3><p>Coordinator in the training and placement cell, bridging academia and industry with leading companies and HR professionals. Free career counseling for students.</p></div>
</div><p class="sk rv">सर्वे भवन्तु सुखिनः · Jai Hind!</p></div></section>
<section class="sec sec-mint"><div class="wrap split">
 <img class="rv" src="https://static.wixstatic.com/media/b90d41_4866adbee9464682abf4a1dfda66fb69~mv2.png/v1/crop/x_185,y_93,w_1153,h_1407/fill/w_520,h_634,al_c,q_85,enc_auto/vkv.png" width="520" height="634" loading="lazy" alt="Prof. Vinod Kumar Verma">
 <div class="rv rv-d1"><span class="kicker">More about VKVSir</span><h2 style="font-size:var(--step-3)">Where education, innovation and mentorship meet</h2>
 <p>Welcome to the official website of Prof. Vinod Kumar Verma, affectionately known as VKVSir, a distinguished figure in the realm of automobile engineering, manufacturing processes, and innovation.</p>
 <p>With over two decades of combined experience in both corporate and academic spheres, Prof. Vinod Kumar Verma brings a wealth of knowledge and expertise to the table. Having spent five years in the corporate world, including a two-year stint abroad as a project manager, he possesses invaluable insights into real-world challenges and solutions.</p>
 <p>However, it is his passion for education and innovation that truly sets him apart. With more than 17 years of teaching experience, Prof. Verma has nurtured countless young minds, guiding them towards their academic and professional aspirations. He is renowned for his dedication to fostering innovation, evident in his numerous research publications and a patented invention in his name.</p>
 <p>Beyond academia, Prof. Verma is celebrated for his role as a mentor and motivator. Students flock to him for career advice and personal guidance, drawn by his genuine desire to see them succeed. As a coordinator in the training and placement cell, he bridges the gap between academia and industry, forging partnerships with leading companies and HR professionals.</p>
 <p>Prof. Verma's academic journey is equally illustrious, with a graduation from MBM Engineering College, Jodhpur, followed by research endeavors at the prestigious Indian Institute of Technology, Jodhpur, and an MBA from Symbiosis, Pune.</p>
 <p>Always at the forefront of networking and engagement, Prof. Verma maintains an active presence on <a href="https://www.linkedin.com/in/vkvsir" target="_blank" rel="noopener">LinkedIn</a>, ensuring that his expertise and mentorship reach a global audience.</p>
 <p>Join us in exploring the multifaceted world of Prof. Vinod Kumar Verma, where education, innovation, and mentorship converge to shape the leaders of tomorrow.</p>
 <div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-primary" href="contact">Contact VKVSir</a><a class="btn btn-ghost" href="research-project-innovation">See R&amp;D work</a></div></div>
</div></section>"""
page("about","About Prof. Vinod Kumar Verma (VKVSir) | Engineering College Ajmer",
 "Prof. Vinod Kumar Verma (VKVSir): Mechanical Engineering faculty at Engineering College Ajmer since 2008. B.E. MBM Jodhpur, M.Tech IIT Jodhpur, MBA Symbiosis. Automobile, EV, renewable energy and innovation.",
 about, crumbs="About")

# =================== COURSES ===================
cbody = banner("Courses taught","Full course lectures in Hindi &amp; English with animations, PPTs, PDFs and MCQs. Course pages are in the free Members Area.","Courses") + f"""
<section class="sec sec-white"><div class="wrap"><div class="grid grid-3">{course_cards()}</div></div></section>
<section class="sec sec-mint"><div class="wrap" style="display:grid;gap:22px;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr))">
 <div class="card rv" style="padding:26px"><span class="tag">Practice</span><h3 style="margin:.6em 0 .3em">MVSI / RTO Inspector Practice Sheet 1</h3><p>Exam-style questions for MVSI / RTO Inspector aspirants.</p><a class="btn btn-primary" style="align-self:flex-start;margin-top:12px" href="https://forms.gle/uDEB4LovbrKjtFTH9" target="_blank" rel="noopener">Open practice sheet</a></div>
 <div class="card rv rv-d1" style="padding:26px"><span class="tag">Online tests</span><h3 style="margin:.6em 0 .3em">VKV Sir Test Lab</h3><p>Topic-wise and unit-wise timed MCQ tests with instant results.</p><a class="btn btn-gold" style="align-self:flex-start;margin-top:12px" href="{TESTLAB}" target="_blank" rel="noopener">Open Test Lab</a></div>
 <div class="card rv rv-d2" style="padding:26px"><span class="tag">Free membership</span><h3 style="margin:.6em 0 .3em">Unlock all course material</h3><p>Free for YouTube subscribers, approved automatically.</p><a class="btn btn-yt" style="align-self:flex-start;margin-top:12px" href="{OLD}/apply">Join membership – free</a></div>
</div></section>"""
page("courses","Courses by VKVSir | Automobile Engineering, EV, Workshop Practice, Machine Drawing",
 "Free full-course lectures by VKVSir in Hindi & English: Automobile Engineering, Hybrid & Electric Vehicles, Workshop Practice, Machine Drawing, Casting Process and New Product Design, with PPTs, PDFs and MCQs.",
 cbody, crumbs="Courses",
 extra_ld={"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":n+1,"item":{"@type":"Course","name":t,"description":d,"url":u,"provider":{"@id":DOMAIN+"/#person"},"inLanguage":["en","hi"]}} for n,(t,i,u,d) in enumerate(COURSES)]})

# =================== R&D (new) ===================
pubs = [("Optimizing Glass to Metal Composite Seal Performance: An integrated approach with ANN, multiple regression and Taguchi","Journal of Polymer and Composites","2025"),
 ("Vehicle safety innovations and electric mobility: technologies, trends, and challenges","Int. Journal of Innovative Trends in Multidisciplinary Research","2025"),
 ("Water-Efficient Air-Cooling Systems: Engineering Sustainable Climate Control","Int. Journal for Research Trends and Innovation","2021"),
 ("Automated Gear Shifting for Auto Clutch Bikes: A Microcontroller Approach","Int. Journal of Scientific Development and Research","2019"),
 ("Factors affecting the performance of glass–metal seal of solar receiver tubes: a review","Int. Journal of Applied Engineering Research","2018"),
 ("Design and Development of Glass-Metal Joints and their Characterization for Solar Receiver Tube","IIT Jodhpur (M.Tech research)","2013")]
rd = banner("R&amp;D, Projects &amp; Innovation","Research in renewable energy, vehicle safety and electric mobility, and student innovations that made the news.","R&amp;D, Projects &amp; Innovation") + f"""
<style>.pat{{display:grid;grid-template-columns:1.2fr .8fr;gap:30px;align-items:center;background:#fff;border-radius:var(--r-lg);padding:clamp(24px,4vw,44px);box-shadow:var(--sh);border-left:6px solid var(--gold)}}.pubs{{display:grid;gap:12px}}.pub{{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:18px 22px;display:grid;grid-template-columns:auto 1fr;gap:16px;align-items:start}}.pub b{{font-family:var(--f-head);background:var(--g100);color:var(--g500);border-radius:8px;padding:4px 10px;font-size:14px}}.pub h3{{font-size:17px;margin:0 0 4px}}.pub p{{margin:0;font-size:14.5px;color:var(--muted)}}@media(max-width:800px){{.pat{{grid-template-columns:1fr}}}}</style>
<section class="sec sec-gold"><div class="wrap"><div class="pat rv"><div><span class="tag" style="background:var(--gold-soft);color:#8a6a1e">Patent granted</span><h2 style="font-size:var(--step-3);margin:.5em 0 .4em">Automatic Fire Extinguisher and Window Breaking System for Passenger Cars</h2><p>Inventors: Vinod Kumar Verma, Arpit Mathur, Jaya Khatwani · Government Engineering College Ajmer (application 201811026495).</p><p style="color:var(--muted)">A safety system that detects fire in a passenger car, extinguishes it automatically and breaks the window so occupants can escape.</p></div>
<img src="{W('b90d41_eb2104b6597649e4a5c0b65bd44f0619~mv2.jpg',600,400)}" width="600" height="400" loading="lazy" alt="Student innovation in the news" style="border-radius:var(--r)"></div></div></section>
<section class="sec sec-white"><div class="wrap"><div class="sec-head rv"><div><span class="kicker">Student projects</span><h2>Innovations that made the news</h2></div><a class="link-more" href="media">See media gallery</a></div>
<div class="grid">{''.join(f'<div class="card rv rv-d{n%3+1}"><div class="ph">{IMG(i,600,400,t)}</div><div class="bd"><h3>{t}</h3><p>{d}</p></div></div>' for n,(i,t,d) in enumerate([("b90d41_72163043971a4e49a9479397ab2d1168~mv2.jpg","Automatic gear system","Microcontroller-based automatic gear shifting for auto-clutch bikes."),("b90d41_eb2104b6597649e4a5c0b65bd44f0619~mv2.jpg","Anti-roll braking","A braking concept to reduce vehicle roll-over risk."),("b90d41_b9aaebb9bd604fa8b5854408b7173a8b~mv2.jpg","Smart stick","Assistive smart stick project featured in Dainik Bhaskar."),("b90d41_d87f56553ddc4852b747b20ab28cde90~mv2.png","SAE BAJA","ECA team at the SAE BAJA main round."),("b90d41_b3fa9e02c8af40e6bd557244e44df2ef~mv2.jpg","Lab experiments","Hands-on experiments in renewable energy and automobile labs."),("b90d41_22ccfd37e9384f73a0c6540086034ff0~mv2.jpg","Air Force seminar","Seminars connecting students with defence and industry experts.")]))}</div></div></section>
<section class="sec sec-mint"><div class="narrow"><div class="sec-head rv"><div><span class="kicker">Publications</span><h2>Selected research</h2></div><a class="link-more" href="https://scholar.google.com/citations?user=CDzm7o8AAAAJ" target="_blank" rel="noopener">Google Scholar</a></div>
<div class="pubs">{''.join(f'<div class="pub rv"><b>{y}</b><div><h3>{E(t)}</h3><p>{E(j)}</p></div></div>' for t,j,y in pubs)}</div>
<p style="margin-top:26px;text-align:center"><a class="btn btn-ghost" href="{OLD}/research-project-innovation">View the original R&amp;D page</a></p></div></section>"""
page("research-project-innovation","R&D, Projects & Innovation | VKVSir – Patent, Research & Student Projects",
 "Research and innovation by Prof. Vinod Kumar Verma: granted patent on an automatic fire extinguisher and window breaking system for cars, solar receiver research, EV and vehicle safety publications, and student projects.",
 rd, crumbs="R&D, Projects & Innovation")

# =================== MEDIA ===================
mbody = banner("Media appearances","Newspaper coverage, seminars and innovations. Tap any picture to view it large.","Media") + f"""
<style>.masonry{{columns:4 240px;column-gap:16px}}.masonry figure{{margin:0 0 16px;break-inside:avoid;background:#fff;border:1px solid var(--line);border-radius:var(--r);overflow:hidden;box-shadow:var(--sh)}}.masonry img{{width:100%;height:auto}}.masonry figcaption{{font-family:var(--f-head);font-size:13.5px;color:var(--muted);padding:10px 12px}}</style>
<section class="sec sec-white"><div class="wrap"><div class="masonry">
{''.join(f'<figure class="rv"><img src="https://static.wixstatic.com/media/{i}/v1/fit/w_480,h_900,q_80,enc_auto/m.jpg" data-full="{FIT(i)}" loading="lazy" decoding="async" alt="{E(c)}"><figcaption>{E(c)}</figcaption></figure>' for i,c in MEDIA)}
</div></div></section>"""
page("media","Media Appearances of VKVSir | Newspaper Coverage & Seminars",
 "Media appearances of Prof. Vinod Kumar Verma (VKVSir): Dainik Bhaskar, Rajasthan Patrika and Navjyoti coverage of seminars, student innovations, BAJA and awards.",
 mbody, "<script>lightbox('.masonry img')</script>", crumbs="Media")

# =================== TEST & ANALYSIS ===================
tbody = banner("Test and analysis","Check your understanding with timed tests, quizzes and practice sheets.","Test and Analysis") + f"""
<section class="sec sec-white"><div class="wrap"><div class="grid">
 <a class="card rv" href="{TESTLAB}" target="_blank" rel="noopener" style="border-top:5px solid var(--gold)"><div class="bd"><span class="tag">Recommended</span><h3>VKV Sir Test Lab</h3><p>Topic and unit tests with per-question timers, extra time for numericals and instant results.</p><span class="go link-more">Open Test Lab</span></div></a>
 <a class="card rv rv-d1" href="https://forms.gle/uDEB4LovbrKjtFTH9" target="_blank" rel="noopener"><div class="bd"><span class="tag">Practice</span><h3>MVSI / RTO Inspector Practice Sheet 1</h3><p>Exam-style questions in Google Forms.</p><span class="go link-more">Open sheet</span></div></a>
 <a class="card rv rv-d2" href="{OLD}/quiz"><div class="bd"><span class="tag">Members</span><h3>Course quizzes</h3><p>Unit-wise quizzes in the free Members Area.</p><span class="go link-more">Open quizzes</span></div></a>
 <a class="card rv" href="courses"><div class="bd"><span class="tag">Courses</span><h3>PPTs, PDFs &amp; full lectures</h3><p>For more quizzes and PPT/PDFs visit the full course pages (Membership Area).</p><span class="go link-more">View courses</span></div></a>
</div></div></section>"""
page("test-and-analysis","Online Tests & Quizzes | VKVSir Test and Analysis",
 "Free online MCQ tests, quizzes and practice sheets by VKVSir for B.Tech Mechanical, Automobile Engineering and MVSI/RTO Inspector exams.",
 tbody, crumbs="Test and Analysis")

# =================== BLOG ===================
years = sorted({p["date"][:4] for p in posts}, reverse=True)
bbody = banner("Blog &amp; LinkedIn","Posts, wishes, events and thoughts from VKVSir.","Blog") + f"""
<style>.filters{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:30px}}.filters button{{font-family:var(--f-head);font-weight:600;font-size:15px;border:1.5px solid var(--line);background:#fff;color:var(--g800);padding:8px 18px;border-radius:999px;cursor:pointer;transition:.15s}}.filters button:hover{{border-color:var(--g500)}}.filters button.on{{background:var(--g800);border-color:var(--g800);color:#fff}}</style>
<section class="sec sec-white"><div class="wrap">
<div class="filters" role="group" aria-label="Filter posts by year"><button class="on" data-y="all">All</button>{''.join(f'<button data-y="{y}">{y}</button>' for y in years)}</div>
<div class="grid grid-3" id="posts">{post_cards(posts)}</div>
<p style="text-align:center;margin-top:40px"><a class="btn btn-ghost" href="https://www.linkedin.com/in/vkvsir" target="_blank" rel="noopener">Follow on LinkedIn</a></p></div></section>"""
bjs = "<script>document.querySelectorAll('.filters button').forEach(b=>b.onclick=()=>{document.querySelectorAll('.filters button').forEach(x=>x.classList.toggle('on',x===b));document.querySelectorAll('#posts .card').forEach(c=>c.hidden=!(b.dataset.y==='all'||c.dataset.year===b.dataset.y));});</script>"
page("blog","Blog & LinkedIn | VKVSir Posts and Articles","Posts, wishes, events, webinars and thoughts by Prof. Vinod Kumar Verma (VKVSir), Engineering College Ajmer.", bbody, bjs, crumbs="Blog")

# =================== FAQ ===================
fbody = FAQ_CSS + banner("Frequently asked questions","Membership, lectures, internships and career counseling.","FAQ") + f"""
<section class="sec sec-mint"><div class="narrow faq">{faq_html(FAQS)}
<p style="margin-top:30px;color:var(--muted);text-align:center">The VKVSIR website helps students learn automobile engineering, manufacturing processes, machine drawing, workshop technology, AutoCAD and more in English &amp; Hindi. All content is free.</p>
<p style="text-align:center"><a class="btn btn-primary" href="contact">Still have a question?</a></p></div></section>"""
page("faq","FAQ | VKVSir – Membership, Lectures, Internships & Career Counseling",
 "Answers about VKVSir: free membership through YouTube, expert lectures, internships, tuitions and free career counseling.", fbody, crumbs="FAQ", extra_ld=faq_ld)

# =================== CONTACT ===================
contacts = [("YouTube channel","Lectures &amp; animations","https://www.youtube.com/@vkvsirdotcom?sub_confirmation=1","a1b09fe8b7f04378a9fe076748ad4a6a.png"),("Email","vinodvermavkvsir@gmail.com","mailto:vinodvermavkvsir@gmail.com",None),("LinkedIn","Professional network","https://www.linkedin.com/in/vkvsir","48a2a42b19814efaa824450f23e8a253.png"),("Instagram","@vkvsir","https://www.instagram.com/vkvsir","8d6893330740455c96d218258a458aa4.png"),("Facebook","/vkvsir","https://www.facebook.com/vkvsir","e316f544f9094143b9eac01f1f19e697.png"),("Twitter","@vkvsir","https://www.twitter.com/vkvsir","9c4b521dd2404cd5a05ed6115f3a0dc8.png"),("Telegram","t.me/vkvsir","https://t.me/vkvsir","11062b_e98838ff3ed04690a4d6de29d5936f77~mv2.png"),("Pinterest","/vkvsir","https://www.pinterest.com/vkvsir/",None)]
def ic(i): return f'<img src="https://static.wixstatic.com/media/{i}/v1/fit/w_96,h_96/i.png" width="44" height="44" alt="" loading="lazy">' if i else '<span style="width:44px;height:44px;border-radius:12px;background:var(--g100);display:grid;place-items:center;font-size:22px">✉</span>'
ctbody = banner("Contact &amp; follow","Questions, guest lectures, internships or career advice: reach VKVSir here.","Contact") + f"""
<style>.cgrid{{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(min(100%,250px),1fr))}}.c{{display:flex;gap:14px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:18px;text-decoration:none;color:var(--ink);box-shadow:var(--sh);transition:transform .2s,box-shadow .2s}}.c:hover{{transform:translateY(-3px);box-shadow:var(--sh-lg)}}.c b{{font-family:var(--f-head);display:block;color:var(--g800)}}.c span{{font-size:14px;color:var(--muted);word-break:break-word}}.addr{{display:grid;grid-template-columns:1fr 1.2fr;gap:30px;align-items:center}}.addr iframe{{width:100%;height:320px;border:0;border-radius:var(--r-lg);box-shadow:var(--sh)}}@media(max-width:860px){{.addr{{grid-template-columns:1fr}}}}</style>
<section class="sec sec-white"><div class="wrap"><div class="cgrid">
{''.join(f'<a class="c rv" href="{u}" {"" if u.startswith("mailto") else "target=_blank rel=noopener"}>{ic(i)}<div><b>{t}</b><span>{s}</span></div></a>' for t,s,u,i in contacts)}
</div></div></section>
<section class="sec sec-mint"><div class="wrap addr">
 <div class="rv"><span class="kicker">Address</span><h2 style="font-size:var(--step-3)">Visit the department</h2><p>Prof. Vinod Kumar Verma<br>NB-202, New Building,<br>Engineering College Ajmer<br>Rajasthan, India – 305025</p><a class="btn btn-primary" href="mailto:vinodvermavkvsir@gmail.com">Send an email</a></div>
 <iframe class="rv rv-d1" loading="lazy" title="Map of Engineering College Ajmer" src="https://www.google.com/maps?q=Government+Engineering+College+Ajmer&output=embed" referrerpolicy="no-referrer-when-downgrade"></iframe>
</div></section>"""
page("contact","Contact VKVSir | Prof. Vinod Kumar Verma, Engineering College Ajmer",
 "Contact Prof. Vinod Kumar Verma (VKVSir) by email, YouTube, LinkedIn, Instagram, Facebook, Twitter, Telegram or visit NB-202, Engineering College Ajmer, Rajasthan 305025.", ctbody, crumbs="Contact")

page("404","Page not found | VKVSir","Page not found", banner("Page not found","This page has moved. Try the menu above or go back home.")+'<section class="sec sec-white"><div class="wrap" style="text-align:center"><a class="btn btn-primary" href="./">Go to homepage</a></div></section>')

# SEO files
pages = ["","about","courses","research-project-innovation","media","test-and-analysis","blog","faq","contact"]
today = date.today().isoformat()
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f'  <url><loc>{DOMAIN}/{p}</loc><lastmod>{today}</lastmod><priority>{"1.0" if not p else "0.8"}</priority></url>\n' for p in pages) + "</urlset>\n")
open("robots.txt","w").write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
print("built ok")
