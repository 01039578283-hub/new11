/** Restore topic/grade relevance using reviewed, already-published reading guides. */
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {parseHTML} from './image-order-build.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));
const config=JSON.parse(fs.readFileSync(path.join(root,'contextual-reading-data.json'),'utf8'));
const sha=s=>createHash('sha256').update(s).digest('hex');
const ancestors=n=>{const a=[];for(let p=n.parent;p;p=p.parent)a.push(p);return a};
export function applyContextualReading(source,name){
 const row=config.entries[name];if(!row)return {html:source,changed:false};
 const nodes=parseHTML(source),sections=nodes.filter(n=>n.tag==='section'&&n.attrs.id==='education-information-link');
 if(sections.length!==1||!ancestors(sections[0]).some(n=>n.tag==='main'))throw Error('Unexpected reading section '+name);
 const section=sections[0],original=source.slice(section.start,section.end);
 if(original!==row.html&&sha(original)!==row.originalSectionSha256)throw Error('Unreviewed reading content '+name);
 const edits=[{start:section.start,end:section.end,value:row.html}];
 const dates=nodes.filter(n=>n.tag==='p'&&/(?:^|\s)rg-date(?:\s|$)/.test(n.attrs.class||''));
 if(dates.length!==1)throw Error('Missing visible revision date '+name);
 const date=nodes.find(n=>n.tag==='time'&&ancestors(n).includes(dates[0]));if(!date)throw Error('Missing revision time '+name);
 const open=source.slice(date.start,date.openEnd).replace(/\bdatetime=["'][^"']*["']/,'datetime="'+config.updatedAt+'"');
 edits.push({start:date.start,end:date.end,value:open+config.updatedAt+source.slice(date.closeStart,date.end)});
 for(const n of nodes.filter(n=>n.tag==='script'&&/\btype\s*=\s*["']application\/ld\+json["']/i.test(source.slice(n.start,source.indexOf('>',n.start)+1)))){
  const start=source.indexOf('>',n.start)+1,end=source.toLowerCase().lastIndexOf('</script',n.end),schema=JSON.parse(source.slice(start,end));let changed=false;
  for(const item of schema['@graph']||[schema]){
   const types=Array.isArray(item['@type'])?item['@type']:[item['@type']];
   if(types.some(t=>['WebPage','CollectionPage','Article'].includes(t))&&item.dateModified!==config.updatedAt){item.dateModified=config.updatedAt;changed=true;}
  }
  if(changed)edits.push({start,end,value:JSON.stringify(schema)});
 }
 edits.sort((a,b)=>b.start-a.start);let html=source,last=source.length;
 for(const e of edits){if(e.end>last)throw Error('Overlapping approved change '+name);html=html.slice(0,e.start)+e.value+html.slice(e.end);last=e.start;}
 return {html,changed:html!==source};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const sourceMode=process.argv.includes('--source');
 if(!sourceMode&&!process.argv.includes('--apply-only')){
  if(config.previousBuildCommand!=='node shared-thumbnail-build.mjs')throw Error('Unreviewed previous pipeline');
  const p=spawnSync(process.execPath,['shared-thumbnail-build.mjs'],{cwd:root,stdio:'inherit'});if(p.error)throw p.error;if(p.status!==0)process.exit(p.status??1);
 }
 const output=sourceMode?root:path.join(root,'.public-release'),names=Object.keys(config.entries);let cursor=0,changed=0;
 await Promise.all(Array.from({length:12},async()=>{while(cursor<names.length){
  const name=names[cursor++],file=path.resolve(output,name);if(!file.startsWith(output+path.sep)||!name.endsWith('/index.html'))throw Error('Unsafe approved path');
  const before=await fs.promises.readFile(file,'utf8'),r=applyContextualReading(before,name);if(r.changed){await fs.promises.writeFile(file,r.html);changed++;}
 }}));
 console.log(JSON.stringify({contextualReadingPages:names.length,changed,sourceMode,fixedReviewedSelection:true,existingImagesAndCoursesPreserved:true}));
}
