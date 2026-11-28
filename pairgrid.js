/* Picture proof: pair the dots of a W × H grid (Modular Worlds, Chapter 0). */
(function(){
const root=document.getElementById('pairgrid');if(!root)return;
const $=s=>root.querySelector(s);let CELL=40;
let W=5,H=3,pairs=[],sel=null,auto=null,focus=[0,0];
const key=(r,c)=>r+','+c;
const partner=()=>{const m=new Map();pairs.forEach(([a,b])=>{m.set(key(...a),b);m.set(key(...b),a)});return m};
function freeLeft(){const m=partner();let n=0;for(let r=0;r<H;r++)for(let c=0;c<W;c++)if(!m.has(key(r,c)))n++;return n}
function canMore(){const m=partner();for(let r=0;r<H;r++)for(let c=0;c<W;c++){if(m.has(key(r,c)))continue;if(c+1<W&&!m.has(key(r,c+1)))return true;if(r+1<H&&!m.has(key(r+1,c)))return true}return false}
function draw(msg){
  $('#pgW').textContent=W;$('#pgH').textContent=H;
  const m=partner(),done=!canMore();
  CELL=Math.max(28,Math.min(40,Math.floor((root.clientWidth-16)/W)));const g=$('.pg-grid');g.style.gridTemplateColumns=`repeat(${W},${CELL}px)`;g.style.setProperty('--cell',CELL+'px');
  let h='';for(let r=0;r<H;r++)for(let c=0;c<W;c++){const k=key(r,c),on=m.has(k),isSel=sel&&sel[0]===r&&sel[1]===c,left=done&&!on;
    h+=`<button data-r="${r}" data-c="${c}" class="${on?'on':''}${isSel?' sel':''}${left?' left':''}" tabindex="${r===focus[0]&&c===focus[1]?0:-1}" aria-label="Row ${r+1}, column ${c+1}: ${on?'paired':left?'left over':isSel?'selected':'free'}"></button>`}
  g.innerHTML=h;
  const svg=$('.pg-svg');svg.setAttribute('width',W*CELL);svg.setAttribute('height',H*CELL);
  svg.innerHTML=pairs.map(([a,b])=>`<line x1="${a[1]*CELL+CELL/2}" y1="${a[0]*CELL+CELL/2}" x2="${b[1]*CELL+CELL/2}" y2="${b[0]*CELL+CELL/2}" style="stroke:var(--sea);stroke-width:5;stroke-linecap:round"/>`).join('');
  const L=freeLeft();$('.pg-count').textContent=`${W} × ${H} = ${W*H} dots · ${pairs.length} pair${pairs.length===1?'':'s'} · ${L} free`;
  if(msg!==undefined)$('.pg-msg').textContent=msg;
  else if(done&&!auto){const bothOdd=W%2&&H%2;
    $('.pg-msg').textContent=L===0?`No dot left: ${W} × ${H} is all pairs.${bothOdd?'':' One side is even, so that always works.'}`:
      bothOdd&&L===1?`No more pairs fit, and exactly one dot is left. Try a different pairing: can you ever leave none?`:
      `No more pairs fit, with ${L} left. There is a better pairing: undo or clear and try again, or press "Show me a way".`}
}
window.addEventListener('resize',()=>draw(''+$('.pg-msg').textContent));
function setSize(w,h){W=Math.max(1,Math.min(9,w));H=Math.max(1,Math.min(7,h));pairs=[];sel=null;auto=null;focus=[0,0];$('#pgAuto').textContent='Show me a way';
  draw(`Click two neighbouring dots to bond them into a pair. Leave as few dots as you can.`)}
function pick(r,c,fromKey){auto=null;$('#pgAuto').textContent='Show me a way';const m=partner(),k=key(r,c);
  if(m.has(k)){const p=m.get(k);pairs=pairs.filter(([a,b])=>!((a[0]===r&&a[1]===c)||(b[0]===r&&b[1]===c)));sel=null;draw('Pair undone.');return}
  if(!sel){sel=[r,c];draw('Now click a neighbour of the gold dot: left, right, above or below.');return}
  if(sel[0]===r&&sel[1]===c){sel=null;draw('Selection cleared.');return}
  if(Math.abs(sel[0]-r)+Math.abs(sel[1]-c)!==1){sel=[r,c];draw('Those two are not neighbours. Starting again from this dot.');return}
  pairs.push([sel,[r,c]]);sel=null;draw()}
$('.pg-grid').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;focus=[+b.dataset.r,+b.dataset.c];pick(focus[0],focus[1]);
  const nb=root.querySelector(`.pg-grid button[data-r="${focus[0]}"][data-c="${focus[1]}"]`);if(nb&&e.detail===0)nb.focus()});
$('.pg-grid').addEventListener('keydown',e=>{const d={ArrowUp:[-1,0],ArrowDown:[1,0],ArrowLeft:[0,-1],ArrowRight:[0,1]}[e.key];if(!d)return;e.preventDefault();
  focus=[Math.max(0,Math.min(H-1,focus[0]+d[0])),Math.max(0,Math.min(W-1,focus[1]+d[1]))];
  root.querySelectorAll('.pg-grid button').forEach(b=>b.tabIndex=-1);const nb=root.querySelector(`.pg-grid button[data-r="${focus[0]}"][data-c="${focus[1]}"]`);nb.tabIndex=0;nb.focus()});
$('#pgWm').onclick=()=>setSize(W-1,H);$('#pgWp').onclick=()=>setSize(W+1,H);$('#pgHm').onclick=()=>setSize(W,H-1);$('#pgHp').onclick=()=>setSize(W,H+1);
$('#pgUndo').onclick=()=>{auto=null;$('#pgAuto').textContent='Show me a way';if(pairs.length){pairs.pop();sel=null;draw('Last pair undone.')}else draw('Nothing to undo.')};
$('#pgClear').onclick=()=>setSize(W,H);
/* automatic pairing in steps, with the algebra */
$('#pgAuto').onclick=()=>{
  if(!auto){pairs=[];sel=null;auto={step:0}}
  const cols=W%2?W-1:W,rows=H%2?H-1:H;auto.step++;
  if(auto.step===1){for(let r=0;r<H;r++)for(let c=0;c+1<cols;c+=2)pairs.push([[r,c],[r,c+1]]);
    draw(cols===0?`The width is 1, so there are no columns to pair across.`:`Step 1. The first ${cols} column${cols>1?'s':''} (an even number) pair up across every row: ${cols} × ${H} = ${cols*H} dots in ${cols*H/2} pairs.`);
    if(W%2===0){$('.pg-msg').textContent+=`\nThe width is even, so that is every dot: ${W} × ${H} is all pairs.`;auto=null;$('#pgAuto').textContent='Show me a way';return}
    $('#pgAuto').textContent='Next step';return}
  if(auto.step===2){for(let r=0;r+1<rows;r+=2)pairs.push([[r,W-1],[r+1,W-1]]);
    draw(`Step 2. The last column has ${H} dot${H>1?'s':''}. ${rows} of them pair up from the top.`+(H%2?'':' The height is even, so the column is all pairs.'));
    if(H%2===0){$('.pg-msg').textContent+=`\nSo ${W} × ${H} is all pairs.`;auto=null;$('#pgAuto').textContent='Show me a way';return}return}
  if(auto.step===3){const k=(W-1)/2,m=(H-1)/2;
    draw(`Step 3. One dot is left over.\n${W} × ${H} = ${W-1}·${H} + ${H-1} + 1 = ${(W-1)*H} + ${H-1} + 1.\nIn letters: (2k + 1)(2m + 1) = 2k(2m + 1) + 2m + 1, which is pairs plus one: odd.`);
    root.querySelectorAll('.pg-grid button').forEach(b=>{if(+b.dataset.r===H-1&&+b.dataset.c===W-1){b.classList.add('left');b.setAttribute('aria-label',`Row ${H}, column ${W}: left over`)}});
    auto=null;$('#pgAuto').textContent='Show me a way'}};
setSize(5,3);
})();
