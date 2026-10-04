/* Progressive enhancement: all guides and article content remain available without JS. */
(() => {
  'use strict';
  const library = document.querySelector('[data-guide-library]');
  if (library) {
    const form = library.querySelector('[data-guide-filter]');
    const stage = form.elements.stage;
    const category = form.elements.category;
    const query = form.elements.q;
    const cards = [...library.querySelectorAll('[data-guide-card]')];
    const sections = [...library.querySelectorAll('[data-guide-category]')];
    const result = library.querySelector('[data-guide-result]');
    const empty = library.querySelector('[data-guide-empty]');
    const valid = (select, value) => [...select.options].some(o => o.value === value) ? value : '';
    const normalize = value => value.toLocaleLowerCase('ko-KR').replace(/\s+/g, ' ').trim();
    function readUrl() {
      const params = new URL(location.href).searchParams;
      stage.value = valid(stage, params.get('stage') || '');
      category.value = valid(category, params.get('category') || '');
      query.value = (params.get('q') || '').slice(0, 100);
    }
    function update(writeUrl = true) {
      const words = normalize(query.value).split(' ').filter(Boolean);
      let count = 0;
      for (const card of cards) {
        const haystack = normalize(card.dataset.search);
        const show = (!stage.value || card.dataset.stages.split(' ').includes(stage.value)) &&
          (!category.value || card.dataset.category === category.value) && words.every(word => haystack.includes(word));
        card.hidden = !show;
        if (show) count++;
      }
      for (const section of sections) {
        const visible = [...section.querySelectorAll('[data-guide-card]')].filter(card => !card.hidden).length;
        section.hidden = visible === 0;
        section.querySelector('[data-category-count]').textContent = `${visible}편`;
      }
      for (const link of library.querySelectorAll('.lg-category-jumps a')) {
        const section = document.getElementById(link.hash.slice(1));
        link.hidden = section.hidden;
      }
      result.textContent = `${count}편의 실천 가이드를 볼 수 있습니다.`;
      empty.hidden = count !== 0;
      if (writeUrl) {
        const next = new URL(location.href);
        for (const [key, value] of [['stage', stage.value], ['category', category.value], ['q', query.value.trim()]]) {
          if (value) next.searchParams.set(key, value); else next.searchParams.delete(key);
        }
        history.replaceState(null, '', next);
      }
    }
    for (const control of form.elements) control.disabled = false;
    form.addEventListener('submit', event => { event.preventDefault(); update(); });
    form.addEventListener('input', () => update());
    form.addEventListener('change', () => update());
    form.addEventListener('reset', event => {
      event.preventDefault();
      stage.value = ''; category.value = ''; query.value = '';
      update();
    });
    library.querySelector('[data-guide-reset]').addEventListener('click', () => { form.reset(); query.focus(); });
    window.addEventListener('popstate', () => { readUrl(); update(false); });
    readUrl(); update(false);
  }
  for (const form of document.querySelectorAll('[data-guide-record]')) {
    const fields = [...form.querySelectorAll('textarea')];
    const status = form.querySelector('[data-record-status]');
    const title = form.dataset.guideTitle;
    let printState = null;
    function textRecord(blank) {
      const lines = [title, '온담학습 · 내 과제로 확인하는 실천 기록', location.href.split('#')[0], ''];
      for (const field of fields) {
        lines.push(field.parentElement.firstChild.textContent.trim(), blank ? '' : field.value, '');
      }
      return lines.join('\r\n');
    }
    function download(blank) {
      const blob = new Blob(['\ufeff', textRecord(blank)], { type: 'text/plain;charset=utf-8' });
      const href = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = href;
      link.download = `${form.dataset.guideSlug}-${blank ? '빈양식' : '실천기록'}.txt`;
      document.body.append(link); link.click(); link.remove();
      setTimeout(() => URL.revokeObjectURL(href), 1000);
      status.textContent = blank ? '빈 기록 양식의 내려받기를 시작했습니다.' : '작성한 메모의 내려받기를 시작했습니다.';
    }
    function clearPrint() { form.querySelectorAll('.lg-print-record').forEach(el => el.remove()); }
    function preparePrint() {
      clearPrint();
      if (!printState) {
        printState = [...document.querySelectorAll('main details')].map(detail => ({ detail, open: detail.open }));
        printState.forEach(({ detail }) => { detail.open = true; });
      }
      for (const field of fields) {
        const mirror = document.createElement('div');
        mirror.className = 'lg-print-record';
        mirror.textContent = field.value || '(직접 기록해 보세요)';
        field.after(mirror);
      }
    }
    function finishPrint() {
      clearPrint();
      if (printState) printState.forEach(({ detail, open }) => { detail.open = open; });
      printState = null;
    }
    form.addEventListener('submit', event => event.preventDefault());
    form.addEventListener('reset', () => { status.textContent = '화면의 메모를 지웠습니다.'; clearPrint(); });
    form.querySelector('[data-record-download]').addEventListener('click', () => download(false));
    form.querySelector('[data-record-blank]').addEventListener('click', () => download(true));
    form.querySelector('[data-record-print]').addEventListener('click', () => { preparePrint(); window.print(); });
    window.addEventListener('beforeprint', preparePrint);
    window.addEventListener('afterprint', finishPrint);
    for (const button of form.querySelectorAll('button[disabled]')) button.disabled = false;
  }
})();
