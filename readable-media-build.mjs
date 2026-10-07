import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {parseHTML} from './image-order-build.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));
const data=JSON.parse(fs.readFileSync(path.join(root,'readable-media-data.json'),'utf8'));
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('"','&quot;').replaceAll('<','&lt;');
function attr(tag,k,v){const re=new RegExp('\\s'+k+'(?:\\s*=\\s*(?:"[^"]*"|\'[^\']*\'|[^\\s>]+))?','i');return re.test(tag)?tag.replace(re,' '+k+'="'+esc(v)+'"'):tag.replace(/\s*\/?>$/,' '+k+'="'+esc(v)+'">')}
export function enhanceReadableHTML(source,name='index.html'){
 const nodes=parseHTML(source),edits=[];let count=0;
 const pageURL=new URL(name,'https://xn--jk1bu21awrcryv.com/');
 for(const n of nodes.filter(n=>n.tag==='img')){
  const ancestry=[];for(let p=n.parent;p;p=p.parent)ancestry.push(p);
  if(!ancestry.some(p=>p.tag==='main')||n.attrs.hidden!==undefined||n.attrs['aria-hidden']==='true')continue;
  let src;try{const resolved=new URL(n.attrs.src,pageURL);if(resolved.origin!==pageURL.origin)continue;src=decodeURIComponent(resolved.pathname)}catch{continue}
  const original=Object.entries(data.lossless).find(([,v])=>v.src===src||v.variants.some(x=>x.src===src))?.[0]||src;
  const image=data.images[original];if(!image)continue;
  let tag=source.slice(n.start,n.end);tag=attr(tag,'width',image.width);tag=attr(tag,'height',image.height);tag=attr(tag,'decoding','async');
  const preservedStyle=(n.attrs.style||'').replace(/(?:^|;)\s*(?:--od-image-width|aspect-ratio)\s*:[^;]*/gi,'').replace(/^\s*;+|;+\s*$/g,'').trim();
  tag=attr(tag,'style',(preservedStyle?preservedStyle+'; ':'')+'--od-image-width: '+image.width+'px; aspect-ratio: '+image.width+' / '+image.height+';');
  const replacement=data.lossless[original];
  if(replacement){tag=attr(tag,'src',replacement.src);tag=attr(tag,'srcset',[...replacement.variants.map(v=>v.src+' '+v.width+'w'),replacement.src+' '+replacement.width+'w'].join(', '));tag=attr(tag,'sizes','(max-width: 720px) calc(100vw - 40px), 900px')}
  const anchor=ancestry.find(p=>p.tag==='a');
  if(anchor){
   // Preserve external/map/navigation actions. Existing original-image anchors gain zoom.
   let href;try{const resolved=new URL(anchor.attrs.href,pageURL);if(resolved.origin===pageURL.origin)href=decodeURIComponent(resolved.pathname)}catch{}
   if(href===original){const open=source.slice(anchor.start,anchor.openEnd);edits.push({start:anchor.start,end:anchor.openEnd,value:attr(attr(attr(open,'data-full-image','true'),'data-full-width',image.width),'data-full-height',image.height)})}
  }else if(ancestry.some(p=>p.tag==='figure')||n.attrs['data-media-role']==='body'||n.attrs['data-media-role']==='map'){
   tag='<a class="od-media-link" data-full-image="true" data-full-width="'+image.width+'" data-full-height="'+image.height+'" href="'+esc(src)+'" aria-label="'+esc((n.attrs.alt||'학습 안내 이미지')+' 확대 보기')+'">'+tag+'</a>';
  }
  edits.push({start:n.start,end:n.end,value:tag});count++;
 }
 edits.sort((a,b)=>b.start-a.start);let result=source;for(const e of edits)result=result.slice(0,e.start)+e.value+result.slice(e.end);
 return {html:result,images:count};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const manifest=JSON.parse(fs.readFileSync(path.join(root,'release-public-manifest.json'),'utf8'));let pages=0,images=0,cursor=0,checked=0;const names=Object.keys(manifest.files).filter(n=>n.endsWith('index.html'));
 await Promise.all(Array.from({length:12},async()=>{while(cursor<names.length){const name=names[cursor++],f=path.join(root,'.public-release',name),source=await fs.promises.readFile(f,'utf8');const r=enhanceReadableHTML(source,name);if(r.html!==source){await fs.promises.writeFile(f,r.html);pages++}images+=r.images;checked++;if(checked%2000===0)console.log(JSON.stringify({readabilityChecked:checked,total:names.length}))}}));
 console.log(JSON.stringify({readableMediaPages:pages,visibleImagesChecked:images,originalsPreserved:true}));
}
