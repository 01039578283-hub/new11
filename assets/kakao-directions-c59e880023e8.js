(()=>{'use strict';
 const frameTimers=new WeakMap();
 const startFrame=frame=>{if(frame.dataset.kdStarted)return;frame.dataset.kdStarted='true';frame.src=frame.dataset.kdSrc;frameTimers.set(frame,setTimeout(()=>{const note=frame.parentElement.querySelector('.kd-frame-error');if(note&&!frame.dataset.kdReady)note.hidden=false;},15000));};
 const observer='IntersectionObserver'in window?new IntersectionObserver(entries=>{for(const e of entries)if(e.isIntersecting){startFrame(e.target);observer.unobserve(e.target);}},{rootMargin:'240px 0px'}):null;
 const register=root=>{for(const frame of root.querySelectorAll('iframe[data-kd-src]'))observer?observer.observe(frame):startFrame(frame);};
 addEventListener('message',event=>{const d=event.data;if(!d||d.type!=='ondam-kakao-ready'||typeof d.key!=='string')return;for(const frame of document.querySelectorAll('iframe[data-kd-key]'))if(event.source===frame.contentWindow&&frame.dataset.kdKey===d.key){clearTimeout(frameTimers.get(frame));frame.dataset.kdReady='true';const note=frame.parentElement.querySelector('.kd-frame-error');if(note)note.hidden=true;}});
 for(const hub of document.querySelectorAll('.od-kd[data-kd-hub]')){
  const select=hub.querySelector('select'),view=hub.querySelector('[data-kd-view]'),status=hub.querySelector('.kd-hub-status');let serial=0,displayed=select.value;
  select.addEventListener('change',async()=>{const current=++serial,choice=select.selectedOptions[0],url=choice.dataset.kdCard;if(!url)return;status.textContent='선택한 지점의 위치를 불러오고 있습니다.';
   try{const parsed=new URL(url,location.href);if(parsed.origin!==location.origin||!parsed.pathname.startsWith('/assets/branch-maps/'))throw Error('Unexpected map card');const response=await fetch(parsed.href,{credentials:'same-origin'});if(!response.ok)throw Error('Map card response');const card=await response.json();if(current!==serial)return;if(card.center!==choice.value||typeof card.html!=='string')throw Error('Unexpected map center');for(const frame of view.querySelectorAll('iframe')){observer?.unobserve(frame);clearTimeout(frameTimers.get(frame));}view.innerHTML=card.html;register(view);displayed=choice.value;status.textContent=choice.value+' 위치 안내를 표시했습니다.';}catch{if(current===serial){select.value=displayed;status.textContent='선택한 지점의 위치를 불러오지 못했습니다. 지점 상세 안내의 주소를 확인해 주세요.';}}
  });
 }
 register(document);
})();
