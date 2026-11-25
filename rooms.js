/* Shared helpers for the Studio rooms. Requires book.js (MW). */
window.MWR=(function(){
  const $=s=>document.querySelector(s);
  const probe=document.createElement('span');probe.style.display='none';
  document.addEventListener('DOMContentLoaded',()=>document.body.appendChild(probe));
  if(document.body)document.body.appendChild(probe);
  function col(v){probe.style.color=`var(${v})`;return getComputedStyle(probe).color}
  function ctx(cv){const d=window.devicePixelRatio||1,W=cv.clientWidth||500,H=cv.clientHeight||500;cv.width=Math.round(W*d);cv.height=Math.round(H*d);const g=cv.getContext('2d');g.setTransform(d,0,0,d,0,0);return[g,W,H]}
  function range(id,fn){const el=$('#'+id),o=$('#'+id+'-o');const up=()=>{if(o)o.textContent=el.value;fn&&fn()};el.addEventListener('input',up);if(o)o.textContent=el.value;return el}
  function setR(id,v){const el=$('#'+id);el.value=v;const o=$('#'+id+'-o');if(o)o.textContent=el.value}
  function seg(id,items,init,fn){const box=$('#'+id);box.innerHTML=items.map(([v,l])=>`<button type="button" data-v="${v}" aria-pressed="${String(v)===String(init)}">${l}</button>`).join('');
    box.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;box.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',x===b));fn(b.dataset.v)})}
  function pressSeg(id,v){document.querySelectorAll('#'+id+' button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.v===String(v)))}
  function still(cvSel,outSel,what){const url=$(cvSel).toDataURL('image/png');$(outSel).innerHTML=`<img alt="A still of ${what}" src="${url}"><p class="note">Right-click or press and hold the picture to save it.</p>`}
  const reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* audio */
  const A={c:null,out:null,noise:null};
  function audio(){if(!A.c){const c=new (window.AudioContext||window.webkitAudioContext)();const comp=c.createDynamicsCompressor();const g=c.createGain();g.gain.value=0.6;g.connect(comp);comp.connect(c.destination);A.c=c;A.out=g;
      const b=c.createBuffer(1,c.sampleRate,c.sampleRate),d=b.getChannelData(0);for(let i=0;i<d.length;i++)d[i]=Math.random()*2-1;A.noise=b}
    if(A.c.state==='suspended')A.c.resume();return A}
  function env(g,t,v,d){g.gain.setValueAtTime(0.0001,t);g.gain.exponentialRampToValueAtTime(v,t+0.008);g.gain.exponentialRampToValueAtTime(0.0001,t+d)}
  function tone(f,t,d=0.4,v=0.25){const c=audio().c;const o=c.createOscillator(),g=c.createGain();o.type='triangle';o.frequency.value=f;env(g,t,v,d);o.connect(g);g.connect(A.out);o.start(t);o.stop(t+d+0.05)}
  function clap(t,v=0.4){const c=audio().c,s=c.createBufferSource(),f=c.createBiquadFilter(),g=c.createGain();s.buffer=A.noise;f.type='bandpass';f.frequency.value=1300;env(g,t,v,0.12);s.connect(f);f.connect(g);g.connect(A.out);s.start(t);s.stop(t+0.2)}
  return {$,col,ctx,range,setR,seg,pressSeg,still,reduce,audio,tone,clap,A};
})();
