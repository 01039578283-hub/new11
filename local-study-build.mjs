/** Add reviewed local study preparation without changing URLs, images or course claims. */
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {parseHTML} from './image-order-build.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));
const config=JSON.parse(fs.readFileSync(path.join(root,'local-study-data.json'),'utf8'));
const sha=s=>createHash('sha256').update(s).digest('hex');
const ancestors=n=>{const a=[];for(let p=n.parent;p;p=p.parent)a.push(p);return a};
export function applyLocalStudy(source,name){
 const row=config.entries[name];if(!row)return {html:source,changed:false};
 const nodes=parseHTML(source),edits=[];
 for(const change of row.changes){
  const matched=nodes.filter(n=>n.tag===change.tag&&n.attrs.id===change.id);
  if(matched.length!==1||!ancestors(matched[0]).some(n=>n.tag==='main'))throw Error('Unexpected target '+name+' '+change.id);
  const n=matched[0],old=source.slice(n.start,n.end);
  // Git/Windows may represent the same textarea lines as LF or CRLF.
  const normalized=old.replaceAll('\r\n','\n');
  if(normalized!==change.html.replaceAll('\r\n','\n')&&sha(normalized)!==change.beforeSha256)throw Error('Unreviewed content '+name+' '+change.id);
  edits.push({start:n.start,end:n.end,value:change.html});
 }
 const dateParents=nodes.filter(n=>n.tag==='p'&&/(?:^|\s)rg-date(?:\s|$)/.test(n.attrs.class||''));
 if(dateParents.length!==1)throw Error('Missing page date '+name);
 const date=nodes.find(n=>n.tag==='time'&&ancestors(n).includes(dateParents[0]));if(!date)throw Error('Missing revision time '+name);
 edits.push({start:date.start,end:date.end,value:source.slice(date.start,date.openEnd).replace(/\bdatetime=["'][^"']*["']/,'datetime="'+config.date+'"')+config.date+source.slice(date.closeStart,date.end)});
 for(const n of nodes.filter(n=>n.tag==='script'&&n.attrs.type==='application/ld+json')){
  const start=n.openEnd,end=n.closeStart,schema=JSON.parse(source.slice(start,end));let changed=false;
  for(const item of schema['@graph']||[schema]){
   const types=Array.isArray(item['@type'])?item['@type']:[item['@type']];
   if(types.some(t=>['WebPage','CollectionPage','Article'].includes(t))&&item.dateModified!==config.date){item.dateModified=config.date;changed=true;}
  }
  if(changed)edits.push({start,end,value:JSON.stringify(schema)});
 }
 edits.sort((a,b)=>b.start-a.start);let html=source,last=source.length;
 for(const e of edits){if(e.end>last)throw Error('Overlapping changes '+name);html=html.slice(0,e.start)+e.value+html.slice(e.end);last=e.start;}
 return {html,changed:html!==source};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const sourceMode=process.argv.includes('--source');
 if(!sourceMode&&!process.argv.includes('--apply-only')){
  if(config.previousBuildCommand!=='node contextual-reading-build.mjs')throw Error('Unexpected previous pipeline');
  const r=spawnSync(process.execPath,['contextual-reading-build.mjs'],{cwd:root,stdio:'inherit'});if(r.error)throw r.error;if(r.status!==0)process.exit(r.status??1);
 }
 const output=sourceMode?root:path.join(root,'.public-release'),names=Object.keys(config.entries);let cursor=0,changed=0;
 await Promise.all(Array.from({length:12},async()=>{while(cursor<names.length){
  const name=names[cursor++],file=path.resolve(output,name);if(!file.startsWith(output+path.sep)||!name.endsWith('/index.html'))throw Error('Unsafe approved path');
  const before=await fs.promises.readFile(file,'utf8'),r=applyLocalStudy(before,name);if(r.changed){await fs.promises.writeFile(file,r.html);changed++;}
 }}));
 console.log(JSON.stringify({localStudyPages:names.length,changed,sourceMode,existingImagesAndUrlsPreserved:true}));
}
