
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
