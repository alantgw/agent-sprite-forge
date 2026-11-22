from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,shutil,hashlib,zipfile
r=Path('/workspace/work/mecha-spin-kick-v001');out=r/'deliverables';out.mkdir(exist_ok=False);root=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2');base=Image.open(root/'v001/mecha-final-1x.png');pal=base.getpalette();p=np.array(pal,dtype=np.int32).reshape(-1,3);labels=['Retract / begin turn','Back-facing half turn','Opposite-side knee chamber','Complete turn / second kick'];rows=[]
for n in range(1,5):
 pose=Image.open(r/f'pose-{n}/spin-{n}.png').convert('RGBA');assert pose.width<=140 and pose.height<=108
 a=np.array(pose);dist=((a[:,:,:3].astype(np.int32)[:,:,None,:]-p[None,None,1:,:])**2).sum(-1);idx=dist.argmin(-1).astype('uint8')+1;idx[a[:,:,3]==0]=0
 at=((144-pose.width)//2,(112-pose.height)//2);im=Image.new('P',(144,112));im.putpalette(pal);im.paste(Image.fromarray(idx),at);im.save(out/f'spin-kick-{n}-1x.png',bits=4);im.save(out/f'spin-kick-{n}.bmp');im.resize((864,672),Image.Resampling.NEAREST).save(out/f'spin-kick-{n}-6x.png',bits=4)
 re=Image.open(out/f'spin-kick-{n}-1x.png');used=len(set(re.get_flattened_data()));assert re.size==(144,112) and re.mode=='P' and re.getpalette()==pal and used<=16 and 'transparency' not in re.info
 assert Image.open(out/f'spin-kick-{n}-6x.png').convert('RGB').tobytes()==re.convert('RGB').resize((864,672),Image.Resampling.NEAREST).tobytes()
 rec=json.loads((r/f'pose-{n}/spin-{n}.json').read_text());rows.append({'order':n,'pose':labels[n-1],'canvas':[144,112],'occupied_size':list(pose.size),'bounds_xyxy_exclusive':[at[0],at[1],at[0]+pose.width,at[1]+pose.height],'stored_palette_entries':16,'used_palette_entries':used,'palette_matches_approved_base':True,'opaque_teal_rgb':pal[:3],'record':rec})
start=root/'actions/airborne-kick/v001/mecha-airborne-kick-1x.png';refs=out/'endpoint';refs.mkdir();shutil.copy2(start,refs/'approved-first-kick-1x.png')
seq=[Image.open(start)]+[Image.open(out/f'spin-kick-{n}-1x.png') for n in range(1,5)];names=['START: approved first kick','1: Retract / turn','2: Back-facing turn','3: Opposite-side chamber','4: Follow-up kick']
page=Image.new('RGB',(2160,390),(88,120,120));d=ImageDraw.Draw(page)
for i,(im,name) in enumerate(zip(seq,names)):
 d.text((i*432+12,12),name,fill='white');page.paste(im.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(i*432,38))
page.save(out/'sequence-review.png')
# Four larger review panels, not a runtime spritesheet.
review=Image.new('RGB',(1152,980),(88,120,120));d=ImageDraw.Draw(review)
for i in range(4):
 x=i%2*576;y=i//2*490;d.text((x+12,y+10),f'{i+1}: {labels[i]}',fill='white');review.paste(Image.open(out/f'spin-kick-{i+1}-1x.png').convert('RGB').resize((576,448),Image.Resampling.NEAREST),(x,y+32))
review.save(out/'four-pose-review.png');video=Path('/tmp/codex-remote-attachments/6afa0878-94f8-8191-9d8f-6674541c9045/B1B7CB73-5BEE-4EE9-B46D-61AFFA48DE08/1-ScreenRecording_11-22-2026-07-34-53_1.mov')
meta={'sequence_order':['endpoint/approved-first-kick-1x.png']+[f'spin-kick-{n}-1x.png' for n in range(1,5)],'new_sprite_count':4,'source_video':{'filename':video.name,'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'duration_seconds':6.74,'inspected_action_region_seconds':[1.1,2.2],'inspection_samples_seconds':[1.12,1.30,1.55,1.78,1.94,2.10],'uploaded_to_repository':False},'sprites':rows,'effects_opponent_ui_excluded_from_sprites':True,'palette_source':'approved Candidate 2 v001','route':'host image_gen and repository pixel-looks ask-view/view grid extraction, then original palette lock','limitations':['Four designed key poses summarize the turn; not a frame-by-frame video trace or an animated transition.','Rear armour hidden in references is inferred from existing plate shapes.','Frames centered on shared native canvas; game-specific root registration and timing remain unverified.','No game-import compatibility claim.']};(out/'specification.json').write_text(json.dumps(meta,indent=2))
report='''Four static mecha-only key poses following approved airborne-kick v001: retract/turn -> rear-facing half-turn -> opposite-side knee chamber -> finish turn and second, higher diagonal kick. This compresses the video move into four readable designed poses, not a claim of exact angular measurements or frame tracing. Rear armour not visible clearly through the video is inferred conservatively from base plates.

The 6.74s user video was inspected as a full contact sequence at 4 fps and at 12 fps over 0.5-2.35s, plus larger samples at 1.12,1.30,1.55,1.78,1.94,2.10s. The action is around 1.1-2.2s. Opponent, impact fire, flashes, energy streaks, screen UI, shadows and other effects excluded from delivered sprites. Only physical mecha armour, limbs, pale upper mane and red attached appendages are represented. Original video and extracted inspection images retained privately in workspace; not republished to repository.

Each PNG is native 144x112 indexed, exact original 16-entry palette, opaque teal RGB(88,120,120). Actual used counts and occupied bounds recorded per sprite. No downscaling of an illustration as the finishing method: existing base stands as a ruler, the model source is read onto its measured pixel grid, foreground colours are locked to approved palette without dithering, and extracted cells are padded onto the canvas without resizing. Previews are exact 6x nearest-neighbour. Four indexed BMPs included. The original first kick is included unchanged for review.

Method: host image_gen, repository pixel-looks ask-view/view custom posed views; existing runtime 2048x1024 ruler layout and narrowed strict fit spread=.15/reach=6. Temporary expanded extraction palette preserves source hues before final original-palette mapping. No repository/editor source or game files modified. These are generated posed views, not literal cut-outs of the base or a tested smooth animation. Body silhouettes and roots change during the turn; game-specific placement, timing and import compatibility are unverified. Visual user review remains necessary. Separate native PNGs are deliverables; contact images are visual review only.

Published workflow height warnings retained verbatim. This tool compares to an upright reference; tucked/spinning bodies intentionally have different vertical extents:
'''
for row in rows:report+=f"\nPose {row['order']}: "+repr(row['record'].get('warnings',[]))+'\n'
(out/'report.txt').write_text(report);proc=out/'processing';proc.mkdir();shutil.copytree(r/'ask',proc/'ask-view');shutil.copy2(r/'read.py',proc/'read.py');shutil.copy2(r/'package.py',proc/'package.py')
fs=['exec-03f28259-0614-4ce0-9965-275a59a0dcda.png','exec-470afa02-0f1f-4285-98d8-1ee69d114dd5.png','exec-5dc665c6-d1c6-404f-ab49-82c2047cd329.png','exec-3288e1f5-eb50-4b20-8cff-eeff29c75771.png']
for n,f in enumerate(fs,1):shutil.copytree(r/f'pose-{n}',proc/f'extraction-{n}');shutil.copy2(r/f'prompt-{n}.txt',proc/f'prompt-{n}.txt');shutil.copy2(Path('/workspace/generated_images')/f,proc/f'generated-{n}.png')
(out/'sha256.json').write_text(json.dumps({str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*') if p.is_file()},indent=2));print(json.dumps([{k:v for k,v in row.items() if k!='record'} for row in rows],indent=2))
with zipfile.ZipFile(r/'four-spin-kick-sprites-v001.zip','w',zipfile.ZIP_DEFLATED) as z:
 for q in out.rglob('*'):
  if q.is_file():z.write(q,str(q.relative_to(out)))
dst=root/'actions/spin-follow-up-kick/v001';dst.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(out,dst)
