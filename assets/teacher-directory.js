(() => {
  'use strict';
  const root = document.querySelector('[data-teacher-search]');
  if (!root) return;
  const form = root.querySelector('[data-teacher-filter]');
  const select = form.querySelector('select');
  const query = form.querySelector('input[type="search"]');
  const cards = Array.from(root.querySelectorAll('[data-teacher-card]'));
  const count = root.querySelector('[data-teacher-count]');
  const empty = root.querySelector('[data-teacher-empty]');
  const kind = root.dataset.teacherSearch;
  const key = kind === 'branches' ? 'region' : 'topic';
  const normalize = value => String(value).normalize('NFKC').toLocaleLowerCase('ko-KR').replace(/[\s*·()＋+]+/g, '');
  const tokenList = value => String(value).trim().split(/\s+/).map(normalize).filter(Boolean);
  const totalProfiles = cards.reduce((sum, card) => sum + Number(card.dataset.profileCount || 1), 0);
  const searchable = new Map(cards.map(card => [card, normalize(card.dataset.search || '')]));
  function apply(writeUrl) {
    const tokens = tokenList(query.value.slice(0, 100));
    let visible = 0;
    let profiles = 0;
    cards.forEach(card => {
      const selected = !select.value || (kind === 'branches' ? card.dataset.region === select.value : (card.dataset.topics || '').split('|').includes(select.value));
      const matches = selected && tokens.every(token => searchable.get(card).includes(token));
      card.hidden = !matches;
      if (matches) { visible++; profiles += Number(card.dataset.profileCount || 1); }
      card.querySelectorAll('[data-teacher-name]').forEach(link => {
        link.classList.toggle('td-match', tokens.length > 0 && tokens.every(token => normalize(link.dataset.teacherName).includes(token)));
      });
    });
    count.textContent = kind === 'branches' ? `${visible}개 지점 묶음의 교사 소개 ${profiles.toLocaleString('ko-KR')}건을 볼 수 있습니다.` : `교사 소개 ${visible}건을 볼 수 있습니다.`;
    empty.hidden = visible !== 0;
    if (writeUrl) {
      const url = new URL(window.location.href);
      if (select.value) url.searchParams.set(key, select.value); else url.searchParams.delete(key);
      if (query.value.trim()) url.searchParams.set('q', query.value.trim().slice(0, 100)); else url.searchParams.delete('q');
      try { window.history.replaceState(null, '', url); } catch (_) { /* Reading and filtering remain available. */ }
    }
  }
  function restore() {
    const url = new URL(window.location.href);
    const value = url.searchParams.get(key) || '';
    select.value = Array.from(select.options).some(option => option.value === value) ? value : '';
    query.value = (url.searchParams.get('q') || '').slice(0, 100);
    apply(false);
  }
  form.querySelectorAll('input,select,button').forEach(control => { control.disabled = false; });
  form.addEventListener('submit', event => { event.preventDefault(); apply(true); });
  select.addEventListener('change', () => apply(true));
  query.addEventListener('input', () => apply(true));
  form.addEventListener('reset', () => { select.value = ''; query.value = ''; apply(true); });
  root.querySelector('[data-teacher-reset]').addEventListener('click', () => form.reset());
  window.addEventListener('popstate', restore);
  window.addEventListener('pageshow', restore);
  restore();
})();
