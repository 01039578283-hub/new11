/** Fixed, source-reviewed branch photographs; preserve their existing positions. */
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {parseHTML} from './image-order-build.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));
const config=JSON.parse(fs.readFileSync(path.join(root,'branch-thumbnail-data.json'),'utf8'));
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('"','&quot;').replaceAll('<','&lt;');
const keys=new Set(['og:image','og:image:url','og:image:secure_url','og:image:width','og:image:height','og:image:type','og:image:alt','twitter:image','twitter:image:src','twitter:image:alt']);
const ancestors=n=>{const a=[];for(let p=n.parent;p;p=p.parent)a.push(p);return a};
const attribute=(tag,key,value)=>{
 const re=new RegExp('\\s'+key+'(?:\\s*=\\s*(?:"[^"]*"|\'[^\']*\'|[^\\s>]+))?','i');
 return re.test(tag)?tag.replace(re,' '+key+'="'+esc(value)+'"'):tag.replace(/\s*\/?>$/,' '+key+'="'+esc(value)+'">');
};
export function applyBranchThumbnail(source,name,settings=config){
 const config=settings;
 const row=config.entries[name];if(!row)return {html:source,removedHidden:0,changed:false};
 const nodes=parseHTML(source),main=nodes.find(n=>n.tag==='main'),head=nodes.find(n=>n.tag==='head');
 if(!main||!head)throw Error('Missing document structure '+name);
 const page=new URL(row.path,config.host),resolve=v=>decodeURIComponent(new URL(v,page).pathname);
 const photos=nodes.filter(n=>n.tag==='img'&&ancestors(n).includes(main)&&resolve(n.attrs.src)===row.image.src);
 if(photos.length!==1)throw Error('Representative must already appear exactly once '+name);
 const image=photos[0];
 if(image.attrs.hidden!==undefined||image.attrs['aria-hidden']==='true'||ancestors(image).some(n=>n.tag==='details'||n.attrs.hidden!==undefined))throw Error('Reviewed photograph is not normally displayed '+name);
 if(!ancestors(image).some(n=>n.attrs.id==='learning-space'||/(?:^|\s)rg-gallery(?:\s|$)/.test(n.attrs.class||'')))throw Error('Photograph left its existing gallery '+name);
 const edits=[];const absolute=new URL(row.image.src,config.host).href;
 for(const n of nodes.filter(n=>n.tag==='meta'&&ancestors(n).includes(head))){
  if(keys.has((n.attrs.property||n.attrs.name||'').toLowerCase()))edits.push({start:n.start,end:n.end,value:''});
 }
 const meta=[['property','og:image',absolute],['property','og:image:width',row.image.width],['property','og:image:height',row.image.height],['property','og:image:type',row.image.mime],['property','og:image:alt',row.image.alt],['name','twitter:image',absolute],['name','twitter:image:alt',row.image.alt]].map(([k,n,v])=>'<meta '+k+'="'+n+'" content="'+esc(v)+'">').join('');
 edits.push({start:head.closeStart,end:head.closeStart,value:meta});
 let tag=source.slice(image.start,image.end);tag=attribute(tag,'alt',row.image.alt);tag=attribute(tag,'width',row.image.width);tag=attribute(tag,'height',row.image.height);tag=attribute(tag,'decoding','async');
 // Existing native src, srcset, lazy loading, anchor, captions and gallery order stay intact.
 edits.push({start:image.start,end:image.end,value:tag});
 let removedHidden=0;
 for(const n of nodes.filter(n=>n.tag==='img'&&ancestors(n).includes(main))){
  const src=resolve(n.attrs.src);const representative=n.attrs['data-media-role']==='representative'||/\/representative\/|\/rep-/.test(src);
  const hidden=[n,...ancestors(n)].some(x=>x.attrs.hidden!==undefined||x.attrs['aria-hidden']==='true'||/display\s*:\s*none/i.test(x.attrs.style||''));
  if(representative&&hidden){edits.push({start:n.start,end:n.end,value:''});removedHidden++;}
 }
 const object=()=>({'@type':'ImageObject',url:absolute,contentUrl:absolute,width:row.image.width,height:row.image.height,caption:row.image.alt});
 // Parse the opening tag only: the HTML tokenizer also exposes attributes from raw script text.
 for(const n of nodes.filter(n=>n.tag==='script'&&/\btype\s*=\s*["']application\/ld\+json["']/i.test(source.slice(n.start,source.indexOf('>',n.start)+1)))){
  const openEnd=source.indexOf('>',n.start)+1,close=source.toLowerCase().lastIndexOf('</script',n.end);
  const graph=JSON.parse(source.slice(openEnd,close));const list=graph['@graph']||[graph];let changed=false;
  for(const node of list){
   const types=Array.isArray(node['@type'])?node['@type']:[node['@type']];let nodeChanged=false;
   if(types.some(t=>['WebPage','CollectionPage','Article'].includes(t))){
    if('primaryImageOfPage' in node){node.primaryImageOfPage=object();nodeChanged=true;}
    if('image' in node){node.image=object();nodeChanged=true;}
    if('thumbnailUrl' in node){node.thumbnailUrl=absolute;nodeChanged=true;}
    if(nodeChanged&&'dateModified' in node)node.dateModified=config.changedAt;
   }else if(types.includes('EducationalOrganization')&&node.name===row.registeredName&&'image' in node){node.image=object();nodeChanged=true;}
   changed ||= nodeChanged;
  }
  if(changed)edits.push({start:openEnd,end:close,value:JSON.stringify(graph)});
 }
 edits.sort((a,b)=>b.start-a.start);let previous=source.length,result=source;
 for(const e of edits){if(e.end>previous)throw Error('Overlapping approved edit '+name);result=result.slice(0,e.start)+e.value+result.slice(e.end);previous=e.start;}
 return {html:result,removedHidden,changed:result!==source};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const sourceMode=process.argv.includes('--source');
 if(!sourceMode&&!process.argv.includes('--apply-only')){
  if(config.previousBuildCommand!=='node favicon-build.mjs')throw Error('Unreviewed prior pipeline');
  const p=spawnSync(process.execPath,['favicon-build.mjs'],{cwd:root,stdio:'inherit'});if(p.error)throw p.error;if(p.status!==0)process.exit(p.status??1);
 }
 const output=sourceMode?root:path.join(root,'.public-release');let cursor=0,checked=0,changed=0,removed=0;const entries=Object.keys(config.entries);
 await Promise.all(Array.from({length:12},async()=>{while(cursor<entries.length){
  const name=entries[cursor++],file=path.resolve(output,name);if(!file.startsWith(output+path.sep)||!name.endsWith('/index.html'))throw Error('Unsafe selected page');
  const before=await fs.promises.readFile(file,'utf8'),r=applyBranchThumbnail(before,name);if(r.changed){await fs.promises.writeFile(file,r.html);changed++;}removed+=r.removedHidden;checked++;
  if(checked%1000===0)console.log(JSON.stringify({branchPhotoPagesChecked:checked,total:entries.length,sourceMode}));
 }}));
 console.log(JSON.stringify({branchPhotoPages:checked,changed,removedHiddenRepresentativeElements:removed,fixedSelection:true,bottomGalleryPositionsPreserved:true,sourceMode}));
}
