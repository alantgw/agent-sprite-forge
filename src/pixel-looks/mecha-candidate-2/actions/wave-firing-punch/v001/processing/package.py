from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,shutil,hashlib,zipfile
r=Path('/workspace/work/mecha-wave-punch-v001');out=r/'deliverables';out.mkdir(exist_ok=False);root=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2');base=Image.open(root/'v001/mecha-final-1x.png');pal=base.getpalette();palette=np.array(pal,dtype=np.int32).reshape(-1,3);frames=[];rows=[];labels=['Left-arm firing punch','Right-arm firing punch'];stems=['left-punch','right-punch']
for n in range(1,3):
 pose=Image.open(r/f'pose-{n}/punch-{n}.png').convert('RGBA');assert pose.width<=132 and pose.height<=103
 a=np.array(pose);dist=((a[:,:,:3].astype(np.int32)[:,:,None,:]-palette[None,None,1:,:])**2).sum(-1);idx=dist.argmin(-1).astype('uint8')+1;idx[a[:,:,3]==0]=0
 full=np.zeros((112,144),dtype='uint8');full[7:7+pose.height,7:7+pose.width]=idx;frames.append(full)
# Same viewpoint and supporting body: only arm and connecting chest regions change.
armmask=np.zeros((112,144),dtype=bool)
for x0,y0,x1,y1 in [(7,39,62,67),(60,49,100,74),(96,47,116,80)]:armmask[y0:y1,x0:x1]=True
second=frames[0].copy();second[armmask]=frames[1][armmask];frames[1]=second;assert np.array_equal(frames[0][~armmask],frames[1][~armmask])
for n,(a,stem) in enumerate(zip(frames,stems),1):
 im=Image.fromarray(a);im.putpalette(pal);im.save(out/f'{stem}-1x.png',bits=4);im.save(out/f'{stem}.bmp');im.resize((864,672),Image.Resampling.NEAREST).save(out/f'{stem}-6x.png',bits=4)
 re=Image.open(out/f'{stem}-1x.png');assert re.mode=='P' and re.size==(144,112) and re.getpalette()==pal and len(set(re.get_flattened_data()))<=16 and 'transparency' not in re.info
 assert Image.open(out/f'{stem}-6x.png').convert('RGB').tobytes()==re.convert('RGB').resize((864,672),Image.Resampling.NEAREST).tobytes()
 mask=Image.new('L',im.size);mask.putdata([255 if q else 0 for q in im.get_flattened_data()]);rec=json.loads((r/f'pose-{n}/punch-{n}.json').read_text());rows.append({'pose':labels[n-1],'native_file':stem+'-1x.png','canvas':[144,112],'bounds_xyxy_exclusive':mask.getbbox(),'palette_entries':16,'used_palette_entries':len(set(re.get_flattened_data())),'palette_identical_to_base':True,'opaque_teal_rgb':pal[:3],'workflow_record':rec})
page=Image.new('RGB',(1152,500),(88,120,120));d=ImageDraw.Draw(page)
for i,stem in enumerate(stems):d.text((i*576+15,10),labels[i]+' - mecha only',fill='white');page.paste(Image.open(out/f'{stem}-1x.png').convert('RGB').resize((576,448),Image.Resampling.NEAREST),(i*576,36))
page.save(out/'left-right-punch-comparison.png')
video=Path('/tmp/codex-remote-attachments/6afa0878-94f8-8191-9d8f-6674541c9045/85E897F6-260C-4835-B392-3758E422A991/1-ScreenRecording_11-22-2026-07-58-46_1.mov');meta={'poses':rows,'same_viewpoint_and_direction':True,'direction':'viewers left for both','not_a_whole_sprite_mirror':True,'pixels_outside_arm_and_chest_regions_identical_between_poses':True,'video_colours_copied':False,'palette_source':'approved Candidate 2 v001 original palette','beam_and_all_effects_excluded':True,'video':{'filename':video.name,'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'duration_seconds':2.281667,'inspected_at_fps':10,'pose_reference_times_seconds':[.3,.7],'published':False},'route':'host image_gen; repository pixel-looks ask-view/view; exact original-palette lock; region-limited arm swap','game_import_compatibility':'not verified'};(out/'specification.json').write_text(json.dumps(meta,indent=2))
report='''Two static firing-punch poses from approved Candidate 2: anatomical left arm reaches across chest, then anatomical right arm extends from the far/viewer-left shoulder while left retracts. Both face and shoot toward viewers left from same camera; not a whole-character mirror. Only mecha poses; light wave, beam, flare, glow, trails, screen UI and all other effects excluded.

USER COLOUR REQUIREMENT: original approved base colours retained; video used only for body/arm placement. Original 16-entry indexed palette matches byte-for-byte, opaque teal RGB(88,120,120). Actual used counts recorded per pose. No video dark/red lighting copied. Head, legs and physical trailing strands identical between final sprites; arm/connecting chest regions carry the swap. These are model-assisted posed edits rather than literal cut-outs of the base.

Method: video inspected at 2fps overview and 10fps close-ups, with .3s and .7s crops as pose-only references. Built-in host image_gen followed by repository ask-view/view on measured master ruler grid, existing 2048x1024 intermediate accommodation and narrowed strict fitting, expanded intermediate palette then exact base-palette lock. Both source takes were 1774x887. Native grid images padded at the same integer position without resizing. Previews are exact 6x nearest-neighbour; indexed BMPs included. No editor/source/game files modified. Video and screenshots retained locally, not republished to repository.

Published upright-height warnings (crouched forward-lean pose deliberately shorter vertically, retained for visual review):
'''
for n,row in enumerate(rows,1):report+=f"\nPose {n}: "+repr(row['workflow_record'].get('warnings',[]))+'\n'
report+='\nNo claim of frame-perfect video tracing, tested smooth animation or game-import compatibility.\n';(out/'report.txt').write_text(report)
proc=out/'processing';proc.mkdir();shutil.copytree(r/'ask',proc/'ask-view');shutil.copy2(r/'read.py',proc/'read.py');shutil.copy2(r/'package.py',proc/'package.py')
fs=['exec-d878a20b-c192-4d89-9451-a5a7e96e5529.png','exec-86af62a5-0bdd-4743-a8ae-c9e87957e2ac.png']
for n,f in enumerate(fs,1):shutil.copytree(r/f'pose-{n}',proc/f'extraction-{n}');shutil.copy2(r/f'prompt-{n}.txt',proc/f'prompt-{n}.txt');shutil.copy2(Path('/workspace/generated_images')/f,proc/f'generated-{n}.png')
(out/'sha256.json').write_text(json.dumps({str(q.relative_to(out)):hashlib.sha256(q.read_bytes()).hexdigest() for q in out.rglob('*') if q.is_file()},indent=2));print(json.dumps([{k:v for k,v in row.items() if k!='workflow_record'} for row in rows],indent=2))
