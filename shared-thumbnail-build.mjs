/** Public, clearly labelled shared-photo fallback for confirmed empty folders. */
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {parseHTML} from './image-order-build.mjs';
import {applyBranchThumbnail} from './branch-thumbnail-build.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));
const config=JSON.parse(fs.readFileSync(path.join(root,'shared-thumbnail-data.json'),'utf8'));
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('"','&quot;').replaceAll('<','&lt;');
export function applySharedThumbnail(source,name){
 const row=config.entries[name];if(!row)return {html:source,removedHidden:0,changed:false,addedBottom:0};
 const nodes=parseHTML(source),main=nodes.find(n=>n.tag==='main');if(!main)throw Error('Missing main '+name);
 let addedBottom=0,prepared=source;
 if(!nodes.some(n=>n.attrs.id==='shared-learning-space')){
  const p=row.image;
  const section='<section class="rg-section" id="shared-learning-space" data-photo-origin="shared-reference"><h2>공통 학습 공간 참고 사진</h2><p class="rg-note">운영자가 제공한 공용사진입니다. 각 지점의 현재 공간과 시설은 방문 상담에서 확인해 주세요.</p><div class="rg-gallery" style="display:block"><figure><a class="od-media-link" data-full-image="true" data-full-width="'+p.width+'" data-full-height="'+p.height+'" href="'+esc(p.src)+'" aria-label="'+esc(p.alt)+' 확대 보기"><img src="'+esc(p.src)+'" alt="'+esc(p.alt)+'" width="'+p.width+'" height="'+p.height+'" loading="lazy" decoding="async" style="--od-image-width: '+p.width+'px; aspect-ratio: '+p.width+' / '+p.height+';"></a><figcaption>온담학습 공용 학습 공간 참고 사진</figcaption></figure></div></section>';
  prepared=source.slice(0,main.closeStart)+section+source.slice(main.closeStart);addedBottom=1;
 }
 // No individual EducationalOrganization image is replaced by a shared reference.
 const result=applyBranchThumbnail(prepared,name,config);
 return {...result,changed:result.html!==source,addedBottom};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const sourceMode=process.argv.includes('--source');
 if(!sourceMode&&!process.argv.includes('--apply-only')){
  if(config.previousBuildCommand!=='node branch-thumbnail-build.mjs')throw Error('Unreviewed existing pipeline');
  const p=spawnSync(process.execPath,['branch-thumbnail-build.mjs'],{cwd:root,stdio:'inherit'});if(p.error)throw p.error;if(p.status!==0)process.exit(p.status??1);
 }
 const output=sourceMode?root:path.join(root,'.public-release');const names=Object.keys(config.entries);let cursor=0,changed=0,removed=0,added=0;
 await Promise.all(Array.from({length:12},async()=>{while(cursor<names.length){
  const name=names[cursor++],file=path.resolve(output,name);if(!file.startsWith(output+path.sep)||!name.endsWith('/index.html'))throw Error('Unsafe approved page');
  const before=await fs.promises.readFile(file,'utf8'),r=applySharedThumbnail(before,name);if(r.changed){await fs.promises.writeFile(file,r.html);changed++;}removed+=r.removedHidden;added+=r.addedBottom;
 }}));
 console.log(JSON.stringify({sharedPhotoPages:names.length,changed,removedHiddenRepresentativeElements:removed,addedBottomSections:added,sourceMode,fixedSharedPhoto:true,existingBranchPhotosPreserved:true}));
}
