/* Modular Worlds web book: shared helpers (prophecy cards, Python cells, small math). */
window.MW = (() => {
  const $ = s => document.querySelector(s);
  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a; };
  const lcm = (a, b) => Math.abs(a * b) / gcd(a, b);
  function egcd(a, b) { if (b === 0) return [a, 1, 0]; const [g, x, y] = egcd(b, a % b); return [g, y, x - Math.floor(a / b) * y]; }
  const mod = (a, m) => ((a % m) + m) % m;

  function store(key) {
    let data = {};
    try { data = JSON.parse(localStorage.getItem(key) || '{}'); } catch (e) {}
    return { data, save() { try { localStorage.setItem(key, JSON.stringify(data)); } catch (e) {} } };
  }

  /* Prophecy cards: list of {id, t (text), s (where it is settled)} */
  const OPTS = ['100% sure it’s true', 'I think it’s true', 'I think it will break'];
  function cards(el, list, key, label) {
    const st = store(key);
    el.innerHTML = list.map((p, i) => `<div class="card"><div class="tag">${esc(label ? label(i, p) : 'Prophecy ' + (i + 1))}</div><p>${esc(p.t)}</p>
      <fieldset><legend class="small">How sure is your crew?</legend>${OPTS.map((o, j) => `<label><input type="radio" name="${esc(p.id)}" value="${j}" ${st.data[p.id] == j ? 'checked' : ''}> ${esc(o)}</label>`).join('')}</fieldset>
      <div class="settle">${esc(p.s)}</div></div>`).join('');
    el.addEventListener('change', e => { if (e.target.name) { st.data[e.target.name] = e.target.value; st.save(); } });
  }

  /* Python cells (Pyodide, loaded on first Run). list of {t (title), c (code)}; setup: code run once before any cell. */
  let py = null, loading = null;
  async function getPy(status) {
    if (py) return py;
    if (!loading) {
      if (status) status.textContent = 'Loading Python…';
      loading = (async () => {
        for (let i = 0; i < 50 && !window.loadPyodide; i++) await new Promise(r => setTimeout(r, 200));
        if (!window.loadPyodide) throw new Error('Python could not load. Check your connection and try again.');
        py = await window.loadPyodide();
        if (status) status.textContent = 'Python is ready.';
        return py;
      })().catch(err => { loading = null; throw err; });
    }
    return loading;
  }
  function cells(el, list, opts = {}) {
    const status = opts.status || null;
    el.innerHTML = list.map((c, i) => `<div class="cell"><div class="bar"><b>${esc(c.t)}</b><span class="row"><button class="primary" data-run="${i}">Run</button><button data-reset="${i}">Reset</button></span></div>
      <textarea id="${el.id}-c${i}" spellcheck="false" aria-label="${esc(c.t)}, Python code">${esc(c.c)}</textarea><pre id="${el.id}-o${i}" aria-live="polite"></pre></div>`).join('');
    let setupDone = false;
    el.addEventListener('click', async e => {
      const b = e.target.closest('button'); if (!b) return;
      if (b.dataset.reset !== undefined) { const i = +b.dataset.reset; $(`#${el.id}-c${i}`).value = list[i].c; $(`#${el.id}-o${i}`).textContent = ''; return; }
      if (b.dataset.run === undefined) return;
      const i = +b.dataset.run, out = $(`#${el.id}-o${i}`);
      out.className = ''; out.textContent = 'Running…';
      try {
        const p = await getPy(status);
        let buf = '';
        p.setStdout({ batched: s => { buf += s + '\n'; } });
        p.setStderr({ batched: s => { buf += s + '\n'; } });
        if (opts.setup && !setupDone) { await p.runPythonAsync(opts.setup); setupDone = true; }
        await p.runPythonAsync($(`#${el.id}-c${i}`).value);
        out.textContent = buf || '(no output)';
      } catch (err) {
        out.className = 'err';
        out.textContent = String(err.message || err).split('\n').slice(-6).join('\n');
      }
    });
  }

  /* Redraw hooks when the theme changes */
  function onTheme(fn) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', fn);
    new MutationObserver(fn).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  }

  return { $, esc, css, gcd, lcm, egcd, mod, store, cards, cells, onTheme };
})();
