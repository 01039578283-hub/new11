/* Builds a memo on this page. It neither saves nor sends entered information. */
(() => {
  'use strict';
  for (const root of document.querySelectorAll('[data-memo-builder]')) {
    const controls = root.querySelector('[data-memo-fields]');
    const textarea = root.querySelector('textarea');
    const sms = root.querySelector('[data-memo-sms]');
    const status = root.querySelector('[role="status"]');
    if (!controls || !textarea || !sms || !status) continue;
    controls.hidden = false;
    const field = name => controls.querySelector(`[data-memo-field="${name}"]`).value.trim();
    controls.querySelector('[data-memo-apply]').addEventListener('click', () => {
      textarea.value = [
        '온담학습 지점 수강 상담을 문의합니다.',
        `희망 지역·지점: ${field('region') || '(상담에서 확인)'}`,
        `학생 학년: ${field('grade') || '(상담에서 확인)'}`,
        `희망 과목: ${field('subject') || '(상담에서 확인)'}`,
        `등원 가능한 요일·시간: ${field('availability') || '(상담에서 확인)'}`,
        '확인할 내용: 실제 수업 지점과 주소, 수강 학년, 수업 요일·시간, 교습비·교재비, 상담·진단 방식',
        '현재 학습 고민: '
      ].join('\n');
      sms.href = 'sms:010-6839-8283?body=' + encodeURIComponent(textarea.value);
      status.textContent = '입력한 내용으로 메모를 만들었습니다. 아래에서 내용을 더 수정할 수 있습니다.';
      textarea.focus();
    });
  }
})();
