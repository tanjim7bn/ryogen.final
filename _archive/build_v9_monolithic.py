import json, math, random
LOGOS = json.load(open('logos_png.json'))
ICON = open('icon_full.txt').read().strip()
BRAND_DARK = open('brand_dark.txt').read().strip()
def L(k): return LOGOS[k]

# ================= CSS =================
CSS = r"""
:root{
 /* dark hero tokens */
 --bg:#0E1014; --bg-2:#14171E; --surface:#171A21; --surface-2:#1E222B;
 --dk-paper:#EDEDE8; --dk-soft:#B9BDC6; --dk-muted:#7E8693; --dk-faint:#4A505B;
 --dk-line:rgba(255,255,255,.08); --dk-line-2:rgba(255,255,255,.05);
 /* light body tokens */
 --paper:#FBFBF9; --paper-2:#F4F4F0; --card:#FFFFFF;
 --ink:#15171C; --soft:#4C545F; --muted:#8A909B; --lline:#E8E8E2; --lline-2:#F0F0EA;
 /* brand */
 --red:#E30613; --red-hover:#c9050f; --red-soft:rgba(227,6,19,.09);
 --teal:#0E9384; --teal-bg:#E0F5F2; --green:#1A8245; --green-bg:#E6F4EB; --amber:#B45309; --amber-bg:#FBF0E2;
 --dteal:#2DD4BF; --dteal-bg:rgba(45,212,191,.12);
 --font:'Poppins',system-ui,sans-serif;
 --ease:cubic-bezier(.16,1,.3,1);
 --pad:5%; --maxw:1240px;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;background-color:#FBFBF9;color-scheme:light}
body{font-family:var(--font);background-color:#FBFBF9;color:#15171C;-webkit-font-smoothing:antialiased;overflow-x:hidden;line-height:1.6}
a{color:inherit;text-decoration:none}
img{display:block;max-width:100%}
::selection{background:var(--red);color:#fff}
:focus-visible{outline:2px solid var(--red);outline-offset:3px;border-radius:6px}
.tnum{font-variant-numeric:tabular-nums}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 var(--pad)}

@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
@keyframes ping{0%{transform:scale(.6);opacity:.7}70%,100%{transform:scale(2.4);opacity:0}}
@keyframes marq{to{transform:translateX(-50%)}}

.btn{display:inline-flex;align-items:center;gap:9px;font-family:var(--font);font-size:.9rem;font-weight:600;padding:13px 24px;border-radius:11px;cursor:pointer;transition:transform .2s var(--ease),box-shadow .2s var(--ease),background .2s,border-color .2s;white-space:nowrap;border:none}
.btn svg{width:15px;height:15px}
.btn-red{background:var(--red);color:#fff}
.btn-red:hover{background:var(--red-hover);transform:translateY(-2px);box-shadow:0 12px 32px rgba(227,6,19,.3)}
.btn-ghost-d{background:transparent;color:var(--dk-paper);border:1px solid var(--dk-line)}
.btn-ghost-d:hover{border-color:var(--dk-soft);background:var(--surface)}
.btn-ghost-l{background:var(--card);color:var(--ink);border:1px solid var(--lline)}
.btn-ghost-l:hover{border-color:var(--ink)}

/* ---------- nav (dark, matches hero) ---------- */
nav{position:sticky;top:0;z-index:400;background-color:rgba(14,16,20,.92);-webkit-backdrop-filter:blur(20px);backdrop-filter:blur(20px);border-bottom:1px solid var(--dk-line)}
.nav-in{max-width:var(--maxw);margin:0 auto;padding:0 var(--pad);height:70px;display:flex;align-items:center;justify-content:space-between}
.brand{display:flex;align-items:center;height:100%}
.brand .wordmark{height:26px;width:auto;display:block}
.foot-brand .brand{height:auto}
.foot-brand .brand .wordmark{height:30px}
.nav-links{display:flex;align-items:center;gap:2px;list-style:none}
.nav-item{position:relative}
.nav-link{display:flex;align-items:center;gap:6px;padding:9px 15px;border-radius:9px;font-size:.875rem;font-weight:500;color:var(--dk-soft);background:none;border:none;cursor:pointer;font-family:var(--font);transition:all .18s}
.nav-link:hover{color:var(--dk-paper);background:var(--surface)}
.caret{width:9px;height:9px;transition:transform .2s}
.nav-item:hover .caret{transform:rotate(180deg)}
.drop{position:absolute;top:calc(100% + 8px);left:0;background:var(--surface);border:1px solid var(--dk-line);border-radius:16px;box-shadow:0 24px 60px rgba(0,0,0,.5);min-width:330px;padding:8px;opacity:0;visibility:hidden;transform:translateY(-8px);transition:all .22s var(--ease);pointer-events:none}
.nav-item:hover .drop{opacity:1;visibility:visible;transform:translateY(0);pointer-events:all}
.drop-item{display:flex;align-items:flex-start;gap:12px;padding:11px 12px;border-radius:10px;transition:all .18s}
.drop-item:hover{background:var(--surface-2);transform:translateX(3px)}
.drop-ic{width:34px;height:34px;flex-shrink:0;border-radius:9px;background:var(--surface-2);border:1px solid var(--dk-line);display:flex;align-items:center;justify-content:center;color:var(--red)}
.drop-ic svg{width:17px;height:17px;stroke-width:1.8}
.drop-item:hover .drop-ic{background:rgba(227,6,19,.14)}
.drop-label{display:block;font-size:.85rem;font-weight:600;color:var(--dk-paper)}
.drop-sub{display:block;font-size:.72rem;color:var(--dk-muted);margin-top:2px;line-height:1.4}
.nav-right{display:flex;align-items:center;gap:12px}
.nav-login{font-size:.875rem;font-weight:500;color:var(--dk-soft)}
.nav-login:hover{color:var(--dk-paper)}
.nav-cta{font-size:.875rem;font-weight:600;color:#fff;background:var(--red);padding:10px 18px;border-radius:10px;transition:all .18s}
.nav-cta:hover{background:var(--red-hover);box-shadow:0 6px 20px rgba(227,6,19,.34)}
.burger{display:none;flex-direction:column;gap:5px;background:none;border:0;cursor:pointer;padding:8px}
.burger span{width:22px;height:2px;background:var(--dk-paper);border-radius:2px}
.mobile-menu{display:none;border-top:1px solid var(--dk-line);padding:12px var(--pad) 22px;background:var(--bg)}
.mobile-menu a{display:block;padding:13px 0;font-size:1rem;font-weight:500;color:var(--dk-paper);border-bottom:1px solid var(--dk-line-2)}
.mobile-menu .mm-cta{margin-top:14px;text-align:center;color:#fff;background:var(--red);border-radius:10px;border-bottom:none}

/* ---------- HERO (dark, kept) ---------- */
.hero{position:relative;min-height:calc(100vh - 70px);min-height:calc(100svh - 70px);overflow:hidden;background-color:#0E1014;color:var(--dk-paper)}
.hero-map{position:absolute;inset:0;z-index:1;transition:transform .3s ease-out}
.hero-map svg{width:100%;height:100%;display:block}
.rings-rotate{animation:spin 160s linear infinite;transform-origin:250px 470px}
.hero-veil{position:absolute;inset:0;z-index:2;pointer-events:none;background:radial-gradient(ellipse 70% 90% at 22% 46%, rgba(14,16,20,.96) 0%, rgba(14,16,20,.55) 44%, transparent 74%)}
.hero-fade{position:absolute;left:0;right:0;bottom:0;height:140px;z-index:3;pointer-events:none;background:linear-gradient(transparent,var(--bg))}
.hero-in{position:relative;z-index:6;max-width:var(--maxw);margin:0 auto;padding:70px var(--pad) 90px;min-height:calc(100vh - 70px);display:flex;flex-direction:column;justify-content:center}
.hero-copy{max-width:560px}
.kicker{display:inline-flex;align-items:center;gap:10px;font-size:.72rem;font-weight:700;letter-spacing:.13em;text-transform:uppercase;color:var(--red);margin-bottom:22px;opacity:0;animation:rise .7s .05s var(--ease) forwards}
.kicker .k-line{width:22px;height:1.5px;background:var(--red)}
.hero-h{font-size:clamp(2.4rem,4.8vw,3.9rem);font-weight:700;line-height:1.06;letter-spacing:-.035em;margin-bottom:22px;opacity:0;animation:rise .8s .16s var(--ease) forwards}
.morph-wrap{display:inline-block;position:relative;white-space:nowrap}
.morph{color:var(--red);font-style:italic;font-weight:600}
.cursor{display:inline-block;width:3px;height:.92em;background:var(--red);margin-left:3px;vertical-align:-.08em;animation:blink 1s step-end infinite;border-radius:2px}
.hero-sub{font-size:1.08rem;font-weight:300;line-height:1.65;color:var(--dk-soft);max-width:460px;margin-bottom:26px;opacity:0;animation:rise .8s .28s var(--ease) forwards}
.social{display:flex;align-items:center;gap:14px;margin-bottom:30px;opacity:0;animation:rise .8s .36s var(--ease) forwards}
.avatars{display:flex}
.av{width:34px;height:34px;border-radius:50%;border:2px solid var(--bg);margin-left:-10px;display:flex;align-items:center;justify-content:center;font-size:.66rem;font-weight:600;color:#fff}
.av:first-child{margin-left:0}
.av-1{background:#E30613}.av-2{background:#2DD4BF;color:#0E1014}.av-3{background:#7E8693}.av-4{background:#FBBF24;color:#0E1014}.av-5{background:#34D399;color:#0E1014}
.social-t{font-size:.85rem;color:var(--dk-muted)}
.social-t strong{color:var(--dk-paper);font-weight:600}
.hero-ctas{display:flex;gap:13px;flex-wrap:wrap;opacity:0;animation:rise .8s .46s var(--ease) forwards}

/* radar sweep (country-agnostic, scales with new destinations) */
.radar{animation:sweep 9s linear infinite}
@keyframes sweep{to{transform:rotate(360deg)}}
/* anonymous university nodes that light up as the sweep passes (9s period) */
.udot{animation:nodeGlow 9s ease-out infinite}
.uring{opacity:0;transform-box:fill-box;transform-origin:center;animation:nodePing 9s ease-out infinite}
@keyframes nodeGlow{0%{fill:#4A505B}6%{fill:#EDEDE8}30%{fill:#4A505B}100%{fill:#4A505B}}
@keyframes nodePing{0%{opacity:.7;transform:scale(1)}12%{opacity:0;transform:scale(4)}100%{opacity:0;transform:scale(4)}}
/* live scan tag, single quiet label anchored bottom-right of the map */
.scan-tag{position:absolute;z-index:5;right:6%;bottom:9%;display:inline-flex;align-items:center;gap:9px;font-size:.72rem;font-weight:500;color:var(--dk-soft);background-color:rgba(20,23,30,.5);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.09);border-radius:30px;padding:8px 15px;opacity:0;animation:rise 1s .9s var(--ease) forwards}
.ping{position:relative;width:8px;height:8px;flex-shrink:0}
.ping i{position:absolute;inset:0;border-radius:50%;background:var(--dteal)}
.ping i.r{animation:ping 2.6s ease-out infinite}

/* ---------- dark stats band bridging into light ---------- */
.stats{background-color:#14171E;border-top:1px solid var(--dk-line);color:var(--dk-paper)}
.stats-in{max-width:var(--maxw);margin:0 auto;display:grid;grid-template-columns:repeat(4,1fr)}
.stat{padding:38px var(--pad);text-align:center}
.stat+.stat{border-left:1px solid var(--dk-line)}
.stat .sv{font-size:clamp(1.7rem,3vw,2.3rem);font-weight:700;letter-spacing:-.03em}
.stat .sv em{color:var(--red);font-style:normal}
.stat .sl{font-size:.8rem;color:var(--dk-muted);margin-top:4px}

/* ---------- LIGHT BODY ---------- */
.light{background-color:#FBFBF9;color:#15171C}
.section{padding:clamp(4.5rem,8vw,6.5rem) 0}
.sec-eyebrow{display:inline-flex;align-items:center;gap:9px;font-size:.72rem;font-weight:700;letter-spacing:.13em;text-transform:uppercase;color:var(--red)}
.sec-eyebrow::before{content:'';width:18px;height:1.5px;background:var(--red)}
.sec-h{font-size:clamp(1.85rem,3.4vw,2.7rem);font-weight:700;letter-spacing:-.03em;line-height:1.12;margin:14px 0 14px}
.sec-h em{font-style:italic;font-weight:600;color:var(--red)}
.sec-intro{font-size:1.02rem;font-weight:300;color:var(--soft);max-width:560px;line-height:1.65}
.sec-head{max-width:640px;margin-bottom:2.8rem}
.sec-head.center{margin:0 auto 2.8rem;text-align:center}
.sec-head.center .sec-eyebrow{justify-content:center}
.reveal{opacity:1;transform:none;transition:opacity .7s var(--ease),transform .7s var(--ease)}
.js .reveal{opacity:0;transform:translateY(22px)}
.reveal.in{opacity:1;transform:none}
.reveal.d1{transition-delay:.08s}.reveal.d2{transition-delay:.16s}.reveal.d3{transition-delay:.24s}

/* logo wall (light) */
.wall{padding:34px 0;background-color:#FBFBF9;border-bottom:1px solid var(--lline)}
.wall-label{text-align:center;font-size:.74rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:22px}
.wall-label b{color:var(--soft);font-weight:600}
.wall-mask{position:relative;overflow:hidden;-webkit-mask-image:linear-gradient(90deg,transparent,#000 7%,#000 93%,transparent);mask-image:linear-gradient(90deg,transparent,#000 7%,#000 93%,transparent)}
.wall-track{display:flex;gap:16px;width:max-content;animation:marq 50s linear infinite}
.wall-mask:hover .wall-track{animation-play-state:paused}
.wall-chip{height:58px;min-width:128px;padding:0 16px;background:var(--card);border:1px solid var(--lline);border-radius:11px;display:flex;align-items:center;justify-content:center}
.wall-chip img{max-height:32px;max-width:116px;object-fit:contain;filter:grayscale(1);opacity:.65;transition:all .2s}
.wall-chip:hover img{filter:grayscale(0);opacity:1}

/* toolkit (light) */
.tools{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}
.tool{background-color:#FFFFFF;border:1px solid var(--lline);border-radius:16px;padding:26px;transition:transform .2s var(--ease),box-shadow .2s var(--ease)}
.tool:hover{transform:translateY(-3px);box-shadow:0 18px 44px -22px rgba(21,23,28,.18)}
.tool .t-ic{width:44px;height:44px;border-radius:11px;background:var(--red-soft);display:flex;align-items:center;justify-content:center;color:var(--red);margin-bottom:18px}
.tool .t-ic svg{width:21px;height:21px;stroke-width:1.7}
.tool .t-n{font-size:.68rem;font-weight:600;color:var(--muted);letter-spacing:.05em;margin-bottom:8px}
.tool h3{font-size:1.08rem;font-weight:600;margin-bottom:8px;letter-spacing:-.01em}
.tool p{font-size:.88rem;color:var(--soft);line-height:1.55;font-weight:300}
.tool.prime{grid-column:span 2;background:linear-gradient(135deg,#E30613,#a2040e);color:#fff;border-color:transparent}
.tool.prime .t-ic{background:rgba(255,255,255,.16);color:#fff}
.tool.prime .t-n{color:rgba(255,255,255,.7)}
.tool.prime h3{font-size:1.45rem}
.tool.prime p{color:rgba(255,255,255,.93);font-size:.98rem;max-width:440px}
.tool.prime .tag{display:inline-block;margin-top:16px;font-size:.66rem;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:#fff;background:rgba(255,255,255,.16);padding:5px 11px;border-radius:20px}

/* how it works (light gray band) */
.how{background-color:#F4F4F0;border-top:1px solid var(--lline);border-bottom:1px solid var(--lline)}
.how-grid{display:grid;grid-template-columns:.85fr 1.15fr;gap:4rem;align-items:center}
.how-steps{margin-top:26px;display:flex;flex-direction:column;gap:6px}
.how-step{display:flex;gap:15px;align-items:center;padding:14px;border-radius:12px;transition:all .3s var(--ease)}
.how-step.on{background:var(--card);box-shadow:0 8px 24px -14px rgba(21,23,28,.16)}
.how-step .sn{width:30px;height:30px;border-radius:8px;background:var(--card);border:1px solid var(--lline);display:flex;align-items:center;justify-content:center;font-weight:600;font-size:.85rem;flex-shrink:0;transition:all .3s}
.how-step.on .sn{background:var(--red);border-color:var(--red);color:#fff}
.how-step .sname{font-size:.92rem;font-weight:600}
.how-step .sdesc{font-size:.78rem;color:var(--muted)}
.terminal{background-color:#FFFFFF;border:1px solid var(--lline);border-radius:18px;overflow:hidden;box-shadow:0 30px 70px -34px rgba(21,23,28,.28)}
.term-bar{display:flex;align-items:center;justify-content:space-between;padding:14px 18px;border-bottom:1px solid var(--lline-2);font-size:.8rem;color:var(--soft)}
.term-bar-l{display:flex;align-items:center;gap:8px;font-weight:600}
.term-bar-l svg{width:15px;height:15px;stroke-width:1.8;stroke:currentColor;fill:none}
.term-dots{display:flex;gap:6px}
.term-dots i{width:9px;height:9px;border-radius:50%;background:var(--lline)}
.term-body{padding:18px}
.tp{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin-bottom:16px}
.tpf{background:var(--paper-2);border:1px solid var(--lline-2);border-radius:10px;padding:10px 12px}
.tpf .k{font-size:.6rem;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);margin-bottom:4px}
.tpf .v{font-size:.9rem;font-weight:600}
.tpf .v .u{font-size:.68rem;color:var(--muted);font-weight:400}
.tm-h{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px}
.tm-t{font-size:.8rem;font-weight:600}
.tm-s{font-size:.68rem;color:var(--muted)}
.mt{display:flex;align-items:center;gap:13px;padding:12px 0;border-bottom:1px solid var(--lline-2)}
.mt:last-of-type{border-bottom:none}
.mt-plate{width:44px;height:44px;border-radius:10px;background:#fff;border:1px solid var(--lline);display:flex;align-items:center;justify-content:center;padding:7px;flex-shrink:0}
.mt-plate img{max-width:100%;max-height:100%;object-fit:contain}
.mt-i{flex:1;min-width:0}
.mt-n{font-size:.88rem;font-weight:600;letter-spacing:-.01em}
.mt-m{font-size:.72rem;color:var(--muted)}
.mt-r{text-align:right;flex-shrink:0;width:96px}
.mt-p{font-size:.92rem;font-weight:700}
.mt-p.cy{color:var(--teal)}.mt-p.hi{color:var(--green)}.mt-p.md{color:var(--amber)}
.mt-bar{height:5px;border-radius:3px;background:var(--lline-2);margin-top:5px;overflow:hidden}
.mt-bar i{display:block;height:100%;border-radius:3px;width:0;transition:width 1s var(--ease) .3s}
.mt-bar i.cy{background:var(--teal)}.mt-bar i.hi{background:var(--green)}.mt-bar i.md{background:var(--amber)}
.tm-f{display:flex;align-items:center;justify-content:space-between;margin-top:14px;padding-top:14px;border-top:1px solid var(--lline-2);font-size:.8rem;color:var(--muted)}
.tm-f b{color:var(--ink)}
.tm-f a{color:var(--red);font-weight:600;display:inline-flex;align-items:center;gap:5px}
.tm-f a svg{width:11px;height:11px;stroke:currentColor;fill:none}

/* 360 ring (light showcase) */
.ring-sec{background-color:#FBFBF9;overflow:hidden;position:relative;border-bottom:1px solid var(--lline)}
.ring-glow{position:absolute;top:58%;left:50%;transform:translate(-50%,-50%);width:760px;height:480px;background:radial-gradient(ellipse,rgba(227,6,19,.06),transparent 62%);pointer-events:none}
.scene{position:relative;height:460px;-webkit-perspective:2000px;perspective:2000px;-webkit-perspective-origin:50% 44%;perspective-origin:50% 44%;z-index:2}
.scene::before{content:'';position:absolute;left:0;right:0;top:0;height:80px;background:linear-gradient(var(--paper),transparent);z-index:40;pointer-events:none}
.scene::after{content:'';position:absolute;left:0;right:0;bottom:0;height:100px;background:linear-gradient(transparent,var(--paper));z-index:40;pointer-events:none}
.ring{position:absolute;left:50%;top:47%;width:250px;height:300px;margin-left:-125px;margin-top:-150px;-webkit-transform-style:preserve-3d;transform-style:preserve-3d;animation:ringspin 46s linear infinite}
@keyframes ringspin{from{transform:rotateY(0)}to{transform:rotateY(360deg)}}
.ring:hover{animation-play-state:paused}
.rcard{position:absolute;width:250px;height:296px;left:0;top:0;-webkit-backface-visibility:hidden;backface-visibility:hidden;background-color:#FFFFFF;border:1px solid var(--lline);border-radius:18px;padding:18px;box-shadow:0 22px 48px -20px rgba(21,23,28,.24);display:flex;flex-direction:column}
.rc-tag{position:absolute;top:-9px;right:16px;font-size:.6rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#fff;background:var(--red);padding:4px 9px;border-radius:6px;box-shadow:0 4px 12px rgba(227,6,19,.35)}
.rc-plate{height:104px;border-radius:12px;background:#fff;border:1px solid var(--lline-2);display:flex;align-items:center;justify-content:center;padding:16px;margin-bottom:14px}
.rc-plate img{max-height:64px;max-width:82%;object-fit:contain}
.rc-name{font-size:.98rem;font-weight:600;letter-spacing:-.01em;line-height:1.25;margin-bottom:4px}
.rc-loc{display:flex;align-items:center;gap:7px;font-size:.72rem;color:var(--muted);margin-bottom:auto}
.rc-flag{width:16px;height:12px;border-radius:2px;overflow:hidden;box-shadow:0 0 0 .5px var(--lline);flex-shrink:0}
.rc-flag svg{width:100%;height:100%;display:block}
.rc-foot{display:flex;align-items:flex-end;justify-content:space-between;border-top:1px solid var(--lline-2);padding-top:13px;margin-top:13px}
.rc-tui{font-size:.92rem;font-weight:700}
.rc-tui span{display:block;font-size:.56rem;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);font-weight:500;margin-bottom:2px}
.rc-badge{font-size:.92rem;font-weight:700;padding:5px 11px;border-radius:9px}
.rc-badge.cy{background:var(--teal-bg);color:var(--teal)}
.rc-badge.hi{background:var(--green-bg);color:var(--green)}
.rc-badge.md{background:var(--amber-bg);color:var(--amber)}
.ring-scroller{display:none}

/* destinations */
.dest-grid{display:grid;grid-template-columns:1fr 1fr;gap:15px}
.dcard{background-color:#FFFFFF;border:1px solid var(--lline);border-radius:18px;padding:26px;position:relative}
.dcard .dtop{display:flex;align-items:center;gap:13px;margin-bottom:20px}
.dcard .dflag{width:44px;height:31px;border-radius:5px;overflow:hidden;box-shadow:0 0 0 1px var(--lline)}
.dcard .dflag svg{width:100%;height:100%;display:block}
.dcard h3{font-size:1.3rem;font-weight:600;letter-spacing:-.02em}
.dcard .dsub{font-size:.76rem;color:var(--muted)}
.dcard .dlive{position:absolute;top:24px;right:24px;font-size:.6rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--teal);background:var(--teal-bg);padding:4px 9px;border-radius:6px}
.dcard .dcrests{display:flex;flex-wrap:wrap;gap:9px;margin-bottom:18px}
.dcard .dcrest{height:46px;padding:8px 12px;background:#fff;border:1px solid var(--lline-2);border-radius:9px;display:flex;align-items:center}
.dcard .dcrest img{max-height:28px;max-width:88px;object-fit:contain}
.dcard .dtags{display:flex;flex-wrap:wrap;gap:8px}
.dcard .dtag{font-size:.72rem;color:var(--soft);background:var(--paper-2);border:1px solid var(--lline);padding:5px 11px;border-radius:20px}
.coming{margin-top:18px;border:1px dashed var(--lline);border-radius:16px;padding:19px 24px;display:flex;align-items:center;gap:22px;flex-wrap:wrap;background:var(--card)}
.coming .cl{font-size:.74rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.coming .cflags{display:flex;gap:20px;flex-wrap:wrap}
.coming .cf{display:flex;align-items:center;gap:8px;font-size:.85rem;color:var(--soft);font-weight:500}
.coming .cf .fl{width:22px;height:16px;border-radius:3px;overflow:hidden;box-shadow:0 0 0 1px var(--lline)}
.coming .cf .fl svg{width:100%;height:100%;display:block}

/* institutions (light gray) */
.b2b{background-color:#F4F4F0;border-top:1px solid var(--lline);border-bottom:1px solid var(--lline)}
.b2b-grid{display:grid;grid-template-columns:1fr 1fr;gap:4rem;align-items:center}
.b2b-list{list-style:none;margin:22px 0 28px;display:flex;flex-direction:column;gap:13px}
.b2b-list li{display:flex;align-items:flex-start;gap:11px;font-size:.92rem;color:var(--soft)}
.b2b-list li b{color:var(--ink);font-weight:600}
.b2b-ck{width:20px;height:20px;border-radius:6px;background:var(--red-soft);color:var(--red);display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px}
.b2b-ck svg{width:11px;height:11px;stroke:currentColor;fill:none;stroke-width:2.4}
.b2b-panel{background-color:#FFFFFF;border:1px solid var(--lline);border-radius:18px;padding:24px;box-shadow:0 30px 70px -36px rgba(21,23,28,.24)}
.b2b-pt{display:flex;align-items:center;justify-content:space-between;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:14px}
.b2b-pt .live{display:inline-flex;align-items:center;gap:6px;color:var(--teal)}
.b2b-pt .live i{width:6px;height:6px;border-radius:50%;background:var(--teal)}
.pipe-row{display:flex;align-items:center;gap:14px;padding:14px 0;border-bottom:1px solid var(--lline-2)}
.pipe-row:last-child{border-bottom:none}
.pipe-row .num{width:30px;height:30px;border-radius:8px;background:var(--ink);color:#fff;font-size:.82rem;font-weight:600;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.pipe-row .a{font-size:.9rem;font-weight:600}
.pipe-row .b{font-size:.72rem;color:var(--muted)}
.pipe-row .val{margin-left:auto;font-size:.95rem;font-weight:700;color:var(--teal)}

/* CTA dark */
.cta{position:relative;overflow:hidden;background-color:#0E1014;color:var(--dk-paper)}
.cta-glow{position:absolute;top:-30%;left:50%;transform:translateX(-50%);width:800px;height:520px;background:radial-gradient(ellipse,rgba(227,6,19,.22),transparent 62%);pointer-events:none}
.cta-in{position:relative;text-align:center;max-width:620px;margin:0 auto}
.cta-in h2{font-size:clamp(2rem,4vw,3rem);font-weight:700;letter-spacing:-.03em;line-height:1.08;margin-bottom:16px}
.cta-in h2 em{font-style:italic;font-weight:600;color:var(--red)}
.cta-in p{font-size:1.02rem;color:var(--dk-soft);font-weight:300;margin-bottom:30px}
.cta-form{display:flex;gap:10px;max-width:440px;margin:0 auto;background:var(--surface);border:1px solid var(--dk-line);border-radius:13px;padding:7px}
.cta-form input{flex:1;background:none;border:none;outline:none;color:var(--dk-paper);font-family:var(--font);font-size:.92rem;padding:0 14px}
.cta-form input::placeholder{color:var(--dk-muted)}
.cta-note{font-size:.7rem;letter-spacing:.05em;text-transform:uppercase;color:var(--dk-muted);margin-top:18px}

/* footer dark */
footer{border-top:1px solid var(--dk-line);padding:64px 0 32px;background-color:#0E1014;color:var(--dk-paper)}
.foot{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;gap:2rem}
.foot-brand .brand{margin-bottom:14px}
.foot-brand p{font-size:.86rem;color:var(--dk-muted);max-width:270px;font-weight:300}
.foot h5{font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;color:var(--dk-muted);margin-bottom:16px;font-weight:600}
.foot-col{display:flex;flex-direction:column;gap:11px}
.foot-col a{font-size:.86rem;color:var(--dk-soft);transition:color .15s}
.foot-col a:hover{color:var(--dk-paper)}
.foot-bot{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-top:44px;padding-top:26px;border-top:1px solid var(--dk-line);font-size:.76rem;color:var(--dk-muted)}
.foot-bot .r{display:flex;gap:22px}

.dev-tag{position:fixed;left:14px;bottom:14px;z-index:999;font-size:.64rem;color:var(--soft);background:var(--card);border:1px solid var(--lline);padding:8px 12px;border-radius:8px;max-width:320px;line-height:1.5;box-shadow:0 8px 24px rgba(21,23,28,.14)}
.dev-tag b{color:var(--ink)}

@media(max-width:1000px){
 .nav-links,.nav-login{display:none}
 .burger{display:flex}
 .how-grid,.b2b-grid{grid-template-columns:1fr;gap:2.5rem}
 .tools{grid-template-columns:1fr 1fr}.tool.prime{grid-column:span 2}
 .scan-tag{display:none}
 .dest-grid{grid-template-columns:1fr}
 .stats-in{grid-template-columns:1fr 1fr}
 .stat:nth-child(3),.stat:nth-child(4){border-top:1px solid var(--dk-line)}
 .stat:nth-child(odd){border-left:none}
 .scene,.ring-glow{display:none}
 .ring-scroller{display:flex;gap:14px;overflow-x:auto;padding:8px var(--pad) 16px;scroll-snap-type:x mandatory}
 .foot{grid-template-columns:1fr 1fr}.foot-brand{grid-column:span 2}
}
@media(max-width:600px){
 .tools{grid-template-columns:1fr}.tool.prime{grid-column:span 1}
 .tp{grid-template-columns:1fr 1fr}
 .stats-in{grid-template-columns:1fr}.stat{border-left:none!important}.stat+.stat{border-top:1px solid var(--dk-line)}
 .foot{grid-template-columns:1fr}.foot-brand{grid-column:span 1}
 .hero-ctas .btn{flex:1;justify-content:center}
 .cta-form{flex-direction:column}
}
@media(prefers-reduced-motion:reduce){
 *{animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important;scroll-behavior:auto!important}
 .cursor{display:none}
}
"""

# ================= flags & icons =================
FLAG = {
 'JP':'<svg viewBox="0 0 24 17"><rect width="24" height="17" fill="#fff"/><circle cx="12" cy="8.5" r="5" fill="#BC002D"/></svg>',
 'MY':'<svg viewBox="0 0 24 17"><rect width="24" height="17" fill="#CC0001"/><rect y="1.2" width="24" height="1.2" fill="#fff"/><rect y="3.6" width="24" height="1.2" fill="#fff"/><rect y="6.1" width="24" height="1.2" fill="#fff"/><rect y="8.5" width="24" height="1.2" fill="#fff"/><rect y="10.9" width="24" height="1.2" fill="#fff"/><rect y="13.4" width="24" height="1.2" fill="#fff"/><rect width="12" height="8.5" fill="#010066"/><circle cx="4.6" cy="4.2" r="1.9" fill="#FC0"/><circle cx="5.4" cy="4.2" r="1.4" fill="#010066"/></svg>',
 'US':'<svg viewBox="0 0 24 17"><rect width="24" height="17" fill="#fff"/><g fill="#B22234"><rect width="24" height="1.3"/><rect y="2.6" width="24" height="1.3"/><rect y="5.2" width="24" height="1.3"/><rect y="7.8" width="24" height="1.3"/><rect y="10.4" width="24" height="1.3"/><rect y="13" width="24" height="1.3"/><rect y="15.6" width="24" height="1.3"/></g><rect width="10" height="9.1" fill="#3C3B6E"/></svg>',
 'UK':'<svg viewBox="0 0 24 17"><rect width="24" height="17" fill="#012169"/><path d="M0 0L24 17M24 0L0 17" stroke="#fff" stroke-width="3.4"/><path d="M0 0L24 17M24 0L0 17" stroke="#C8102E" stroke-width="1.7"/><rect x="9.5" width="5" height="17" fill="#fff"/><rect y="6" width="24" height="5" fill="#fff"/><rect x="10.5" width="3" height="17" fill="#C8102E"/><rect y="7" width="24" height="3" fill="#C8102E"/></svg>',
 'CA':'<svg viewBox="0 0 24 17"><rect width="24" height="17" fill="#fff"/><rect width="6" height="17" fill="#FF0000"/><rect x="18" width="6" height="17" fill="#FF0000"/><path d="M12 3.6l.8 2.5 2-.8-.9 2.3 2.2.2-1.7 1.4.8.8-2.5-.3.2 2.3-1.3-1.4-1.3 1.4.2-2.3-2.5.3.8-.8-1.7-1.4 2.2-.2-.9-2.3 2 .8z" fill="#FF0000"/></svg>',
 'AU':'<svg viewBox="0 0 24 17"><rect width="24" height="17" fill="#00247D"/><path d="M0 0L12 8.5M12 0L0 8.5" stroke="#fff" stroke-width="1.6"/><path d="M6 0V8.5M0 4.25H12" stroke="#fff" stroke-width="2.6"/><path d="M6 0V8.5M0 4.25H12" stroke="#C8102E" stroke-width="1.3"/><circle cx="6" cy="12.5" r="1.3" fill="#fff"/><circle cx="18" cy="4" r=".7" fill="#fff"/><circle cx="20" cy="8" r=".7" fill="#fff"/><circle cx="17" cy="9" r=".6" fill="#fff"/><circle cx="19" cy="12" r=".7" fill="#fff"/></svg>',
}
def FL(c): return FLAG[c]
def ic(p): return '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">'+p+'</svg>'
IC = {
 'match':ic('<circle cx="10" cy="10" r="7"/><path d="M10 6v4l3 2"/>'),
 'search':ic('<circle cx="9" cy="9" r="6"/><path d="M14.5 14.5l3 3"/>'),
 'pen':ic('<path d="M4 16l9-9 3 3-9 9H4z"/><path d="M12 5l3 3"/>'),
 'review':ic('<path d="M5 3h8l3 3v11H5z"/><path d="M8 11l1.6 1.6L13 9"/>'),
 'dash':ic('<rect x="3" y="3" width="6.5" height="6.5" rx="1.4"/><rect x="10.5" y="3" width="6.5" height="6.5" rx="1.4"/><rect x="3" y="10.5" width="6.5" height="6.5" rx="1.4"/><rect x="10.5" y="10.5" width="6.5" height="6.5" rx="1.4"/>'),
 'scholar':ic('<path d="M10 3l8 4-8 4-8-4z"/><path d="M5 9v4c0 1.4 2.2 2.5 5 2.5s5-1.1 5-2.5V9"/>'),
 'road':ic('<circle cx="5" cy="15" r="2"/><circle cx="15" cy="5" r="2"/><path d="M7 14c5-.8 6.5-2.5 6.5-7"/>'),
 'crm':ic('<circle cx="7" cy="7" r="2.6"/><path d="M2.5 16c.6-2.8 2.4-4.2 4.5-4.2S10.9 13.2 11.5 16"/><circle cx="14.5" cy="6.5" r="2"/><path d="M12.8 11.4c2.4-.4 4.2.8 4.7 3.4"/>'),
 'analytics':ic('<path d="M3 17V9M8 17V4M13 17v-6M18 17V7"/>'),
 'report':ic('<rect x="4" y="3" width="12" height="14" rx="2"/><path d="M7 7h6M7 10h6M7 13h4"/>'),
 'grow':ic('<path d="M3 16c4 0 5-8 14-9"/><path d="M13 6h4v4"/>'),
 'workspace':ic('<rect x="3" y="4" width="14" height="10" rx="2"/><path d="M3 8h14M7 18h6"/>'),
}
ARROW='<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 8h11M9 4l4 4-4 4"/></svg>'
CHK='<svg viewBox="0 0 12 12"><path d="M2 6l2.5 2.5L10 3"/></svg>'

# ================= nav =================
def dropitem(icon,label,sub):
    return ('<a class="drop-item" href="#"><span class="drop-ic">'+IC[icon]+'</span>'
      '<span><span class="drop-label">'+label+'</span><span class="drop-sub">'+sub+'</span></span></a>')
STUDENTS = ''.join([
 dropitem('match','SmartMatch','Rank the universities you actually qualify for'),
 dropitem('search','University Search','Browse 800+ universities, free'),
 dropitem('pen','Essay Builder','Draft your statement of purpose with AI'),
 dropitem('review','Essay Review','Honest AI feedback on your draft'),
 dropitem('dash','Admission Dashboard','Track every application in one place'),
 dropitem('scholar','Scholarship Search','Funding matched to your profile'),
 dropitem('road','Country Roadmaps','Visa, cost, and timeline guides'),
])
COLLAB = ''.join([
 dropitem('workspace','Partner Workspace','One dashboard for every student you guide'),
 dropitem('crm','Student CRM','Profiles, documents, and deadlines in one place'),
 dropitem('analytics','Cohort Analytics','Progress and outcomes at a glance'),
 dropitem('report','Branded Shortlists','Ranked lists shared under your identity'),
 dropitem('grow','Partnership Program','Grow with Ryogen on real outcomes'),
])
NAV=('<nav><div class="nav-in">'
 '<a href="#top" class="brand"><img class="wordmark" src="'+BRAND_DARK+'" alt="Ryogen"></a>'
 '<ul class="nav-links">'
 '<li class="nav-item"><button class="nav-link">For Students <svg class="caret" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3.5l3 3 3-3"/></svg></button><div class="drop">'+STUDENTS+'</div></li>'
 '<li class="nav-item"><button class="nav-link">For Collaborators <svg class="caret" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3.5l3 3 3-3"/></svg></button><div class="drop">'+COLLAB+'</div></li>'
 '<li class="nav-item"><a href="#scholarships" class="nav-link">Scholarships</a></li>'
 '<li class="nav-item"><a href="#" class="nav-link">Roadmap &amp; Blogs</a></li>'
 '</ul>'
 '<div class="nav-right"><a href="#" class="nav-login">Log in</a><a href="#" class="nav-cta">Get Started Free</a>'
 '<button class="burger" id="burger" aria-label="Menu"><span></span><span></span><span></span></button></div></div>'
 '<div class="mobile-menu" id="mm"><a href="#tools">For Students</a><a href="#partners">For Collaborators</a>'
 '<a href="#scholarships">Scholarships</a><a href="#">Roadmap &amp; Blogs</a><a href="#">Log in</a>'
 '<a href="#" class="mm-cta">Get Started Free</a></div></nav>')

# ================= hero map: crisp arcs, no blur =================
# country-agnostic node field: anonymous "universities" the radar sweep lights up in sequence.
# no destination beams, so adding new countries never means editing the hero.
SWEEP_PERIOD = 9.0  # must match .radar animation duration
CENTER = (250, 470)
random.seed(11)
NODES = [
 (690,205),(830,300),(905,455),(830,615),(650,540),
 (560,175),(760,150),(880,235),(505,300),(600,660),(945,375),(720,410),
]
def node_angle(x, y):
    ang = math.degrees(math.atan2(y - CENTER[1], x - CENTER[0]))  # 0 at +x, clockwise (y down)
    return (ang + 360) % 360
node_svg = ''
for (x, y) in NODES:
    delay = round(node_angle(x, y) / 360.0 * SWEEP_PERIOD, 2)
    r_small = round(random.uniform(1.6, 2.6), 1)
    node_svg += (
      '<g class="unode" style="transform-origin:'+str(x)+'px '+str(y)+'px">'
      '<circle class="uring" cx="'+str(x)+'" cy="'+str(y)+'" r="'+str(r_small)+'" fill="none" stroke="#E30613" stroke-width="1.4" style="animation-delay:'+str(delay)+'s"/>'
      '<circle class="udot" cx="'+str(x)+'" cy="'+str(y)+'" r="'+str(r_small)+'" fill="#EDEDE8" style="animation-delay:'+str(delay)+'s"/>'
      '</g>')
rings=''
for r in [130,250,380,520,660]:
    rings+='<circle cx="250" cy="470" r="'+str(r)+'" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="1"/>'
spokes=''
for a in range(0,360,30):
    rad=math.radians(a)
    spokes+='<line x1="250" y1="470" x2="'+str(round(250+750*math.cos(rad),1))+'" y2="'+str(round(470+750*math.sin(rad),1))+'" stroke="rgba(255,255,255,0.022)" stroke-width="1"/>'
random.seed(7)
dots=''
for _ in range(38):
    x=random.randint(300,1000);y=random.randint(0,700)
    dots+='<circle cx="'+str(x)+'" cy="'+str(y)+'" r="'+str(round(random.uniform(.5,1.3),1))+'" fill="rgba(255,255,255,'+str(round(random.uniform(.04,.14),2))+')"/>'
HERO_MAP=('<div class="hero-map" id="heroMap"><svg viewBox="0 0 1000 700" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">'
 '<defs>'
 '<radialGradient id="sweepG"><stop offset="0%" stop-color="#E30613" stop-opacity="0.30"/><stop offset="70%" stop-color="#E30613" stop-opacity="0.05"/><stop offset="100%" stop-color="#E30613" stop-opacity="0"/></radialGradient>'
 '<linearGradient id="sweepLine" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#E30613" stop-opacity="0"/><stop offset="100%" stop-color="#E30613" stop-opacity="0.55"/></linearGradient>'
 '</defs>'
 '<g class="rings-rotate">'+rings+spokes+'</g>'+dots+
 '<g class="radar" style="transform-origin:250px 470px"><path d="M250 470 L820 470 A570 570 0 0 1 690 861 Z" fill="url(#sweepG)"/><line x1="250" y1="470" x2="820" y2="470" stroke="url(#sweepLine)" stroke-width="1.5"/></g>'
 + node_svg +
 '<circle cx="250" cy="470" r="16" fill="rgba(237,237,232,.07)"/><circle cx="250" cy="470" r="4" fill="#EDEDE8"/>'
 '</svg></div>')

def chip_crest(k): return '<span class="chip-crest"><img src="'+L(k)+'" alt=""></span>'
HERO=('<section class="hero" id="top">'+HERO_MAP+'<div class="hero-veil"></div><div class="hero-fade"></div>'
 '<div class="scan-tag"><span class="ping"><i></i><i class="r"></i></span>Live, matching students to universities worldwide</div>'
 '<div class="hero-in"><div class="hero-copy">'
 '<div class="kicker"><span class="k-line"></span>AI Study Abroad Co-Pilot</div>'
 '<h1 class="hero-h">The <span class="morph-wrap"><span class="morph" id="morph">smarter</span><span class="cursor"></span></span><br>way to study abroad</h1>'
 '<p class="hero-sub">Ryogen matches your academic profile to the right universities anywhere in the world, for free. No consultants, no guesswork.</p>'
 '<div class="social"><div class="avatars"><span class="av av-1">RF</span><span class="av av-2">TI</span><span class="av av-3">SH</span><span class="av av-4">MR</span><span class="av av-5">AN</span></div>'
 '<span class="social-t">Trusted by <strong>2,400+</strong> students worldwide</span></div>'
 '<div class="hero-ctas"><a href="#" class="btn btn-red">Generate my list '+ARROW+'</a><a href="#" class="btn btn-ghost-d">Browse universities</a></div>'
 '</div></div></section>')

# ================= stats (dark bridge, count-up) =================
STATS=('<div class="stats"><div class="stats-in">'
 '<div class="stat"><div class="sv tnum"><span data-count="800">800</span><em>+</em></div><div class="sl">universities indexed</div></div>'
 '<div class="stat"><div class="sv tnum"><span data-count="24">24</span></div><div class="sl">avg matches per profile</div></div>'
 '<div class="stat"><div class="sv tnum"><span data-count="2400" data-comma="1">2,400</span><em>+</em></div><div class="sl">students matched worldwide</div></div>'
 '<div class="stat"><div class="sv">Free</div><div class="sl">for every student</div></div>'
 '</div></div>')

# ================= light body =================
WALL_KEYS=['waseda','kyoto','tsukuba','hokkaido','kuas','toyo','temple','tokyo_intl','monash_my','taylors','sunway','petronas','mmu','utm','harvard','michigan','toronto','mcgill','bristol','coventry','waterloo','asu','manitoba','lakeland']
def wchip(k): return '<span class="wall-chip"><img src="'+L(k)+'" alt=""></span>'
WALL=('<div class="wall light"><div class="wall-label"><b>Verified records</b> from 800+ universities</div>'
 '<div class="wall-mask"><div class="wall-track" id="wallTrack">'+''.join(wchip(k) for k in WALL_KEYS)+'</div></div></div>')

TOOLS=[
 ('01','match','SmartMatch','Enter your grades and test scores. Ryogen ranks every university you realistically qualify for, each with an honest fit score.','Core tool',True),
 ('02','search','University Search','Filter 800+ universities by tuition, deadline, language, and intake. Fully open, no paywall on your research.','',False),
 ('03','pen','Essay Builder','Build your statement of purpose question by question, turning your story into a structured first draft.','',False),
 ('04','review','Essay Review','Get AI feedback on tone, structure, and fit. Coaching, not generation, so your voice stays yours.','',False),
 ('05','dash','Admission Dashboard','Every transcript, essay, and document in one place, with each application tracked end to end.','',False),
 ('06','scholar','Scholarship Search','A searchable index of university and government scholarships, matched to your destination.','',False),
 ('07','road','Country Roadmaps','Step by step guides for visas, costs, and timelines in every live destination.','',False),
]
def tool(t):
    n,icon,name,desc,tag,prime=t
    cls='tool prime reveal' if prime else 'tool reveal'
    tagh='<span class="tag">'+tag+'</span>' if tag else ''
    return '<div class="'+cls+'"><div class="t-ic">'+IC[icon]+'</div><div class="t-n">'+n+'</div><h3>'+name+'</h3><p>'+desc+'</p>'+tagh+'</div>'
TOOLKIT=('<section class="section light" id="tools"><div class="wrap">'
 '<div class="sec-head reveal"><div class="sec-eyebrow">The toolkit</div><h2 class="sec-h">Everything to get you <em>abroad.</em></h2>'
 '<p class="sec-intro">Seven free tools that take you from "I want to study abroad" to a submitted application, all in one place.</p></div>'
 '<div class="tools">'+''.join(tool(t) for t in TOOLS)+'</div></div></section>')

def mrow(name,key,city,tui,cls,pct):
    return ('<div class="mt"><div class="mt-plate"><img src="'+L(key)+'" alt="'+name+'"></div>'
      '<div class="mt-i"><div class="mt-n">'+name+'</div><div class="mt-m">'+city+' \u00b7 '+tui+'/yr</div></div>'
      '<div class="mt-r"><div class="mt-p '+cls+' tnum">'+str(pct)+'%</div><div class="mt-bar"><i class="'+cls+'" data-w="'+str(pct)+'"></i></div></div></div>')
HOW=('<div class="how light"><div class="section"><div class="wrap"><div class="how-grid">'
 '<div class="reveal"><div class="sec-eyebrow">How it works</div><h2 class="sec-h">Profile to shortlist in <em>seconds.</em></h2>'
 '<div class="how-steps">'
 '<div class="how-step on"><div class="sn">1</div><div><div class="sname">Enter your profile</div><div class="sdesc">GPA, test scores, field, and destination</div></div></div>'
 '<div class="how-step"><div class="sn">2</div><div><div class="sname">Ryogen ranks your matches</div><div class="sdesc">Scored against verified admission data</div></div></div>'
 '<div class="how-step"><div class="sn">3</div><div><div class="sname">Apply with confidence</div><div class="sdesc">Essays, deadlines, scholarships, all guided</div></div></div>'
 '</div></div>'
 '<div class="reveal d2"><div class="terminal"><div class="term-bar"><div class="term-bar-l">'+IC['match']+' SmartMatch</div><div class="term-dots"><i></i><i></i><i></i></div></div>'
 '<div class="term-body"><div class="tp">'
 '<div class="tpf"><div class="k">GPA</div><div class="v">3.72 <span class="u">/ 4.0</span></div></div>'
 '<div class="tpf"><div class="k">IELTS</div><div class="v">7.0 <span class="u">band</span></div></div>'
 '<div class="tpf"><div class="k">Field</div><div class="v" style="font-size:.78rem">Computer Science</div></div>'
 '<div class="tpf"><div class="k">Budget</div><div class="v">\u00a51.3M</div></div>'
 '</div><div class="tm-h"><span class="tm-t">Ranked matches</span><span class="tm-s">sorted by fit</span></div>'
 + mrow('Waseda University','waseda','Tokyo','\u00a51.29M','cy',92)
 + mrow('Monash University Malaysia','monash_my','Subang Jaya','RM 42K','cy',91)
 + mrow('Kyoto University','kyoto','Kyoto','\u00a5536K','hi',86)
 + mrow('Universiti Teknologi Malaysia','utm','Johor Bahru','RM 16K','md',79)
 + '<div class="tm-f"><div class="l"><b>20</b> more matched</div><a href="#">View all '+ARROW+'</a></div>'
 '</div></div></div></div></div></div></div>')

# ---- ring (light) ----
UNIS=[
 ('Waseda University','waseda','JP','Tokyo','\u00a51.29M','cy',92,True),
 ('Monash University Malaysia','monash_my','MY','Subang Jaya','RM 42K','cy',91,True),
 ('Kyoto University','kyoto','JP','Kyoto','\u00a5536K','hi',86,False),
 ('University of Tsukuba','tsukuba','JP','Tsukuba','\u00a5536K','hi',84,False),
 ('Hokkaido University','hokkaido','JP','Sapporo','\u00a5536K','hi',83,False),
 ('Taylor\u2019s University','taylors','MY','Subang Jaya','RM 48K','cy',90,True),
 ('Sunway University','sunway','MY','Subang Jaya','RM 40K','hi',88,False),
 ('Universiti Teknologi PETRONAS','petronas','MY','Seri Iskandar','RM 34K','hi',85,False),
 ('Multimedia University','mmu','MY','Cyberjaya','RM 32K','hi',82,False),
 ('Universiti Teknologi Malaysia','utm','MY','Johor Bahru','RM 16K','md',79,False),
 ('Toyo University','toyo','JP','Tokyo','\u00a51.10M','md',78,False),
 ('Temple University Japan','temple','JP','Tokyo','\u00a51.55M','md',76,False),
]
def ringcard(u,angle):
    name,key,co,city,tui,cls,pct,top=u
    tag='<div class="rc-tag">Top fit</div>' if top else ''
    return ('<div class="rcard" style="transform:rotateY('+str(angle)+'deg) translateZ(480px)">'+tag+
      '<div class="rc-plate"><img src="'+L(key)+'" alt="'+name+'"></div>'
      '<div class="rc-name">'+name+'</div><div class="rc-loc"><span class="rc-flag">'+FL(co)+'</span>'+city+'</div>'
      '<div class="rc-foot"><div class="rc-tui"><span>Tuition / yr</span>'+tui+'</div><div class="rc-badge '+cls+' tnum">'+str(pct)+'%</div></div></div>')
def ringflat(u):
    name,key,co,city,tui,cls,pct,top=u
    tag='<div class="rc-tag">Top fit</div>' if top else ''
    return ('<div class="rcard" style="position:relative;flex:0 0 220px;width:220px;height:280px;scroll-snap-align:start">'+tag+
      '<div class="rc-plate" style="height:88px"><img src="'+L(key)+'" alt="'+name+'"></div>'
      '<div class="rc-name">'+name+'</div><div class="rc-loc"><span class="rc-flag">'+FL(co)+'</span>'+city+'</div>'
      '<div class="rc-foot"><div class="rc-tui"><span>Tuition / yr</span>'+tui+'</div><div class="rc-badge '+cls+' tnum">'+str(pct)+'%</div></div></div>')
ringcards=''.join(ringcard(u,round(i*360/len(UNIS))) for i,u in enumerate(UNIS))
RING=('<section class="ring-sec section light" id="explore"><div class="ring-glow"></div>'
 '<div class="wrap"><div class="sec-head center reveal"><div class="sec-eyebrow">Matched universities</div>'
 '<h2 class="sec-h">A world of options, <em>ranked for you.</em></h2>'
 '<p class="sec-intro" style="margin:0 auto">Every card is a real university in a live destination, scored against a sample profile. Hover to pause and explore.</p></div></div>'
 '<div class="scene"><div class="ring">'+ringcards+'</div></div>'
 '<div class="ring-scroller" aria-hidden="true">'+''.join(ringflat(u) for u in UNIS)+'</div>'
 '</section>')

def dcrest(k): return '<span class="dcrest"><img src="'+L(k)+'" alt=""></span>'
DEST=('<section class="section light" id="destinations"><div class="wrap">'
 '<div class="sec-head reveal"><div class="sec-eyebrow">Live destinations</div><h2 class="sec-h">Two countries live. <em>More on the way.</em></h2>'
 '<p class="sec-intro">Every destination is a fully verified database of admission criteria, tuition, deadlines, and scholarships, kept current.</p></div>'
 '<div class="dest-grid">'
 '<div class="dcard reveal d1"><span class="dlive">Live</span><div class="dtop"><span class="dflag">'+FL('JP')+'</span><div><h3>Japan</h3><div class="dsub">320 universities indexed</div></div></div>'
   '<div class="dcrests">'+dcrest('waseda')+dcrest('kyoto')+dcrest('tsukuba')+dcrest('hokkaido')+dcrest('kuas')+'</div>'
   '<div class="dtags"><span class="dtag">MEXT scholarships</span><span class="dtag">English programs</span><span class="dtag">Low national fees</span></div></div>'
 '<div class="dcard reveal d2"><span class="dlive">Live</span><div class="dtop"><span class="dflag">'+FL('MY')+'</span><div><h3>Malaysia</h3><div class="dsub">180 universities indexed</div></div></div>'
   '<div class="dcrests">'+dcrest('monash_my')+dcrest('taylors')+dcrest('sunway')+dcrest('petronas')+dcrest('mmu')+'</div>'
   '<div class="dtags"><span class="dtag">English medium</span><span class="dtag">Affordable living</span><span class="dtag">Global campuses</span></div></div>'
 '</div>'
 '<div class="coming reveal d3"><span class="cl">Charting next</span><div class="cflags">'
 '<span class="cf"><span class="fl">'+FL('US')+'</span>United States</span>'
 '<span class="cf"><span class="fl">'+FL('UK')+'</span>United Kingdom</span>'
 '<span class="cf"><span class="fl">'+FL('CA')+'</span>Canada</span>'
 '<span class="cf"><span class="fl">'+FL('AU')+'</span>Australia</span>'
 '</div></div></div></section>')

# ---- institutions (abstract, no agency/counselor wording) ----
B2B=('<div class="b2b light" id="partners"><div class="section"><div class="wrap"><div class="b2b-grid">'
 '<div class="reveal"><div class="sec-eyebrow">For collaborators</div><h2 class="sec-h">One workspace for every <em>student journey.</em></h2>'
 '<p class="sec-intro">Ryogen partners with schools, universities, and education organizations around the world. Bring the students you guide onto one platform and back every decision with data.</p>'
 '<ul class="b2b-list">'
 '<li><span class="b2b-ck">'+CHK+'</span><span><b>Student CRM.</b> Every profile, document, and deadline in a single dashboard.</span></li>'
 '<li><span class="b2b-ck">'+CHK+'</span><span><b>Cohort analytics.</b> See where every student stands, from shortlist to enrolment.</span></li>'
 '<li><span class="b2b-ck">'+CHK+'</span><span><b>Branded shortlists.</b> Share ranked, data backed lists under your own identity.</span></li>'
 '<li><span class="b2b-ck">'+CHK+'</span><span><b>Partnership on outcomes.</b> Grow with Ryogen as your students succeed.</span></li>'
 '</ul><a href="#" class="btn btn-red">Talk to our team '+ARROW+'</a></div>'
 '<div class="reveal d2"><div class="b2b-panel"><div class="b2b-pt"><span>Partner workspace</span><span class="live"><i></i>This quarter</span></div>'
 '<div class="pipe-row"><span class="num">1</span><div><div class="a">Profiles onboarded</div><div class="b">Students brought onto the platform</div></div><span class="val tnum">1,240</span></div>'
 '<div class="pipe-row"><span class="num">2</span><div><div class="a">Shortlists generated</div><div class="b">Ranked with SmartMatch</div></div><span class="val tnum">980</span></div>'
 '<div class="pipe-row"><span class="num">3</span><div><div class="a">Applications tracked</div><div class="b">Managed end to end</div></div><span class="val tnum">640</span></div>'
 '<div class="pipe-row"><span class="num">4</span><div><div class="a">Enrolments confirmed</div><div class="b">Real outcomes, this intake</div></div><span class="val tnum">210</span></div>'
 '</div></div></div></div></div></div>')

SCH=('<section class="section light" id="scholarships"><div class="wrap"><div class="sec-head center reveal">'
 '<div class="sec-eyebrow">Scholarships</div><h2 class="sec-h">Funding you can actually <em>win.</em></h2>'
 '<p class="sec-intro" style="margin:0 auto">Ryogen surfaces university and government scholarships matched to your country, field, and destination, so you never miss one you qualify for.</p></div>'
 '<div class="dest-grid">'
 '<div class="dcard reveal d1"><div class="dtop"><span class="dflag">'+FL('JP')+'</span><div><h3>Japan</h3><div class="dsub">MEXT, JASSO, and university awards</div></div></div>'
 '<div class="dtags"><span class="dtag">Full tuition waivers</span><span class="dtag">Monthly stipends</span><span class="dtag">No IELTS routes</span></div></div>'
 '<div class="dcard reveal d2"><div class="dtop"><span class="dflag">'+FL('MY')+'</span><div><h3>Malaysia</h3><div class="dsub">Merit and need based funding</div></div></div>'
 '<div class="dtags"><span class="dtag">Up to 100% tuition</span><span class="dtag">Foundation grants</span><span class="dtag">Early bird awards</span></div></div>'
 '</div></div></section>')

CTA=('<div class="cta section"><div class="cta-glow"></div><div class="wrap"><div class="cta-in reveal">'
 '<h2>Your route abroad<br>starts <em>here.</em></h2>'
 '<p>Free, AI powered, and built for every student aiming to study abroad. No consultant required.</p>'
 '<div class="cta-form"><input type="email" placeholder="Enter your email address"><button class="btn btn-red">Get early access</button></div>'
 '<div class="cta-note">Free forever for students \u00b7 no card required</div></div></div></div>')

def fcol(h,items): return '<div class="foot-col"><h5>'+h+'</h5>'+''.join('<a href="#">'+i+'</a>' for i in items)+'</div>'
FOOTER=('<footer><div class="wrap"><div class="foot">'
 '<div class="foot-brand"><a href="#top" class="brand"><img class="wordmark" src="'+BRAND_DARK+'" alt="Ryogen"></a>'
 '<p>The AI co-pilot for students charting their path to universities abroad. Free, for every student, everywhere.</p></div>'
 +fcol('For Students',['SmartMatch','University Search','Essay Builder','Essay Review','Admission Dashboard','Scholarship Search'])
 +fcol('For Collaborators',['Partner Workspace','Student CRM','Cohort Analytics','Partnership Program'])
 +fcol('Company',['Destinations','Country Roadmaps','Blog','About','Contact'])
 +'</div><div class="foot-bot"><span>\u00a9 2026 Ryogen.ai \u00b7 For students charting their path to universities worldwide</span>'
 '<span class="r"><a href="#">Privacy</a><a href="#">Terms</a></span></div></div></footer>')

SCRIPT=r"""
<script>
(function(){
  var d=document, root=d.documentElement, win=window;
  var reduce=false; try{reduce=win.matchMedia('(prefers-reduced-motion:reduce)').matches;}catch(e){}

  // Collect animated elements, then arm the reveal system.
  // Content is visible by default (CSS); we only hide it once JS is confirmed running,
  // so a script failure can never leave the page blank.
  var reveals=[].slice.call(d.querySelectorAll('.reveal'));
  var counters=[].slice.call(d.querySelectorAll('[data-count]'));
  var terminals=[].slice.call(d.querySelectorAll('.terminal'));
  root.className += ' js';                 // arms .js .reveal{opacity:0}
  if(!reduce){ for(var c=0;c<counters.length;c++){ counters[c].textContent='0'; } }

  function show(el){ el.classList.add('in'); }
  function runCount(el){
    if(el._d)return; el._d=1;
    var t=+el.getAttribute('data-count'), comma=el.getAttribute('data-comma');
    if(reduce){ el.textContent=comma?t.toLocaleString():t; return; }
    var n=0, steps=40, inc=t/steps;
    var iv=setInterval(function(){ n+=inc; if(n>=t){n=t;clearInterval(iv);}
      var v=Math.round(n); el.textContent=comma?v.toLocaleString():v; },26);
  }
  function runBars(t){ if(t._d)return; t._d=1; var b=t.querySelectorAll('.mt-bar i');
    for(var i=0;i<b.length;i++){ b[i].style.width=b[i].getAttribute('data-w')+'%'; } }

  function inView(el){ var r=el.getBoundingClientRect(); var h=win.innerHeight||root.clientHeight;
    return r.top < h*0.9; }   // triggers when top enters view OR has scrolled above it (never missed)
  function sweep(){
    var i;
    for(i=0;i<reveals.length;i++){ if(!reveals[i].classList.contains('in') && inView(reveals[i])) show(reveals[i]); }
    for(i=0;i<counters.length;i++){ if(!counters[i]._d && inView(counters[i])) runCount(counters[i]); }
    for(i=0;i<terminals.length;i++){ if(!terminals[i]._d && inView(terminals[i])) runBars(terminals[i]); }
  }

  // Reliable scroll/resize/load driven reveal (works on iOS Safari regardless of IO).
  var ticking=false;
  function onScroll(){ if(ticking)return; ticking=true;
    (win.requestAnimationFrame||function(f){setTimeout(f,16);})(function(){ sweep(); ticking=false; }); }
  win.addEventListener('scroll',onScroll,{passive:true});
  win.addEventListener('resize',onScroll,{passive:true});
  win.addEventListener('load',sweep);
  sweep();                    // reveal anything already in view
  setTimeout(sweep,250);      // after layout settles
  setTimeout(sweep,800);
  setTimeout(sweep,1800);     // final safety pass for in-view content

  // IntersectionObserver as a smoothness enhancement only.
  try{ if('IntersectionObserver' in win){
    var io=new IntersectionObserver(function(es){ for(var i=0;i<es.length;i++){ var e=es[i]; if(!e.isIntersecting)continue;
      var el=e.target;
      if(el.classList.contains('reveal')) show(el);
      if(el.getAttribute && el.getAttribute('data-count')!==null) runCount(el);
      if(el.classList.contains('terminal')) runBars(el);
      io.unobserve(el);
    }},{threshold:.08});
    var all=reveals.concat(counters).concat(terminals);
    for(var i=0;i<all.length;i++) io.observe(all[i]);
  }}catch(e){}

  // ---- enhancements (each isolated so one failure can't cascade) ----
  try{ var words=['smarter','faster','clearer','data-driven','honest'];
    var el=d.getElementById('morph');
    if(el&&!reduce){ var wi=0,ci=el.textContent.length,del=true;
      (function type(){ var w=words[wi];
        if(!del){ el.textContent=w.slice(0,++ci); if(ci===w.length){del=true;setTimeout(type,1700);return;} }
        else{ el.textContent=w.slice(0,--ci); if(ci===0){del=false;wi=(wi+1)%words.length;} }
        setTimeout(type,del?55:100); })(); }
  }catch(e){}

  try{ var bg=d.getElementById('burger'),mm=d.getElementById('mm');
    if(bg&&mm){ bg.addEventListener('click',function(){ mm.style.display=(mm.style.display==='block')?'none':'block'; });
      var ml=mm.querySelectorAll('a'); for(var i=0;i<ml.length;i++){ ml[i].addEventListener('click',function(){mm.style.display='none';}); } }
  }catch(e){}

  try{ var wt=d.getElementById('wallTrack'); if(wt){ wt.innerHTML+=wt.innerHTML; } }catch(e){}

  try{ var steps=[].slice.call(d.querySelectorAll('.how-step'));
    if(steps.length&&!reduce){ var si=0; setInterval(function(){ si=(si+1)%steps.length;
      for(var i=0;i<steps.length;i++) steps[i].classList.toggle('on',i===si); },2600); }
  }catch(e){}

  try{ var map=d.getElementById('heroMap');
    if(map&&!reduce){ win.addEventListener('mousemove',function(e){
      var x=(e.clientX/win.innerWidth-.5),y=(e.clientY/win.innerHeight-.5);
      map.style.transform='translate('+(x*10).toFixed(1)+'px,'+(y*10).toFixed(1)+'px)'; }); }
  }catch(e){}
})();
</script>"""

DEV='<div class="dev-tag"><b>Ryogen v9</b><br>iOS reveal fix: content visible by default, scroll-driven reveal + failsafe. Remove before ship.</div>'

HEAD=('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">'
 '<meta name="color-scheme" content="light">'
 '<title>Ryogen, AI Study Abroad Co-Pilot</title>'
 '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400;1,500;1,600&display=swap" rel="stylesheet">'
 '<style>'+CSS+'</style></head><body>')

HTML=HEAD+NAV+HERO+STATS+WALL+TOOLKIT+HOW+RING+DEST+SCH+B2B+CTA+FOOTER+DEV+SCRIPT+'</body></html>'
HTML=HTML.replace('\u2014',', ').replace('\u2013','-')
out='/home/claude/work/build_compare/test_v9.html'
open(out,'w',encoding='utf-8').write(HTML)
import re
print('written',len(HTML),out)
print('dashes:',HTML.count('\u2014')+HTML.count('\u2013'),'| coords:',len(re.findall(r'\d+\.?\d*\s*\u00b0\s*[NSEW]',HTML)),
 '| agency/counselor mentions:',len(re.findall(r'agenc|counsel|coaching cent',HTML,re.I)))
