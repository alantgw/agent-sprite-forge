from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,shutil
r=Path('/workspace/work/mecha-wave-punch-v003');out=r/'deliverables';out.mkdir(exist_ok=False);root=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2');base=Image.open(root/'v001/mecha-final-1x.png');pal=base.getpalette();p=np.array(pal,dtype=np.int32).reshape(-1,3);stems=['left-punch','right-punch'];rows=[];images=[]
for n,stem in enumerate(stems,1):
 pose=Image.open(r/f'pose-{n}/punch-{n}.png').convert('RGBA');assert pose.width<=132 and pose.height<=108
 a=np.array(pose);d=((a[:,:,:3].astype(np.int32)[:,:,None,:]-p[None,None,1:,:])**2).sum(-1);idx=d.argmin(-1).astype('uint8')+1;idx[a[:,:,3]==0]=0;at=(136-pose.width,109-pose.height)
 im=Image.new('P',(144,112));im.putpalette(pal);im.paste(Image.fromarray(idx),at);im.save(out/f'{stem}-1x.png',bits=4);im.save(out/f'{stem}.bmp');im.resize((864,672),Image.Resampling.NEAREST).save(out/f'{stem}-6x.png',bits=4);images.append(im)
 re=Image.open(out/f'{stem}-1x.png');assert re.mode=='P' and re.size==(144,112) and re.getpalette()==pal and len(set(re.get_flattened_data()))<=16 and 'transparency' not in re.info
 assert Image.open(out/f'{stem}-6x.png').convert('RGB').tobytes()==re.convert('RGB').resize((864,672),Image.Resampling.NEAREST).tobytes()
 rows.append({'pose':stem,'canvas':[144,112],'occupied_size':list(pose.size),'bounds_xyxy_exclusive':[at[0],at[1],at[0]+pose.width,at[1]+pose.height],'palette_entries':16,'used_palette_entries':len(set(re.get_flattened_data())),'palette_matches_base':True,'opaque_teal_rgb':pal[:3],'record':json.loads((r/f'pose-{n}/punch-{n}.json').read_text())})
page=Image.new('RGB',(1296,390),(88,120,120));dr=ImageDraw.Draw(page)
for i,(im,label) in enumerate(zip([base]+images,['Approved base proportions','Reworked left-arm punch','Reworked right-arm punch'])):dr.text((432*i+12,10),label+' - same 3x scale',fill='white');page.paste(im.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(432*i,38))
page.save(out/'base-and-revised-proportions.png');pair=Image.new('RGB',(1152,500),(88,120,120));dr=ImageDraw.Draw(pair)
for i,im in enumerate(images):dr.text((576*i+12,10),stems[i]+' - compact build revision',fill='white');pair.paste(im.convert('RGB').resize((576,448),Image.Resampling.NEAREST),(576*i,36))
pair.save(out/'left-right-punch-comparison.png')
(out/'specification.json').write_text(json.dumps({'revision':'v003','intent':'correct thin/long-limbed v002 toward approved broad compact body proportions','sprites':rows,'requirements_retained':['forward torso lean','horizontal short punch, palm facing down','original gauntlet identity','natural retracted inactive arm','all flowing strands behind/up from head; none behind feet','original colours; no video shading','no beam or effects'],'visual_acceptance':'awaiting user review','game_import_compatibility':'not verified'},indent=2))
(out/'README.md').write_text('''# Firing punches — v003 body-build revision

Reworks the thin/long-limbed v002 toward approved Candidate 2's heavy compact build: broader chest and shoulders, a substantial layered waist/pelvis, shorter thicker bent legs and larger clawed feet. The pose is a forward lean of a solid torso, rather than a stretched slim humanoid.

![Base and revisions at identical scale](base-and-revised-proportions.png)

[Left native PNG](left-punch-1x.png) · [Left 6× preview](left-punch-6x.png) · [Right native PNG](right-punch-1x.png) · [Right 6× preview](right-punch-6x.png)

The near left arm crosses in front of the chest; the far right-arm variant reveals more of the chest. Both keep horizontal palm-down punches, original angular gauntlet identity, a naturally retracted inactive arm, upper-swept strands with none behind the feet, original bright palette, and no 光波 or effects.

Native 144×112 indexed PNGs, exact original 16-entry palette, opaque teal RGB(88,120,120). Actual used counts are recorded in specification.json. Previews are exact 6× nearest-neighbour; indexed BMPs included. Body and pose fidelity require visual review, not automatic numeric acceptance. Prior revisions are retained.

[Method and retained warnings](report.txt) · [Specifications](specification.json)
''')
report='''Body-build revision after user rejected v002 as too thin overall. Base image was given priority over thin pose reference for silhouette/body mass; v002 guided gesture only. Built-in host image generation, followed by repository pixel-looks ask-view/view grid extraction with existing runtime 2048x1024 layout and narrowed strict ruler fit. Expanded intermediate palette then final original-palette lock. Native extracted cells padded to144x112 without resizing, common bottom line y109. No uniform horizontal stretch was used to fake bulk. The actual helmet, chest/waist and legs were reposed/redrawn by image model and need visual review; this is not literal reuse of unchanged original body pixels. Original bright base palette is exactly retained.

Restored heavy torso, layered waist, thick short legs and large feet are artistic targets, not numerically certified identical proportions. The body tilt was balanced against maintaining broad chest mass. Sources and prompt stages retained. No beams/effects, ROM changes, editor/source changes or game-import compatibility claim.

Published height warnings, verbatim, from upright-reference comparison of crouching poses:
'''
for n,row in enumerate(rows,1):report+=f"\nPose {n}: "+repr(row['record'].get('warnings',[]))+'\n'
(out/'report.txt').write_text(report);proc=out/'processing';proc.mkdir();shutil.copytree(r/'ask',proc/'ask-view');shutil.copy2(r/'read.py',proc/'read.py');shutil.copy2(r/'package.py',proc/'package.py')
for q in r.glob('prompt-*.txt'):shutil.copy2(q,proc/q.name)
fs=['exec-604c2fcb-5832-4003-92e7-2851b0a753d0.png','exec-d897eb6e-7c5e-4afa-b70a-c97015ec4e18.png']
for n,f in enumerate(fs,1):shutil.copytree(r/f'pose-{n}',proc/f'extraction-{n}');shutil.copy2(Path('/workspace/generated_images')/f,proc/f'generated-{n}.png')
(out/'sha256.json').write_text(json.dumps({str(q.relative_to(out)):hashlib.sha256(q.read_bytes()).hexdigest() for q in out.rglob('*') if q.is_file()},indent=2));print(json.dumps([{k:v for k,v in row.items() if k!='record'} for row in rows],indent=2));shutil.copytree(out,root/'actions/wave-firing-punch/v003')
