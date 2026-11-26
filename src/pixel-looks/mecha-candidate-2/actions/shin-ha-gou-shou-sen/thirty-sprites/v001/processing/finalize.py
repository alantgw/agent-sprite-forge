from pathlib import Path
from PIL import Image
import json,hashlib,shutil,zipfile,numpy as np
r=Path('/workspace/work/mecha-thirty-v001');o=r/'deliverables';meta=json.loads((o/'specification.json').read_text());timeline=json.loads((o/'timeline.json').read_text());lineup=json.loads((o/'processing/lineup/lineup.json').read_text());warnings=[]
for row in meta['frames']:
 for w in row.get('extraction',{}).get('warnings',[]):warnings.append({'id':row['id'],'file':row['file'],'warning':w})
qa={'native_frames':30,'distinct_pixel_drawings':30,'new_generations':10,'existing_drawings':20,'existing_byte_identical':18,'legacy_eye_only_palette_corrections':['17','18'],'canvas':[144,112],'stored_palette_entries':16,'used_palette_entries_per_frame':{row['id']:row['used_colours'] for row in meta['frames']},'opaque_teal_rgb':[88,120,120],'nearest_previews_scale':6,'all_frames_fit_native_canvas':True,'original_long_left_punch':'frame22 byte-identical to latestv005/v01004','combo_shared_body':'20–25 exact protected head/feet outside documented arm mask;21/24 generated arms aligned by integer translation only','gif_readback_checks':timeline['gif_checks'],'extraction_warnings':warnings,'lineup':lineup,'visual_review':'draft for user review; numerical checks do not approve artwork','game_import_compatibility':'unverified'}
# Palette, no crop, unchanged known endpoints, uniqueness, fixed preview sampling.
ims=[Image.open(o/row['file']) for row in meta['frames']];pal=ims[0].getpalette();assert len({im.tobytes() for im in ims})==30
for row,im in zip(meta['frames'],ims):
 assert im.mode=='P' and im.size==(144,112) and im.getpalette()==pal and 'transparency' not in im.info
 assert row['used_colours']<=16;preview=Image.open(o/'previews'/(Path(row['file']).stem+'-6x.png'));assert preview.size==(864,672) and preview.convert('RGB').tobytes()==im.convert('RGB').resize((864,672),Image.Resampling.NEAREST).tobytes()
assert all(c['readback_matches'] for c in timeline['gif_checks']);(o/'qa-report.json').write_text(json.dumps(qa,indent=2))
(o/'README.md').write_text('''# Thirty-pose moveset — v001

30 unique144×112 sprite PNGs representing the established six-part video moveset with extra connecting drawings.10 newly generated poses and20 previously base-derived drawings (18 copied byte-for-byte,2 legacy spin-eye palettes corrected). The approved Candidate2v001 is the visual ruler and identity master. Latest long left punch with lower-face occlusion and accepted palm ending stay unchanged. Bothv008 forward kick and user-selectedv010 turning kick are included.

![Full30-pose moveset](moveset-30.gif)

[Slow17.6s GIF](moveset-30-slow.gif) · [Numbered8.8s GIF](moveset-30-labelled.gif) · [All30 poses](all-30-poses.png) · [Individual PNG ZIP](mecha-30-individual-sprites.zip)

Sequence: standing/guard/power coil → dash → knee chamber → rising kick → turning kick → back-facing landing and unwind → uppercut and aerial pursuit/turn/kick → landing → six-pose left/right punch cycle repeated4times → palm settle/charge/extension/release → recovery.

Thirty distinct native drawings are used; repeated combo cycles and held frames do not count as extra drawings. Native PNGs in native/ (one pose per file),6x nearest-neighbour previews in previews/, indexed BMPs in bmp/. Original16-entry palette,15 actual colours including opaque teal RGB(88,120,120). No opponent, energy beam, aura, hit flash, scenery or UI inside native sprites. Pixel outlines and original red eyes retained. No game-import compatibility claim.

The10 new transitions cover dash anticipation, knee chamber, back landing, unwind, uppercut preparation, left/right half strikes, palm settle, half release and recovery. Built-in image_gen uses a wide master-ruler reference; strict repository pixel-looks lattice extraction turns each measured cell into one native pixel, then original palette mapping. No illustration downscaling.21/24 align generated arms by integer translation and restore the common20 head/legs/tail outside a documented arm mask so the six-pose punch loop keeps a common body. No source-code edits or paid APIs. Original and generated sources, prompts, lattice checks and wrappers retained under processing/; previous versions remain intact. Private video frames are not redistributed.

Motion is a condensed staging interpretation of the supplied video plus the established approved kick/spin/punch choices, rather than literal44-second/60fps reproduction. Normal8.8s, slow17.6s. Stage384×160 displayed3x nearest; sprites remain144×112. Static key drawings snap without morphing; whole-sprite positions move on integer pixels.30unique drawings,4combo cycles. Finish-to-start is a deliberate inspection replay reset. Clean GIF uses the original16-entry palette; numbered GIF has extra colours only outside the stage.

All3 GIFs were decoded and matched against all176 intended time intervals. Native palette/canvas,30-pose uniqueness and exact6x preview pixels verified. Numerical checks establish file integrity, not artistic approval. This version is for review.

## Height review flags

Standing body reference101rows; lineup tolerance1row. `lineup` verdict is `differs` for crouches, kicks and airborne poses. Full per-file measurements are in processing/lineup/lineup.json and qa-report.json. The six-pose punch block20–25 is consistently92rows. Drawing height changes with pose; full camera/body continuity still needs visual review. New extraction warnings are retained verbatim below:

'''+ '\n'.join('- '+q['id']+' ('+q['file']+'): '+q['warning'] for q in warnings)+'\n\nThe doctor reports missing optional API credentials, video-generation route and SVG renderer; none is used. Host image generation and supplied-clip inspection were available.\n')
for f in ['build-demo.py','check-lineup.py','finalize.py']:shutil.copy2(r/f,o/'processing'/f)
# Runtime download stays small; full source/provenance remains in the repository.
with zipfile.ZipFile(o/'mecha-30-individual-sprites.zip','w',zipfile.ZIP_DEFLATED) as z:
 for folder in ['native','previews','bmp']:
  for f in sorted((o/folder).glob('*')):z.write(f,str(f.relative_to(o)))
 for name in ['README.md','specification.json','timeline.json','qa-report.json']:z.write(o/name,name)
with zipfile.ZipFile(o/'mecha-30-native-only.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted((o/'native').glob('*.png')):z.write(f,'native/'+f.name)
(o/'sha256.json').write_text(json.dumps({str(f.relative_to(o)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(o.rglob('*')) if f.is_file() and f.name!='sha256.json'},indent=2));dest=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/actions/shin-ha-gou-shou-sen/thirty-sprites/v001');assert not dest.exists();shutil.copytree(o,dest);print(json.dumps({'native_count':30,'new_drawings':10,'duration_ms':timeline['duration_ms'],'lineup_verdict':lineup['verdict'],'warnings':len(warnings),'repo_destination':str(dest),'bundle_bytes':sum(f.stat().st_size for f in dest.rglob('*') if f.is_file())},indent=2))
