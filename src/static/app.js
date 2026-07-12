// Auto-dismiss flash messages
setTimeout(() => {
  document.querySelectorAll('.flash').forEach(el => {
    el.style.transition = 'opacity .5s';
    el.style.opacity = '0';
    setTimeout(() => el.remove(), 500);
  });
}, 3000);

// Modal helpers
function openModal(id) {
  document.getElementById(id).classList.add('open');
}
function closeModal(id) {
  document.getElementById(id).classList.remove('open');
}
document.addEventListener('keydown', e => {
  if (e.key === 'Escape')
    document.querySelectorAll('.modal-overlay.open').forEach(m => m.classList.remove('open'));
});

// Number formatter
function fmtNum(n) {
  return Number(n).toLocaleString('th-TH');
}

// Budget inline: auto-calculate annual when monthly changes
document.addEventListener('input', e => {
  if (e.target.matches('[data-monthly]')) {
    const id = e.target.dataset.monthly;
    const annualEl = document.querySelector(`[data-annual="${id}"]`);
    if (annualEl) annualEl.textContent = fmtNum((parseFloat(e.target.value) || 0) * 12);
    updatePct(id);
  }
  if (e.target.matches('[data-actual]')) {
    updatePct(e.target.dataset.actual);
  }
});

function updatePct(id) {
  const monthly = parseFloat(document.querySelector(`[data-monthly="${id}"]`)?.value) || 0;
  const actual  = parseFloat(document.querySelector(`[data-actual="${id}"]`)?.value) || 0;
  const annual  = monthly * 12;
  const pct     = annual ? Math.round(actual / annual * 100) : 0;
  const pctEl   = document.querySelector(`[data-pct="${id}"]`);
  const barEl   = document.querySelector(`[data-bar="${id}"]`);
  if (pctEl) pctEl.textContent = pct + '%';
  if (barEl) {
    barEl.style.width = Math.min(pct, 100) + '%';
    barEl.className = 'prog-bar ' + (pct > 100 ? 'red' : pct > 80 ? 'gold' : 'green');
  }
}

// Monthly log: auto-calc savings rate on input
function calcSavingsRate() {
  const income   = parseFloat(document.getElementById('income')?.value) || 0;
  const expenses = parseFloat(document.getElementById('expenses')?.value) || 0;
  const rateEl   = document.getElementById('savings_rate_display');
  if (rateEl && income) {
    const rate = ((income - expenses) / income * 100).toFixed(1);
    rateEl.textContent = rate + '%';
    rateEl.className = 'font-bold ' + (rate >= 20 ? 'text-green' : rate >= 10 ? 'text-gold' : 'text-accent');
  }
}
