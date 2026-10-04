(() => {
  'use strict';
  const form = document.querySelector('[data-curriculum-filter]');
  if (!form) return;
  const fields = ['stage', 'grade', 'subject', 'q'].map(k => form.querySelector('#curriculum-' + k));
  const [stage, grade, subject, query] = fields;
  const reset = form.querySelector('[data-curriculum-reset]');
  const cards = [...document.querySelectorAll('[data-curriculum-card]')];
  const status = document.querySelector('#curriculum-results');
  const empty = document.querySelector('#curriculum-empty');
  fields.concat(reset).forEach(e => e.disabled = false);
  const normalize = s => s.normalize('NFKC').toLocaleLowerCase('ko-KR');
  const valid = (field, value) => [...field.options].some(o => o.value === value) ? value : '';
  function restore() {
    const p = new URLSearchParams(location.search);
    [stage,grade,subject].forEach(f => f.value = valid(f, p.get(f.name)));
    query.value = p.get('q') || '';
  }
  function filter(update) {
    const terms = normalize(query.value).trim().split(/\s+/).filter(Boolean);
    let n = 0;
    cards.forEach(c => {
      const match = (!stage.value || c.dataset.stage === stage.value) && (!grade.value || c.dataset.grade === grade.value) && (!subject.value || c.dataset.subject === subject.value) && terms.every(t => normalize(c.dataset.search).includes(t));
      c.hidden = !match;
      if (match) n++;
    });
    status.textContent = `학년·과목 안내 66개 중 ${n}개를 보고 있습니다.`;
    empty.hidden = n !== 0;
    if (update) {
      const u = new URL(location.href);
      fields.forEach(f => f.value.trim() ? u.searchParams.set(f.name,f.value.trim()) : u.searchParams.delete(f.name));
      history.replaceState(null,'',u.pathname+u.search+u.hash);
    }
  }
  stage.addEventListener('change', () => { if (grade.value && !cards.some(c => (!stage.value || c.dataset.stage===stage.value) && c.dataset.grade===grade.value)) grade.value='';filter(true); });
  grade.addEventListener('change', () => { if (grade.value) stage.value=cards.find(c=>c.dataset.grade===grade.value).dataset.stage;filter(true); });
  subject.addEventListener('change', () => filter(true));
  query.addEventListener('input', () => filter(true));
  reset.addEventListener('click', () => { fields.forEach(f=>f.value='');filter(true);query.focus(); });
  form.addEventListener('submit',e=>{e.preventDefault();filter(true);});
  addEventListener('popstate',()=>{restore();filter(false);});
  restore();filter(false);
})();
