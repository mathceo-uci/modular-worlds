/* Practice Deck drills (Modular Worlds) */
(function(){
const R=(a,b)=>a+Math.floor(Math.random()*(b-a+1));
const pick=a=>a[Math.floor(Math.random()*a.length)];
const gcd=(a,b)=>{a=Math.abs(a);b=Math.abs(b);while(b)[a,b]=[b,a%b];return a};
const egcd=(a,b)=>{if(b===0)return[a,1,0];const[g,x,y]=egcd(b,a%b);return[g,y,x-Math.floor(a/b)*y]};
const isP=n=>{if(n<2)return false;for(let d=2;d*d<=n;d++)if(n%d===0)return false;return true};
const fac=n=>{const f=[];for(let p=2;p*p<=n;p++){let e=0;while(n%p===0){n/=p;e++}if(e)f.push([p,e])}if(n>1)f.push([n,1]);return f};
const sup=e=>String(e).split('').map(c=>'⁰¹²³⁴⁵⁶⁷⁸⁹'[+c]).join('');
const fstr=f=>f.map(([p,e])=>e>1?p+sup(e):String(p)).join(' · ');
const divs=n=>{const d=[];for(let k=1;k<=n;k++)if(n%k===0)d.push(k);return d};
const norm=s=>String(s).trim().toLowerCase().replace(/[−–]/g,'-');
const N=s=>{const t=norm(s).replace(/,/g,'');return t===''?NaN:Number(t)};
const par=n=>n%2?'odd':'even';
const euclidSteps=(a,b)=>{const L=[];while(b){L.push(`${a} = ${Math.floor(a/b)} · ${b} + ${a%b}`);[a,b]=[b,a%b]}return [a,L]};

const SK=[
{ch:'ch0',t:'Even or odd?',gen(){const a=R(11,999),b=R(11,999),c=R(11,999);const v=a*b+c;
  return {q:`Is ${a} · ${b} + ${c} even or odd? Decide without multiplying.`,f:[['even or odd','',1]],ok:x=>norm(x[0])===par(v),
  sol:`${a} is ${par(a)}, ${b} is ${par(b)}, so the product is ${par(a*b)}.\n${par(a*b)} + ${par(c)} = ${par(v)}.\n(Check: ${v.toLocaleString('en-US')}.)`}}},
{ch:'ch0',t:'Count the divisors',gen(){const n=pick([R(12,150),R(12,150),pick([16,25,36,49,64,81,100,121,144])]);const d=divs(n);
  return {q:`How many positive divisors does ${n} have?`,f:[['divisors','']],ok:x=>N(x[0])===d.length,
  sol:`Pairs d · (${n}/d): ${d.filter(k=>k*k<=n).map(k=>k*k===n?`${k} · ${k}`:`${k} · ${n/k}`).join(', ')}\n${d.length} divisors${d.length%2?`, odd: ${n} is a square`:''}.`}}},
{ch:'ch1',t:'The division algorithm',gen(){const b=R(3,12),a=R(-150,150);const q=Math.floor(a/b),r=a-q*b;
  return {q:`Divide ${a} by ${b}: find q and r with ${a} = q · ${b} + r and 0 ≤ r < ${b}.`,f:[['q',''],['r','']],ok:x=>N(x[0])===q&&N(x[1])===r,
  sol:`${a} = ${q<0?'('+q+')':q} · ${b} + ${r}${a<0?'\n(For a negative number, go down to the next multiple of '+b+' so that r is not negative.)':''}`}}},
{ch:'ch1',t:'Is it a water weight?',gen(){const n=R(9,400);const yes=n%4===1;
  return {q:`Is ${n} a water weight in Mojadito (in the Book 9, 13, 17, …)? Type yes or no.`,f:[['yes or no','',1]],ok:x=>norm(x[0])===(yes?'yes':'no'),
  sol:`${n} = 4 · ${Math.floor(n/4)} + ${n%4}: remainder ${n%4}.\n`+(yes?`Yes. Each hydrogen weighs (${n} − 5)/2 = ${(n-5)/2}.`:`No: water weights leave remainder 1.`)}}},
{ch:'ch2',t:'gcd and lcm',gen(){const g=pick([1,2,3,4,6,5]);const a=g*R(2,15),b=g*R(2,15);
  return {q:`Find gcd(${a}, ${b}) and lcm(${a}, ${b}).`,f:[['gcd',''],['lcm','']],ok:x=>N(x[0])===gcd(a,b)&&N(x[1])===a*b/gcd(a,b),
  sol:`gcd(${a}, ${b}) = ${gcd(a,b)}\nlcm = ${a} · ${b} / ${gcd(a,b)} = ${a*b/gcd(a,b)}`}}},
{ch:'ch2',t:'Do the Books meet?',gen(){const d=R(2,12),e=R(2,12),s=R(1,12),t=R(1,12);const l=d*e/gcd(d,e);let first=null;
  for(let w=Math.max(s,t);w<Math.max(s,t)+l+1;w++)if(w>=s&&w>=t&&(w-s)%d===0&&(w-t)%e===0){first=w;break}
  return {q:`Books (start ${s}, step ${d}) and (start ${t}, step ${e}): type their first shared weight, or never.`,f:[['first shared weight or never','',1]],ok:x=>first===null?norm(x[0])==='never':N(x[0])===first,
  sol:`gcd(${d}, ${e}) = ${gcd(d,e)} and the starts differ by ${Math.abs(s-t)}.\n`+(first===null?`${gcd(d,e)} does not divide ${Math.abs(s-t)}: never (Theorem 2.3).`:`They meet at ${first}, then every lcm = ${l}: ${first}, ${first+l}, ${first+2*l}, …`)}}},
{ch:'ch3',t:"Euclid's algorithm",gen(){const g=pick([1,1,2,3,7,11,13]);let a=g*R(10,90),b=g*R(10,90);if(a<b)[a,b]=[b,a];if(a===b)a+=g;
  const [G,L]=euclidSteps(a,b);return {q:`Use Euclid's algorithm to find gcd(${a}, ${b}).`,f:[['gcd','']],ok:x=>N(x[0])===G,sol:L.join('\n')+`\ngcd = ${G}`}}},
{ch:'ch3',t:'Bézout coefficients',gen(){let a=R(20,300),b=R(20,300);if(a===b)b++;const [g,x,y]=egcd(a,b);
  return {q:`Find integers x and y with ${a}x + ${b}y = gcd(${a}, ${b}) = ${g}.`,f:[['x',''],['y','']],ok:v=>Number.isInteger(N(v[0]))&&Number.isInteger(N(v[1]))&&a*N(v[0])+b*N(v[1])===g,
  sol:euclidSteps(Math.max(a,b),Math.min(a,b))[1].join('\n')+`\nRun it backwards: ${a} · (${x}) + ${b} · (${y}) = ${g}.\nOther answers: x + ${b/g}t, y − ${a/g}t.`}}},
{ch:'ch4',t:'Nonnegative solutions',gen(){let a=R(2,9),b=R(2,11);while(gcd(a,b)>1)b++;const c=R(a*b,4*a*b);const sols=[];for(let y=0;y*b<=c;y++)if((c-y*b)%a===0)sols.push([(c-y*b)/a,y]);
  return {q:`How many solutions does ${a}x + ${b}y = ${c} have with x, y ≥ 0?`,f:[['how many','']],ok:v=>N(v[0])===sols.length,
  sol:sols.length?`The solutions: ${sols.map(([x,y])=>`(${x}, ${y})`).join(', ')}.\nConsecutive ones differ by (${b}, −${a}) (Theorem 4.2).`:'None.'}}},
{ch:'ch4',t:'The largest unpayable toll',gen(){let a=R(3,12),b=R(3,15);while(gcd(a,b)>1||a===b)b++;
  return {q:`With coins of ${a} and ${b} only, what is the largest toll you cannot pay?`,f:[['largest toll','']],ok:v=>N(v[0])===a*b-a-b,
  sol:`gcd(${a}, ${b}) = 1, so Corollary 4.4 gives ${a} · ${b} − ${a} − ${b} = ${a*b-a-b}.\nThere are (${a} − 1)(${b} − 1)/2 = ${(a-1)*(b-1)/2} unpayable tolls in all.`}}},
{ch:'ch5',t:'Smallest prime factor',gen(){const n=pick([R(100,999),R(100,999)*1,pick([7,11,13,17,19,23,29,31])*pick([11,13,17,19,23,29,31,37])]);const p=fac(n)[0][0];
  return {q:`What is the smallest prime factor of ${n}? (If ${n} is prime, type ${n}.)`,f:[['prime','']],ok:v=>N(v[0])===p,
  sol:`Test primes up to √${n} ≈ ${Math.sqrt(n).toFixed(1)}.\n`+(p===n?`None divides it: ${n} is prime.`:`${p} divides it: ${n} = ${p} · ${n/p}.`)}}},
{ch:'ch5',t:'Factor it',gen(){let n=1;const ps=[2,2,2,3,3,5,7,11,13];const k=R(3,5);for(let i=0;i<k;i++)n*=pick(ps);if(n<20)n*=pick([3,5,7]);const f=fac(n);
  return {q:`Factor ${n} into primes. Type it like 2^3 * 3 * 5 (or 2 2 2 3 5).`,f:[['factorization','',1]],ok:v=>{const t=norm(v[0]).replace(/[·×x]/g,'*');let prod=1;const parts=t.split(/[*\s]+/).filter(Boolean);if(!parts.length)return false;
    for(const p of parts){const m=p.match(/^(\d+)(?:\^(\d+))?$/);if(!m)return false;const b=+m[1],e=m[2]?+m[2]:1;if(!isP(b))return false;prod*=Math.pow(b,e)}return prod===n},
  sol:`${n} = ${fstr(f)}\nIt has ${f.reduce((a,[,e])=>a*(e+1),1)} divisors (Corollary 5.6).`}}}];

document.querySelectorAll('.skills').forEach(box=>{
  SK.filter(s=>s.ch===box.dataset.ch).forEach((s,si)=>{
    const id=s.ch+'-'+si,card=document.createElement('article');card.className='skill';card.setAttribute('aria-labelledby',id+'-h');
    card.innerHTML=`<h3 id="${id}-h">${s.t}</h3><p class="pq" aria-live="polite"></p><div class="flds"></div><div class="btns"><button class="primary ck">Check</button><button class="nw">New problem</button><button class="sh">Show solution</button></div><div class="fb" aria-live="polite"></div><div class="sol" hidden></div><div class="streak"></div>`;
    box.appendChild(card);let P=null,streak=0,shown=false;
    const $=sel=>card.querySelector(sel);
    const fresh=()=>{P=s.gen();shown=false;$('.pq').textContent=P.q;$('.flds').innerHTML=P.f.map(([l,,w],i)=>`<label>${l}<input class="${w?'wide':''}" id="${id}-i${i}" autocomplete="off"></label>`).join('');
      $('.fb').textContent='';$('.fb').className='fb';$('.sol').hidden=true;$('.sol').textContent='';
      card.querySelectorAll('input').forEach(i=>i.addEventListener('keydown',e=>{if(e.key==='Enter')check()}))};
    const check=()=>{const vals=[...card.querySelectorAll('.flds input')].map(i=>i.value);if(vals.some(v=>v.trim()==='')){$('.fb').className='fb';$('.fb').textContent='Fill in every box first.';return}
      if(P.ok(vals)){if(!shown)streak++;$('.fb').className='fb ok';$('.fb').textContent='✓ Correct! Press New problem for another.'}
      else{streak=0;$('.fb').className='fb no';$('.fb').textContent='✗ Not yet. Try again, or show the solution.'}
      $('.streak').textContent=streak?`Streak: ${streak}`+(streak>=5?' · ready for the next card':''):''};
    $('.ck').onclick=check;$('.nw').onclick=fresh;$('.sh').onclick=()=>{shown=true;$('.sol').hidden=false;$('.sol').textContent=P.sol};
    fresh()})});
})();
