/** Build verified, automatically deferred branch maps after the preserved site pipeline. */
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath}from'node:url';import{createHash}from'node:crypto';import{spawnSync}from'node:child_process';import{parseHTML}from'./image-order-build.mjs';
const root=path.dirname(fileURLToPath(import.meta.url)),config=JSON.parse(fs.readFileSync(path.join(root,'kakao-directions-data.json'),'utf8')),output=path.join(root,'.public-release');
const sha=s=>createHash('sha256').update(s).digest('hex');const up=n=>{const a=[];for(let p=n.parent;p;p=p.parent)a.push(p);return a;};
export function applyDirections(source,name){const entry=config.pages[name];if(!entry)return source;const nodes=parseHTML(source);if(nodes.some(n=>n.attrs.id==='kakao-directions')){if(!source.includes(entry.html))throw Error('Unreviewed existing directions '+name);return source;}
 const edits=[];let at;
 if(entry.placement==='after-map'){
  const maps=nodes.filter(n=>n.tag==='img'&&n.attrs['data-media-role']==='map'&&up(n).some(p=>p.tag==='main'));if(maps.length!==1)throw Error('Unexpected existing map '+name);const figure=up(maps[0]).find(n=>n.tag==='figure');if(!figure)throw Error('Map figure missing '+name);at=figure.end;
 }else if(entry.placement==='after-media'){
  const section=nodes.filter(n=>n.tag==='section'&&n.attrs.id==='center-images');if(section.length!==1)throw Error('Missing preserved media '+name);at=section[0].end;
 }else{const main=nodes.filter(n=>n.tag==='main');if(main.length!==1)throw Error('Main missing '+name);at=main[0].closeStart;}
 edits.push({start:at,end:at,value:entry.html});
 const head=nodes.filter(n=>n.tag==='head');if(head.length!==1)throw Error('Head missing');edits.push({start:head[0].closeStart,end:head[0].closeStart,value:'<link rel="stylesheet" href="'+config.css+'"><script src="'+config.js+'" defer></script>'});
 const toc=nodes.filter(n=>n.tag==='a'&&n.attrs.href==='#center-images'&&up(n).some(p=>p.tag==='nav'));if(toc.length>1)throw Error('Ambiguous media anchor '+name);if(toc.length)edits.push({start:toc[0].end,end:toc[0].end,value:'<a href="#kakao-directions" data-kd-toc>찾아오시는 길</a>'});
 for(const n of nodes.filter(n=>n.tag==='time'&&up(n).some(p=>p.tag==='p'&&/(?:^|\s)rg-date(?:\s|$)/.test(p.attrs.class||''))).slice(0,1))edits.push({start:n.start,end:n.end,value:'<time datetime="'+config.date+'">'+config.date+'</time>'});
 for(const n of nodes.filter(n=>n.tag==='script'&&n.attrs.type==='application/ld+json')){const schema=JSON.parse(source.slice(n.openEnd,n.closeStart));let changed=false;for(const item of schema['@graph']||[schema]){const ts=Array.isArray(item['@type'])?item['@type']:[item['@type']];if(ts.some(t=>['WebPage','CollectionPage','Article'].includes(t))){item.dateModified=config.date;changed=true;}}if(changed)edits.push({start:n.openEnd,end:n.closeStart,value:JSON.stringify(schema)});}
 edits.sort((a,b)=>b.start-a.start);let last=source.length,result=source;for(const e of edits){if(e.end>last)throw Error('Overlapping directions '+name);result=result.slice(0,e.start)+e.value+result.slice(e.end);last=e.start;}return result;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 if(!process.argv.includes('--apply-only')){
  if(config.previousBuildCommand!=='node local-study-build.mjs')throw Error('Unexpected previous pipeline');
  // The upstream output guard accepts source-manifest files only. Remove just
  // this wrapper's reproducible HTML/JSON outputs, after checking every byte.
  for(const[name,record]of Object.entries(config.generated)){
   const file=path.resolve(output,name);if(!name.startsWith('assets/branch-maps/')||name.includes('..')||!file.startsWith(output+path.sep)||!name.match(/\.(html|json)$/))throw Error('Unsafe generated output');
   if(fs.existsSync(file)){if(sha(fs.readFileSync(file))!==record.sha256)throw Error('Unreviewed existing generated output '+name);fs.unlinkSync(file);}
  }
  const p=spawnSync(process.execPath,['local-study-build.mjs'],{cwd:root,stdio:'inherit'});if(p.error)throw p.error;if(p.status!==0)process.exit(p.status??1);
 }
 for(const[name,record]of Object.entries(config.generated)){if(!name.startsWith('assets/branch-maps/')||name.includes('..')||sha(record.content)!==record.sha256)throw Error('Unreviewed generated asset');const file=path.join(output,name);await fs.promises.mkdir(path.dirname(file),{recursive:true});await fs.promises.writeFile(file,record.content);}
 const names=Object.keys(config.pages);let cursor=0,changed=0;await Promise.all(Array.from({length:12},async()=>{while(cursor<names.length){const name=names[cursor++],file=path.join(output,name);const before=await fs.promises.readFile(file,'utf8'),after=applyDirections(before,name);if(after!==before){await fs.promises.writeFile(file,after);changed++;}}}));
 const sitemap=path.join(output,'sitemap.xml'),before=await fs.promises.readFile(sitemap,'utf8');const selected=new Set(Object.values(config.pages).map(p=>p.path));let updated=0;const after=before.replace(/<url>[\s\S]*?<\/url>/g,block=>{const loc=block.match(/<loc>(.*?)<\/loc>/)?.[1];if(loc&&selected.has(decodeURIComponent(new URL(loc).pathname))){updated++;return block.replace(/<lastmod>[^<]*<\/lastmod>/,'<lastmod>'+config.date+'</lastmod>');}return block;});if(updated!==names.length)throw Error('Sitemap coverage mismatch');if(after!==before)await fs.promises.writeFile(sitemap,after);
 console.log(JSON.stringify({kakaoDirectionsPages:names.length,changed,generatedMapAssets:Object.keys(config.generated).length,allExistingImagesPreserved:true,date:config.date}));
}
