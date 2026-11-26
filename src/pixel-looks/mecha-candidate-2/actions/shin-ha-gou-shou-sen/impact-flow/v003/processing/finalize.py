from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,shutil,zipfile
r=Path('/workspace/work/mecha-impact-v003');o=r/'deliverables';meta=json.loads((o/'specification.json').read_text());tl=json.loads((o/'timeline.json').read_text());lineup=json.loads((o/'processing/lineup/lineup.json').read_text());rows=meta['frames'];pal=Image.open(o/rows[0]['file']).getpalette();warnings=[dict(id=q['id'],warning=w) for q in rows for w in q.get('extraction',{}).get('warnings',[])];used=[]
for q in rows:
 f=o/q['file'];im=Image.open(f);a=np.array(im);assert im.mode=='P' and im.size==(144,112) and im.getpalette()==pal and 'transparency' not in im.info;assert q['sha256']==hashlib.sha256(f.read_bytes()).hexdigest();used.append(len(np.unique(a)));assert used[-1]<=16
 preview=o/'previews'/(f.stem+'-6x.png');assert Image.open(preview).convert('RGB').tobytes()==im.convert('RGB').resize((864,672),Image.Resampling.NEAREST).tobytes()
 if not q['new']:assert f.read_bytes()==Path(q['source']).read_bytes()
assert len({Image.open(o/q['file']).tobytes() for q in rows})==30
assert sum(q['new'] for q in rows)==22
assert sum(q['group']=='dash' for q in rows)==2
assert sum(q['group']=='kick' for q in rows)==7
assert all(t['root_xy'][1]==145 for t in tl['timeline'])
assert all(q['readback_matches'] for q in tl['gif_checks'])
qa=dict(unique_native_drawings=30,new_pose_edits=22,unchanged_sprites=8,dash_drawings=2,attack_drawings=28,rotating_sweep_kick_drawings=7,native_canvas=[144,112],stored_palette_entries=16,actual_used_colours_by_pose=dict(zip([q['id'] for q in rows],used)),background_rgb=[88,120,120],alpha='fully opaque teal',nearest_preview_scale=6,no_jump_attacks=True,animation='Ground baseline fixed at145; support-foot kick anchors and rear-foot palm anchors. No flight/vertical body translation.',gif_checks=tl['gif_checks'],lineup=lineup,extraction_warnings=warnings,alignment_recovery=dict(initial_palm29_error='the picture does not show the master again: only 41 percent of its cells come back equal. Generate again (the prompt asks for the same figure in the same place)',resolution='Expanded ruler alignment search from6px/.15px spread to24px/.3px spread for wide palm references, within upstream default36px/1px. Strict nine-point matching and60% gate unchanged.',final_palm29_ruler_share=rows[28]['extraction']['rulerEqualShare']),visual_review='Draft for user review; dimensions/palette/timing checks do not approve art. Reviewed limb counts, back planes, low lateral kick, planted feet, original mechanical hands and palm readability at1x/nearest scale.',game_import_compatibility='unverified')
(o/'qa-report.json').write_text(json.dumps(qa,indent=2))
old=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/actions/shin-ha-gou-shou-sen/impact-flow/v002/video-reference.json');vid=json.loads(old.read_text());vid.update(user_clarification='Juno was a typo for JUMP ATTACK. Latest instruction overrides previous inferred airborne pursuit: grounded dash, uppercuts and alternating punches.',current_pose_authority='Three latest user screenshots: left-rear body planes, pelvis+torso turning right in a lateral sweeping kick, not front-facing high leg lift.',current_sequence='Forward heavy punch -> uppercut -> rotating horizontal sweep kick -> grounded uppercut -> grounded left/right combination -> palm.',scope='Mecha body only, no enemy/VFX inside sprites. Recoil power interpreted through body mechanics, advancing ground steps and impact holds. Private supplied video/screenshots not redistributed.');(o/'video-reference.json').write_text(json.dumps(vid,indent=2))
# Equal-native-scale review, with labels separate from sprites.
page=Image.new('RGB',(1296,736),(88,120,120));d=ImageDraw.Draw(page)
oldkick=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/actions/shin-ha-gou-shou-sen/impact-flow/v002/native/14-kick-impact.png')
items=[(oldkick,'v002 high kick - replaced'),(o/rows[12]['file'],'v003 left-rear horizontal sweep'),(o/rows[13]['file'],'v003 waist/back turn through'),(o/rows[26]['file'],'27 palm coil - open hand pulled back'),(o/rows[28]['file'],'29 palm heel drive - planted lunge'),(o/rows[29]['file'],'30 palm committed followthrough')]
for j,(f,label) in enumerate(items):
 x=j%3*432;y=j//3*368;page.paste(Image.open(f).convert('RGB').resize((432,336),Image.Resampling.NEAREST),(x,y+28));d.text((x+6,y+7),label,fill='white')
page.save(o/'kick-and-palm-comparison.png')
# Preserve all new art attempts, including rejected takes and original narrow-fit records.
reject=json.loads((r/'rejected-takes.json').read_text());p=o/'processing/rejected';p.mkdir()
for i,q in enumerate(reject['rejected'],1):
 shutil.copy2(q['source'],p/f'{i:02}-{q["id"]}-generated.png');(p/f'{i:02}-{q["id"]}-prompt.txt').write_text(q['prompt'])
(p/'reasons.json').write_text(json.dumps(reject,indent=2));shutil.copytree(r/'initial-palm-alignment',o/'processing/initial-palm-alignment');shutil.copytree(r/'rejected-extra-limb',p/'extra-limb-native-review')
for name in ['plan.json','generation-records.json','rejected-takes.json','doctor.json','ask.py','ask-wide.py','read.py','extract.py','batch-extract.py','prepare.py','package.py','build-demo.py','check-lineup.py','finalize.py','revision-notes.json','setup.py','refine-plan.py','ground-combat.py','palm-wide.py']:
 shutil.copy2(r/name,o/'processing'/name)
shutil.copy2('/workspace/work/mecha-impact-v002/approved-action-reference.png',o/'processing/approved-action-reference.png')
(o/'README.md').write_text('''# Grounded moveset and rear-view sweep — v003

Draft for visual review. Latest correction: **Juno meant jump attack**. Removed airborne pursuit and the extra opening jab; the first heavy punch follows a low ground dash. Seven kick drawings show waist and shoulders turning to the mecha's right, exposing the left-rear body, sweeping laterally below the head and continuing through the back before landing. This replaces the front-facing high leg lift.

![Moveset](moveset-30.gif)

[Slow full moveset](moveset-30-slow.gif) · [Numbered timing view](moveset-30-labelled.gif) · [Enlarged slow rotating kick](rotating-kick-detail.gif) · [Enlarged slow palm](palm-detail.gif) · [Kick/palm comparison](kick-and-palm-comparison.png) · [All30 poses](all-30-poses.png)

[30 individual native PNG ZIP](mecha-30-native-only.zip) · [PNG/nearest previews/indexed BMP bundle](mecha-30-individual-sprites.zip)

Sequence: **前方重拳 → uppercut → rotating horizontal sweep kick → grounded uppercut → 左右連環拳 → 掌擊**.30 distinct drawings:2 dash,4 heavy punch,3 first uppercut,7 rotating kick,4 second uppercut,6 ground combination,4 palm.22 new edits and8 byte-identical retained sprites. The6-drawing combination repeats3times. There is no separate jab before the heavy punch, no jumping or airborne attack and no idle/power-up padding. The support leg stays under the rotating kick; native body drawings and GIF positions are not lifted into flight.

The palm has a clearly withdrawn open-hand coil, short hip drive, upright palm-heel impact in a planted forward lunge, then committed followthrough. The rear foot stays fixed in the motion preview. Coil440ms, drive80ms, impact280ms, follow440ms; force comes from pose contrast, waist/shoulder/leg drive and impact holds. No visual effects were added to substitute for the pose. The normal complete move is5.36s, slow10.72s; detail clips2.48s each. End-to-start is an inspection replay reset.

Native files in native/ are144×112 indexed PNGs with the exact original16-entry palette,15 colours actually used per file, opaque teal RGB(88,120,120).6x previews are exact nearest-neighbour; indexed BMPs included. Original red-eye palette retained; faces hidden by rear view/mane are not invented. Sprites contain only the mecha, no opponent, energy wave, aura, trails, flashes, dust, scenery, shadow or UI. Labels in the optional timing/review images are outside the sprites. No engine import compatibility is claimed.

Art source: built-in host image_gen, model not reported by tool; no paid API used. Existing approved base/punch/palm construction is the identity reference. Repository pixel-looks ask-view/view workflow: original standing master on left gives scale/grid; new action on right. Initial image-generation canvas2048×1024, palm references widened to2304×1024 to keep fingers out of the ruler exclusion area. These are source reference canvases only; native output remains144×112. Generated grid is measured and sampled, then mapped to the original palette and padded by whole native pixels; no arbitrary illustration shrinking, body stretching or coded redraw.7 kick poses use support-foot registration; palms use rear-foot registration; other poses use their original ground canvas origin. No vertical flight offsets or morphing.

26 image requests:22 retained drawings,3 rejected art takes and1 provider error retried successfully through the same host route. Rejected takes: swapped open-palm arm, fingers entering the ruler exclusion margin, extra clawed appendage at waist. The initially valid back-recovery drawing was reassigned to slot16; a new full-back recovery fills15. Sources, prompts, requests, native extraction reviews, rejected art and initial alignment records are preserved under processing/. Original base/reference files and all earlier versions remain unchanged. Existing editor/game/tool source code was not modified. Private supplied video and screenshots are not published.

## Quality review and limits

30 different native drawings, fixed original canvas/palette/opaque background, exact6x nearest previews and all intended time intervals in5GIFs were verified by decoding the saved GIFs back to RGB. Limb counts and silhouette/hand/foot construction were visually inspected, including the rejected extra appendage. These checks do not constitute the user's artistic approval. Hidden back armour is simplified/interpreted from the supplied left-rear screenshot and base; separately drawn rotating views can vary in projected mane/armour shape. This is a condensed pose interpretation, not1:1 video staging or60fps motion. Small bevels/claw details simplify at1x.

Palm29 initially failed ruler registration with `the picture does not show the master again: only 41 percent of its cells come back equal. Generate again (the prompt asks for the same figure in the same place)`. A larger alignment search recovers the shifted ruler, within the upstream default search window; the strict nine-point equality and60% gate are unchanged. Final match is recorded in qa-report.json. No threshold was lowered and no pipeline substitution was made.

The lineup result is **differs**, not a pass: standing master body101rows, tolerance1row. Exact per-file heights are retained in processing/lineup/ and qa-report.json. Crouched/leaned/back projections and the narrow foot-column height detector (especially25) differ from the standing column; source/native side-by-side reviews remain available. All new-source height warnings are retained verbatim below:

'''+ '\n'.join('- '+q['id']+': '+q['warning'] for q in warnings)+'\n\nCapability doctor: host image generation and supplied-clip decoding available. Optional API credentials, SVG renderer and video-generation route are missing and were not used. No ROM, game image or editor source modified.\n')
for bundle,folders in [('mecha-30-native-only.zip',['native']),('mecha-30-individual-sprites.zip',['native','previews','bmp'])]:
 with zipfile.ZipFile(o/bundle,'w',zipfile.ZIP_DEFLATED) as z:
  for folder in folders:
   for f in sorted((o/folder).glob('*')):z.write(f,str(f.relative_to(o)))
  for name in ['README.md','specification.json','timeline.json','qa-report.json','video-reference.json']:z.write(o/name,name)
(o/'sha256.json').write_text(json.dumps({str(f.relative_to(o)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(o.rglob('*')) if f.is_file() and f.name!='sha256.json'},indent=2))
dest=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/actions/shin-ha-gou-shou-sen/impact-flow/v003');assert not dest.exists();shutil.copytree(o,dest);print(json.dumps(dict(destination=str(dest),unique_drawings=30,new=22,reused=8,dash=2,kick_phases=7,no_jump_attacks=True,duration_ms=tl['duration_ms'],used_colour_counts=sorted(set(used)),lineup=lineup['verdict'],source_height_warnings=len(warnings)),indent=2))
