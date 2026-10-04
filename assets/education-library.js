(() => {
  'use strict';
  const data = window.ondamEducationLinkData;
  const params = new URLSearchParams(location.search);
  const centers = data?.centers || [];
  const centerByKey = new Map(centers.map(c => [c.key, c]));
  const areaByName = new Map((data?.areas || []).map(a => [a.name, a]));
  let contextCenter = centerByKey.get(params.get('center'));
  let contextArea = areaByName.get(params.get('area'));
  if (contextCenter && contextArea && contextArea.center !== (contextCenter.base || contextCenter.key)) contextArea = undefined;
  if (!contextCenter && contextArea) contextCenter = centerByKey.get(contextArea.center);
  function contextLinks() {
    document.querySelectorAll('a[data-education-article]').forEach(a => {
      const url = new URL(a.dataset.educationArticle, location.origin);
      if (contextCenter) url.searchParams.set('center', contextCenter.key);
      if (contextArea) url.searchParams.set('area', contextArea.name);
      a.href = url.pathname + url.search;
    });
  }
  contextLinks();
  const form = document.querySelector('[data-education-filter]');
  if (form) {
    const query = form.querySelector('#education-search');
    const category = form.querySelector('#education-category');
    const type = form.querySelector('#education-type');
    const reset = form.querySelector('[data-education-reset]');
    const cards = Array.from(document.querySelectorAll('[data-education-card]'));
    const count = document.querySelector('#education-results');
    const empty = document.querySelector('#education-empty');
    [query, category, type, reset].forEach(e => e.disabled = false);
    const normalize = s => s.normalize('NFKC').toLocaleLowerCase('ko-KR');
    const validOption = (select, value) => Array.from(select.options).some(o => o.value === value) ? value : '';
    function restore() {
      const p = new URLSearchParams(location.search);
      query.value = p.get('q') || '';
      category.value = validOption(category, p.get('category'));
      type.value = validOption(type, p.get('type'));
    }
    function filter(updateUrl) {
      const terms = normalize(query.value).trim().split(/\s+/).filter(Boolean);
      let visible = 0;
      cards.forEach(c => {
        const match = (!category.value || c.dataset.category === category.value) && (!type.value || c.dataset.type === type.value) && terms.every(t => normalize(c.dataset.search).includes(t));
        c.hidden = !match;
        if (match) visible++;
      });
      count.textContent = `${cards.length}편 중 ${visible}편을 보고 있습니다.`;
      empty.hidden = visible !== 0;
      if (updateUrl) {
        const u = new URL(location.href);
        [['q', query.value.trim()], ['category', category.value], ['type', type.value]].forEach(([k, v]) => v ? u.searchParams.set(k, v) : u.searchParams.delete(k));
        history.replaceState(null, '', u.pathname + u.search + u.hash);
      }
    }
    restore(); filter(false);
    form.addEventListener('submit', e => { e.preventDefault(); filter(true); });
    query.addEventListener('input', () => filter(true));
    [category, type].forEach(s => s.addEventListener('change', () => filter(true)));
    reset.addEventListener('click', () => { query.value = ''; category.value = ''; type.value = ''; filter(true); query.focus(); });
    addEventListener('popstate', () => { restore(); filter(false); });
  }
  const picker = document.querySelector('[data-education-local]');
  if (picker && centers.length) {
    const region = picker.querySelector('#education-region');
    const center = picker.querySelector('#education-center');
    const area = picker.querySelector('#education-area');
    const branchLink = picker.querySelector('[data-local-branch]');
    const areaLink = picker.querySelector('[data-local-area]');
    const status = picker.querySelector('[data-local-status]');
    [region, center, area].forEach(e => e.disabled = false);
    function options(select, placeholder, rows) {
      select.replaceChildren(new Option(placeholder, ''), ...rows.map(r => new Option(r.label, r.key)));
    }
    options(region, '지역 전체', [...new Set(centers.map(c => c.region))].sort((a,b) => a.localeCompare(b,'ko')).map(r => ({label:r,key:r})));
    function centerOptions() {
      options(center, '지점을 선택하세요', centers.filter(c => !region.value || c.region === region.value).map(c => ({label:`${c.name} · ${c.district}`,key:c.key})));
    }
    function areaOptions() {
      const c = centerByKey.get(center.value);
      options(area, c ? '연결된 동네를 선택하세요' : '지점을 먼저 선택하세요', c ? data.areas.filter(a => a.center === (c.base || c.key)).map(a => ({label:a.name,key:a.name})) : []);
      area.disabled = !c || area.options.length < 2;
    }
    function update(replaceUrl) {
      contextCenter = centerByKey.get(center.value);
      contextArea = areaByName.get(area.value);
      branchLink.href = contextCenter?.path || data.branchHub;
      branchLink.textContent = contextCenter ? `${contextCenter.name} 지점 안내` : '전체 지점 찾기';
      areaLink.href = contextArea?.path || data.areaHub;
      areaLink.textContent = contextArea ? `${contextArea.name} 동네 안내` : '전체 동네 찾기';
      status.textContent = contextCenter ? `${contextCenter.region} ${contextCenter.district} · ${contextCenter.name}${contextArea ? ' · ' + contextArea.name : ''} 안내로 연결합니다.` : '지역과 지점을 고르면 해당 안내 페이지로 이동할 수 있습니다.';
      contextLinks();
      if (replaceUrl) {
        const u = new URL(location.href);
        [['center',contextCenter?.key],['area',contextArea?.name]].forEach(([k,v]) => v ? u.searchParams.set(k,v) : u.searchParams.delete(k));
        history.replaceState(null,'',u.pathname+u.search+u.hash);
      }
    }
    function restorePicker() {
      const p = new URLSearchParams(location.search);
      const c = centerByKey.get(p.get('center'));
      const a = areaByName.get(p.get('area'));
      const chosen = c || (a && centerByKey.get(a.center));
      region.value = chosen?.region || ''; centerOptions(); center.value = chosen?.key || ''; areaOptions();
      area.value = a && chosen && a.center === (chosen.base || chosen.key) ? a.name : '';
      update(false);
    }
    restorePicker();
    region.addEventListener('change', () => { centerOptions(); areaOptions(); update(true); });
    center.addEventListener('change', () => { areaOptions(); update(true); });
    area.addEventListener('change', () => update(true));
    addEventListener('popstate', restorePicker);
  }
})();
