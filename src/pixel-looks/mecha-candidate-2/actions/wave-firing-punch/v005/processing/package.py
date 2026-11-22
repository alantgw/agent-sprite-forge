from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,shutil,hashlib
r=Path('/workspace/work/mecha-wave-punch-v005');out=r/'deliverables';out.mkdir(exist_ok=False);root=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2');base=Image.open(root/'v001/mecha-final-1x.png');pal=base.getpalette();p=np.array(pal,dtype=np.int32).reshape(-1,3);rawframes={};records={}
for key in ['A','B']:
 im=Image.open(r/f'extracted-{key}/frame-{key}.png').convert('RGBA');a=np.array(im);d=((a[:,:,:3].astype(np.int32)[:,:,None,:]-p[None,None,1:,:])**2).sum(-1);idx=d.argmin(-1).astype('uint8')+1;idx[a[:,:,3]==0]=0;full=np.zeros((112,144),dtype='uint8');at=(136-im.width,109-im.height);full[at[1]:at[1]+im.height,at[0]:at[0]+im.width]=idx;rawframes[key]=full;records[key]=json.loads((r/f'extracted-{key}/frame-{key}.json').read_text())
# Register frame A's fixed body to B before using only its arms.
b=rawframes['B'];stable=np.zeros(b.shape,dtype=bool);stable[:45,:]=True;stable[80:,:]=True;stable &= b!=0
choices=[]
for dy in range(-3,4):
 for dx in range(-3,4):
  im=Image.fromarray(rawframes['A']);shift=Image.new('L',(144,112));shift.paste(im,(dx,dy));v=np.array(shift);choices.append((int(((v==b)&stable).sum()),-abs(dx)-abs(dy),dx,dy,v))
score,_,dx,dy,registered=max(choices,key=lambda x:x[:4]);maskim=Image.new('1',(144,112));ImageDraw.Draw(maskim).polygon([(15,45),(61,45),(61,58),(90,58),(92,48),(116,48),(122,61),(117,77),(91,78),(89,72),(57,72),(48,66),(15,65)],fill=1);armmask=np.array(maskim)
# Keep head/face, body silhouette, stance and hair exactly common. Shoulder/chest overlaps may alternate with arms.
left=b.copy();left[armmask]=registered[armmask];right=b.copy()
from scipy.ndimage import label
components,count=label(left!=0,structure=np.ones((3,3)));sizes=np.bincount(components.ravel());sizes[0]=0;main=int(sizes.argmax());fragments=(components!=0)&(components!=main);assert np.all(armmask[fragments]);removed_fragments=int(fragments.sum());left[fragments]=0
assert np.array_equal(left[~armmask],right[~armmask]);assert np.array_equal(left[:45],right[:45]);assert np.array_equal(left[80:],right[80:])
frames=[];rows=[]
for name,a,label in [('frame-A-left-punch',left,'A: left punch / right retracts'),('frame-B-right-punch',right,'B: right punch / left retracts')]:
 im=Image.fromarray(a);im.putpalette(pal);im.save(out/f'{name}-1x.png',bits=4);im.save(out/f'{name}.bmp');im.resize((864,672),Image.Resampling.NEAREST).save(out/f'{name}-6x.png',bits=4);frames.append(im)
 re=Image.open(out/f'{name}-1x.png');assert re.mode=='P' and re.size==(144,112) and re.getpalette()==pal and len(set(re.get_flattened_data()))<=16 and 'transparency' not in re.info
 assert Image.open(out/f'{name}-6x.png').convert('RGB').tobytes()==re.convert('RGB').resize((864,672),Image.Resampling.NEAREST).tobytes();rows.append({'file':name+'-1x.png','pose':label,'canvas':[144,112],'palette_entries':16,'used_palette_entries':len(set(re.get_flattened_data())),'palette_matches_approved_base':True,'opaque_teal_rgb':pal[:3]})
# Diagnostic animation only: the requested deliverables remain exactly two sprite frames.
for filename,ms,scale in [('alternating-preview.gif',140,4),('alternating-preview-slow.gif',260,4)]:
 enlarged=[im.resize((144*scale,112*scale),Image.Resampling.NEAREST) for im in frames];enlarged[0].save(out/filename,save_all=True,append_images=enlarged[1:],duration=[ms,ms],loop=0,optimize=False,disposal=2)
 check=Image.open(out/filename);assert check.n_frames==2 and check.info['loop']==0
page=Image.new('RGB',(1152,500),(88,120,120));dr=ImageDraw.Draw(page)
for i,im in enumerate(frames):dr.text((i*576+15,10),rows[i]['pose'],fill='white');page.paste(im.convert('RGB').resize((576,448),Image.Resampling.NEAREST),(i*576,36))
page.save(out/'two-frame-comparison.png');cmp=Image.new('RGB',(1296,390),(88,120,120));dr=ImageDraw.Draw(cmp)
for i,(im,txt) in enumerate(zip([base]+frames,['Approved base','A: left punch','B: right punch'])):dr.text((i*432+12,10),txt+' / same3x',fill='white');cmp.paste(im.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(i*432,38))
cmp.save(out/'base-and-loop-frames.png')
meta={'revision':'v005','purpose':'two reciprocal poses for repeated A-B-A-B punching, not independent poses','sequence':['frame-A-left-punch-1x.png','frame-B-right-punch-1x.png'],'frames':rows,'pixels_outside_arm_chest_mask_identical_between_frames':True,'head_upper_hair_identical':True,'hips_legs_feet_identical':True,'shared_body_source':'frame B, with lower loose strands removed','arm_chest_mask_polygon':[(15,45),(61,45),(61,58),(90,58),(92,48),(116,48),(122,61),(117,77),(91,78),(89,72),(57,72),(48,66),(15,65)],'frame_A_registration_shift':[dx,dy],'changed_pixels_between_frames':int((left!=right).sum()),'detached_composite_fragment_pixels_removed':removed_fragments,'preview_timing_ms_per_frame':140,'slow_preview_ms_per_frame':260,'preview_loop':'infinite; illustrative timing, not fixed playback requirement','effects':'none','game_import_compatibility':'not verified','workflow_records':records};(out/'specification.json').write_text(json.dumps(meta,indent=2))
(out/'README.md').write_text('''# Alternating punch loop — v005

Exactly **two sprites** built to alternate **A → B → A → B**: left-arm punch/right-arm recovery, then right-arm punch/left-arm recovery. A common forward-leaning body is retained so the stance, head, hips, feet and hair do not jump. Arm/shoulder/chest overlap pixels carry the exchange. Forearms are reworked toward the original base thickness, rather than the thin v004 arms.

![Alternating punch preview](alternating-preview.gif)

[Slow inspection loop](alternating-preview-slow.gif) · [Two-frame comparison](two-frame-comparison.png) · [Equal-scale base comparison](base-and-loop-frames.png)

| Frame | Native PNG | 6× preview | Indexed BMP |
| --- | --- | --- | --- |
| A: left punch | [PNG](frame-A-left-punch-1x.png) | [Preview](frame-A-left-punch-6x.png) | [BMP](frame-A-left-punch.bmp) |
| B: right punch | [PNG](frame-B-right-punch-1x.png) | [Preview](frame-B-right-punch-6x.png) | [BMP](frame-B-right-punch.bmp) |

144×112 indexed PNGs, exact original 16-entry palette, opaque teal RGB(88,120,120). Actual used counts are recorded in specification.json. Preview scaling is integer nearest-neighbour. Both punches remain horizontal with palm down, original armoured gauntlet identity and no beam/光波 effects. All lower loose hair has been omitted, strands sit behind/up from head.

GIFs are diagnostic previews made from the same two PNGs; no additional animation frames or runtime sprite sheet. Preview speed is adjustable: 140ms per pose (normal), 260ms (slow); both repeat indefinitely. Two-frame motion necessarily snaps between extension and retraction; no interpolation or unrequested extra sprites are claimed. Body/gauntlet anatomy still requires visual user review, not automatic approval. Original base is unchanged; no game-import compatibility claim.

[Method and checks](report.txt) · [Specifications](specification.json)
''')
(out/'report.txt').write_text('''v005 rebuild for alternating loop rather than independent stills. Host image_gen used approved base and pose-only video crop; second take exchanged arms and removed lower loose hair. Model also removed lower hair from left ruler in second source; strict ruler fit still passed, and this difference is not presented as cell-identical source preservation. Repository pixel-looks ask-view/view custom pose extraction, existing2048x1024 layout, narrowed strict fitter, expanded intermediate colours then exact original-palette lock. Final grid cells are not resized. Common frame B body retained, A aligned against stable head/leg cells then only documented arm/chest polygon composited. Detached composite fragments inside that polygon removed (26 pixels); no standing/body cells altered by cleanup. All pixels outside that polygon are verified exactly identical, including upper head/hair and legs/feet. No old upright base torso patch used to overwrite leaning body. Original palette exact; no dark video tint copied. No editor/source/game files changed.\nBoth source view extractions returned warnings=[]; their ruler matches were88.85% and72.55%. These numerical results do not establish artistic quality. GIFs have exactly2 frames, infinite loop and documented timing; both use nearest-neighbour scaling. Two-frame toggling has no transition in-betweens and may appear abrupt. Repeat count/speed are not inferred from the ambiguous phrase1x times; previews loop indefinitely and the two PNGs can be repeated any count. No game-import compatibility claim.\n''')
proc=out/'processing';proc.mkdir();shutil.copytree(r/'ask',proc/'ask-view');shutil.copy2(r/'read.py',proc/'read.py');shutil.copy2(r/'package.py',proc/'package.py')
for key,f in [('A','exec-6c008a90-08ee-482c-9340-21750e02ed14.png'),('B','exec-3bde408b-c7af-4176-97e5-439a93a931af.png')]:shutil.copytree(r/f'extracted-{key}',proc/f'extracted-{key}');shutil.copy2(r/f'prompt-{key}.txt',proc/f'prompt-{key}.txt');shutil.copy2(Path('/workspace/generated_images')/f,proc/f'generated-{key}.png')
(out/'sha256.json').write_text(json.dumps({str(q.relative_to(out)):hashlib.sha256(q.read_bytes()).hexdigest() for q in out.rglob('*') if q.is_file()},indent=2));print(json.dumps({k:v for k,v in meta.items() if k!='workflow_records'},indent=2))
