/* Progressive enhancement only: all content and links exist in the HTML. */
(() => {
  'use strict';
  document.querySelectorAll('[data-od-directory]').forEach(root => {
    const input=root.querySelector('[data-od-query]'), select=root.querySelector('[data-od-subject]');
    const cards=[...root.querySelectorAll('[data-od-center]')];
    const count=root.querySelector('[data-od-count]'), empty=root.querySelector('[data-od-empty]');
    const normal=s=>s.normalize('NFKC').toLocaleLowerCase('ko').replace(/\s+/g,'');
    const update=()=>{
      const terms=input.value.trim().split(/\s+/).filter(Boolean).map(normal), subject=select.value;
      let n=0;
      for(const card of cards){const match=terms.every(t=>normal(card.dataset.odCenter).includes(t))&&(!subject||card.dataset.subjects.split(',').includes(subject));card.hidden=!match;if(match)n++;}
      count.textContent=`${n}개 지점 · 전체 ${cards.length}개`;empty.hidden=n!==0;
    };
    input.addEventListener('input',update);select.addEventListener('change',update);
    root.querySelector('[data-od-reset]').addEventListener('click',()=>{input.value='';select.value='';update();input.focus();});
    update();
  });
  const allowed=new Set(['avpJfW7eIV0','UIXUaBZdNXU']);
  document.querySelectorAll('[data-od-video]').forEach(card=>{
    const id=card.dataset.odVideo,stage=card.querySelector('.od-video-stage'),play=card.querySelector('.od-play'),stop=card.querySelector('.od-stop');
    if(!allowed.has(id))return;
    play.addEventListener('click',()=>{
      const frame=document.createElement('iframe');frame.src=`https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0`;
      frame.title=play.dataset.title;frame.allow='accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; web-share';frame.allowFullscreen=true;frame.referrerPolicy='strict-origin-when-cross-origin';
      play.hidden=true;stage.append(frame);stop.hidden=false;stop.focus();
    });
    stop.addEventListener('click',()=>{stage.querySelector('iframe')?.remove();play.hidden=false;stop.hidden=true;play.focus();});
  });
  document.addEventListener('keydown',event=>{if(event.key==='Escape'){const d=document.querySelector('.od-mobile-menu[open]');if(d){d.open=false;d.querySelector('summary').focus();}}});
  document.addEventListener('click',event=>{const d=document.querySelector('.od-mobile-menu[open]');if(d&&!d.contains(event.target))d.open=false;});
})();
