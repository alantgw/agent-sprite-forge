from pathlib import Path
from PIL import Image
import json,hashlib,shutil,zipfile,numpy as np,subprocess
r=Path('/workspace/work/mecha-video-rebuild-v001');o=r/'deliverables';meta=json.loads((o/'specification.json').read_text());timeline=json.loads((o/'timeline.json').read_text());lineup=json.loads((o/'processing/lineup/lineup.json').read_text());warnings=[{'id':q['id'],'source_slot':q['source_slot'],'file':q['file'],'warning':w} for q in meta['frames'] for w in q.get('extraction',{}).get('warnings',[])];ims=[Image.open(o/q['file']) for q in meta['frames']];pal=ims[0].getpalette();assert len({im.tobytes() for im in ims})==30
for q,im in zip(meta['frames'],ims):
 assert im.mode=='P' and im.size==(144,112) and im.getpalette()==pal and 'transparency' not in im.info
 preview=Image.open(o/'previews'/(Path(q['file']).stem+'-6x.png'));assert preview.convert('RGB').tobytes()==im.convert('RGB').resize((864,672),Image.Resampling.NEAREST).tobytes()
 assert q['used_colours']==15
assert all(x['readback_matches'] for x in timeline['gif_checks'])
qa={'unique_native_drawings':30,'new_generated_pose_designs':22,'retained_or_adapted_key_poses':8,'exact_file_copies':6,'reused_punch_endpoints_adapted':2,'generation_attempts':23,'rejected_take':'initial half-punch had oversized gauntlet and covered most of face; replaced by model edit of new chamber pose','canvas':[144,112],'stored_palette_entries':16,'used_colours_all_frames':15,'background_rgb':[88,120,120],'alpha':'fully opaque teal, no transparency','nearest_preview_scale':6,'common_punch_body':'frames06–10 use a shared base-derived head/legs, generated arm poses and2retained strike arm endpoints; integer alignment and documented pixel-restoration mask, no interpolation','gif_checks':timeline['gif_checks'],'extraction_warnings':warnings,'lineup':lineup,'visual_review':'pending user review, not automatically approved by numeric checks','game_import_compatibility':'unverified'};(o/'qa-report.json').write_text(json.dumps(qa,indent=2))
# Source-video provenance without publishing private clips/stills.
paths=json.loads(Path('/workspace/work/mecha-video-ten-v001/videos.json').read_text());vid=[]
for i,path in enumerate(paths,1):
 f=Path(path);d={'part':i,'file_name':f.name,'private_clip_uploaded_to_repository':False}
 if f.exists():
  d['sha256']=hashlib.sha256(f.read_bytes()).hexdigest();probe=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(f)],capture_output=True,text=True,check=True);d['duration_seconds']=float(json.loads(probe.stdout)['format']['duration'])
 vid.append(d)
(o/'video-reference.json').write_text(json.dumps({'clips':vid,'inspection':'six supplied clips; original per-part contact/detail samples inspected for motion, not colour','mapping':'each frame specification lists approximate video_part and video_time; posed transitions interpolate motion hidden by cuts/FX','scope':'character poses only; opponent, VFX, colour grading and cinematic cameras excluded'},indent=2))
(o/'README.md').write_text('''# Video rebuild —30 poses, v001

A newly planned30-drawing moveset from the six-part video and approved base mecha.22 new pose designs;8 suitable key poses retained/adapted with user authorization (6 whole-sprite exact copies,2 existing punch-arm endpoints adapted to the shared base-derived combat body). This is separate from the earlier thirty-sprites/v001 collection. No previous aerial spin-followup cycle is reused.

![Rebuilt moveset](moveset-30.gif)

[Slow15.9s](moveset-30-slow.gif) · [Numbered7.95s](moveset-30-labelled.gif) · [All30 poses](all-30-poses.png) · [30native PNG ZIP](mecha-30-native-only.zip) · [PNG/previews/BMP bundle](mecha-30-individual-sprites.zip)

New sequence: guard/gather power → load/rush → short alternating close-combat block → plant/knee chamber/turning kick → back-facing landing/unwind → uppercut/rising followthrough → coiled aerial pursuit, alternating lead/counter attacks → descending pursuit/recovery/landing → palm reset/windup/drive/hit/followthrough → guard recovery. The5-drawing ground combination repeats2times; the2-drawing airborne attack exchange repeats2times. Holds/repetitions are not counted as extra drawings.

Native PNGs are individually numbered01–30 in native/, each144×112 with the original16-entry palette,15 used colours, fully opaque teal RGB(88,120,120).6x nearest previews and indexed BMPs included. Red eyes explicitly locked; gauntlets remain armoured mechanical shells with original claws. No opponent, beam, aura, impact flash, scenery or UI inside sprites. Prior versions and reference files preserved.

Built-in image_gen and the documented pixel-looks master-ruler workflow: each new pose is generated beside the original approved standing ruler, measured with strict lattice fitting and sampled to1x, then mapped to the original palette. No high-resolution illustration shrinking.23 generation attempts produce22 retained new pose designs; the first half-punch with an oversized gauntlet was rejected and replaced by an edit from the new chamber pose. Sources/prompts/grid records retained under processing/. Five ground-combat poses share protected base-derived head/legs and integer-aligned arm artwork to avoid body flicker; original arm pixels and component restoration are documented. No editor or repository source code changed; no paid APIs.

This is a condensed character-only interpretation, not a literal shot-by-shot or60fps reproduction of the entire clip. Dark video grading, closeup/camera cuts and long effect-only holds are omitted; hidden limb positions require interpretation. Normal7.95s, slow15.9s. Stage384×160 displayed3x nearest. Whole-sprite positions move in integer pixels; held drawings snap, without morphing. Last-to-first is an inspection replay reset. Native-grid simplification loses some tiny generated bevels/claw highlights. Game-import compatibility unverified.

30 different native pixel drawings, original palette/canvas, exact6x previews and all159 intended intervals of3GIFs checked. File checks do not constitute artistic approval; this version is for review. The baseline palette/layout stays fixed, while projected height changes in coiled/airborne poses. Some extended mane/attack poses use up to111 of112canvas rows; no source pixels were clipped or resized.

## Height review records

Standing body's reference height101rows, lineup tolerance1row. `lineup` verdict: `differs`. Exact per-file measurements are in processing/lineup/lineup.json and qa-report.json; frames06–10 share a consistent92-row combat build. New source extraction warnings are retained verbatim:

'''+ '\n'.join('- '+q['id']+' ('+q['file']+'): '+q['warning'] for q in warnings)+'\n\nCapability doctor: optional API credentials, video-generation route and SVG renderer missing; these were not used. Host image generation, supplied-clip inspection and PNG/GIF processing were available. Original clips/stills are private and not redistributed; video-reference.json records provenance.\n')
for f in ['build-demo.py','check-lineup.py','finalize.py','eyes-review.py']:shutil.copy2(r/f,o/'processing'/f)
with zipfile.ZipFile(o/'mecha-30-individual-sprites.zip','w',zipfile.ZIP_DEFLATED) as z:
 for folder in ['native','previews','bmp']:
  for f in sorted((o/folder).glob('*')):z.write(f,str(f.relative_to(o)))
 for name in ['README.md','specification.json','timeline.json','qa-report.json','video-reference.json']:z.write(o/name,name)
with zipfile.ZipFile(o/'mecha-30-native-only.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted((o/'native').glob('*.png')):z.write(f,'native/'+f.name)
(o/'sha256.json').write_text(json.dumps({str(f.relative_to(o)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(o.rglob('*')) if f.is_file() and f.name!='sha256.json'},indent=2));dest=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/actions/shin-ha-gou-shou-sen/video-rebuild/v001');assert not dest.exists();shutil.copytree(o,dest);print(json.dumps({'sprites':30,'new_pose_designs':22,'retained_adapted_keys':8,'duration_ms':timeline['duration_ms'],'lineup':lineup['verdict'],'extraction_warnings':len(warnings),'destination':str(dest),'bytes':sum(f.stat().st_size for f in dest.rglob('*') if f.is_file())},indent=2))
