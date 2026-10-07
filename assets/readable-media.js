/* Native image URLs remain useful when this optional enhancement is unavailable. */
(()=>{
 if(typeof HTMLDialogElement==='undefined')return;
 let dialog,frame,full,heading,toggle,origin;
 function create(){
  dialog=document.createElement('dialog');dialog.className='od-media-dialog';dialog.setAttribute('aria-labelledby','od-media-heading');
  dialog.innerHTML='<div class="od-media-toolbar"><h2 id="od-media-heading"></h2><button type="button" data-media-size>원본 크기</button><button type="button" data-media-close>닫기</button></div><p class="od-media-help">작은 글씨는 원본 크기로 확인하세요. 확대 후 좌우·위아래로 이동할 수 있습니다.</p><div class="od-media-viewport is-fit" tabindex="0" role="region" aria-label="확대한 이미지 이동 영역"><img alt=""></div>';
  document.body.append(dialog);frame=dialog.querySelector('.od-media-viewport');full=frame.querySelector('img');heading=dialog.querySelector('h2');toggle=dialog.querySelector('[data-media-size]');
  toggle.addEventListener('click',()=>{const fit=frame.classList.toggle('is-fit');toggle.textContent=fit?'원본 크기':'화면에 맞추기';toggle.setAttribute('aria-pressed',String(!fit))});
  dialog.querySelector('[data-media-close]').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close()});
  dialog.addEventListener('close',()=>{document.documentElement.classList.remove('od-media-open');full.removeAttribute('src');full.removeAttribute('width');full.removeAttribute('height');origin?.focus()});
 }
 document.addEventListener('click',event=>{
  const a=event.target.closest('a[data-full-image]');if(!a||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
  const image=a.querySelector('img');if(!image)return;event.preventDefault();if(!dialog)create();origin=a;heading.textContent=image.alt||'이미지 확대';full.alt=image.alt;frame.classList.add('is-fit');toggle.textContent='원본 크기';toggle.setAttribute('aria-pressed','false');
  full.width=Number(a.dataset.fullWidth||image.width);full.height=Number(a.dataset.fullHeight||image.height);full.src=a.href;document.documentElement.classList.add('od-media-open');dialog.showModal();frame.scrollTop=0;frame.scrollLeft=0;
 });
})();
