/* Filters source-backed HTML; a search match does not confirm current intake. */
(() => {
  'use strict';
  const directory = document.querySelector('[data-verified-directory]');
  if (directory) {
    const input = directory.querySelector('#hub-search');
    const grade = directory.querySelector('#hub-grade');
    const status = directory.querySelector('#hub-search-result');
    const recovery = directory.querySelector('#hub-grade-all');
    const cards = [...directory.querySelectorAll('[data-verified-grades]')];
    const districts = [...directory.querySelectorAll('.subject-district')];
    const regions = [...directory.querySelectorAll('.region-block')];
    const grades = new Set(['고1', '고2', '고3']);
    const context = new Set(['고등', '고등수학', '고등수학학원', '고등학원', '수학', '수학학원', '학원']);
    const normalize = value => value.normalize('NFKC').toLocaleLowerCase('ko-KR').replace(/\s+/g, '');
    const tokens = value => value.normalize('NFKC').trim().split(/[\s,，·]+/u).filter(Boolean);
    const term = value => normalize(value).replace(/(?:고등수학학원|고등수학|수학학원)$/u, '');
    const records = cards.map(card => ({card, search: normalize(card.dataset.localSearch + ' ' + card.dataset.verifiedGrades)}));
    const syncUrl = () => {
      const url = new URL(location.href);
      const query = input.value.trim();
      if (query) url.searchParams.set('q', query); else url.searchParams.delete('q');
      if (grade.value) url.searchParams.set('grade', grade.value); else url.searchParams.delete('grade');
      history.replaceState(null, '', url.pathname + url.search + url.hash);
    };
    const apply = (updateUrl = true) => {
      const words = tokens(input.value);
      const terms = words.filter(word => !context.has(normalize(word))).map(term).filter(Boolean);
      let count = 0;
      for (const record of records) {
        const match = terms.every(word => record.search.includes(word)) && (!grade.value || record.card.dataset.verifiedGrades.split(',').includes(grade.value));
        record.card.hidden = !match;
        if (match) count++;
      }
      for (const district of districts) district.hidden = !cards.some(card => district.contains(card) && !card.hidden);
      for (const region of regions) region.hidden = !cards.some(card => region.contains(card) && !card.hidden);
      for (const anchor of directory.querySelectorAll('.region-jump a')) anchor.hidden = !!document.getElementById(anchor.hash.slice(1))?.hidden;
      recovery.hidden = count !== 0 || (!grade.value && !words.some(word => grades.has(normalize(word))));
      status.textContent = count ? `${count}개 동네 · 학년 표기는 수강 자료 기준이며 현재 모집 여부는 별도 확인이 필요합니다.` : '일치하는 수강 자료가 없습니다. 학년 조건을 풀거나 동네·지점 이름을 짧게 입력해 보세요.';
      if (updateUrl) syncUrl();
    };
    const readState = () => {
      const params = new URLSearchParams(location.search);
      input.value = (params.get('q') || '').replace(/[\u0000-\u001f\u007f]/g, '').slice(0, 80);
      grade.value = grades.has(params.get('grade')) ? params.get('grade') : '';
    };
    input.addEventListener('input', () => apply());
    grade.addEventListener('change', () => apply());
    directory.querySelector('#hub-search-reset').addEventListener('click', () => {
      input.value = ''; grade.value = ''; apply(); input.focus();
    });
    recovery.addEventListener('click', () => {
      input.value = tokens(input.value).filter(word => !grades.has(normalize(word))).join(' ');
      grade.value = ''; apply(); input.focus();
    });
    window.addEventListener('popstate', () => { readState(); apply(false); });
    readState();
    apply();
  }
  for (const root of document.querySelectorAll('[data-consultation-memo]')) {
    const textarea = root.querySelector('textarea');
    const status = root.querySelector('[role="status"]');
    const sms = root.querySelector('[data-memo-sms]');
    const update = () => { sms.href = 'sms:010-6839-8283?body=' + encodeURIComponent(textarea.value); };
    textarea.addEventListener('input', () => { update(); status.textContent = ''; });
    root.querySelector('[data-memo-copy]').addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(textarea.value);
        status.textContent = '문의 메모를 복사했습니다. 상담할 때 붙여 넣어 주세요.';
      } catch {
        textarea.focus(); textarea.select();
        status.textContent = '메모를 선택했습니다. 기기의 복사 기능을 이용해 주세요.';
      }
    });
    update();
  }
})();
