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

PERSON = {"@type":"Person","@id":DOMAIN+"/#person","name":"Dr. Vinod Kumar Verma","honorificPrefix":"Dr.","alternateName":["VKVSir","Vinod Kr. Verma","VKV Sir","Prof. Vinod Kumar Verma"],
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
<meta name="author" content="Dr. Vinod Kumar Verma">
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
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.min.js"></script>
<script src="assets/auth.js"></script>
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

COURSES = [("Automobile Engineering","11062b_42b9ecea6a1540668defdedea80d1a9d~mv2.jpg","course-automobile-engineering","Engines, transmission, steering, brakes and vehicle systems explained with animations."),
 ("Hybrid & Electric Vehicles","11062b_0d56d33639234010a96c69ca297bf60a~mv2.jpg","course-hev","Batteries, motors, controllers and the technology shaping electric mobility."),
 ("Workshop Practice","e592d5b87e234c849e8363ee949932a0.jpg","course-workshop-practice","Welding, fitting, carpentry, smithy and safe shop-floor practice."),
 ("Machine Drawing","7fba3905ea184ee29642cf0def056821.jpg","course-machine-drawing","Projections, sections, fasteners and assembly drawings, step by step."),
 ("Casting Process","aef2ab657d574a17adc9dc6a7312c958.jpg","course-casting-process","Patterns, moulds, melting and defects in metal casting."),
 ("Manufacturing Processes","b90d41_b3fa9e02c8af40e6bd557244e44df2ef~mv2.jpg","course-manufacturing-processes","Casting, welding, forming, powder metallurgy and much more."),
 ("New Product Design & Launching","9d090cf24c96432db9c956dbdac792f6.jpg","course-pdl","From idea to market: design thinking, prototyping and launch strategy.")]
def course_cards(reveal=True):
    return "".join(f'<a class="card{" rv rv-d"+str(n%3+1) if reveal else ""}" href="{u}"><div class="ph">{IMG(i,600,400,t)}</div><div class="bd"><h3>{t}</h3><p>{d}</p><span class="go link-more">Course details</span></div></a>' for n,(t,i,u,d) in enumerate(COURSES))

MEDIA = [("b90d41_92b1f87de246438386291d40d248e62b~mv2.jpg","PCRA"),("b90d41_ba9d6f25da3d449eaffd545359b5f097~mv2.jpeg","Dainik NavJyoti, 23 May 2018"),("b90d41_6e032864d49c412f9950856d0d3ee018~mv2.jpg","Bhaskar & Patrika, 17 Aug 2017"),("b90d41_963bdfc7ea9d4260838aaced8793fc8a~mv2.jpeg","Dainik Bhaskar, 23 May 2018"),("b90d41_6f3957c5d8504c8d845fc6fc8ead26d2~mv2.jpg","Bhaskar, 30 June 2017"),("b90d41_7cec79804645421a83efd91284441225~mv2.jpg","Bhaskar, 19 Sep 2017"),("b90d41_2f515a0836eb4cf3b7303f9c41419bfb~mv2.jpg","Bhaskar, 7 Oct 2016"),("b90d41_72163043971a4e49a9479397ab2d1168~mv2.jpg","Automatic gear system"),("b90d41_eb2104b6597649e4a5c0b65bd44f0619~mv2.jpg","Anti-roll braking system"),("b90d41_22ccfd37e9384f73a0c6540086034ff0~mv2.jpg","Air Force seminar"),("b90d41_1323325e93a44bab99e23dcca99bb22f~mv2.jpg","Air Force seminar"),("b90d41_fabdd8eeadc5438fb668094ed3bd18e5~mv2.jpg","Bhaskar & Patrika, 17 Aug 2017"),("b90d41_d2b156d8092848489d33c90634c0b568~mv2.jpg","Bhaskar, 12 Aug 2016"),("b90d41_d87f56553ddc4852b747b20ab28cde90~mv2.png","Bhaskar – BAJA, 3 Sep 2018"),("b90d41_0a6314db80f148f2837606043d55ac01~mv2.jpg","Patrika, 17 Aug 2017"),("b90d41_00ace1642c7e41c883b7f5cc13a93806~mv2.jpg","Patrika, 17 Aug 2017"),("b90d41_b9aaebb9bd604fa8b5854408b7173a8b~mv2.jpg","Silicon Valley smart stick – Bhaskar, 23 July 2018"),("b90d41_2b0fabb766804dd18cac674d3abd6f79~mv2.jpeg","Bhaskar, 16 March 2021"),("b90d41_efc2ea2689de462b91981f586dd4ba01~mv2.jpeg","Dainik NavJyoti, 23 May 2018"),("b90d41_9f2ea0acbea04b7bacba6478d1de33ae~mv2.jpg","Dainik Bhaskar, 23 May 2018"),("b90d41_0c3c0aba71354922833dfb52621aea4d~mv2.jpeg","Bhaskar, 20 March 2021"),("b90d41_ea9d919649d64b1a8ab7028e786125ff~mv2.jpeg","Navjyoti, 16 March 2021"),("b90d41_9bb6427654b3401f839048387e53d890~mv2.jpg","Dainik Navjyoti Ajmer, 16 March 2021"),("b90d41_707b8c2b5b8a4269a47936ebb093cf24~mv2.jpg","Rajasthan Patrika Ajmer, 16 March 2021"),("b90d41_139f4d7b832a4ca08979443334c181c7~mv2.jpg","Media appearance"),
 ("b90d41_f8d7b46bf8ef4e02a2f843e58c2fdf16~mv2.jpg","Media appearance"),("b90d41_ae1e83e73dd6481598341637786512d7~mv2.jpg","Media appearance"),("b90d41_f092db602bf744719a308a9403cb38a4~mv2.jpg","Media appearance"),("b90d41_de1bdfb6fbee45d48ef1c051f74ae05e~mv2.jpeg","Media appearance"),("b90d41_37ebd5a8adc548abab515507462c8ccb~mv2.jpeg","Media appearance"),("b90d41_1fb7211d22994a669b0071c450a3e3ed~mv2.jpg","Media appearance"),("b90d41_3092ac066fe54b44a1a853116385b953~mv2.jpg","Media appearance"),("b90d41_b3fa9e02c8af40e6bd557244e44df2ef~mv2.jpg","Experimenting in lab"),("b90d41_13e95f61ad114a59b38860e2a7316532~mv2.jpg","College campus"),("b90d41_0504ef60c2e14cea83781638f9bac1de~mv2.jpeg","Students on a break")]
VIEWS = ["b90d41_4b0b2e74e44241968531a826ee177608~mv2.png","b90d41_1eceb170101d4e18a61b447ab23b4892~mv2.png","b90d41_883c935dac5a4542a30294f91f8fb922~mv2.png","b90d41_d75231deb0d84b6caa5cd3ff86bd9cd5~mv2.png","b90d41_b13b4fe9d1964223a95e5da29c2073a3~mv2.png","b90d41_e2e15e52de6e4d9f9c2342a5dfd74afa~mv2.png","b90d41_6cc1a4a2b7cd432bb5fd1d633638432d~mv2.png","b90d41_142d5d1f99f6466bba10646d3e681be9~mv2.png"]
FAQS = [
 ("What subject/topic does VKVSir like most?", 'He likes to experiment with new topics and fields, especially technical ones. He likes to work on innovations and new ideas and to develop new products and solutions. His major <a href="courses">courses</a> cover Automobile, Hybrid &amp; Electric Vehicles, Robotics, Renewable Energy Sources, Solar Energy, App development, IoT, Machine Learning, AI &amp; AR, etc.'),
 ("How do I get membership and access to premium content?", f'Premium content like PPT/PDF and objective &amp; subjective questions is absolutely free. Subscribe to our <a href="https://www.youtube.com/@vkvsirdotcom?sub_confirmation=1" target="_blank" rel="noopener">YouTube channel</a> (or comment on 5+ of our videos), then <a href="join">apply here</a> with the same Google account. Your YouTube account must be at least 1 month old. Subscribers get access within seconds.'),
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
.hero .wrap:not(.stats-wrap){display:grid;grid-template-columns:1.15fr .85fr;gap:32px;align-items:end;padding:clamp(28px,4vw,52px) 0 0}
.hero .wrap:not(.stats-wrap)>div:first-child{padding-bottom:clamp(20px,3vw,40px)}
.hero h1{color:#fff;font-size:var(--step-4);margin:.1em 0 .3em}
.hero h1 span{display:block;color:var(--gold);font-size:.42em;font-weight:600;letter-spacing:.02em;margin-bottom:.4em}
.he{font-size:var(--step-1);line-height:1.6;color:#cfe0d9;margin:0 0 1.2em}
.he em{color:var(--lime);font-style:normal}
.quote{border-left:3px solid var(--gold);padding:4px 0 4px 16px;font-style:italic;color:#e9dcb8;margin:0 0 28px}
.actions{display:flex;gap:12px;flex-wrap:wrap}
.hero-ph{align-self:end;justify-self:center;position:relative;max-width:470px}
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
@media (max-width:640px){.hero h1{font-size:clamp(34px,10vw,44px)}.he{font-size:17px}.stats div{padding:16px 8px}.stats b{font-size:28px}.hero-ph{max-width:260px}.hero .wrap:not(.stats-wrap)>div:first-child{padding-bottom:0}.cta-band{padding:56px 16px}.mock{padding:16px}.mock h4{font-size:16px}}
@media (max-width:900px){.hero .wrap:not(.stats-wrap),.split,.lab,.rd,.views{grid-template-columns:1fr}.hero .wrap:not(.stats-wrap){text-align:center}.actions{justify-content:center}.quote{text-align:left}.hero-ph{max-width:320px}.stats{grid-template-columns:repeat(2,1fr)}.steps{grid-template-columns:1fr}.mock{transform:none}}
@media (max-width:520px){.feat{gap:10px}.feat div{padding:12px}.feat b{font-size:14.5px}.feat span{font-size:13px}}
</style>"""
home = H_CSS + f"""
<section class="hero"><div class="wrap">
  <div class="rv in">
    <h1><span>VKVSir · Engineering College Ajmer</span>Dr. Vinod Kr. Verma</h1>
    <p class="he">He is <em>a professor by profession</em>, an innovator by intelligence, a motivator by mood, brilliant with brain &amp; humble with heart.</p>
    <p class="quote">"In today's era, there is nothing better than human networking!!" … VKVSir</p>
    <div class="actions"><a class="btn btn-gold" href="courses">Explore courses</a><a class="btn btn-light" href="{TESTLAB}" target="_blank" rel="noopener">Take a free test</a></div>
  </div>
  <div class="hero-ph"><img src="https://static.wixstatic.com/media/b90d41_0e9d277a56394502abc7bd99cb2779c1~mv2.png/v1/crop/x_110,y_0,w_1074,h_1296/fill/w_440,h_531,al_c,q_85,enc_auto/vkvsir.png" width="440" height="531" alt="Dr. Vinod Kumar Verma (VKVSir), Engineering College Ajmer" fetchpriority="high"></div>
</div>
<div class="wrap stats-wrap"><div class="stats">
  <div><b>18+</b><span>years teaching</span></div><div><b>5+</b><span>years in industry</span></div><div><b>60+</b><span>seminars &amp; workshops</span></div><div><b>1</b><span>patent granted</span></div>
</div></div></section>

<section class="sec sec-white" id="about"><div class="wrap split">
  <img class="rv" src="https://static.wixstatic.com/media/b90d41_4866adbee9464682abf4a1dfda66fb69~mv2.png/v1/crop/x_185,y_93,w_1153,h_1407/fill/w_520,h_634,al_c,q_85,enc_auto/vkv.png" width="520" height="634" loading="lazy" alt="VKVSir portrait">
  <div class="rv rv-d1"><span class="kicker">About VKVSir</span><h2 style="font-size:var(--step-3)">Teacher, innovator and mentor since 2008</h2>
    <p>Faculty in the Department of Mechanical Engineering at Engineering College Ajmer since 2008, recognised for excellence in Automobile Engineering, Renewable Energy, Marketing and New Product Design &amp; Launching.</p>
    <ul class="ticks"><li>Topper in Diploma · B.E. MBM Jodhpur · M.Tech IIT Jodhpur · Ph.D. · MBA Symbiosis</li><li>Consultancy for various industries &amp; government projects; expert examiner for RPSC, RTU Kota, MPUAT, Rajasthan Board, Rajasthan University, etc.</li><li>SAE founder at ECA, BAJA main round, free career counseling for students</li></ul>
    <a class="btn btn-primary" href="about">Know more about him</a></div>
</div></section>

<section class="sec sec-mint" id="courses"><div class="wrap">
  <div class="sec-head rv"><div><span class="kicker">Courses</span><h2>Learn in Hindi &amp; English</h2><p>Full course lectures with animations, PPTs, PDFs and MCQs, free for members.</p></div><a class="link-more" href="courses">All courses</a></div>
  <div class="grid grid-3 swipe">{course_cards()}</div>
</div></section>

<section class="sec sec-deep" id="test-lab"><div class="wrap lab">
  <div class="rv"><span class="kicker">VKV Sir Test Lab</span><h2 style="font-size:var(--step-3)">Practise like the real exam</h2>
    <p><b style="color:var(--gold)" data-stat="total">Thousands of</b> MCQs across three tracks: <b>Foundation</b> (internal exams &amp; viva), <b>Competitive exams</b> (GATE, PSU, RTO/MVI, SSC) and <b>Career &amp; interview</b> preparation.</p>
    <div class="feat"><div><b>Topic &amp; unit tests</b><span>Pick a unit or a single topic and start in one tap.</span></div><div><b>Fair timing</b><span>Per-question timers with extra time for numericals.</span></div><div><b>Easy → hard mix</b><span>Balanced difficulty, from concepts to analytical problems.</span></div><div><b>Instant results</b><span>See your score and correct answers right away.</span></div></div>
    <div class="actions" style="justify-content:flex-start"><a class="btn btn-gold" href="{TESTLAB}" target="_blank" rel="noopener">Open Test Lab</a><a class="btn btn-light" href="test-lab">How Test Lab works</a></div></div>
  <div class="mock rv rv-d2" aria-hidden="true"><div class="top"><span>Automobile Engg. · Unit 3</span><span class="timer">⏱ 00:42</span></div><div class="bar"><i></i></div>
    <h4>Q 6 / 10 · Which component converts reciprocating motion into rotary motion?</h4>
    <div class="opt"><b>A</b> Camshaft</div><div class="opt ok"><b>B</b> Crankshaft ✓</div><div class="opt"><b>C</b> Flywheel</div><div class="opt"><b>D</b> Connecting rod</div></div>
</div></section>

<section class="sec sec-gold" id="rd"><div class="wrap rd">
  <div class="rv"><span class="kicker" style="color:#8a6a1e">R&amp;D, Innovation &amp; Industrial Consultancy</span><h2 style="font-size:var(--step-3)">Ideas that leave the classroom</h2>
    <p>Research in renewable energy, vehicle safety and electric mobility, structural and CFD consultancy for government projects, and student innovations that made national news.</p>
    <div class="chips"><span>Solar receiver glass-metal seals</span><span>Vehicle safety</span><span>Electric mobility</span><span>Auto gear shifting</span><span>Smart stick</span><span>Anti-roll braking</span></div>
    <div class="actions" style="justify-content:flex-start"><a class="btn btn-primary" href="research-project-innovation">Explore R&amp;D</a><a class="btn btn-ghost" href="research-project-innovation#consultancy">Consultancy</a></div></div>
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
  <div class="steps swipe" style="grid-template-columns:repeat(4,1fr)"><div class="step rv"><i>▶</i><b>Lecture plans &amp; videos</b><span>40–50 structured lectures per subject</span></div><div class="step rv"><i>⬇</i><b>Notes &amp; PPT/PDF</b><span>Download-ready lecture resources</span></div><div class="step rv"><i>✎</i><b>Quizzes &amp; tests</b><span>Topic quizzes linked to Test Lab</span></div><div class="step rv"><i>💡</i><b>Project ideas</b><span>Innovation and final-year project ideas</span></div></div>
  <p style="margin:6px 0 18px;color:var(--gold);font-family:var(--f-head);font-weight:700">Free forever. One-time 30-second sign-up:</p>
  <div class="steps"><div class="step rv"><i>1</i><b>Subscribe</b><span>Subscribe to the VKVSir YouTube channel (account 1+ month old).</span></div><div class="step rv rv-d1"><i>2</i><b>Sign in with Google</b><span>Use the same Google account on the join page.</span></div><div class="step rv rv-d2"><i>3</i><b>Start learning</b><span>Access all courses, notes and quizzes instantly.</span></div></div>
  <div class="actions" style="justify-content:flex-start"><a class="btn btn-gold" href="join">Join membership – free</a><a class="btn btn-light" href="members">Explore members area</a></div>
</div></section>

<section class="sec sec-white" id="blog"><div class="wrap">
  <div class="sec-head rv"><div><span class="kicker">Blog &amp; LinkedIn</span><h2>Posts &amp; articles</h2><p>In today's world networking is the key to success.</p></div><a class="link-more" href="blog">All posts</a></div>
  <div class="grid grid-3 swipe">{post_cards(posts[:3], True)}</div>
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
page("index","VKVSir – Dr. Vinod Kumar Verma | Automobile Engineering, EV & Workshop Courses",
 "Free Automobile Engineering, Hybrid & Electric Vehicles, Workshop Practice and Machine Drawing lectures in Hindi & English by Dr. Vinod Kumar Verma (VKVSir), Engineering College Ajmer. PPTs, PDFs, MCQs and online tests.",
 home, home_js.replace("</script>", "dbRpc('get_public_stats').then(s=>document.querySelectorAll('[data-stat=total]').forEach(e=>e.textContent=s.total_questions.toLocaleString('en-IN'))).catch(()=>{});</script>"))

# =================== ABOUT ===================
about = banner("About VKVSir","Dr. Vinod Kumar Verma (Ph.D., M.Tech., MBA): professor, innovator, consultant and mentor at Engineering College Ajmer.","About") + """
<style>.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:18px}.fact{background:#fff;border:1px solid var(--line);border-top:4px solid var(--gold);border-radius:var(--r);padding:22px;box-shadow:var(--sh)}.fact h3{font-size:var(--step-1);margin-bottom:.4em}.fact p,.fact li{color:var(--muted)}.fact p{margin:0}.fact ul{margin:0;padding-left:18px}.split{display:grid;grid-template-columns:.85fr 1.15fr;gap:clamp(30px,5vw,60px);align-items:start}.split img{border-radius:var(--r-lg);box-shadow:var(--sh-lg);position:sticky;top:calc(var(--hh) + 20px)}.sk{text-align:center;font-size:var(--step-2);font-family:var(--f-head);color:var(--g800);margin-top:40px}@media(max-width:900px){.split{grid-template-columns:1fr}.split img{position:static;max-width:420px;margin:0 auto}}</style>
<section class="sec sec-white"><div class="wrap"><div class="facts">
 <div class="fact rv"><h3>Profile</h3><p>Dr. Vinod Kumar Verma has served as a faculty member in the Department of Mechanical Engineering at Engineering College Ajmer since 2008. He is recognised for his expertise in Automobile Engineering, Renewable Energy, Marketing, and New Product Design &amp; Launching.</p></div>
 <div class="fact rv rv-d1"><h3>Education</h3><p>Diploma topper (Govt. Polytechnic, Kota); B.E. (MBM Engineering College, Jodhpur); M.Tech. (IIT Jodhpur); Ph.D.; and MBA in Marketing (Symbiosis, Pune).</p></div>
 <div class="fact rv rv-d2"><h3>Experience</h3><p>More than five years in industry, including two years as a project manager in Dubai and Afghanistan, and over seventeen years in teaching, with a mission to empower the young generation through quality education and meaningful opportunities.</p></div>
 <div class="fact rv"><h3>Awards &amp; recognition</h3><p>Honoured and appreciated by the Former President of India, Late Shri Pranab Mukherjee; the Union MHRD Minister, Dr. Satyapal Singh; the Education Minister of Rajasthan; the District Collector of Ajmer; and many other dignitaries.</p></div>
 <div class="fact rv rv-d1"><h3>Consultancy &amp; expert roles</h3><ul><li>Consultancy work delivered for various industries and government projects.</li><li>Expert in examination and evaluation for statutory bodies including RPSC, Rajasthan Board, MPUAT, RTU Kota, the University of Rajasthan, etc.</li></ul></div>
 <div class="fact rv rv-d2"><h3>Milestones</h3><ul><li>Granted patent on an automatic fire-extinguishing and window-breaking system for cars.</li><li>Publications in reputed national and international journals.</li><li>Founder of SAEINDIA at ECA; team reached the BAJA main round.</li><li>Organised 60+ seminars, industrial tours and workshops; invited expert and keynote speaker.</li></ul></div>
</div><p class="sk rv">सर्वे भवन्तु सुखिनः · Jai Hind!</p></div></section>
<section class="sec sec-mint"><div class="wrap split">
 <img class="rv" src="https://static.wixstatic.com/media/b90d41_4866adbee9464682abf4a1dfda66fb69~mv2.png/v1/crop/x_185,y_93,w_1153,h_1407/fill/w_520,h_634,al_c,q_85,enc_auto/vkv.png" width="520" height="634" loading="lazy" alt="Dr. Vinod Kumar Verma">
 <div class="rv rv-d1"><span class="kicker">More about VKVSir</span><h2 style="font-size:var(--step-3)">Where education, innovation and mentorship meet</h2>
 <p>Welcome to the official website of Dr. Vinod Kumar Verma, affectionately known as VKVSir, a respected name in automobile engineering, manufacturing processes and innovation.</p>
 <p>With more than two decades of combined corporate and academic experience, Dr. Verma brings practical insight to every classroom. His five years in industry, including two years abroad as a project manager, gave him a first-hand understanding of real-world engineering challenges and how to solve them.</p>
 <p>What truly sets him apart is his passion for teaching and innovation. Over more than seventeen years in academia, he has guided countless students towards their academic and professional goals. His commitment to innovation is reflected in his research publications, a granted patent, and consultancy work delivered for various industries and government projects.</p>
 <p>Beyond the classroom, Dr. Verma is valued as a mentor and motivator. Students regularly seek his advice on careers and personal growth, drawn by his genuine wish to see them succeed. As a coordinator of the Training and Placement Cell, he bridges academia and industry by building partnerships with leading companies and HR professionals. He also serves statutory bodies such as RPSC, RTU Kota, MPUAT, the Rajasthan Board and the University of Rajasthan as an expert in examination and evaluation.</p>
 <p>His academic journey spans a B.E. from MBM Engineering College, Jodhpur, an M.Tech. from the Indian Institute of Technology Jodhpur, a Ph.D., and an MBA from Symbiosis, Pune.</p>
 <p>An active voice on <a href="https://www.linkedin.com/in/vkvsir" target="_blank" rel="noopener">LinkedIn</a>, Dr. Verma shares his knowledge and mentorship with learners and professionals worldwide.</p>
 <p>We invite you to explore the world of Dr. Vinod Kumar Verma, where education, innovation and mentorship come together to shape the leaders of tomorrow.</p>
 <div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-primary" href="contact">Contact VKVSir</a><a class="btn btn-ghost" href="research-project-innovation">R&amp;D &amp; consultancy</a></div></div>
</div></section>"""
page("about","About Dr. Vinod Kumar Verma (VKVSir) | Engineering College Ajmer",
 "Dr. Vinod Kumar Verma (VKVSir): Mechanical Engineering faculty at Engineering College Ajmer since 2008. Ph.D., M.Tech IIT Jodhpur, MBA Symbiosis. Government consultancy, expert examiner for RPSC, RTU, MPUAT.",
 about, crumbs="About")

# =================== COURSES ===================
cbody = banner("Courses taught","Full course lectures in Hindi &amp; English with animations, PPTs, PDFs and MCQs. Course pages are in the free Members Area.","Courses") + f"""
<section class="sec sec-white"><div class="wrap"><div class="grid grid-3">{course_cards()}</div></div></section>
<section class="sec sec-mint"><div class="wrap" style="display:grid;gap:22px;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr))">
 <div class="card rv" style="padding:26px"><span class="tag">Practice</span><h3 style="margin:.6em 0 .3em">MVSI / RTO Inspector Practice Sheet 1</h3><p>Exam-style questions for MVSI / RTO Inspector aspirants.</p><a class="btn btn-primary" style="align-self:flex-start;margin-top:12px" href="https://forms.gle/uDEB4LovbrKjtFTH9" target="_blank" rel="noopener">Open practice sheet</a></div>
 <div class="card rv rv-d1" style="padding:26px"><span class="tag">Online tests</span><h3 style="margin:.6em 0 .3em">VKV Sir Test Lab</h3><p>Topic-wise and unit-wise timed MCQ tests with instant results.</p><a class="btn btn-gold" style="align-self:flex-start;margin-top:12px" href="{TESTLAB}" target="_blank" rel="noopener">Open Test Lab</a></div>
 <div class="card rv rv-d2" style="padding:26px"><span class="tag">Free membership</span><h3 style="margin:.6em 0 .3em">Unlock all course material</h3><p>Free for YouTube subscribers, approved automatically.</p><a class="btn btn-yt" style="align-self:flex-start;margin-top:12px" href="join">Join membership – free</a></div>
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
def fea_svg(kind):
    # Representative FE-style contour renders (illustrative)
    if kind == "tent":
        mesh = "".join(f'<path d="M{40+i*20} 200 L{40+i*20} {200-min(i,16-i)*13}" stroke="#0b1f2a" stroke-width=".6" opacity=".5"/>' for i in range(17))
        return f'''<svg viewBox="0 0 400 250" width="100%" height="100%" role="img" aria-label="Representative von Mises stress contour of a tent frame"><defs><linearGradient id="g1" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#1e3cff"/><stop offset=".3" stop-color="#00c2ff"/><stop offset=".55" stop-color="#2bd96b"/><stop offset=".8" stop-color="#ffe14d"/><stop offset="1" stop-color="#ff3b30"/></linearGradient><radialGradient id="h1" cx=".5" cy=".25" r=".6"><stop offset="0" stop-color="#ff3b30" stop-opacity=".9"/><stop offset=".4" stop-color="#ffe14d" stop-opacity=".6"/><stop offset="1" stop-color="#00c2ff" stop-opacity="0"/></radialGradient></defs><rect width="400" height="250" fill="#0b1f2a"/><path d="M40 200 L200 44 L360 200Z" fill="url(#g1)" opacity=".85"/><path d="M40 200 L200 44 L360 200Z" fill="url(#h1)"/>{mesh}<g stroke="#e8f1f4" stroke-width="2.2" fill="none"><path d="M40 200 L200 44 L360 200 M120 200 L120 122 M200 200 L200 44 M280 200 L280 122 M40 200 L360 200"/></g><rect x="14" y="14" width="10" height="120" fill="url(#g1)"/><g fill="#cfd8d5" font-family="Arial" font-size="9"><text x="28" y="22">186 MPa</text><text x="28" y="134">0.4 MPa</text><text x="300" y="236">ANSYS-style FEA</text></g></svg>'''
    return '''<svg viewBox="0 0 400 250" width="100%" height="100%" role="img" aria-label="Representative wind pressure contour on a stainless-steel hangar"><defs><linearGradient id="g2" x1="0" x2="1"><stop offset="0" stop-color="#ff3b30"/><stop offset=".25" stop-color="#ffe14d"/><stop offset=".5" stop-color="#2bd96b"/><stop offset=".75" stop-color="#00c2ff"/><stop offset="1" stop-color="#1e3cff"/></linearGradient><linearGradient id="g3" x1="0" x2="1"><stop offset="0" stop-color="#1e3cff"/><stop offset=".5" stop-color="#2bd96b"/><stop offset="1" stop-color="#ff3b30"/></linearGradient></defs><rect width="400" height="250" fill="#0b1f2a"/><g fill="none" stroke="url(#g3)" stroke-width="1.6" opacity=".85"><path d="M0 70 C140 70 160 48 220 48 S320 72 400 72"/><path d="M0 92 C130 92 150 66 220 66 S330 96 400 96"/><path d="M0 114 C120 114 140 86 220 86 S340 120 400 118"/><path d="M0 136 C110 136 140 108 220 106 S350 150 400 140"/></g><path d="M90 205 L90 158 Q200 82 310 158 L310 205Z" fill="url(#g2)"/><g stroke="#0b1f2a" stroke-width=".7" opacity=".55">''' + "".join(f'<path d="M{90+i*11} 205 L{90+i*11} {158-((i*(20-i))*0.75)}"/>' for i in range(21)) + '''</g><path d="M90 205 L90 158 Q200 82 310 158 L310 205" fill="none" stroke="#e8f1f4" stroke-width="2"/><rect x="0" y="205" width="400" height="45" fill="#13303a"/><rect x="14" y="14" width="120" height="8" fill="url(#g2)"/><g fill="#cfd8d5" font-family="Arial" font-size="9"><text x="14" y="34">+0.9 kPa</text><text x="104" y="34">−1.2 kPa</text><text x="300" y="236">CFD wind study</text></g></svg>'''

AREAS = ["Automobile engineering","IC engines","Electric vehicles &amp; batteries","Renewable energy","Bi-metallic joints","Glass–metal joints","Nano-materials"]
SERVICES = [("Structural &amp; CFD analysis","FEA of frames, tents, hangars and machine parts; wind and flow studies."),("Material strength testing","Mechanical and joint-strength testing with expert interpretation."),("Research &amp; development","Sponsored research, prototyping and product development."),("Design &amp; testing","Concept-to-drawing design, validation and test planning."),("Plant commissioning &amp; erection","Guidance for new plant and machinery, installation and trials."),("Capacity building &amp; scale-up","Scaling plants, process improvement, business planning, etc.")]
MAIL = "mailto:vinodvermavkvsir@gmail.com?subject="
rd = banner("R&amp;D, Innovation &amp; Industrial Consultancy","Research, a granted patent, consultancy for government and industry, and student innovations that made national news.","R&amp;D &amp; Consultancy") + f"""
<style>.pat{{display:grid;grid-template-columns:1.2fr .8fr;gap:28px;align-items:center;background:#fff;border-radius:var(--r-lg);padding:clamp(20px,4vw,40px);box-shadow:var(--sh);border-left:6px solid var(--gold)}}
.pubs{{display:grid;gap:12px}}.pub{{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:16px 20px;display:grid;grid-template-columns:auto 1fr;gap:14px;align-items:start}}.pub b{{font-family:var(--f-head);background:var(--g100);color:var(--g500);border-radius:8px;padding:4px 10px;font-size:14px}}.pub h3{{font-size:16.5px;margin:0 0 4px}}.pub p{{margin:0;font-size:14.5px;color:var(--muted)}}
.viz{{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}}.viz figure{{margin:0;background:#0b1f2a;border-radius:var(--r);overflow:hidden;border:1px solid rgba(255,255,255,.12)}}.viz figcaption{{padding:14px 16px;color:#cfdcd7;font-size:15px}}.viz figcaption b{{font-family:var(--f-head);color:#fff;display:block;margin-bottom:4px}}.viz .rep{{display:inline-block;font-family:var(--f-head);font-size:11.5px;font-weight:700;background:#fff3cd;color:#7a5b00;padding:2px 8px;border-radius:999px;margin-bottom:8px}}
.svc{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:22px}}.svc div{{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:var(--r);padding:16px}}.svc b{{font-family:var(--f-head);color:#fff;display:block}}.svc span{{color:#b9cbc4;font-size:14.5px}}
.areas{{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 4px}}.areas span{{font-family:var(--f-head);font-weight:600;font-size:14px;padding:7px 14px;border-radius:999px;background:rgba(216,178,90,.15);color:var(--gold);border:1px solid rgba(216,178,90,.35)}}
.invite{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}.inv{{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:22px;box-shadow:var(--sh);display:flex;flex-direction:column;gap:8px}}.inv h3{{font-size:19px;margin:0}}.inv p{{margin:0;color:var(--muted);font-size:15.5px}}.inv .btn{{margin-top:auto;align-self:flex-start}}
@media(max-width:900px){{.pat,.viz{{grid-template-columns:1fr}}.svc,.invite{{grid-template-columns:1fr 1fr}}}}@media(max-width:600px){{.svc,.invite{{grid-template-columns:1fr}}}}</style>
<section class="sec sec-gold"><div class="wrap"><div class="pat rv"><div><span class="tag" style="background:var(--gold-soft);color:#8a6a1e">Patent granted</span><h2 style="font-size:var(--step-3);margin:.5em 0 .4em">Automatic Fire Extinguisher and Window Breaking System for Passenger Cars</h2><p>Inventors: Vinod Kumar Verma, Arpit Mathur, Jaya Khatwani · Government Engineering College Ajmer (application 201811026495).</p><p style="color:var(--muted)">A safety system that detects fire in a passenger car, extinguishes it automatically and breaks the window so occupants can escape.</p></div>
<img src="{W('b90d41_eb2104b6597649e4a5c0b65bd44f0619~mv2.jpg',600,400)}" width="600" height="400" loading="lazy" alt="Student innovation in the news" style="border-radius:var(--r)"></div></div></section>
<section class="sec sec-deep" id="consultancy"><div class="wrap">
 <div class="sec-head rv"><div><span class="kicker">Industrial consultancy</span><h2>Engineering expertise for industry &amp; government</h2><p>We have delivered consultancy work for various industries and government projects, and we are <b style="color:#fff">open to new consultancy assignments</b>: structural analysis, material testing, research, design, plant commissioning, business scale-up and much more.</p></div><a class="btn btn-gold" href="{MAIL}Consultancy%20enquiry">✉ Contact now</a></div>
 <div class="viz">
  <figure class="rv"><picture><source srcset="assets/img/analysis-tent.webp" type="image/webp"><img src="assets/img/analysis-tent.jpg" width="1159" height="609" loading="lazy" alt="Structural analysis of a large tent frame (representative)" style="width:100%;height:auto;display:block"></picture><figcaption><span class="rep">Representative illustration · not actual project data</span><b>Structural analysis of a large tent frame</b>A finite-element model of the tubular steel frame under dead, live and wind loads. Stress contours locate the most loaded members and joints, so sections are sized safely without over-design, and anchorage forces are checked for uplift.</figcaption></figure>
  <figure class="rv rv-d1"><picture><source srcset="assets/img/analysis-hangar.webp" type="image/webp"><img src="assets/img/analysis-hangar.jpg" width="1097" height="617" loading="lazy" alt="Wind study of a stainless-steel hangar (representative)" style="width:100%;height:auto;display:block"></picture><figcaption><span class="rep">Representative illustration · not actual project data</span><b>Wind study of a stainless-steel hangar</b>A CFD wind-flow simulation gives the pressure distribution over the curved roof. These loads feed the structural model to verify deflection, buckling and fatigue life of the SS arches and purlins.</figcaption></figure>
 </div>
 <figure class="rv" style="margin:18px 0 0;background:#0b1f2a;border-radius:var(--r);overflow:hidden;border:1px solid rgba(255,255,255,.12);display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));align-items:center" id="susp"><div style="aspect-ratio:16/10"><svg viewBox="0 0 400 250" width="100%" height="100%" role="img" aria-label="Representative stress plot of a suspension arm"><defs><linearGradient id="sg" x1="0" x2="1"><stop offset="0" stop-color="#1e3cff"/><stop offset=".35" stop-color="#00c2ff"/><stop offset=".55" stop-color="#2bd96b"/><stop offset=".78" stop-color="#ffe14d"/><stop offset="1" stop-color="#ff3b30"/></linearGradient></defs><rect width="400" height="250" fill="#0b1f2a"/><path d="M60 190 C110 170 160 120 230 92 L320 60 Q340 54 344 72 Q348 88 330 94 L246 124 C190 146 140 196 92 214 Q66 222 58 206 Q54 196 60 190Z" fill="url(#sg)" stroke="#e8f1f4" stroke-width="2"/><circle cx="74" cy="204" r="14" fill="#13303a" stroke="#e8f1f4" stroke-width="2"/><circle cx="330" cy="74" r="12" fill="#13303a" stroke="#e8f1f4" stroke-width="2"/><g stroke="#ffb547" stroke-width="2.5"><path d="M330 20 L330 52"/><path d="M324 44 L330 54 L336 44" fill="none"/></g></svg></div><figcaption style="padding:18px 20px;color:#cfdcd7;font-size:15px"><span class="rep">Representative illustration</span><b style="font-family:var(--f-head);color:#fff;display:block;margin-bottom:4px">Structural Static &amp; Stress Analysis of Automotive Components</b>Evaluates the internal shear stress, bending moment distribution and elastic deflection of critical vehicle suspension members under operational loads. This ensures the component meets structural strength requirements, prevents mechanical failure and satisfies safe payload capacities.</figcaption></figure>

 <h3 class="rv" style="margin-top:34px;font-size:var(--step-2)">Areas of expertise</h3><div class="areas rv">{''.join(f'<span>{a}</span>' for a in AREAS)}<span>…and many more</span></div>
 <div class="svc">{''.join(f'<div class="rv"><b>{t}</b><span>{d}</span></div>' for t,d in SERVICES)}</div>
</div></section>
<section class="sec sec-white"><div class="wrap"><div class="sec-head rv"><div><span class="kicker">Work with us</span><h2>Let's build something together</h2><p>Whether you are a student, a researcher or an industry professional, we welcome collaboration in these fields. Write to us with a short description and we will get back to you.</p></div></div>
<div class="invite">
 <div class="inv rv"><span class="tag">Industry &amp; government</span><h3>Consultancy projects</h3><p>Structural and CFD analysis, material testing, R&amp;D, design and testing, plant commissioning, capacity building, scale-up, etc.</p><a class="btn btn-primary" href="{MAIL}Consultancy%20project%20enquiry">Discuss a project</a></div>
 <div class="inv rv rv-d1"><span class="tag">Students &amp; scholars</span><h3>M.Tech &amp; Ph.D. guidance</h3><p>Students interested in pursuing an M.Tech or Ph.D. under Dr. Verma's guidance, by joining Engineering College Ajmer or as a scholar of another university through research collaboration, are welcome to get in touch. Please share your background and research interest.</p><a class="btn btn-primary" href="{MAIL}M.Tech%20%2F%20PhD%20guidance%20enquiry">Enquire about guidance</a></div>
 <div class="inv rv rv-d2"><span class="tag">Institutes &amp; companies</span><h3>Expert lectures &amp; lab setup</h3><p>Invite Dr. Verma for expert lectures, keynote talks, technical advice, lab-setup guidance and more in these domains. Faculty and industry professionals are equally welcome to collaborate.</p><a class="btn btn-gold" href="{MAIL}Invitation%20for%20expert%20lecture%20%2F%20advice">Send an invitation</a></div>
</div></div></section>
<section class="sec sec-mint"><div class="wrap"><div class="sec-head rv"><div><span class="kicker">Student projects</span><h2>Innovations that made the news</h2></div><a class="link-more" href="media">Media gallery</a></div>
<div class="grid swipe">{''.join(f'<div class="card rv rv-d{n%3+1}"><div class="ph">{IMG(i,600,400,t)}</div><div class="bd"><h3>{t}</h3><p>{d}</p></div></div>' for n,(i,t,d) in enumerate([("b90d41_72163043971a4e49a9479397ab2d1168~mv2.jpg","Automatic gear system","Microcontroller-based automatic gear shifting for auto-clutch bikes."),("b90d41_eb2104b6597649e4a5c0b65bd44f0619~mv2.jpg","Anti-roll braking","A braking concept to reduce vehicle roll-over risk."),("b90d41_b9aaebb9bd604fa8b5854408b7173a8b~mv2.jpg","Smart stick","Assistive smart stick project featured in Dainik Bhaskar."),("b90d41_d87f56553ddc4852b747b20ab28cde90~mv2.png","SAE BAJA","ECA team at the SAE BAJA main round."),("b90d41_b3fa9e02c8af40e6bd557244e44df2ef~mv2.jpg","Lab experiments","Hands-on experiments in renewable energy and automobile labs."),("b90d41_22ccfd37e9384f73a0c6540086034ff0~mv2.jpg","Air Force seminar","Seminars connecting students with defence and industry experts.")]))}</div></div></section>
<section class="sec sec-white"><div class="narrow"><div class="sec-head rv"><div><span class="kicker">Publications</span><h2>Selected research</h2></div><a class="link-more" href="https://scholar.google.com/citations?user=CDzm7o8AAAAJ" target="_blank" rel="noopener">Google Scholar</a></div>
<div class="pubs">{''.join(f'<div class="pub rv"><b>{y}</b><div><h3>{E(t)}</h3><p>{E(j)}</p></div></div>' for t,j,y in pubs)}</div></div></section>"""
page("research-project-innovation","R&D, Innovation & Industrial Consultancy | Dr. Vinod Kumar Verma (VKVSir)",
 "Research, innovation and consultancy by Dr. Vinod Kumar Verma: structural FEA and CFD consultancy, granted patent on an automatic fire extinguisher and window breaking system for cars, solar receiver research, EV and vehicle safety publications, and student projects.",
 rd, crumbs="R&D & Industrial Consultancy")

# =================== MEDIA ===================
def rplus(n):
    step=1000 if n>=1000 else 100 if n>=100 else 10 if n>=50 else 5
    r=(n//step)*step
    return f'{r or n}+'
def mcat(c):
    c2=c.lower()
    if any(k in c2 for k in ["gear","braking","smart stick","baja"]): return "innovation"
    if any(k in c2 for k in ["seminar","pcra","lab"]): return "events"
    if any(k in c2 for k in ["campus","students"]): return "campus"
    if any(k in c2 for k in ["bhaskar","patrika","navjyoti"]): return "press"
    return "events"
cats=[("all","All"),("press","Newspaper coverage"),("innovation","Student innovations"),("events","Seminars & events"),("campus","Campus life")]
counts={k:sum(1 for i,c in MEDIA if mcat(c)==k) for k,_ in cats[1:]}
mbody = banner("Media appearances","Press coverage, student innovations, seminars and campus moments from 2016 onwards. Tap any picture to view it in full.","Media") + f"""
<style>.mstats{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:30px}}.mstats div{{background:var(--g100);border-radius:var(--r);padding:18px;text-align:center}}.mstats b{{display:block;font-family:var(--f-head);font-size:var(--step-3);color:var(--g800);line-height:1}}.mstats span{{font-family:var(--f-head);font-size:14px;color:var(--muted)}}
.filters{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:26px}}.filters button{{font-family:var(--f-head);font-weight:600;font-size:15px;border:1.5px solid var(--line);background:#fff;color:var(--g800);padding:8px 18px;border-radius:999px;cursor:pointer}}.filters button.on{{background:var(--g800);border-color:var(--g800);color:#fff}}
.masonry{{columns:4 240px;column-gap:16px}}.masonry figure{{margin:0 0 16px;break-inside:avoid;background:#fff;border:1px solid var(--line);border-radius:var(--r);overflow:hidden;box-shadow:var(--sh);position:relative;transition:transform .2s}}.masonry figure:hover{{transform:translateY(-3px)}}.masonry img{{width:100%;height:auto}}.masonry figcaption{{font-family:var(--f-head);font-size:13.5px;color:var(--muted);padding:10px 12px;display:flex;justify-content:space-between;gap:8px}}.masonry figcaption i{{font-style:normal;color:var(--g500);font-size:12px;white-space:nowrap}}
.ytband{{display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap;background:linear-gradient(120deg,#1a0f0f,#3a1212);color:#fff;border-radius:var(--r-lg);padding:clamp(24px,4vw,40px);margin-top:40px}}.ytband h2{{color:#fff;margin:0 0 6px}}.ytband p{{margin:0;color:#e6caca}}
@media(max-width:700px){{.mstats{{grid-template-columns:repeat(2,1fr)}}}}</style>
<section class="sec sec-white"><div class="wrap">
<div class="mstats rv">{''.join(f'<div><b>{rplus(counts[k])}</b><span>{t}</span></div>' for k,t in cats[1:])}</div>
<div class="filters" role="group" aria-label="Filter media">{''.join(f'<button data-c="{k}" class="{"on" if k=="all" else ""}">{t}</button>' for k,t in cats)}</div>
<div class="masonry" id="mgrid">
{''.join(f'<figure data-c="{mcat(c)}"><img src="https://static.wixstatic.com/media/{i}/v1/fit/w_480,h_900,q_80,enc_auto/m.jpg" data-full="{FIT(i)}" loading="lazy" decoding="async" alt="{E(c)}"><figcaption>{E(c)}<i>{dict(cats)[mcat(c)]}</i></figcaption></figure>' for i,c in MEDIA)}
</div>
<div class="ytband rv"><div><h2>Watch the lectures on YouTube</h2><p>Free full courses in Hindi &amp; English with animations. New videos every month.</p></div><a class="btn btn-yt" href="https://www.youtube.com/@vkvsirdotcom?sub_confirmation=1" target="_blank" rel="noopener">▶ Subscribe on YouTube</a></div>
</div></section>"""
mjs = "<script>lightbox('#mgrid img');document.querySelectorAll('.filters button').forEach(b=>b.onclick=()=>{document.querySelectorAll('.filters button').forEach(x=>x.classList.toggle('on',x===b));document.querySelectorAll('#mgrid figure').forEach(f=>f.hidden=!(b.dataset.c==='all'||f.dataset.c===b.dataset.c));});</script>"
page("media","Media Appearances of VKVSir | Newspaper Coverage & Seminars",
 "Media appearances of Dr. Vinod Kumar Verma (VKVSir): Dainik Bhaskar, Rajasthan Patrika and Navjyoti coverage of seminars, student innovations, BAJA and awards.",
 mbody, mjs, crumbs="Media")

# =================== BLOG ===================
years = sorted({p["date"][:4] for p in posts}, reverse=True)
bbody = banner("Blog &amp; LinkedIn","Posts, wishes, events and thoughts from VKVSir.","Blog") + f"""
<style>.filters{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:30px}}.filters button{{font-family:var(--f-head);font-weight:600;font-size:15px;border:1.5px solid var(--line);background:#fff;color:var(--g800);padding:8px 18px;border-radius:999px;cursor:pointer;transition:.15s}}.filters button:hover{{border-color:var(--g500)}}.filters button.on{{background:var(--g800);border-color:var(--g800);color:#fff}}</style>
<section class="sec sec-white"><div class="wrap">
<div class="filters" role="group" aria-label="Filter posts by year"><button class="on" data-y="all">All</button>{''.join(f'<button data-y="{y}">{y}</button>' for y in years)}</div>
<div class="grid grid-3" id="posts">{post_cards(posts)}</div>
<p style="text-align:center;margin-top:40px"><a class="btn btn-ghost" href="https://www.linkedin.com/in/vkvsir" target="_blank" rel="noopener">Follow on LinkedIn</a></p></div></section>"""
bjs = "<script>document.querySelectorAll('.filters button').forEach(b=>b.onclick=()=>{document.querySelectorAll('.filters button').forEach(x=>x.classList.toggle('on',x===b));document.querySelectorAll('#posts .card').forEach(c=>c.hidden=!(b.dataset.y==='all'||c.dataset.year===b.dataset.y));});</script>"
page("blog","Blog & LinkedIn | VKVSir Posts and Articles","Posts, wishes, events, webinars and thoughts by Dr. Vinod Kumar Verma (VKVSir), Engineering College Ajmer.", bbody, bjs, crumbs="Blog")

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
 <div class="rv"><span class="kicker">Address</span><h2 style="font-size:var(--step-3)">Visit the department</h2><p>Dr. Vinod Kumar Verma<br>NB-202, New Building,<br>Engineering College Ajmer<br>Rajasthan, India – 305025</p><a class="btn btn-primary" href="mailto:vinodvermavkvsir@gmail.com">Send an email</a></div>
 <iframe class="rv rv-d1" loading="lazy" title="Map of Engineering College Ajmer" src="https://www.google.com/maps?q=Government+Engineering+College+Ajmer&output=embed" referrerpolicy="no-referrer-when-downgrade"></iframe>
</div></section>"""
page("contact","Contact VKVSir | Dr. Vinod Kumar Verma, Engineering College Ajmer",
 "Contact Dr. Vinod Kumar Verma (VKVSir) by email, YouTube, LinkedIn, Instagram, Facebook, Twitter, Telegram or visit NB-202, Engineering College Ajmer, Rajasthan 305025.", ctbody, crumbs="Contact")

page("404","Page not found | VKVSir","Page not found", banner("Page not found","This page has moved. Try the menu above or go back home.")+'<section class="sec sec-white"><div class="wrap" style="text-align:center"><a class="btn btn-primary" href="./">Go to homepage</a></div></section>')


# =================== COURSE & MEMBERS PAGES ===================
JOIN_BOX = f"""<div class="free rv"><div><span class="kicker">Members only · free forever</span><h2>Unlock videos, notes &amp; quizzes</h2><p>Membership is completely free, and will always stay free. It takes about 30 seconds, only once:</p><ol><li>Subscribe to the VKVSir YouTube channel (account at least 1 month old).</li><li>Click <b>Join free</b> and sign in with the same Google account.</li><li>Access is granted instantly.</li></ol></div><div class="actions"><a class="btn btn-gold" href="join">Join free now</a><a class="btn btn-light" href="https://www.youtube.com/@vkvsirdotcom?sub_confirmation=1" target="_blank" rel="noopener">Subscribe on YouTube</a></div></div>"""
CMETA = {
 "automobile-engineering": dict(title="Automobile Engineering", course="Automobile Engineering", img="11062b_42b9ecea6a1540668defdedea80d1a9d~mv2.jpg",
   lead="A complete 36-hour course (about 6 weeks) covering the modern vehicle from chassis to air-conditioning, in easy Hindi &amp; English with animations.",
   why=["The core subject for Mechanical and Automobile students in Diploma, B.Tech and AMIE programmes.","Directly useful for RTO / MVI Inspector, GATE, PSU and automotive industry interviews.","Builds the foundation for electric and hybrid vehicle technology."],
   learn=["Chassis, frames and automotive materials","Clutches, gearboxes, automatic transmission and differentials","Brakes, steering geometry and suspension systems","Wheels, tyres, axles and drive layouts","Battery, starting, charging, ignition and lighting systems","Automotive air-conditioning and refrigerants"],
   books=[("Automobile Engineering, Vol. 1","Dr. Kirpal Singh"),("A Textbook of Automobile Engineering – I","P. S. Gill"),("Automobile Engineering","R. B. Gupta"),("Automotive Mechanics","N. K. Giri")]),
 "manufacturing-processes": dict(title="Manufacturing Processes", course="Manufacturing Processes", img="aef2ab657d574a17adc9dc6a7312c958.jpg",
   lead="Foundry, casting, welding, forming and powder metallurgy: how engineering parts are actually made, from fundamentals to advanced processes.",
   why=["A core subject for Mechanical, Production and Industrial engineering in Diploma, B.Tech and AMIE.","Heavily asked in GATE, ESE, PSU and state engineering service exams.","Directly applicable on the shop floor, in quality and in process engineering roles."],
   learn=["Patterns, moulding sand, cores, gating and risering","Sand, die, centrifugal, investment and other casting processes","Gas, arc, TIG, MIG, resistance and special welding processes","Forging, rolling, extrusion, drawing and press work","Powder metallurgy, defects and their remedies, and much more"],
   books=[("Manufacturing Technology, Vol. 1","P. N. Rao"),("Elements of Workshop Technology, Vol. 1","Hajra Choudhury"),("Manufacturing Science","Ghosh &amp; Mallik"),("Materials and Processes in Manufacturing","DeGarmo, Black &amp; Kohser")]),
 "hev": dict(title="Hybrid & Electric Vehicles", course="Hybrid & Electric Vehicles", img="11062b_0d56d33639234010a96c69ca297bf60a~mv2.jpg",
   lead="From batteries and motors to power electronics and charging: understand the technology driving electric mobility.",
   why=["Electric mobility is the fastest-growing area in the automotive industry.","Essential for EV-focused jobs, projects and research.","Connects mechanical, electrical and electronics knowledge."],
   learn=["EV and HEV architectures","Battery types, BMS and charging","Electric motors and controllers","Regenerative braking and energy management"],
   books=[("Electric and Hybrid Vehicles: Design Fundamentals","Iqbal Husain"),("Modern Electric, Hybrid Electric and Fuel Cell Vehicles","M. Ehsani et al.")]),
 "workshop-practice": dict(title="Workshop Practice", course="Workshop Practice", img="e592d5b87e234c849e8363ee949932a0.jpg",
   lead="Hands-on fundamentals of the engineering workshop: tools, processes and safe practice.",
   why=["Compulsory first-year subject for all engineering branches.","Builds practical skills valued in labs and industry.","Foundation for manufacturing and production subjects."],
   learn=["Fitting, carpentry and smithy","Welding and sheet-metal work","Measuring instruments","Workshop safety"],
   books=[("Elements of Workshop Technology, Vol. 1 & 2","Hajra Choudhury"),("Workshop Technology","W. A. J. Chapman")]),
 "machine-drawing": dict(title="Machine Drawing", course="Machine Drawing", img="7fba3905ea184ee29642cf0def056821.jpg",
   lead="Read and create engineering drawings with confidence: projections, sections, fasteners and assemblies.",
   why=["The language of engineers across design and manufacturing.","Essential for CAD, design roles and university exams.","Improves visualisation and precision."],
   learn=["Orthographic projections and sections","Fasteners, keys and couplings","Limits, fits and tolerances","Assembly and detail drawings"],
   books=[("Machine Drawing","N. D. Bhatt"),("Machine Drawing","K. L. Narayana")]),
 "casting-process": dict(title="Casting Process", course="Casting Process", img="aef2ab657d574a17adc9dc6a7312c958.jpg",
   lead="Metal casting from pattern to finished part: moulding, melting, pouring and defect control.",
   why=["A core manufacturing process asked in university, GATE and PSU exams.","Widely used in automotive and heavy industry.","Links materials science with production."],
   learn=["Patterns and allowances","Moulding sands and methods","Gating and risering","Special casting processes and defects"],
   books=[("Manufacturing Technology, Vol. 1","P. N. Rao"),("Manufacturing Processes for Engineering Materials","Kalpakjian &amp; Schmid")]),
 "pdl": dict(title="New Product Design & Launching", course="New Product Design & Launching", img="9d090cf24c96432db9c956dbdac792f6.jpg",
   lead="Turn ideas into successful products: design thinking, prototyping, validation and market launch.",
   why=["Bridges engineering with marketing and entrepreneurship.","Useful for start-ups, innovation challenges and product roles.","Builds a structured approach to innovation."],
   learn=["Identifying customer needs","Concept generation and selection","Prototyping and testing","Pricing, positioning and launch strategy"],
   books=[("Product Design and Development","K. T. Ulrich &amp; S. D. Eppinger"),("Marketing Management","Philip Kotler")]),
}
AE_UNITS={"Lec 0":1,"Lec 1":1,"Lec 2":1,"Lec 3":1,"Lec 4":1,"Lec 5":2,"Lec 6":2,"Lec 7":2,"Lec 8":3,"Lec 9":3,"Lec 10":4,"Lec 10B":4,"Lec 11":4,"Lec 12":4,"Lec 13":4,"Lec 14":4,"Lec 15":5,"Lec 16":5,"Lec 17":5,"Lec 18":6,"Lec 19":6,"Lec 20":6,"Lec 21":6,"Lec 22":7,"Lec 23":7,"Lec 24":7,"Lec 25":7,"Lec 26":8,"Lec 27":8,"Lec 28":8,"Lec 29":9,"Lec 30":9,"Lec 31":9,"Lec 32":9,"Lec 33":9,"Lec 34":9,"Lec 35A":10,"Lec 35B":10,"Lec 36A":10,"Lec 36B":10,"Lec 37A":10,"Lec 37B":10}
AE_UN={1:"Introduction, Chassis & Materials",2:"Clutch & Fluid Coupling",3:"Brakes",4:"Gearbox & Transmission",5:"Final Drive, Axles & Drive Layouts",6:"Wheels & Tyres",7:"Steering System",8:"Suspension System",9:"Automotive Electrical Systems",10:"Automotive Air Conditioning"}
MPD=json.load(open('data_mp.json'))
FALLBACK={"Manufacturing Processes":[dict(item_type='lecture',unit=f"Unit {x['u']}: {x['un']}",lecture=f'Lec {i+1}',topic=x['t'],duration='45',url=None,ppt_url=None,test_url=f"https://test.vkvsir.com/t/mp-u{x['u']}") for i,x in enumerate(MPD)],"Automobile Engineering":[dict(item_type="lecture",unit=f"Unit {AE_UNITS[x['lec']]}: {AE_UN[AE_UNITS[x['lec']]]}",lecture=x['lec'],topic=x['topic'],duration=x['dur'],url=x['video'] or None,ppt_url=x['ppt'] or None,quiz_url=(x['quizUrl'] if 'forms.gle' in x['quizUrl'] else None),extra_videos=(['https://youtu.be/tpDPlVveAYo'] if x['lec']=='Lec 10B' else []),test_url='https://test.vkvsir.com/t/'+('ae-u4' if x['lec'] in ('Lec 13','Lec 14') else {1:'ae-u1-2',2:'ae-u1-2',3:'ae-u1-2',4:'ae-u3',5:'ae-u4',6:'ae-u5',7:'ae-u5',8:'ae-u5',9:'ae-u6',10:'ae-u7'}[AE_UNITS[x['lec']]])) for x in json.load(open('data_ae.json'))]}
def course_public(slug, m):
    body = banner(m["title"], m["lead"], "Courses") + f"""
<section class="sec sec-white"><div class="wrap"><div class="kpis rv" id="kpis"></div>
<div class="split" style="display:grid;grid-template-columns:1fr 1fr;gap:clamp(24px,4vw,50px);align-items:start">
 <div class="rv"><h2 style="font-size:var(--step-2)">Why this subject matters</h2><ul class="ticks" style="list-style:none;padding:0">{''.join(f'<li style="margin-bottom:10px">✔ {w}</li>' for w in m["why"])}</ul>
 <h2 style="font-size:var(--step-2);margin-top:26px">What you will learn</h2><ul>{''.join(f'<li>{w}</li>' for w in m["learn"])}</ul></div>
 <div class="rv rv-d1">{IMG(m["img"],640,420,m["title"])}<p style="margin-top:16px;color:var(--muted)">Every lecture comes with a video, downloadable notes and, where available, a topic quiz, all inside the free Members Area.</p><a class="btn btn-primary" href="{slug}">Open members page</a></div>
</div></div></section>
<section class="sec sec-mint"><div class="wrap"><div class="sec-head rv"><div><span class="kicker">Syllabus &amp; lecture plan</span><h2>Unit-wise outline</h2><p>Topics are listed openly. Videos, notes and quizzes unlock with free membership.</p></div><a class="link-more" href="{slug}">Members lecture plan</a></div><div id="syl"><p class="muted">Loading syllabus…</p></div></div></section>
<section class="sec sec-white"><div class="wrap"><h2 class="rv" style="font-size:var(--step-2)">Recommended books</h2><div class="blur rv"><div class="books" aria-hidden="true">{''.join(f'<div class="book"><b>{t}</b><span>{a}</span></div>' for t,a in m["books"])}</div><div class="lockbox"><div>🔒 Book list is for members<br><a href="join">Join free in 30 seconds</a></div></div></div>
<div style="margin-top:40px">{JOIN_BOX}</div></div></section>"""
    js = f'<script>window.LIB_FALLBACK={json.dumps([{k:v for k,v in r.items() if k in ("unit","lecture","topic","duration","item_type")} for r in FALLBACK.get(m["course"],[])],ensure_ascii=False)}</script><script src="assets/course.js"></script><script>renderPublic({json.dumps(m["course"])}, document.getElementById("syl"), document.getElementById("kpis"));</script>'
    page("course-"+slug, f'{m["title"]} – Free Course in Hindi & English | VKVSir', f'Free {m["title"]} course by Dr. Vinod Kumar Verma (VKVSir): syllabus, lecture plan, video lectures, PPT/PDF notes, quizzes and recommended books.', body, js, crumbs="Courses",
         extra_ld={"@context":"https://schema.org","@type":"Course","name":html.unescape(m["title"]),"description":html.unescape(m["lead"]),"provider":{"@id":DOMAIN+"/#person"},"inLanguage":["en","hi"],"isAccessibleForFree":True,"hasCourseInstance":{"@type":"CourseInstance","courseMode":"online"}})

def course_members(slug, m):
    body = banner(f'{m["title"]} · Members', "Complete lecture plan with video, PPT/PDF notes, quizzes and Test Lab practice.", "Members") + f"""
<section class="sec sec-white"><div class="wrap">

<div class="kpis rv" id="kpis"></div>
<input class="search" id="q" type="search" placeholder="Search a topic, e.g. clutch, steering, battery" aria-label="Search lectures">
<div id="plan"><p class="muted">Loading lecture plan…</p></div>
<div class="members-only" hidden><h2 style="font-size:var(--step-2);margin-top:40px">Recommended books</h2><div class="books">{''.join(f'<div class="book"><b>{t}</b><span>{a}</span></div>' for t,a in m["books"])}</div></div>
<p style="margin-top:30px"><a class="btn btn-ghost" href="course-{slug}">Course overview</a> <a class="btn btn-gold" href="test-lab">Practise on Test Lab</a></p>
</div></section>"""
    js = f'<script src="assets/course.js"></script><script>renderMembers({json.dumps(m["course"])}, document.getElementById("plan"), document.getElementById("kpis"), document.getElementById("q"));</script>'
    page(slug, f'{m["title"]} – Members Lecture Plan, Videos, Notes & Quiz | VKVSir', f'{m["title"]} members resources by VKVSir: unit-wise lecture plan with YouTube videos, PPT/PDF notes, quizzes and Test Lab practice.', body, js, crumbs="Members")

for slug, m in CMETA.items():
    course_public(slug, m); course_members(slug, m)

# Members hub
IDEAS = [("Auto fire-safety system","Sensor-based fire detection with automatic extinguishing for cars."),("EV battery health monitor","Low-cost BMS dashboard using a microcontroller and app."),("Smart parking assist","Ultrasonic sensing with audio-visual guidance for drivers."),("Solar-assisted e-cycle","Hybrid human-solar drive for short commutes."),("Regenerative braking demo rig","Bench setup to measure energy recovery."),("Tyre wear analyser","Image-based tread-depth estimation using a phone camera.")]
hub = banner("Members area","Everything you need to learn, revise and practise, free forever for our YouTube family.","Members") + f"""
<section class="sec sec-white" id="lectures"><div class="wrap"><div class="sec-head rv"><div><span class="kicker">Lecture plans &amp; videos</span><h2>Structured courses</h2><p>40–50 lectures per subject, unit by unit, each with a video and notes.</p></div></div>
<div class="grid grid-3">{''.join(f'<a class="card rv" href="{sl}"><div class="ph">{IMG(m["img"],600,400,m["title"])}</div><div class="bd"><h3>{m["title"]}</h3><p>Lecture plan · videos · notes · quizzes</p><span class="go link-more">Open</span></div></a>' for sl,m in CMETA.items())}</div></div></section>
<section class="sec sec-mint" id="downloads"><div class="wrap"><div class="sec-head rv"><div><span class="kicker">Notes &amp; downloads</span><h2>PPT &amp; PDF resources</h2><p>Lecture slides and notes, linked beside every lecture in each members course page.</p></div><a class="btn btn-primary" href="automobile-engineering">Automobile Engineering notes</a></div></div></section>
<section class="sec sec-white" id="quizzes"><div class="wrap"><div class="sec-head rv"><div><span class="kicker">Quizzes &amp; practice tests</span><h2>Check your understanding</h2><p>Topic quizzes beside each lecture, plus timed unit tests on Test Lab.</p></div><a class="btn btn-gold" href="test-lab">Open Test Lab</a></div></div></section>
<section class="sec sec-gold" id="projects"><div class="wrap"><div class="sec-head rv"><div><span class="kicker" style="color:#8a6a1e">Project &amp; innovation ideas</span><h2>Ideas for your next project</h2><p>Starter ideas for mini, major and hackathon projects, with guidance available to members.</p></div></div>
<div class="grid">{''.join(f'<div class="card rv" style="padding:20px"><span class="tag">Idea</span><h3 style="margin:.5em 0 .3em">{t}</h3><p>{d}</p><a class="btn btn-primary" style="align-self:flex-start;margin-top:14px" href="mailto:vinodvermavkvsir@gmail.com?subject=Project%20idea%3A%20{t.replace(" ","%20")}">Discuss / collaborate</a></div>' for t,d in IDEAS)}</div></div></section>
<section class="sec sec-white"><div class="wrap">{JOIN_BOX}</div></section>"""
page("members","Members Area – Free Lectures, Notes, Quizzes & Project Ideas | VKVSir","VKVSir members area: free lecture plans with videos, PPT/PDF notes, quizzes, Test Lab practice and project ideas. Free forever for YouTube subscribers.", hub, crumbs="Members")

# =================== TEST LAB ===================
CAT_FALLBACK = json.loads(r'''[{"track": "foundation", "grp": "Mechanical Engineering", "subgrp": "Diploma · UG · PG", "title": "Automobile Engineering", "description": "Unit and topic MCQs for internal exams, viva and semester preparation.", "subject_id": "AE", "status": "live"}, {"track": "foundation", "grp": "Mechanical Engineering", "subgrp": "Diploma · UG · PG", "title": "Manufacturing Processes", "description": "Casting, welding, forming and machining from basics to analytical level.", "subject_id": "MP", "status": "live"}, {"track": "foundation", "grp": "Mechanical Engineering", "subgrp": "Diploma · UG · PG", "title": "Hybrid & Electric Vehicles", "description": "Batteries, motors, controllers and EV architecture.", "subject_id": null, "status": "coming"}, {"track": "foundation", "grp": "Mechanical Engineering", "subgrp": "Diploma · UG", "title": "Workshop Practice", "description": "Shop-floor processes, tools and safety.", "subject_id": null, "status": "planned"}, {"track": "foundation", "grp": "Mechanical Engineering", "subgrp": "UG · PG", "title": "New Product Design & Launching", "description": "Design thinking, prototyping and launch strategy.", "subject_id": null, "status": "planned"}, {"track": "foundation", "grp": "Research", "subgrp": "PG · PhD", "title": "Research Methodology & Viva", "description": "Fundamentals for PG/PhD coursework and viva.", "subject_id": null, "status": "planned"}, {"track": "competitive", "grp": "Engineering Exams", "subgrp": "Transport", "title": "RTO / MVI Inspector", "description": "Previous-year style questions for MVSI / RTO / MVI exams.", "subject_id": "RTO", "status": "live"}, {"track": "competitive", "grp": "Engineering Exams", "subgrp": "GATE · ESE · PSU", "title": "GATE / ESE / PSU – Mechanical", "description": "Analytical and numerical practice, with long problems broken into steps.", "subject_id": null, "status": "coming"}, {"track": "competitive", "grp": "Engineering Exams", "subgrp": "ISRO · DRDO", "title": "Scientist / Engineer Exams", "description": "Mechanical core for ISRO, DRDO and similar exams.", "subject_id": null, "status": "planned"}, {"track": "competitive", "grp": "General Exams", "subgrp": "SSC · Banking · State", "title": "General Knowledge", "description": "Static GK and current affairs.", "subject_id": null, "status": "planned"}, {"track": "competitive", "grp": "General Exams", "subgrp": "SSC · Banking · State", "title": "Quantitative Aptitude", "description": "Arithmetic, data interpretation and speed maths.", "subject_id": null, "status": "planned"}, {"track": "competitive", "grp": "General Exams", "subgrp": "SSC · Banking · State", "title": "Reasoning (Logical & Analytical)", "description": "LR, AR, puzzles and pattern problems.", "subject_id": null, "status": "planned"}, {"track": "competitive", "grp": "Innovation", "subgrp": "Hackathons", "title": "Hackathon & Innovation Challenges", "description": "Problem-solving rounds for hackathons and innovation contests.", "subject_id": null, "status": "planned"}, {"track": "career", "grp": "Interview Preparation", "subgrp": "Freshers", "title": "Fresher Interview Readiness", "description": "Fundamentals to moderate level, mapped to the company, role and job description you target.", "subject_id": null, "status": "research"}, {"track": "career", "grp": "Interview Preparation", "subgrp": "Experienced", "title": "Mid-level Role Switch", "description": "Applied, domain-specific and design-level questions for professionals switching roles.", "subject_id": null, "status": "research"}, {"track": "career", "grp": "Interview Preparation", "subgrp": "Experienced", "title": "Senior & Leadership Roles", "description": "Emerging technology, R&D-stage concepts and strategic thinking.", "subject_id": null, "status": "research"}, {"track": "career", "grp": "Interview Modes", "subgrp": "All levels", "title": "Step-by-step Problem Solving", "description": "Long PSU/GATE/ISRO problems asked as a chain: formula, units, next step, final answer.", "subject_id": null, "status": "research"}, {"track": "career", "grp": "Interview Modes", "subgrp": "All levels", "title": "Group Discussion & HR", "description": "GD topics, communication and HR rounds.", "subject_id": null, "status": "research"}]''')
TRACKS = [("foundation","Foundation","For internal exams, practicals, viva and semester preparation: Diploma, UG, PG and PhD.","📘"),
          ("competitive","Competitive exams","GATE, ESE, PSU, ISRO, RTO/MVI, SSC, aptitude, reasoning and many more, grouped by level and domain.","🏆"),
          ("career","Career &amp; interview","Job, interview, group-discussion and role-switch preparation for freshers, experienced and senior professionals, tailored to the company, role and job description.","🚀")]
tl = """<style>.tl-hero{background:radial-gradient(900px 500px at 85% 10%,#1f6253 0,transparent 60%),var(--g900);color:#dfe9e4;padding:clamp(54px,8vw,96px) 0}.tl-hero h1{color:#fff;font-size:var(--step-4);margin:.1em 0 .3em}.tl-hero p{max-width:720px;font-size:var(--step-1);color:#c6d6cf}
.live{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:rgba(255,255,255,.12);border-radius:var(--r);overflow:hidden;margin-top:36px}.live div{background:rgba(255,255,255,.05);padding:20px;text-align:center}.live b{display:block;font-family:var(--f-head);font-size:var(--step-3);color:var(--gold);line-height:1}.live span{font-family:var(--f-head);font-size:14px;color:#b9cbc4}
.track{border-radius:var(--r-lg);padding:clamp(24px,4vw,40px);margin-bottom:24px;border:1px solid var(--line);background:#fff;box-shadow:var(--sh)}.track h2{font-size:var(--step-3);margin:.2em 0}.track .ico{font-size:34px}
.track.foundation{border-top:6px solid var(--g500)}.track.competitive{border-top:6px solid var(--gold)}.track.career{border-top:6px solid #6b4bd8;background:linear-gradient(180deg,#f6f3ff,#fff)}
.cgroup{margin-top:20px}.cgroup h3{font-size:16px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:10px}
.items{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(min(100%,260px),1fr))}
.item{border:1px solid var(--line);border-radius:var(--r);padding:16px;background:#fff;text-decoration:none;color:var(--ink);display:flex;flex-direction:column;gap:6px;transition:transform .2s,box-shadow .2s}.item:hover{transform:translateY(-3px);box-shadow:var(--sh)}
.item b{font-family:var(--f-head);color:var(--g800)}.item p{margin:0;font-size:14.5px;color:var(--muted)}
.st{font-family:var(--f-head);font-size:12px;font-weight:700;padding:3px 9px;border-radius:999px;align-self:flex-start}.st.live{background:#e3f5ea;color:#1e7a46}.st.coming{background:var(--gold-soft);color:#7a5b00}.st.planned{background:#eef1f0;color:#5a6663}.st.research{background:#ece7ff;color:#5536c9}
.qn{font-family:var(--f-head);font-size:13px;color:var(--g500)}
.how{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,230px),1fr));gap:16px}.how div{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:20px}.how b{font-family:var(--f-head);display:block;color:var(--g800);margin-bottom:4px}
@media(max-width:700px){.live{grid-template-columns:repeat(2,1fr)}}</style>
<section class="tl-hero"><div class="wrap"><p class="crumbs"><a href="./">Home</a> › Test Lab</p><span class="kicker">VKV Sir Test Lab</span><h1>Practise smarter. Score higher.</h1><p>A free online test platform built on VKVSir's own question bank, from semester basics to competitive exams and, soon, interview readiness.</p>
<div class="actions" style="margin-top:26px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-gold" href="TESTLAB" target="_blank" rel="noopener">Start a free test</a><a class="btn btn-light" href="#tracks">Explore tracks</a></div>
<div class="live" id="live"><div><b data-k="total">Thousands</b><span>of questions</span></div><div><b>Many</b><span>subjects &amp; exams</span></div><div><b data-k="tests">Ready</b><span>practice tests</span></div><div><b>3</b><span>learning tracks</span></div></div></div></section>
<section class="sec sec-paper" id="tracks"><div class="wrap"><div id="trackwrap">""" + "".join(f'<div class="track {k} rv" id="{k}"><span class="ico">{ic}</span><h2>{t}</h2><p style="color:var(--muted);max-width:760px">{d}</p><div class="cg" data-track="{k}"><p class="muted">Loading…</p></div></div>' for k,t,d,ic in TRACKS) + """</div></div></section>
<section class="sec sec-white"><div class="wrap"><div class="sec-head rv"><div><span class="kicker">How it works</span><h2>Designed for real exam conditions</h2></div></div><div class="how rv">
<div><b>Pick your scope</b>A whole subject, a unit, or a single topic.</div><div><b>Fair timing</b>Per-question timers, extra time for numericals.</div><div><b>Balanced difficulty</b>Easy, moderate and hard questions mixed sensibly.</div><div><b>Step-wise problems</b>Long GATE/PSU problems broken into steps: formula, units, next step, answer.</div><div><b>Instant results</b>Score and correct answers right after the test.</div><div><b>Interview mode</b>Chained questions that test complete problem-solving: formula, units, steps and answer.</div></div></div></section>
<section class="sec sec-mint"><div class="wrap" style="display:grid;gap:22px;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr))">
 <a class="card rv" href="https://forms.gle/uDEB4LovbrKjtFTH9" target="_blank" rel="noopener"><div class="bd"><span class="tag">Practice sheet</span><h3>MVSI / RTO Inspector Practice Sheet 1</h3><p>Exam-style questions in Google Forms.</p><span class="go link-more">Open</span></div></a>
 <a class="card rv rv-d1" href="members#quizzes"><div class="bd"><span class="tag">Members</span><h3>Lecture-wise quizzes</h3><p>Short quizzes beside every lecture in the members area.</p><span class="go link-more">Open</span></div></a>
 <a class="card rv rv-d2" href="courses"><div class="bd"><span class="tag">Courses</span><h3>Learn first, then test</h3><p>Video lectures and notes for each subject.</p><span class="go link-more">View courses</span></div></a>
</div></section>""".replace("TESTLAB", TESTLAB)
tljs = """<script>
const STL={live:'Live',coming:'Coming soon',planned:'Planned',research:'In research'};
Promise.all([dbRpc('get_public_stats').catch(()=>null), dbGet('catalog?select=*&active=eq.true&order=track,sort').catch(()=>window.CAT_FALLBACK||[])]).then(([s,cat])=>{
 const qmap={}; if(s){ document.querySelector('[data-k=total]').textContent=plus(s.total_questions); document.querySelector('[data-k=tests]').textContent=plus(s.tests_listed); s.subjects.forEach(x=>qmap[x.id]=x.questions); }
 document.querySelectorAll('.cg').forEach(el=>{ const rows=cat.filter(c=>c.track===el.dataset.track); if(!rows.length){el.innerHTML='<p class="muted">Categories will appear here soon.</p>';return;}
  const groups={}; rows.forEach(r=>(groups[r.grp]=groups[r.grp]||[]).push(r));
  el.innerHTML=Object.entries(groups).map(([g,rs])=>`<div class="cgroup"><h3>${esc(g)}</h3><div class="items">${rs.map(r=>{const href=r.url||(r.status==='live'?TESTLAB:'');const tag=href?'a':'div';return `<${tag} class="item" ${href?`href="${esc(href)}" target="_blank" rel="noopener"`:''}><b>${esc(r.title)}</b><p>${esc(r.description||'')}</p><span class="qn">${esc(r.subgrp||'')}${r.subject_id&&qmap[r.subject_id]?' · '+plus(qmap[r.subject_id])+' questions':''}</span></${tag}>`}).join('')}</div></div>`).join('')+'<p class="muted" style="margin:14px 0 0">…and many more categories being added regularly.</p>';});
});
</script>"""
tljs = "<script>window.CAT_FALLBACK=" + json.dumps(CAT_FALLBACK) + "</script>" + tljs
page("test-lab","VKV Sir Test Lab – Free Online MCQ Tests for Engineering, GATE, PSU, RTO & Interviews",
 "Free online MCQ tests by VKVSir: thousands of questions for internal exams and viva, competitive exams (GATE, PSU, RTO/MVI, SSC) and upcoming interview preparation.", tl, tljs, crumbs="Test Lab")
# old Test & Analysis → Test Lab
open("test-and-analysis.html","w").write('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Test Lab | VKVSir</title><link rel="canonical" href="'+DOMAIN+'/test-lab"><meta http-equiv="refresh" content="0; url=test-lab"><meta name="robots" content="noindex"></head><body><p>Moved to <a href="test-lab">Test Lab</a>.</p></body></html>')

# =================== JOIN & MEMBERSHIP FLOW PAGES ===================
START = OLD + "/_functions/start"     # Google sign-in check (runs on the Wix membership system)
STEP_CSS = '<style>.jsteps{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:24px 0}.js{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:20px;box-shadow:var(--sh)}.js i{font-style:normal;font-family:var(--f-head);font-weight:800;background:var(--gold);color:#1a1a1a;width:34px;height:34px;border-radius:50%;display:grid;place-items:center;margin-bottom:10px}.js b{font-family:var(--f-head);display:block;color:var(--g800);margin-bottom:4px}.js p{margin:0;color:var(--muted);font-size:15px}.bigcta{display:flex;flex-direction:column;align-items:center;gap:12px;text-align:center;background:linear-gradient(120deg,var(--g800),var(--g700));color:#e4ece8;border-radius:var(--r-lg);padding:clamp(26px,5vw,48px)}.bigcta h2{color:#fff;margin:0}.bigcta .btn{font-size:18px;padding:16px 30px}@media(max-width:760px){.jsteps{grid-template-columns:1fr}}</style>'
join = STEP_CSS + banner("Join VKVSir membership – free","Free forever for our YouTube family. One-time sign-up, about 30 seconds.","Join") + f"""
<section class="sec sec-white"><div class="narrow">
<div class="bigcta rv"><h2>Get every lecture, note and quiz</h2><p style="margin:0">Sign in with the Google account you use on YouTube.</p><button class="btn btn-gold" onclick="joinWithGoogle()">▶ Join now – Continue with Google</button><div id="jcheck" hidden style="background:rgba(255,255,255,.08);border-radius:12px;padding:14px 18px;max-width:560px"></div><a style="color:var(--lime)" href="https://www.youtube.com/@vkvsirdotcom?sub_confirmation=1" target="_blank" rel="noopener">Not subscribed yet? Subscribe first</a></div>
<div class="jsteps"><div class="js rv"><i>1</i><b>Choose your account</b><p>Pick the Google account you use on YouTube. It must be at least 1 month old.</p></div><div class="js rv rv-d1"><i>2</i><b>"Google hasn't verified this app"?</b><p>That's normal while Google reviews our new app. Click <b>Advanced</b> → <b>Go to vkvsir.com</b>.</p></div><div class="js rv rv-d2"><i>3</i><b>Keep YouTube ticked</b><p>Keep "View your YouTube account" ticked and press Continue. We only read your subscription.</p></div></div>
<h2 class="rv" style="font-size:var(--step-2);margin-top:30px">What you will see (it is safe)</h2><p class="rv muted">Google shows these screens because our app is new and still under Google review. Just follow the red arrows.</p>
<div class="guide"><figure class="rv"><img src="assets/img/guide-1-advanced.png" data-full="assets/img/guide-1-advanced.png" alt="Step 1: click Advanced on the Google warning" loading="lazy"><figcaption><b>Step 1</b>Click "Advanced".</figcaption></figure><figure class="rv rv-d1"><img src="assets/img/guide-2-continue.png" data-full="assets/img/guide-2-continue.png" alt="Step 2: click Go to vkvsir.com" loading="lazy"><figcaption><b>Step 2</b>Click "Go to vkvsir.com (unsafe)". It is safe.</figcaption></figure><figure class="rv rv-d2"><img src="assets/img/guide-3-youtube.png" data-full="assets/img/guide-3-youtube.png" alt="Step 3: tick View your YouTube account and Continue" loading="lazy"><figcaption><b>Step 3</b>Tick "View your YouTube account", then Continue.</figcaption></figure></div>

<p class="rv" style="color:var(--muted);text-align:center;margin-top:20px">Subscribers are approved instantly. Others get an email with the last step and are approved automatically. <a href="privacy-policy">Privacy policy</a></p>
</div></section>"""
page("join","Join VKVSir Membership – Free Lectures, Notes & Quizzes","Join VKVSir membership free: sign in with your YouTube Google account to unlock lecture videos, PPT/PDF notes, quizzes and Test Lab practice.", join, "<script>lightbox('.guide img');runJoinCheck(document.getElementById('jcheck'))</script>", crumbs="Join")
pend = STEP_CSS + banner("Almost there – one step left","Your membership request is received and we've emailed you the details.","Join") + f"""
<section class="sec sec-white"><div class="narrow"><div class="bigcta rv"><h2>Subscribe with the same Google account</h2><p style="margin:0">You'll be approved automatically within about an hour and get a welcome email.</p><a class="btn btn-yt" href="https://www.youtube.com/@vkvsirdotcom?sub_confirmation=1" target="_blank" rel="noopener">▶ Subscribe on YouTube</a></div>
<div class="jsteps"><div class="js"><b>Already subscribed?</b><p>Your YouTube account may be under 1 month old; you'll be approved when it turns 1 month.</p></div><div class="js"><b>Different account?</b><p>Apply again using the Google account you subscribed with.</p></div><div class="js"><b>Prefer comments?</b><p>Genuine comments on 5+ of our videos also qualify you.</p></div></div>
<p style="text-align:center"><a class="btn btn-ghost" href="join">Back to join page</a></p></div></section>"""
page("membership-pending","Membership request received | VKVSir","Your VKVSir membership request is received.", pend)
helpp = STEP_CSS + banner("Let's try that again","We couldn't complete your membership check. It usually takes 30 seconds to fix.","Join") + f"""
<section class="sec sec-white"><div class="narrow"><div class="jsteps"><div class="js"><b>YouTube box not ticked</b><p>On Google's permission screen keep "View your YouTube account" ticked.</p></div><div class="js"><b>Clicked "Back to safety"?</b><p>Click Advanced → Go to vkvsir.com. It is safe; Google's review is in progress.</p></div><div class="js"><b>Page left open too long</b><p>Just start again below.</p></div></div>
<div class="bigcta"><button class="btn btn-gold" onclick="joinWithGoogle()">Try again – Continue with Google</button><p style="margin:0">Still stuck? <a style="color:var(--lime)" href="mailto:vinodvermavkvsir@gmail.com">Email us</a> with a screenshot.</p></div></div></section>"""
page("membership-help","Membership – try again | VKVSir","Help with VKVSir membership sign-in.", helpp)
pp = banner("Privacy policy","Last updated: 18 October 2026","Privacy policy") + """<section class="sec sec-white"><div class="narrow prose">
<p>This Privacy Policy explains how www.vkvsir.com ("VKV Sir", "we", "us"), run by Dr. Vinod Kumar Verma, collects and uses information when you visit the website or apply for free membership.</p>
<h2>1. Information we collect</h2><p>When you apply using "Continue with Google", we receive your name, email address and profile picture. With your permission we also read, in read-only mode, basic information about your own YouTube account: your channel ID, the channel creation date, whether you are subscribed to the VKV Sir channel, and whether you have commented on VKV Sir videos. Optionally you may share your role and college or company.</p>
<h2>2. How we use it</h2><p>Only to decide and manage free membership, to re-check pending applications automatically, and to email you about your membership status. We never post, comment, subscribe or change anything in your account, and we never sell or share your data.</p>
<h2>3. Google API Services – Limited Use</h2><p>VKV Sir's use and transfer of information received from Google APIs adheres to the Google API Services User Data Policy, including the Limited Use requirements. Google user data is used only for membership verification and is not used for advertising or AI model training.</p>
<h2>4. Storage &amp; retention</h2><p>Data is stored securely in admin-only storage. Pending applications not completed within 90 days stop being checked.</p>
<h2>5. Your choices</h2><p>Revoke access anytime at myaccount.google.com/permissions, or email vinodvermavkvsir@gmail.com to delete your data within 30 days.</p>
<h2>6. Contact</h2><p>Dr. Vinod Kumar Verma, Department of Mechanical Engineering, Engineering College Ajmer, Rajasthan, India. Email: vinodvermavkvsir@gmail.com.</p></div></section>"""
page("privacy-policy","Privacy Policy | VKVSir","Privacy policy of vkvsir.com and the VKV Sir Membership app, including Google API Limited Use.", pp, crumbs="Privacy policy")

import re as _re, glob as _g, urllib.parse as _up
def _gm(m):
    subj = _up.unquote(m.group(1)) if m.group(1) else 'Enquiry from vkvsir.com'
    return 'href="https://mail.google.com/mail/?view=cm&amp;fs=1&amp;to=vinodvermavkvsir@gmail.com&amp;su=' + _up.quote(subj) + '" target="_blank" rel="noopener"'
for _f in _g.glob('*.html'):
    _t = open(_f).read()
    _t = _re.sub(r'href="mailto:vinodvermavkvsir@gmail\.com(?:\?subject=([^"]*))?"(?: target=_blank rel=noopener| target="_blank" rel="noopener")?', _gm, _t)
    open(_f,'w').write(_t)
# SEO files
pages = ["","about","courses","test-lab","members","join","privacy-policy","research-project-innovation","media","blog","faq","contact"] + [p for sl in CMETA for p in ("course-"+sl, sl)]
today = date.today().isoformat()
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f'  <url><loc>{DOMAIN}/{p}</loc><lastmod>{today}</lastmod><priority>{"1.0" if not p else "0.8"}</priority></url>\n' for p in pages) + "</urlset>\n")
open("robots.txt","w").write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
print("built ok")
