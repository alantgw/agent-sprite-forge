from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,shutil,zipfile
r=Path('/workspace/work/mecha-impact-v002');o=r/'deliverables';meta=json.loads((o/'specification.json').read_text());tl=json.loads((o/'timeline.json').read_text());lineup=json.loads((o/'processing/lineup/lineup.json').read_text());warnings=[dict(id=q['id'],warning=w) for q in meta['frames'] for w in q.get('extraction',{}).get('warnings',[])];pal=Image.open(o/meta['frames'][0]['file']).getpalette();used=[]
for q in meta['frames']:
 f=o/q['file'];im=Image.open(f);a=np.array(im);assert im.mode=='P' and im.size==(144,112) and im.getpalette()==pal and 'transparency' not in im.info;assert q['sha256']==hashlib.sha256(f.read_bytes()).hexdigest();used.append(len(np.unique(a)))
 preview=o/'previews'/(f.stem+'-6x.png');assert Image.open(preview).convert('RGB').tobytes()==im.convert('RGB').resize((864,672),Image.Resampling.NEAREST).tobytes()
 if not q['new']:assert f.read_bytes()==Path(q['source']).read_bytes()
assert len({Image.open(o/q['file']).tobytes() for q in meta['frames']})==30
assert len([q for q in meta['frames'] if q['group']=='dash'])==2
assert len([q for q in meta['frames'] if q['new']])==23
assert list(dict.fromkeys(q['group'] for q in meta['frames']))==['dash','heavy','uppercut1','kick','uppercut2','combo','palm']
assert all(x['readback_matches'] for x in tl['gif_checks'])
qa=dict(unique_native_drawings=30,new_generated_drawings=23,unchanged_approved_attack_endpoints=5,unchanged_dash_drawings=2,canvas=[144,112],stored_palette_entries=16,actual_used_colours_by_pose=dict(zip([q['id'] for q in meta['frames']],used)),background_rgb=[88,120,120],alpha='fully opaque teal',nearest_previews=6,gif_checks=tl['gif_checks'],lineup=lineup,extraction_warnings=warnings,visual_review='Draft for user review. Numeric checks do not approve anatomy or motion.',hand_review='Compared every pose to approved punch/palm/uppercut art. Articulated curled knuckles and open digits allowed; solid pointed cap hands rejected.',game_import_compatibility='unverified')
(o/'qa-report.json').write_text(json.dumps(qa,indent=2))
old=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/actions/shin-ha-gou-shou-sen/video-rebuild/v001/video-reference.json');vid=json.loads(old.read_text());vid.update(inspection='Revisited original parts3,4,5 at closer time intervals for enemy displacement and attack order; all six clips retained privately.',mapping='Heavy front strike -> uppercut -> rising kick -> second uppercut -> alternating pursuit punches -> palm. Hit direction and pauses are interpreted; no 1:1 timing/physics claim.',observations=['Part3 around4.8-5.0s: forward heavy hit, enemy driven away.','Part3 around6.4-6.6s: uppercut lifts enemy.','Part3 around6.6-7.0s: kick pushes enemy farther back/up.','Part3 around7.2-7.6s: second uppercut launches enemy high.','Part4: airborne pursuit contacts; actor follows the target rather than punching in place.','Part5: finishing palm; long effects/camera cuts condensed.'],scope='Mecha-only pose PNGs. Separate outlined target diagram demonstrates designed recoil, not opponent artwork. No private video/still copied into repository.');(o/'video-reference.json').write_text(json.dumps(vid,indent=2))
# Compare native art at equal scale; approved references on the left, revised poses beside them.
a=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/actions');rows=[[(a/'alternating-wave-punch/v004/left-punch-1x.png','Approved LEFT punch'),(o/meta['frames'][3]['file'],'04 revised cross-body drive'),(o/meta['frames'][21]['file'],'22 revised airborne LEFT')],[(a/'shin-ha-gou-shou-sen/v010/native/10-palm-release.png','Approved PALM - reused as29'),(o/meta['frames'][27]['file'],'28 revised palm drive'),(o/meta['frames'][29]['file'],'30 revised palm follow')],[(a/'shin-ha-gou-shou-sen/v008/native/07-forward-far-side-kick.png','Retained kick - reused as14'),(o/meta['frames'][12]['file'],'13 revised kick drive'),(o/meta['frames'][14]['file'],'15 revised support leg')]]
page=Image.new('RGB',(1296,1104),(88,120,120));d=ImageDraw.Draw(page)
for j,row in enumerate(rows):
 for i,(f,label) in enumerate(row):
  x=i*432;y=j*368;page.paste(Image.open(f).convert('RGB').resize((432,336),Image.Resampling.NEAREST),(x,y+28));d.text((x+6,y+7),label,fill='white')
page.save(o/'approved-and-revised.png')
for f in ['plan.json','generation-records.json','read.py','extract.py','prepare.py','seed.py','package.py','build-demo.py','check-lineup.py','finalize.py','revision-notes.json']:
 shutil.copy2(r/f,o/'processing'/f)
for f in ['approved-action-reference.png','approved-kick-uppercut.png']:shutil.copy2(r/f,o/'processing'/f)
shutil.copy2('/workspace/work/mecha-impact-v001/doctor.json',o/'processing/doctor.json')
rejected=json.loads(Path('/workspace/work/mecha-impact-v001/generation-records.json').read_text());(o/'processing/rejected-v001-manifest.json').write_text(json.dumps({'status':'rejected for hand construction; source images preserved unchanged in workspace','records':rejected},indent=2))
shutil.copy2('/workspace/generated_images/exec-889fa398-0055-4395-89cd-0fadfa9fa55c.png',o/'processing/rejected-first-04-pilot.png')
(o/'README.md').write_text('''# Impact flow v002 — articulated-hand revision

Draft for visual review. Corrected after the rigid shield/capsule hands in the previous unpublished draft were rejected. The visual authority is the user's previously approved punches, uppercut and palm artwork: closed fingers form gold-tipped knuckles; an open palm has actual articulated digits. Forearm armour stays behind the wrist. Hand-like articulation is allowed. Supporting kick legs use the retained kick's segmented knee/shin/ankle/foot structure.

![Moveset](moveset-30.gif)

[Slow clean GIF](moveset-30-slow.gif) · [Approved/revised comparison](approved-and-revised.png) · [All30 poses](all-30-poses.png) · [30 individual native PNGs](mecha-30-native-only.zip) · [PNG/previews/BMP bundle](mecha-30-individual-sprites.zip)

Sequence: **前方重拳 → uppercut → kick → uppercut → 左右連環拳 → 掌擊**. Two dash drawings,28 attacking drawings (including attack preparation, drive and links). No idle/power-up/neutral recovery padding. The6-pose pursuit block repeats3times; repetitions are timing uses, not extra drawings.30 distinct native drawings:23 new pose edits,5 byte-identical approved attack endpoints and2 byte-identical dash poses. The retained left-facing v8 kick keeps the same target side; the separate v10 right-facing option is preserved unchanged in its existing directory.

Every native PNG is144×112, indexed with the exact original16-entry palette and opaque teal RGB(88,120,120). Actual used colours are recorded per file in specification.json/qa-report.json;16 palette entries does not mean16 colours necessarily occur.6x previews use nearest-neighbour. Indexed BMPs included. Native sprites contain only the mecha: no target, beam, aura, hit flashes, scenery, UI or cast shadow. Original colours and red-eye design retained; occluded eyes are not painted over the forearm/jaw.

The separate [hit-reference GIF](hit-reference.gif) and [slow version](hit-reference-slow.gif) add a simple outlined TARGET box only as a motion diagram. Recoil/lift and integer pursuit offsets show the designed hit reference from the video, not a physical simulation, enemy drawing or1:1 recreation. Main GIF is clean. Heavy contacts have held impact poses; alternating airborne punches chase left with vertical variations; palm produces the largest final displacement. Normal duration and exact timing are in timeline.json. End-to-start is an inspection replay reset.

Processing uses built-in image_gen edits and repository pixel-looks ask-view/view: original approved standing ruler on left, approved action seed on right, approved articulated-hand reference board. Each generated picture is measured on the ruler's lattice and sampled to1x; no arbitrary illustration shrinking. Native cells map to the approved palette, then receive only integer canvas padding. New sources, prompts, seeds, extraction records and review images are retained under processing/. Original reference files and older versions remain unchanged. The rigid-hand v001 draft and rejected pilot remain preserved in the workspace; the manifest records them. No editor/game source or ROM changes, no paid API used. Game-import compatibility is unverified.

Visual limits: condensed pose interpretation where video effects obscure limbs; some small joint/claw details simplify on the native grid; separately generated poses can vary in projected head/mane shape. Numeric file checks are not artistic approval. All30 hand/foot constructions were inspected against approved artwork. Extended punches can obscure the lower face, and coiled/airborne projection changes measured height.

## Recorded height review

The lineup tool reports `differs` against the101-row standing master. It uses a1-row tolerance and does not recognize all angled/occluded feet reliably. Per-frame heights and exact extraction warnings are retained in qa-report.json and processing/lineup/. Warnings are not suppressed or represented as passing art approval:

'''+ '\n'.join('- '+q['id']+': '+q['warning'] for q in warnings)+'\n\nCapability doctor: supplied-video decoding and host image generation available; optional API credentials, SVG renderer and video-generation route were not used. Private source clips/stills are not redistributed.\n')
for bundle,folders in [('mecha-30-native-only.zip',['native']),('mecha-30-individual-sprites.zip',['native','previews','bmp'])]:
 with zipfile.ZipFile(o/bundle,'w',zipfile.ZIP_DEFLATED) as z:
  for folder in folders:
   for f in sorted((o/folder).glob('*')):z.write(f,str(f.relative_to(o)))
  for name in ['README.md','specification.json','timeline.json','qa-report.json','video-reference.json']:z.write(o/name,name)
(o/'sha256.json').write_text(json.dumps({str(f.relative_to(o)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(o.rglob('*')) if f.is_file() and f.name!='sha256.json'},indent=2));dest=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/actions/shin-ha-gou-shou-sen/impact-flow/v002');assert not dest.exists();shutil.copytree(o,dest);print(json.dumps(dict(destination=str(dest),new=23,reused=7,drawings=30,dash=2,attack=28,used_colour_counts=sorted(set(used)),duration_ms=tl['duration_ms'],lineup=lineup['verdict'],warnings=len(warnings)),indent=2))
