from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,shutil,hashlib,zipfile
r=Path('/workspace/work/mecha-kick-transition-v001');out=r/'deliverables';out.mkdir(exist_ok=False);root=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2');base=Image.open(root/'v001/mecha-final-1x.png');pal=base.getpalette();palette=np.array(pal,dtype=np.int32).reshape(-1,3);rows=[]
labels=['Crouch / weight shift','Airborne knee lift','Partial kick extension'];places=[(10,23),(10,15),(10,17)]
for n in range(1,4):
 pose=Image.open(r/f'pose-{n}-hues/transition-{n}.png').convert('RGBA');assert pose.width<=124 and pose.height<=103;raw=np.array(pose);dist=((raw[:,:,:3].astype(np.int32)[:,:,None,:]-palette[None,None,1:,:])**2).sum(-1);idx=dist.argmin(-1).astype('uint8')+1;idx[raw[:,:,3]==0]=0
 im=Image.new('P',(144,112));im.putpalette(pal);im.paste(Image.fromarray(idx),places[n-1]);im.save(out/f'transition-{n}-1x.png',bits=4);im.save(out/f'transition-{n}.bmp');im.resize((864,672),Image.Resampling.NEAREST).save(out/f'transition-{n}-6x.png',bits=4)
 re=Image.open(out/f'transition-{n}-1x.png');used=len(set(re.get_flattened_data()));assert re.size==(144,112) and re.mode=='P' and re.getpalette()==pal and used<=16 and 'transparency' not in re.info
 assert Image.open(out/f'transition-{n}-6x.png').convert('RGB').tobytes()==re.convert('RGB').resize((864,672),Image.Resampling.NEAREST).tobytes()
 rec=json.loads((r/f'pose-{n}-hues/transition-{n}.json').read_text());rows.append({'order':n,'pose':labels[n-1],'canvas':[144,112],'occupied_size':list(pose.size),'placement':places[n-1],'bounds_xyxy_exclusive':[places[n-1][0],places[n-1][1],places[n-1][0]+pose.width,places[n-1][1]+pose.height],'palette_entries':16,'used_palette_entries':used,'palette_identical_to_base':True,'opaque_teal_rgb':pal[:3],'record':rec})
ref=out/'endpoints';ref.mkdir();start=root/'actions/right-fist/v004/mecha-base-arm-1x.png';end=root/'actions/airborne-kick/v001/mecha-airborne-kick-1x.png';shutil.copy2(start,ref/'start-right-fist-v004.png');shutil.copy2(end,ref/'end-airborne-kick-v001.png')
seq=[Image.open(start)]+[Image.open(out/f'transition-{n}-1x.png') for n in range(1,4)]+[Image.open(end)]
# Review contact sheet only; independent sprites are deliverables, no animation or runtime spritesheet.
page=Image.new('RGB',(2160,390),(88,120,120));d=ImageDraw.Draw(page);names=['START: right-fist v004','1: Crouch','2: Airborne knee lift','3: Partial extension','END: approved kick']
for i,(im,name) in enumerate(zip(seq,names)):
 d.text((i*432+12,12),name,fill='white');page.paste(im.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(i*432,38))
page.save(out/'five-pose-sequence-review.png');(out/'specification.json').write_text(json.dumps({'sequence_order':['endpoints/start-right-fist-v004.png','transition-1-1x.png','transition-2-1x.png','transition-3-1x.png','endpoints/end-airborne-kick-v001.png'],'sprites':rows,'endpoints_unchanged':True,'static_sprites_only':True,'game_import_compatibility':'not verified'},indent=2))
report='''Three intermediate static sprites from accepted right-fist v004 to accepted airborne-kick v001.
Order: start -> crouch/weight shift -> airborne knee chamber -> partial extension -> final kick. Endpoint PNGs copied byte-for-byte for review; originals untouched. No animation or runtime spritesheet generated. The sequence contact image is a visual review only.

Each intermediate is 144x112 indexed PNG, exact original 16-entry palette, opaque teal RGB(88,120,120). Actual used colour counts are recorded per frame; unused base colours are not artificially forced into artwork. All source poses extracted on the ruler grid and placed without resizing. Crouch is aligned to the original y=109 foot line; later poses rise and change height intentionally. Native PNG, exact 6x nearest-neighbour preview and indexed BMP provided for each.

Method: host image_gen using approved base ruler, both endpoint sprites and preceding intermediate for continuity; repository pixel-looks ask-view/view custom full-body pose extraction, existing runtime WIDE=2048x1024 layout and narrowed strict ruler fit, temporary expanded extraction palette to preserve hues followed by exact original-palette lock. Original gauntlet design, pale upper mane and red trailing appendages are the identity guides. No opponent/debris/effects or new human-like fists intended. No repository/editor source or game-file changes.

These are generated key-pose in-betweens rather than a claim of pixel-identical body parts throughout or a tested smooth animation. Three additional poses reduce the large change in stance, but silhouette, limb lengths, gauntlets and clusters require user visual review. A linear interpolation is not substituted for drawn leg articulation. No game-import compatibility claim.

Published warnings retained verbatim (the upright-view height comparison also flags intentional crouch and airborne poses):
'''
for row in rows:
 report+=f"\nTransition {row['order']}: "+repr(row['record'].get('warnings',[]))+f"; ruler equality {row['record']['read']['lattice']['share'] if 'read' in row['record'] else 'see record'}.\n"
(out/'report.txt').write_text(report)
proc=out/'processing';proc.mkdir();shutil.copytree(r/'ask',proc/'ask-view');shutil.copy2(r/'read.py',proc/'read.py');shutil.copy2(r/'package.py',proc/'package.py')
fs=['exec-2b74b96c-a06a-4bff-8e89-1b9f78c91826.png','exec-df5e8d0a-ce48-42e8-8fc0-d6bace671cf6.png','exec-c732caac-367f-4ac3-bd4a-aadda3b431cb.png']
for n,f in enumerate(fs,1):
 shutil.copytree(r/f'pose-{n}-hues',proc/f'extraction-{n}');shutil.copy2(r/f'prompt-{n}.txt',proc/f'prompt-{n}.txt');shutil.copy2(Path('/workspace/generated_images')/f,proc/f'generated-{n}.png')
(out/'sha256.json').write_text(json.dumps({str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*') if p.is_file()},indent=2));print(json.dumps([{k:v for k,v in row.items() if k!='record'} for row in rows],indent=2))
with zipfile.ZipFile(r/'three-transitions-v001.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in out.rglob('*'):
  if p.is_file():z.write(p,str(p.relative_to(out)))
dst=root/'actions/kick-transition/v001';dst.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(out,dst)
