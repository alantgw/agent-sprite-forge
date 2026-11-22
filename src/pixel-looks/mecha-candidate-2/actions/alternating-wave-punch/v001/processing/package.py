from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,shutil,hashlib
r=Path('/workspace/work/mecha-punch-redesign-v001');o=r/'deliverables';o.mkdir();repo=Path('/workspace/agent-sprite-forge');base=Image.open(repo/'src/pixel-looks/mecha-candidate-2/v001/mecha-final-1x.png');pal=base.getpalette();p=np.array(pal,dtype=np.int32).reshape(-1,3);raw=[];records=[]
for d,n in [('A','right-punch'),('B','left-punch')]:
 a=np.array(Image.open(r/f'extracted-{d}/{n}.png').convert('RGBA'));allowed=np.array([1,2]+list(range(4,16)));idx=allowed[(((a[:,:,:3].astype(np.int32)[:,:,None,:]-p[None,None,allowed,:])**2).sum(-1)).argmin(-1)].astype('uint8');idx[a[:,:,3]==0]=0
 full=np.zeros((112,144),dtype='uint8');h,w=idx.shape;full[109-h:109,136-w:136]=idx;raw.append(full);records.append(json.loads((r/f'extracted-{d}/{n}.json').read_text()))
# Register stable head and legs with integer translation only.
b=raw[1];stable=np.zeros(b.shape,bool);stable[:44]=True;stable[78:]=True;stable&=b!=0;choices=[]
for dy in range(-2,3):
 for dx in range(-2,3):
  tmp=Image.new('L',(144,112));tmp.paste(Image.fromarray(raw[0]),(dx,dy));a=np.array(tmp);choices.append((int(((a==b)&stable).sum()),-abs(dx)-abs(dy),dx,dy,a))
_,_,dx,dy,a=max(choices,key=lambda q:q[:4]);mask=np.zeros(b.shape,bool);mask[44:76]=True
# Preserve shared head, mane, legs and tail. Only arm/chest overlap band changes.
a[~mask]=b[~mask];frames=[];info=[]
for name,x in [('A-right-punch',a),('B-left-punch',b)]:
 im=Image.fromarray(x);im.putpalette(pal);im.save(o/f'{name}-1x.png',bits=4);im.save(o/f'{name}.bmp');im.resize((864,672),Image.Resampling.NEAREST).save(o/f'{name}-6x.png',bits=4);frames.append(im)
 yy,xx=np.where(x!=0);row={'file':name+'-1x.png','canvas':[144,112],'occupied_bounds_exclusive':[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)],'used_colours':len(set(x.ravel().tolist())),'stored_palette_entries':16};info.append(row)
 check=Image.open(o/f'{name}-1x.png');assert check.mode=='P' and check.getpalette()==pal and 'transparency' not in check.info and check.size==(144,112)
fx=Image.open(r/'extracted-fx/chi-wave.png').convert('RGBA');fx.save(o/'chi-wave-1x.png');fx.resize((fx.width*6,fx.height*6),Image.Resampling.NEAREST).save(o/'chi-wave-6x.png')
# Two body drawings, separate moving projectile; 40ms ticks, 200ms per punch.
anchors=[(16,55),(69,56)];stageframes=[];timeline=[]
for t in range(20):
 phase=(t//5)%2;stage=Image.new('RGB',(280,128),tuple(pal[:3]));body=frames[phase].convert('RGBA');ar=np.array(body);ar[np.array(frames[phase])==0,3]=0;body=Image.fromarray(ar);stage.paste(body,(128,8),body)
 # One blast each punch; projectile begins at the current fist then travels left.
 for birth in range(0,t+1,5):
  age=t-birth
  if age>8:continue
  bi=(birth//5)%2;ex,ey=anchors[bi];px=128+ex-fx.width-age*15;py=8+ey-fx.height//2;stage.paste(fx,(px,py),fx)
 stageframes.append(stage.resize((1120,512),Image.Resampling.NEAREST));timeline.append({'tick':t,'body':phase,'tick_ms':40})
stageframes[0].save(o/'firing-loop.gif',save_all=True,append_images=stageframes[1:],duration=40,loop=0,optimize=False,disposal=2)
plain=[im.resize((576,448),Image.Resampling.NEAREST) for im in frames];plain[0].save(o/'pose-only-loop.gif',save_all=True,append_images=plain[1:],duration=200,loop=0,optimize=False,disposal=2)
page=Image.new('RGB',(1296,390),tuple(pal[:3]));draw=ImageDraw.Draw(page)
for i,(im,s) in enumerate(zip([base]+frames,['Approved base / same 3x scale','A: right punch','B: left punch'])):
 draw.text((432*i+12,12),s,fill='white');page.paste(im.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(432*i,38))
page.save(o/'base-and-two-poses.png')
# Ensure GIF encoding retains all intended pixels.
g=Image.open(o/'firing-loop.gif');assert g.n_frames==20
for i,expected in enumerate(stageframes):g.seek(i);assert g.convert('RGB').tobytes()==expected.tobytes()
meta={'version':'v001','art_source':'host_image','route':'built-in image_gen, no paid API invoked','design':'planted alternating short punches; video posture abandoned by user request','frames':info,'body_frame_count':2,'projectile_size':list(fx.size),'character_palette_exactly_matches_approved_base':True,'opaque_background_rgb':pal[:3],'shared_pixels':'all rows outside y44..75 identical between two poses','registration_A_shift':[dx,dy],'emitter_anchors_xy':anchors,'preview':{'body_duration_ms':200,'tick_ms':40,'wave_motion_px_per_tick':15,'loop':'infinite'},'extraction_records':records,'game_import_compatibility':'not verified'};(o/'specification.json').write_text(json.dumps(meta,indent=2))
(o/'README.md').write_text('''# Alternating wave punches — redesigned v001

Two reciprocal, planted short punches using approved Candidate 2 v001 as the body-size and identity reference. The video pose is deliberately abandoned. A punches with the right arm; B with the left arm across the chest. The inactive gauntlet is chambered near the ribs. Head, mane, feet and stance share identical pixels outside the arm/chest band; the character does not bounce between drawings.

![Firing loop](firing-loop.gif)

[Pose-only loop](pose-only-loop.gif) · [Approved base and both poses at equal scale](base-and-two-poses.png)

| Pose | Native PNG | Nearest 6x preview | Indexed BMP |
| --- | --- | --- | --- |
| A: right punch | [PNG](A-right-punch-1x.png) | [Preview](A-right-punch-6x.png) | [BMP](A-right-punch.bmp) |
| B: left punch | [PNG](B-left-punch-1x.png) | [Preview](B-left-punch-6x.png) | [BMP](B-left-punch.bmp) |

Both body canvases are 144×112, indexed with the exact approved 16-entry palette and opaque teal RGB(88,120,120). Actual used colour counts and occupied bounds are in specification.json. Character frames contain no effects. The [separate transparent energy projectile](chi-wave-1x.png) travels away from each gauntlet in the preview. It has its own 3-colour FX palette. The preview uses only two body drawings; extra GIF ticks move the projectile rather than create new body poses. Emission anchors and adjustable timing are documented in specification.json.

Art route: built-in image_gen. Repository pixel-looks ask-view/view with approved master as left-hand grid ruler; strict ruler matches 88.48% and 79.58%, warnings=[] for both. Source dimensions 1774×887; generated cells measured on the master lattice, then palette locked to the original without resizing native cells. Integer registration and a shared-body arm/chest-band composite reduce flicker. This is a custom pose use of ask-view, not a video-generated motion extraction. FX uses pixel_look master, measured 23×13 cells, proportions=blocks; no repeated rows. Its original blocks are rectangular, so the native FX is slightly flatter than the generated picture.

No automatic artistic approval is claimed. Two poses snap directly without wind-up or recovery in-betweens; the GIF illustrates a rapid repeating attack. No game-import compatibility claim. Original base, older attempts and references remain unchanged. Generated sources and extraction records are retained in processing/. Uploaded videos are not included.
''')
proc=o/'processing';proc.mkdir();shutil.copytree(r/'ask',proc/'ask-view');shutil.copy2(r/'read.py',proc/'read.py');shutil.copy2(r/'package.py',proc/'package.py')
for tag,file in [('A','exec-8647ab1c-d0b6-4c3a-8431-354177eaf643.png'),('B','exec-af847cf2-8df4-4141-94d9-60fad7d65c18.png'),('fx','exec-2e79e134-5bbf-43ea-8e5e-363441b26ad8.png')]:
 shutil.copytree(r/f'extracted-{tag}',proc/f'extracted-{tag}');shutil.copy2(Path('/workspace/generated_images')/file,proc/f'generated-{tag}.png')
(proc/'prompt-summary.txt').write_text('A: approved base beside unchanged ruler, planted short horizontal punch, palm down, chamber other beast gauntlet, retain base proportions. First generated take actually extends right arm. B: edit only arms of A to reciprocal cross-body left punch; preserve ruler and common body. FX: isolated white/pink/red left-travelling chi projectile on green, coarse pixel blocks. Host image_gen used original attached images; source outputs retained. ask-view/prompt.txt stores requested initial pose wording; this summary documents actual edits, not a verbatim tool-call transcript.')
(o/'sha256.json').write_text(json.dumps({str(f.relative_to(o)):hashlib.sha256(f.read_bytes()).hexdigest() for f in o.rglob('*') if f.is_file()},indent=2));print(json.dumps(info,indent=2))
