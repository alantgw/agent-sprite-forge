from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,shutil,hashlib
r=Path('/workspace/work/mecha-wave-punch-v004');out=r/'deliverables';out.mkdir(exist_ok=False);root=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2');base=Image.open(root/'v001/mecha-final-1x.png');b=np.array(base);pal=base.getpalette();p=np.array(pal,dtype=np.int32).reshape(-1,3)
lm=Image.new('1',(144,112));dr=ImageDraw.Draw(lm)
dr.polygon([(36,76),(60,76),(62,84),(57,91),(55,99),(57,102),(54,106),(40,109),(16,109),(16,101),(22,95),(29,89),(32,83)],fill=1)
dr.polygon([(76,76),(87,76),(91,81),(93,89),(96,96),(103,99),(108,104),(110,109),(80,110),(77,105),(77,99),(75,93),(71,88),(70,82)],fill=1)
legs=np.array(lm)&(b!=0);rows=[];images=[]
for side in ['left','right']:
 pose=Image.open(r/f'master-{side}/{side}-punch.png').convert('RGBA');a=np.array(pose);dist=((a[:,:,:3].astype(np.int32)[:,:,None,:]-p[None,None,1:,:])**2).sum(-1);idx=dist.argmin(-1).astype('uint8')+1;idx[a[:,:,3]==0]=0
 candidates=[]
 for dy in range(0,7):
  if dy+pose.height>112:continue
  for dx in range(8,29):
   if dx+pose.width>144:continue
   tmp=np.zeros((112,144),dtype='uint8');tmp[dy:dy+pose.height,dx:dx+pose.width]=idx
   score=int(((tmp==b)&legs).sum());candidates.append((score,-abs(dy-3)-abs(dx-16),dx,dy))
 score,_,dx,dy=max(candidates);f=np.zeros((112,144),dtype='uint8');f[dy:dy+pose.height,dx:dx+pose.width]=idx
 # Restore original waist, actual leg silhouettes and every source leg/foot colour.
 f[76:,:]=0;f[legs]=b[legs];f[64:79,40:86]=b[64:79,40:86]
 torso_image=Image.new('1',(144,112));ImageDraw.Draw(torso_image).polygon([(50,44),(78,44),(87,48),(86,55),(84,60),(91,64),(93,72),(89,78),(73,82),(54,79),(43,75),(43,66),(48,59),(46,52)],fill=1)
 torso=np.array(torso_image);posed=f.copy();f[torso]=b[torso]
 if side=='left':
  arm=np.zeros(f.shape,dtype=bool);arm[50:63,26:81]=True;arm &= posed!=0;f[arm]=posed[arm]
 assert np.array_equal(f[legs],b[legs])
 im=Image.fromarray(f);im.putpalette(pal);im.save(out/f'{side}-punch-1x.png',bits=4);im.save(out/f'{side}-punch.bmp');im.resize((864,672),Image.Resampling.NEAREST).save(out/f'{side}-punch-6x.png',bits=4);images.append(im)
 re=Image.open(out/f'{side}-punch-1x.png');assert re.mode=='P' and re.size==(144,112) and re.getpalette()==pal and len(set(re.get_flattened_data()))<=16 and 'transparency' not in re.info
 assert Image.open(out/f'{side}-punch-6x.png').convert('RGB').tobytes()==re.convert('RGB').resize((864,672),Image.Resampling.NEAREST).tobytes()
 rows.append({'pose':side+'-arm punch','canvas':[144,112],'palette_entries':16,'used_palette_entries':len(set(re.get_flattened_data())),'palette_matches_base':True,'opaque_teal_rgb':pal[:3],'source_grid_size':list(pose.size),'placement':[dx,dy],'lower_body_restored_from_original_base':True,'waist_and_selected_leg_foot_pixels_identical_to_base':True,'torso_restored_from_base_beneath_foreground_arm':True,'source_master_record':json.loads((r/f'master-{side}/{side}-punch.json').read_text())})
page=Image.new('RGB',(1296,390),(88,120,120));dr=ImageDraw.Draw(page)
for i,(im,label) in enumerate(zip([base]+images,['Approved base','Left punch - base body preserved','Right punch - base body preserved'])):dr.text((432*i+12,10),label+' / same 3x',fill='white');page.paste(im.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(432*i,38))
page.save(out/'base-and-revised-proportions.png');pair=Image.new('RGB',(1152,500),(88,120,120));dr=ImageDraw.Draw(pair)
for i,im in enumerate(images):dr.text((i*576+12,10),['Left-arm punch','Right-arm punch'][i],fill='white');pair.paste(im.convert('RGB').resize((576,448),Image.Resampling.NEAREST),(576*i,36))
pair.save(out/'left-right-comparison.png');(out/'specification.json').write_text(json.dumps({'revision':'v004','intent':'keep original base thickness/proportions by editing approved sprite instead of redesigning body','sprites':rows,'visual_review_required':True,'game_import_compatibility':'not verified'},indent=2))
(out/'README.md').write_text('''# Firing punches — v004, base-body preservation

Edits start from the approved Candidate 2 sprite itself, rather than using thin v002 or over-bulky v003 as body guides. Original central torso, waist and masked leg/foot pixels are restored directly from the base at their original positions. Upper body is reposed without a global thickness stretch.

![Base and revised punches at equal scale](base-and-revised-proportions.png)

[Left native PNG](left-punch-1x.png) · [Left 6x preview](left-punch-6x.png) · [Right native PNG](right-punch-1x.png) · [Right 6x preview](right-punch-6x.png)

144×112 indexed PNGs, original 16-entry palette, opaque teal RGB(88,120,120), exact nearest-neighbour previews and indexed BMPs. No beam/effects. Hair is gathered behind head, not behind feet. Horizontal punches have palm facing down, with a forward torso lean and retracted inactive arm. Original base stance is prioritized over the video's wider lunge to avoid distorting the body.

The upper body remains model-assisted reposing, not a claim of identical upper-body pixels or certified perfect proportions. [Workflow limitation and method](report.txt) · [Specifications](specification.json). No game-import compatibility claim.
''')
(out/'report.txt').write_text('''v004: original approved base provided directly as ask-pose source. No bulky/thin revision used as anatomy authority. Host image_gen reposed upper body with unchanged lower body requested. Strict pose extraction REJECTED these source redraws: only 24% and 23% full-master cells matched, below its 60% gate, so these are not represented as verified surgical pose outputs. The failure was disclosed. The repository pixel-looks master command then measured each source picture's own grid (about9.7-10 source px per cell), extracted one cell per block with --proportions blocks and 32 intermediate colours, followed by exact original-palette mapping. No scaling of extracted sprite cells. Body placement fitted to base lower-leg pixels, then original central torso and waist region plus explicitly masked original legs/feet were restored pixel-for-pixel, preserving the near posed forearm in front of that torso for the left punch. Source hair near the feet was omitted; all final lower-body foreground comes from base leg/waist regions. This preserves actual base lower-body thickness rather than generating a new silhouette. Head/shoulder placement and foreground-arm proportions still need visual user review.

Preview enlargements are exact6x nearest-neighbour. Native PNGs 144x112, original16-entry palette, opaque teal RGB(88,120,120). No image-generation API paid credits used; built-in host_image route. Source master extraction published no warning envelopes; strict pose failures retained in report rather than claimed passed. No ROM, game-file or editor-source changes; no game-import compatibility claim.
''')
proc=out/'processing';proc.mkdir();shutil.copytree(r/'ask-pose',proc/'ask-pose');shutil.copy2(r/'package.py',proc/'package.py')
for side in ['left','right']:shutil.copytree(r/f'master-{side}',proc/f'master-{side}')
for n,filename in enumerate(['exec-1baee942-7e4c-4fd7-b166-ac02363ddc77.png','exec-707570e4-cc7a-4e1d-9d08-eb60c5f7b16f.png'],1):shutil.copy2(Path('/workspace/generated_images')/filename,proc/f'generated-{n}.png');shutil.copy2(r/f'prompt-{n}.txt',proc/f'prompt-{n}.txt')
(out/'sha256.json').write_text(json.dumps({str(q.relative_to(out)):hashlib.sha256(q.read_bytes()).hexdigest() for q in out.rglob('*') if q.is_file()},indent=2));print(json.dumps([{k:v for k,v in row.items() if k!='source_master_record'} for row in rows],indent=2))
