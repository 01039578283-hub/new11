/** Merge repeated learning guidance into source-grounded, visible study records. */
import fs from 'node:fs';import path from 'node:path';import{fileURLToPath}from'node:url';import{createHash}from'node:crypto';import{gunzipSync}from'node:zlib';import{spawnSync}from'node:child_process';import{parseHTML}from'./image-order-build.mjs';
const root=path.dirname(fileURLToPath(import.meta.url)),output=path.join(root,'.public-release'),config=JSON.parse(gunzipSync(fs.readFileSync(path.join(root,'answer-quality-data.json.gz'))));
const sha=s=>createHash('sha256').update(s.replaceAll('\r\n','\n')).digest('hex');
const types=x=>Array.isArray(x?.['@type'])?x['@type']:[x?.['@type']];
function updateSchema(node,row){let changed=false;if(!node||typeof node!=='object')return false;
 if(Array.isArray(node)){for(const v of node)changed=updateSchema(v,row)||changed;return changed;}
 if(types(node).includes('FAQPage')){const entities=row.faq.map(v=>({'@type':'Question',name:v.question,acceptedAnswer:{'@type':'Answer',text:v.answer}}));if(JSON.stringify(node.mainEntity)!==JSON.stringify(entities)){node.mainEntity=entities;changed=true;}}
 const current=String(node.url||node['@id']||'').split('#')[0];let pagePath;try{pagePath=decodeURIComponent(new URL(current).pathname)}catch{}
 if(types(node).some(v=>['WebPage','Article','CollectionPage'].includes(v))&&pagePath===row.path&&node.dateModified!==config.date){node.dateModified=config.date;changed=true;}
 for(const[key,value]of Object.entries(node))if(key!=='mainEntity'||!types(node).includes('FAQPage'))changed=updateSchema(value,row)||changed;
 return changed;
}
export function applyAnswerQuality(source,name){const row=config.pages[name];if(!row)return source;
 const nodes=parseHTML(source),edits=[];
 for(const c of row.changes){const found=nodes.filter(n=>n.tag===c.tag&&n.attrs.id===c.id);if(found.length!==1)throw Error('Ambiguous answer target '+name+' '+c.id);const n=found[0],before=source.slice(n.start,n.end),after=config.blocks[c.htmlRef];if(typeof after!=='string')throw Error('Missing reviewed block');if(before.replaceAll('\r\n','\n')===after.replaceAll('\r\n','\n'))continue;if(sha(before)!==c.beforeSha256)throw Error('Unreviewed answer target '+name+' '+c.id);edits.push({start:n.start,end:n.end,value:after});}
 const head=nodes.filter(n=>n.tag==='head');if(head.length!==1)throw Error('Missing head');const styles=nodes.filter(n=>n.tag==='link'&&n.attrs.href===config.css);if(styles.length>1)throw Error('Duplicate answer stylesheet');if(!styles.length)edits.push({start:head[0].closeStart,end:head[0].closeStart,value:'<link rel="stylesheet" href="'+config.css+'">'});
 // The shared parser stores raw script tokens whole. Read only their opening attributes;
 // parsing the full token as attributes can mistake JSON keys for HTML attributes.
 for(const n of nodes.filter(n=>n.tag==='script')){const token=source.slice(n.start,n.end),opening=token.match(/^<script\b(?:"[^"]*"|'[^']*'|[^'">])*?>/i)?.[0];if(!opening||!/\btype\s*=\s*(["'])application\/ld\+json\1/i.test(opening))continue;const start=n.start+opening.length,end=n.start+token.toLowerCase().lastIndexOf('</script');if(end<start)throw Error('Unclosed JSON-LD '+name);const object=JSON.parse(source.slice(start,end));if(updateSchema(object,row))edits.push({start,end,value:JSON.stringify(object)});}
 const dateParents=nodes.filter(n=>n.tag==='p'&&/(?:^|\s)rg-date(?:\s|$)/.test(n.attrs.class||''));
 for(const n of nodes.filter(n=>n.tag==='time'&&dateParents.includes(n.parent))){const after='<time datetime="'+config.date+'">'+config.date+'</time>';if(source.slice(n.start,n.end)!==after)edits.push({start:n.start,end:n.end,value:after});}
 edits.sort((a,b)=>b.start-a.start);let html=source,last=source.length;for(const e of edits){if(e.end>last)throw Error('Overlapping answer targets '+name);html=html.slice(0,e.start)+e.value+html.slice(e.end);last=e.start;}return html;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 if(!process.argv.includes('--apply-only')){if(config.previousBuildCommand!=='node kakao-directions-build.mjs')throw Error('Unexpected previous pipeline');const p=spawnSync(process.execPath,['kakao-directions-build.mjs'],{cwd:root,stdio:'inherit'});if(p.error)throw p.error;if(p.status!==0)process.exit(p.status??1);}
 let cursor=0,changed=0;const names=Object.keys(config.pages);await Promise.all(Array.from({length:12},async()=>{while(cursor<names.length){const name=names[cursor++],file=path.join(output,name),before=await fs.promises.readFile(file,'utf8'),after=applyAnswerQuality(before,name);if(before!==after){await fs.promises.writeFile(file,after);changed++;}}}));
 const sitemap=path.join(output,'sitemap.xml'),before=await fs.promises.readFile(sitemap,'utf8'),selected=new Set(Object.values(config.pages).map(r=>r.path));let matched=0;const after=before.replace(/<url>[\s\S]*?<\/url>/g,block=>{const u=block.match(/<loc>(.*?)<\/loc>/)?.[1];if(u&&selected.has(decodeURIComponent(new URL(u).pathname))){matched++;return block.replace(/<lastmod>[^<]*<\/lastmod>/,'<lastmod>'+config.date+'</lastmod>');}return block;});if(matched!==names.length)throw Error('Sitemap answer coverage');if(after!==before)await fs.promises.writeFile(sitemap,after);
 console.log(JSON.stringify({answerQualityPages:names.length,changed,sourceGradesPreserved:true,originalImagesAndUrlsPreserved:true}));
}
