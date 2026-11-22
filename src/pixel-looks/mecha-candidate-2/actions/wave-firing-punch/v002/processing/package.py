from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,shutil
r=Path('/workspace/work/mecha-wave-punch-v002');out=r/'deliverables';out.mkdir(exist_ok=False);root=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2');base=Image.open(root/'v001/mecha-final-1x.png');pal=base.getpalette();p=np.array(pal,dtype=np.int32).reshape(-1,3);rows=[];stems=['left-punch','right-punch'];names=['Left-arm punch - palm down','Right-arm punch - palm down']
for n,stem in enumerate(stems,1):
 pose=Image.open(r/f'pose-{n}-clean/punch-{n}.png').convert('RGBA');assert pose.width<=132 and pose.height<=110
 a=np.array(pose);d=((a[:,:,:3].astype(np.int32)[:,:,None,:]-p[None,None,1:,:])**2).sum(-1);idx=d.argmin(-1).astype('uint8')+1;idx[a[:,:,3]==0]=0
 at=(136-pose.width,1);im=Image.new('P',(144,112));im.putpalette(pal);im.paste(Image.fromarray(idx),at);im.save(out/f'{stem}-1x.png',bits=4);im.save(out/f'{stem}.bmp');im.resize((864,672),Image.Resampling.NEAREST).save(out/f'{stem}-6x.png',bits=4)
 re=Image.open(out/f'{stem}-1x.png');assert re.size==(144,112) and re.mode=='P' and re.getpalette()==pal and len(set(re.get_flattened_data()))<=16 and 'transparency' not in re.info
 assert Image.open(out/f'{stem}-6x.png').convert('RGB').tobytes()==re.convert('RGB').resize((864,672),Image.Resampling.NEAREST).tobytes()
 rec=json.loads((r/f'pose-{n}-clean/punch-{n}.json').read_text());rows.append({'pose':names[n-1],'native_file':stem+'-1x.png','canvas':[144,112],'occupied_size':list(pose.size),'bounds_xyxy_exclusive':[at[0],at[1],at[0]+pose.width,at[1]+pose.height],'palette_entries':16,'used_palette_entries':len(set(re.get_flattened_data())),'palette_identical_to_base':True,'opaque_teal_rgb':pal[:3],'record':rec})
page=Image.new('RGB',(1152,500),(88,120,120));dr=ImageDraw.Draw(page)
for i,stem in enumerate(stems):dr.text((i*576+15,10),names[i],fill='white');page.paste(Image.open(out/f'{stem}-1x.png').convert('RGB').resize((576,448),Image.Resampling.NEAREST),(i*576,36))
page.save(out/'left-right-punch-comparison.png')
meta={'revision':'v002, supersedes rejected v001','requirements':['Stronger forward upper-body tilt','Horizontal punching arm and straight wrist; palm faces downward by forearm pronation, not a drooping hand','Shorter arm reach and compact original-design armoured gauntlet','Inactive arm bent back naturally beside ribs','All loose pale/red strands swept up behind head; none behind feet','Original approved base colours; no video lighting tint','Mecha only, no 光波/beam or effects'],'sprites':rows,'direction':'viewers left for both, same camera; anatomical left arm then right arm','same_original_palette':True,'game_import_compatibility':'not verified'};(out/'specification.json').write_text(json.dumps(meta,indent=2))
text='''# Alternating firing punches — reworked v002

Reworks the rejected v001 poses using the user's latest corrections:

- Strong forward upper-body tilt, with the head ahead of the hips.
- Punch stays **horizontal** with a **straight wrist and palm facing downward**; the hand is not bent downward.
- Shorter reach and smaller original-design angular gauntlet; no human knuckle fist.
- Inactive arm bends back beside the ribs.
- All loose strands sweep up behind the head; **no hair behind the feet**.
- Original bright base palette; video dark/red lighting is excluded.
- Mecha poses only; no 光波, beam or other effects.

![Reworked pair](left-right-punch-comparison.png)

| Pose | Native PNG | 6× preview | Indexed BMP |
| --- | --- | --- | --- |
| Left arm active | [PNG](left-punch-1x.png) | [Preview](left-punch-6x.png) | [BMP](left-punch.bmp) |
| Right arm active | [PNG](right-punch-1x.png) | [Preview](right-punch-6x.png) | [BMP](right-punch.bmp) |

Both aim toward viewer-left from the same camera, rather than mirroring the whole character. Each PNG is **144 × 112**, indexed with the approved **16-entry palette**; actual used counts are in [specification.json](specification.json). Background is opaque teal **RGB (88,120,120)**. Previews are exact 6× nearest-neighbour. This is a new model-assisted posed revision, not a claim of pixel-identical body parts between the pair. Earlier versions remain untouched.

[Method and retained workflow warnings](report.txt). No game-import compatibility claim.
''';(out/'README.md').write_text(text)
report='''Latest correction order: first forward lean and natural inactive arm; then user clarified horizontal punch with palm down (not wrist flexion); then shorter hands/reach and no duplicate lower hair. Final source images incorporate these requirements. Upright, drooping-hand and long-reach intermediate sources are retained in workspace but are not presented as final artwork.

Method: built-in host image_gen targeted edits with approved base identity and video pose references. Repository pixel-looks ask-view/view uses approved standing master as grid ruler. Existing runtime 2048x1024 intermediate accommodation and strict narrowed grid fit are retained; expanded intermediate palette preserves hues, followed by exact original 16-entry palette lock with no dithering. Source images are 1774x887. One intermediate source failed the 60% ruler agreement gate (58%); it was regenerated against the approved reference, not forced through the gate. Final ruler matches: left 89.50%, right 86.29%. Separate sprites are extracted on the source lattice, padded to 144x112 without resizing and right-edge aligned with complete upper strand tips.

These images are intended to correct the pose, not to claim exact frame tracing. Rear-arm foreshortening and gauntlet orientation still require user visual approval. No editor/source/game files modified. No animation or game-import compatibility claim. Original video screenshots remain local, not republished. Original approved palette retained exactly; no dark video shading copied.

Published upright-height warnings retained verbatim; forward-leaning/crouched posture changes vertical body envelope:
'''
for n,row in enumerate(rows,1):report+=f"\nPose {n}: "+repr(row['record'].get('warnings',[]))+'\n'
(out/'report.txt').write_text(report);proc=out/'processing';proc.mkdir();shutil.copytree(r/'ask',proc/'ask-view');shutil.copy2(r/'read.py',proc/'read.py');shutil.copy2(r/'package.py',proc/'package.py')
fs=['exec-3424170f-3e1c-4ad0-a8ae-73987732b9a3.png','exec-076a5682-6604-4eb1-b169-41ae56a0ed7e.png']
for n,f in enumerate(fs,1):
 shutil.copytree(r/f'pose-{n}-clean',proc/f'extraction-{n}');shutil.copy2(r/f'prompt-clean-{n}.txt',proc/f'prompt-clean-{n}.txt');shutil.copy2(r/f'prompt-final-{n}.txt',proc/f'prompt-edit-{n}.txt');shutil.copy2(Path('/workspace/generated_images')/f,proc/f'generated-final-{n}.png')
(out/'sha256.json').write_text(json.dumps({str(q.relative_to(out)):hashlib.sha256(q.read_bytes()).hexdigest() for q in out.rglob('*') if q.is_file()},indent=2));print(json.dumps([{k:v for k,v in row.items() if k!='record'} for row in rows],indent=2))
shutil.copytree(out,root/'actions/wave-firing-punch/v002')
