/* Only filters existing HTML and prepares a user-initiated consultation memo. */
(() => {
  'use strict';
  const directory = document.querySelector('[data-verified-directory]');
  if (directory) {
    const input = directory.querySelector('#hub-search');
    const grade = directory.querySelector('#hub-grade');
    const status = directory.querySelector('#hub-search-result');
    const cards = [...directory.querySelectorAll('[data-verified-grades]')];
    const districts = [...directory.querySelectorAll('.subject-district')];
    const regions = [...directory.querySelectorAll('.region-block')];
    const normalize = value => value.normalize('NFKC').toLocaleLowerCase('ko-KR').replace(/\s+/g, '');
    const records = cards.map(card => ({card, search: normalize(card.dataset.localSearch)}));
    const apply = () => {
      const terms = input.value.trim().split(/\s+/).filter(Boolean).map(normalize);
      let count = 0;
      for (const record of records) {
        const match = terms.every(term => record.search.includes(term)) && (!grade.value || record.card.dataset.verifiedGrades.split(',').includes(grade.value));
        record.card.hidden = !match;
        if (match) count++;
      }
      for (const district of districts) district.hidden = !cards.some(card => district.contains(card) && !card.hidden);
      for (const region of regions) region.hidden = !cards.some(card => region.contains(card) && !card.hidden);
      for (const anchor of directory.querySelectorAll('.region-jump a')) anchor.hidden = !!document.getElementById(anchor.hash.slice(1))?.hidden;
      status.textContent = count ? `${count}개 동네 · 학년 표기는 수강 자료 기준이며 현재 모집 여부는 별도 확인이 필요합니다.` : '일치하는 수강 자료가 없습니다. 학년 필터를 전체로 바꾸거나 지역 이름을 짧게 입력해 보세요.';
    };
    const params = new URLSearchParams(location.search);
    input.value = params.get('q') || '';
    grade.value = ['고1', '고2', '고3'].includes(params.get('grade')) ? params.get('grade') : '';
    input.addEventListener('input', apply);
    grade.addEventListener('change', apply);
    directory.querySelector('#hub-search-reset').addEventListener('click', () => { input.value = ''; grade.value = ''; apply(); input.focus(); });
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
