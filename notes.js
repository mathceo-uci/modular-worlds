/* Paradox notes and puzzles (Modular Worlds). Each instrument runs only if its elements are on the page. */
(function(){
const $=s=>document.querySelector(s);
const gcd=(a,b)=>{a=Math.abs(a);b=Math.abs(b);while(b){[a,b]=[b,a%b]}return a};
const egcd=(a,b)=>{if(b===0)return[a,1,0];const[g,x,y]=egcd(b,a%b);return[g,y,x-Math.floor(a/b)*y]};
const mod=(a,n)=>((a%n)+n)%n;
const DAYS=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];

/* guess-first buttons: <div class="guess" data-for="ID" data-right="a|b"> with buttons data-g="a"/"b" */
document.querySelectorAll('.guess').forEach(g=>{
  const rev=document.getElementById(g.dataset.for);
  g.querySelectorAll('button[data-g]').forEach(b=>b.addEventListener('click',()=>{
    g.querySelectorAll('button[data-g]').forEach(x=>x.setAttribute('aria-pressed',x===b));
    const v=rev.querySelector('.verdict');
    if(v)v.textContent=(b.dataset.g===g.dataset.right?'Your guess was right. ':'Surprise! ')+v.dataset.msg;
    rev.hidden=false;
  }));
});

/* Ch0: odd squares on an 8-hour clock */
if($('#sq8go')){const run=()=>{const n=Math.floor(+$('#sq8n').value);
  if(!(n>=1&&n<=99999)){$('#sq8out').textContent='Enter a whole number from 1 to 99999.';return}
  const s=n*n,q=Math.floor(s/8),r=s%8;
  $('#sq8out').textContent=`${n}² = ${s.toLocaleString('en-US')} = 8 · ${q.toLocaleString('en-US')} + ${r}\n`+(n%2?`Remainder 1, as for every odd number.`:`${n} is even, so its square is a multiple of 4: remainder ${r}.`)};
  $('#sq8go').addEventListener('click',run);$('#sq8n').addEventListener('keydown',e=>{if(e.key==='Enter')run()});run()}

/* Ch0: chameleons */
if($('#chgo')){const C={r:13,g:15,b:17};const names={r:'red',g:'green',b:'blue'};
  const draw=(msg)=>{const d=(x,y)=>mod(C[x]-C[y],3);
    $('#chout').textContent=`Red ${C.r} · Green ${C.g} · Blue ${C.b}   (total ${C.r+C.g+C.b})\nRemainders of the differences when divided by 3:\n  green − red → ${d('g','r')}   blue − green → ${d('b','g')}   blue − red → ${d('b','r')}`+(msg?'\n'+msg:'');
    ['rg','rb','gb'].forEach(k=>{$('#ch'+k).disabled=!(C[k[0]]>0&&C[k[1]]>0)})};
  const meet=(x,y)=>{const z='rgb'.replace(x,'').replace(y,'');C[x]--;C[y]--;C[z]+=2;
    const one=[C.r,C.g,C.b].filter(v=>v>0).length===1;
    draw(`A ${names[x]} and a ${names[y]} chameleon met: both turned ${names[z]}.`+(one?' Everyone is one color!':''))};
  $('#chrg').addEventListener('click',()=>meet('r','g'));$('#chrb').addEventListener('click',()=>meet('r','b'));$('#chgb').addEventListener('click',()=>meet('g','b'));
  $('#chgo').addEventListener('click',()=>{const r=Math.floor(+$('#chR').value),g=Math.floor(+$('#chG').value),b=Math.floor(+$('#chB').value);
    if(![r,g,b].every(v=>v>=0&&v<=99)){draw('Counts must be whole numbers from 0 to 99.');return}C.r=r;C.g=g;C.b=b;draw('New island.')});
  draw()}

/* Ch1: birthday weekdays */
if($('#bdgo')){const run=()=>{const m=+$('#bdm').value,d=Math.floor(+$('#bdd').value),y=Math.floor(+$('#bdy').value);
  const dt=new Date(Date.UTC(y,m-1,d));
  if(!(y>=1900&&y<=2400)||dt.getUTCMonth()!==m-1||dt.getUTCDate()!==d){$('#bdout').textContent='Pick a real date between 1900 and 2400.';return}
  if(m===2&&d===29){$('#bdout').textContent='February 29 only exists in leap years: that birthday moves 5 weekdays every 4 years (4 · 365 + 1 = 1461 days = 7 · 208 + 5). Try another date.';return}
  const lines=[];let first=null;const w0=dt.getUTCDay();
  for(let k=0;k<12;k++){const t=new Date(Date.UTC(y+k,m-1,d));const w=t.getUTCDay();
    let note='';if(k>0){const prev=new Date(Date.UTC(y+k-1,m-1,d));const days=Math.round((t-prev)/864e5);note=`  (+${days} days = 52 weeks + ${days-364} → ${days-364} weekday${days-364>1?'s':''} on)`}
    if(k>0&&w===w0&&first===null)first=k;lines.push(`${y+k}: ${DAYS[w]}${note}`)}
  $('#bdout').textContent=lines.join('\n')+(first?`\nSame weekday as ${y} again after ${first} years.`:'')};
  $('#bdgo').addEventListener('click',run);run()}

/* Ch1: Bachet's pile */
if($('#bpgo')){const B={n:20,turn:'you',over:true};
  const draw=(msg)=>{$('#bppile').textContent='●'.repeat(B.n)||'(empty)';$('#bppile').setAttribute('aria-label',B.n+' stones left');
    $('#bpn').textContent=B.n;[1,2,3].forEach(k=>{$('#bp'+k).disabled=B.over||B.turn!=='you'||k>B.n});if(msg)$('#bpout').textContent=msg};
  const pesado=()=>{let k=B.n%4;let line;if(k===0){k=1;line='El Gran Pesado frowns and takes 1.'}else line=`El Gran Pesado takes ${k} with a grin.`;
    B.n-=k;if(B.n===0){B.over=true;draw(line+' He took the last stone: he wins! Want a rematch?');return}B.turn='you';draw(line+` Your turn: ${B.n} left.`)};
  const take=k=>{if(B.over||B.turn!=='you'||k>B.n)return;B.n-=k;if(B.n===0){B.over=true;draw(`You took the last stone. You win! Can you explain why ${$('#bpstart').value} was ${(+$('#bpstart').value)%4?'a winning start for whoever moves first':'a winning start for whoever moves second'}?`);return}
    B.turn='pesado';draw(`You took ${k}. ${B.n} left.`);setTimeout(pesado,650)};
  [1,2,3].forEach(k=>$('#bp'+k).addEventListener('click',()=>take(k)));
  $('#bpgo').addEventListener('click',()=>{B.n=Math.max(5,Math.min(40,Math.floor(+$('#bpstart').value)||20));B.over=false;
    if($('#bpwho').value==='me'){B.turn='you';draw(`New pile of ${B.n}. You go first: take 1, 2 or 3.`)}else{B.turn='pesado';draw(`New pile of ${B.n}. El Gran Pesado goes first…`);setTimeout(pesado,650)}});
  draw('Choose a pile size and who starts, then press "New game".')}

/* Ch2: Friday the 13th */
if($('#f13go')){const cnt=[0,0,0,0,0,0,0];for(let y=2000;y<2400;y++)for(let m=0;m<12;m++)cnt[new Date(Date.UTC(y,m,13)).getUTCDay()]++;
  const mx=Math.max(...cnt);
  $('#f13bars').textContent=cnt.map((c,i)=>`${DAYS[i].slice(0,3)}  ${'█'.repeat(c-680)} ${c}`).join('\n')+'\n(bars show how far each count is above 680)';
  const run=()=>{const y=Math.floor(+$('#f13y').value);if(!(y>=1600&&y<=3000)){$('#f13out').textContent='Pick a year from 1600 to 3000.';return}
    const fr=[];for(let m=0;m<12;m++)if(new Date(Date.UTC(y,m,13)).getUTCDay()===5)fr.push(new Date(Date.UTC(y,m,13)).toLocaleString('en-US',{month:'long',timeZone:'UTC'}));
    $('#f13out').textContent=`${y} has ${fr.length} Friday the 13th${fr.length>1?'s':''}: ${fr.join(', ')}.`};
  $('#f13go').addEventListener('click',run);run()}

/* Ch3: halves on a clock */
if($('#hfgo')){const run=()=>{const n=Math.floor(+$('#hfn').value),a=Math.floor(+$('#hfa').value);
  if(!(n>=2&&n<=999&&a>=1&&a<n)){$('#hfout').textContent='Clock size 2 to 999, and a number from 1 to one less than the clock size.';return}
  const [g,x]=egcd(a,n);
  if(g!==1){$('#hfout').textContent=`gcd(${a}, ${n}) = ${g}. Every multiple of ${a} lands on a multiple of ${g} on this clock, never on 1.\nSo there is no "1 ÷ ${a}" on a ${n}-hour clock.`;return}
  const inv=mod(x,n),y=(1-a*inv)/n;
  $('#hfout').textContent=`Bézout: ${a} · ${inv} ${y<0?'−':'+'} ${n} · ${Math.abs(y)} = 1\nSo ${a} · ${inv} = ${a*inv} lands on 1 on a ${n}-hour clock: "1 ÷ ${a}" is ${inv}.`};
  $('#hfgo').addEventListener('click',run);run()}

/* Ch5: zero products */
if($('#zpgo')){const run=()=>{const n=Math.floor(+$('#zpn').value);if(!(n>=2&&n<=60)){$('#zpout').textContent='Pick a clock size from 2 to 60.';return}
  const pairs=[];for(let a=1;a<n;a++)for(let b=a;b<n;b++)if((a*b)%n===0)pairs.push(`${a} × ${b}`);
  const prime=n>1&&[...Array(n).keys()].slice(2).every(d=>d*d>n||n%d);
  $('#zpout').textContent=pairs.length?`On a ${n}-hour clock these products land on 0:\n${pairs.slice(0,24).join(',  ')}${pairs.length>24?', …':''}\n${n} is not prime, so it splits into smaller factors.`:`On a ${n}-hour clock no two nonzero hours multiply to 0.\n${prime?n+' is prime: by Lemma 5.4, if '+n+' divides a × b it divides a or b.':''}`};
  $('#zpgo').addEventListener('click',run);run()}
})();
