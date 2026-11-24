from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,shutil,hashlib,zipfile
r=Path('/workspace/work/mecha-angular-v002');o=r/'deliverables';o.mkdir();repo=Path('/workspace/agent-sprite-forge');old=repo/'src/pixel-looks/mecha-candidate-2/actions/shin-ha-gou-shou-sen/v001';base=Image.open(repo/'src/pixel-looks/mecha-candidate-2/v001/mecha-final-1x.png');pal=base.getpalette();p=np.array(pal,dtype=np.int32).reshape(-1,3);allowed=np.array([1,2]+list(range(4,16)));plan=json.loads((r/'generation-records.json').read_text());oldspec=json.loads((old/'specification.json').read_text());spec=[];frames=[];originals=[]
eye_boxes=[(60,48,63,50),(57,49,60,51),(42,62,45,64),(71,53,75,55),(56,40,59,42),(41,36,45,39),(55,35,58,37),(63,59,66,62),(74,50,78,52),(67,50,70,52)]
face_boxes=[(51,40,74,59),(48,40,71,61),(35,54,60,74),(62,44,83,64),(48,32,66,49),(30,29,48,48),(45,26,65,48),(51,52,74,72),(60,40,82,61),(56,42,79,62)]
for d in ['native','previews','bmp','comparisons','processing','references']:(o/d).mkdir()
for i,q in enumerate(plan):
 id=q['id'];n=id+'-'+q['name'];orig=Image.open(old/f'native/{n}.png');a0=np.array(orig);originals.append(orig);folder=r/(f'extracted-{id}-retry' if id in ['01','09'] else f'extracted-{id}');rec=json.loads((folder/f'pose-{id}.json').read_text());a=np.array(Image.open(folder/f'pose-{id}.png').convert('RGBA'));idx=allowed[(((a[:,:,:3].astype(np.int32)[:,:,None,:]-p[None,None,allowed,:])**2).sum(-1)).argmin(-1)].astype('uint8');idx[a[:,:,3]==0]=0;mx,my=rec['masterAt'];xx,yy=oldspec['frames'][i]['placement_xy'];at=(xx-mx,yy-my);h,w=idx.shape;assert at[0]>=0 and at[1]>=0 and at[0]+w<=144 and at[1]+h<=112
 full=np.zeros((112,144),dtype='uint8');full[at[1]:at[1]+h,at[0]:at[0]+w]=idx
 # User-authorized colour correction uses exact original palette entries; preserve the original face.
 x0,y0,x1,y1=face_boxes[i];full[y0:y1,x0:x1]=a0[y0:y1,x0:x1];before=full.copy();ex0,ey0,ex1,ey1=eye_boxes[i];eye=full[ey0:ey1,ex0:ex1].copy()
 for src,dst in [(8,6),(13,11),(9,10),(12,10),(14,10),(15,10)]:eye[eye==src]=dst
 full[ey0:ey1,ex0:ex1]=eye;assert 11 in set(eye.ravel());assert not(set(eye.ravel())&{8,9,12,13,14,15})
 eyemask=np.zeros(full.shape,bool);eyemask[ey0:ey1,ex0:ex1]=True;assert np.array_equal(full[~eyemask],before[~eyemask]);facemask=np.zeros(full.shape,bool);facemask[y0:y1,x0:x1]=True;assert np.array_equal(full[facemask&~eyemask],a0[facemask&~eyemask])
 im=Image.fromarray(full);im.putpalette(pal);im.save(o/f'native/{n}.png',bits=4);im.save(o/f'bmp/{n}.bmp');im.resize((864,672),Image.Resampling.NEAREST).save(o/f'previews/{n}-6x.png',bits=4);frames.append(im)
 re=Image.open(o/f'native/{n}.png');assert re.mode=='P' and re.size==(144,112) and re.getpalette()==pal and 'transparency' not in re.info;assert len(set(full.ravel()))<=16
 y,x=np.where(full!=0);row={'id':id,'file':f'native/{n}.png','canvas':[144,112],'stored_palette_entries':16,'used_colours':len(set(full.ravel().tolist())),'occupied_bounds_exclusive':[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],'placement_xy':list(at),'eye_box_exclusive':list(eye_boxes[i]),'face_restore_box_exclusive':list(face_boxes[i]),'eye_core_palette_index':11,'eye_core_rgb':pal[33:36],'eye_shade_palette_indices':[6,10],'eye_region_palette_indices':sorted(set(eye.ravel().tolist())),'colour_correction_pixels':int((full!=before).sum()),'changed_pixels_vs_v001':int((full!=a0).sum()),'face_outside_eye_identical_to_v001':True,'pose_extraction':rec};spec.append(row)
 # Before / after at the exact same scale.
 page=Image.new('RGB',(864,390),(88,120,120));d=ImageDraw.Draw(page);d.text((10,10),id+' v001 before',fill='white');d.text((442,10),id+' v002 angular armour + original red eyes',fill='white');page.paste(orig.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(0,38));page.paste(im.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(432,38));page.save(o/f'comparisons/{n}-before-after.png')
 sub=o/'processing'/id;sub.mkdir();shutil.copytree(r/f'ask-large-{id}',sub/'ask-pose');shutil.copytree(folder,sub/'extracted');shutil.copy2(q['source'],sub/'generated-source.png');(sub/'host-prompt.txt').write_text(q['host_prompt'])
 # Model source versus final native; source may visibly contain eye drift that final rejects.
 source=Image.open(q['source']).convert('RGB');source.thumbnail((440,440));review=Image.new('RGB',(900,490),(88,120,120));dd=ImageDraw.Draw(review);review.paste(source,((450-source.width)//2,35));review.paste(im.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(458,80));dd.text((10,10),'Generated source / eye drift not accepted',fill='white');dd.text((458,10),'Final 1x sampled / original face + red eyes',fill='white');review.save(o/f'comparisons/{n}-source-native.png')
# Same10-pose timing as preceding version.
dur=[f['preview_hold_ms'] for f in oldspec['frames']]
for name,ms in [('sequence-preview.gif',dur),('sequence-slow.gif',[550]*10)]:
 big=[im.resize((720,560),Image.Resampling.NEAREST) for im in frames];big[0].save(o/name,save_all=True,append_images=big[1:],duration=ms,loop=0,optimize=False,disposal=2);g=Image.open(o/name);assert g.n_frames==10
 for k,f in enumerate(big):g.seek(k);assert g.convert('RGB').tobytes()==f.convert('RGB').tobytes()
page=Image.new('RGB',(1440,508),(88,120,120));d=ImageDraw.Draw(page)
for i,(q,im) in enumerate(zip(plan,frames)):
 x=(i%5)*288;y=(i//5)*254;d.text((x+7,y+7),q['id']+' '+q['name'],fill='white');page.paste(im.convert('RGB').resize((288,224),Image.Resampling.NEAREST),(x,y+28))
page.save(o/'all-ten-poses.png')
# Eye-only inspection row with original base eye at same integer zoom.
eye_page=Image.new('RGB',(1188,135),(88,120,120));d=ImageDraw.Draw(eye_page)
for i,(im,box,txt) in enumerate([(base,(58,43,65,49),'BASE')]+[(f,b,q['id']) for f,b,q in zip(frames,eye_boxes,plan)]):
 x0,y0,x1,y1=box;cx=(x0+x1)//2;cy=(y0+y1)//2;crop=im.crop((cx-4,cy-4,cx+5,cy+5)).convert('RGB').resize((108,108),Image.Resampling.NEAREST);eye_page.paste(crop,(i*108,22));d.text((i*108+4,5),txt,fill='white')
eye_page.save(o/'red-eye-inspection.png')
for f in (old/'references').iterdir():shutil.copy2(f,o/'references'/f.name)
rejected=json.loads((r/'rejected-sources.json').read_text());reject=o/'processing/rejected';reject.mkdir()
for id in ['01','09']:shutil.copy2(rejected['pose'+id],reject/f'pose-{id}-rejected-source.png')
(reject/'reasons.json').write_text(json.dumps(rejected,indent=2));shutil.copy2(r/'read.py',o/'processing/read.py');shutil.copy2(r/'ask.py',o/'processing/ask.py');shutil.copy2(r/'package.py',o/'processing/package.py')
meta={'version':'v002','status':'amendment for visual review','art_source':'host_image','route':'built-in image_gen; no paid API invoked','changes':'angular mechanical armour, fixed original-base red eye palette; same10 poses','eye_main_rgb':pal[33:36],'eye_shades_rgb':[pal[18:21],pal[30:33]],'eye_policy':'all visible eye cores use palette11 and only base red shades6/10, no orange/yellow/white/pink eye highlights','frames':spec,'original_v001_unchanged':True,'failed_takes':'01 equality50%,09 equality57% rejected and regenerated; no gate bypass','inherited_pose_height_warnings':oldspec['warnings'],'game_import_compatibility':'not verified'};(o/'specification.json').write_text(json.dumps(meta,indent=2))
rows='\n'.join(f"| {q['id']} {q['name']} | [PNG](native/{q['id']}-{q['name']}.png) | [6x](previews/{q['id']}-{q['name']}-6x.png) | [Compare](comparisons/{q['id']}-{q['name']}-before-after.png) |" for q in plan)
warn='\n'.join('- `'+x['file']+'`: '+x['warning'] for x in oldspec['warnings'])
(o/'README.md').write_text('''# Ten-pose amendment v002 — fixed red eyes and angular armour

Amends v001 rather than changing the action: sharpened shoulders, gauntlet shells, knee/shin plates and feet into planar bevels and wedges with dark joint gaps. Original flowing hair and round luminous components remain. The original pose face is restored, then only the documented visible-eye pixels are colour-corrected to the approved base palette: main red **RGB(184,21,14)**, shadow RGB(46,11,19), muted red RGB(148,54,78). Orange/yellow/pink/white eye highlights are excluded. Automated assertions inspect every documented eye box; face pixels outside the eye box equal v001 exactly. This restores original red identity rather than trusting model-written eye colours.

![Amended poses](all-ten-poses.png)

[Sequence](sequence-preview.gif) · [Slow](sequence-slow.gif) · [Eyes beside original base](red-eye-inspection.png)

| Pose | Native PNG | Nearest6x | Before/after |
| --- | --- | --- | --- |
'''+rows+'''

144×112 indexed PNGs, exact original16-entry palette,15 used entries, opaque teal RGB(88,120,120). Indexed BMPs in bmp/. Native cells are not rescaled; registration uses the preceding pose's placement and masterAt. The source1536×1536 canvas with10px cells is an enlarged editing reference only, not a change in native output resolution. No enemy/effects; same10-drawing preview timing. v001 and approved earlier actions preserved.

Built-in image_gen edits followed by repository pixel-looks ask-pose/pose. The pose reader takes connected changed cells while retaining the master elsewhere. Strict master-gate readings recorded for every pose. Pose01 first take50% and pose09 first take57% failed and were regenerated, not bypassed. Failed sources retained. Final eye/face lock is a targeted source-pixel restoration and user-requested palette correction, not a new art pipeline. Processing requests, prompts, generated sources, extracted native sprites, before/after and generated-source/native comparisons retained. No editor/source/game file modified. No game-import compatibility claim. Mechanical shape and silhouette remain subject to visual review; numeric checks do not approve art.

## Inherited pose-height warnings

The ten underlying poses retain v001's crouch/lean/flight central-column height differences against standing master101. This armour edit is not a claim those warnings disappeared. Original warnings retained verbatim below; source records remain in ../v001/.

'''+warn+'\n')
(o/'qa-report.txt').write_text('Exact red-eye checks:all10 boxes contain index11 RGB(184,21,14), none contain indices8,9,12,13,14,15; black/dark eye surrounds retained. Other face pixels inside documented restore box identical to v001. Native PNG144x112/P/exact palette16/no transparency. Eye recolouring changes only eye boxes. GIF decoded pixels match intended nearest frames. Both failed source reads rejected and regenerated. Inherited height warnings:\n'+warn+'\n')
with zipfile.ZipFile(o/'ten-amended-sprites.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
 for folder in ['native','previews','bmp']:
  for f in (o/folder).iterdir():z.write(f,str(f.relative_to(o)))
 for n in ['README.md','specification.json','qa-report.txt','all-ten-poses.png','sequence-preview.gif','red-eye-inspection.png']:z.write(o/n,n)
(o/'sha256.json').write_text(json.dumps({str(f.relative_to(o)):hashlib.sha256(f.read_bytes()).hexdigest() for f in o.rglob('*') if f.is_file() and f.name!='sha256.json'},indent=2));print(json.dumps([{k:s[k] for k in ['id','used_colours','eye_region_palette_indices','colour_correction_pixels','changed_pixels_vs_v001']} for s in spec],indent=2))
