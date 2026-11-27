/* Check-yourself questions (Modular Worlds). Markup:
 <div class="cyq" data-kind="num|word|set|lin" data-a="answer(s), | separates alternatives; lin: a,b,c" data-hint="..." data-show="full answer">
   <label for=ID>question</label><div class="row2"><input id=ID>[<input> for lin]<button class="ck">Check</button></div><div class="fb" aria-live="polite"></div></div> */
(function(){
const norm=s=>String(s).trim().toLowerCase().replace(/[−–]/g,'-').replace(/\s+/g,' ');
const num=s=>{const t=norm(s).replace(/,/g,'');return t===''?NaN:Number(t)};
function judge(q){const kind=q.dataset.kind||'num',a=q.dataset.a||'',ins=[...q.querySelectorAll('input')];
  if(kind==='lin'){const [A,B,C]=a.split(',').map(Number),x=num(ins[0].value),y=num(ins[1].value);
    if(!Number.isInteger(x)||!Number.isInteger(y))return null;return A*x+B*y===C}
  const v=ins[0].value;if(norm(v)==='')return null;
  if(kind==='num'){const x=num(v);return a.split('|').some(t=>Number(t)===x)}
  if(kind==='set'){const got=norm(v).split(/[ ,;]+/).filter(Boolean).map(Number).sort((p,q)=>p-q).join(',');
    return a.split('|').some(t=>t.split(/[ ,;]+/).map(Number).sort((p,q)=>p-q).join(',')===got)}
  return a.split('|').some(t=>norm(t)===norm(v))}
document.querySelectorAll('.cyq').forEach(q=>{const fb=q.querySelector('.fb'),btn=q.querySelector('.ck');let tries=0;
  const go=()=>{const r=judge(q);fb.className='fb';
    if(r===null){fb.textContent=q.dataset.kind==='lin'?'Type a whole number in each box.':'Type an answer first.';return}
    if(r){fb.className='fb ok';fb.textContent='✓ Correct. '+(q.dataset.why||'');return}
    tries++;fb.className='fb no';fb.textContent='✗ Not yet. '+(q.dataset.hint||'Try again.');
    if(tries>=2&&q.dataset.show&&!q.querySelector('.showa')){const b=document.createElement('button');b.className='showa';b.textContent='Show the answer';b.style.marginTop='6px';
      b.onclick=()=>{fb.className='fb';fb.textContent='Answer: '+q.dataset.show;b.remove()};q.appendChild(b)}};
  btn.addEventListener('click',go);q.querySelectorAll('input').forEach(i=>i.addEventListener('keydown',e=>{if(e.key==='Enter')go()}))});
})();
