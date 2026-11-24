from pathlib import Path
from PIL import Image
import numpy as np,shutil,json,hashlib,subprocess
r=Path('/workspace/work/mecha-sequence-v008');o=r/'deliverables';repo=Path('/workspace/agent-sprite-forge');p=o/'processing/lineup-inputs';p.mkdir();master=repo/'src/pixel-looks/mecha-candidate-2/v001/mecha-final-1x.png'
for f in [*sorted((o/'native').glob('*.png')),master]:
 im=Image.open(f);a=np.array(im);im=im.convert('RGBA');im.putalpha(Image.fromarray((a!=0).astype('uint8')*255));im.save(p/f.name)
args=['python',str(repo/'skills/generate2dsprite/scripts/pixel_look.py'),'lineup','--master',str(p/master.name)]
for f in sorted(p.glob('[0-9]*.png')):args+=['--item',str(f)]
args+=['--output-dir',str(o/'processing/lineup')];subprocess.run(args,check=True)
for n in ['moveset-demonstration.gif','moveset-demonstration-slow.gif','timeline.json','motion-overview.png']:shutil.copy2(r/'demo-build'/n,o/n)
shutil.copy2(r/'build-demo.py',o/'processing/build-demo.py');shutil.copy2(r/'finalize.py',o/'processing/finalize.py');rec=json.loads((r/'extracted-07-forward/pose-07.json').read_text());lineup=json.loads((o/'processing/lineup/lineup.json').read_text())
(o/'README.md').write_text('''# v008 — forward upper body, far-side rising kick

07 revised for visual review: torso leans forward rather than backward. The left thigh, knee, shin and toes turn together toward the robot-relative right-up direction, away from the camera. Foot uses side armour/profile rather than a broad sole facing the screen. Original left-facing character orientation, body palette and red eyes retained.

![Kick](previews/07-forward-far-side-kick-6x.png)

![Full animation](moveset-demonstration.gif)

[Slow animation](moveset-demonstration-slow.gif) · [Latest04 punch](previews/04-combo-left-hit-6x.png) · [All10 poses](all-ten-poses.png)

Latest04 is byte-identical tov005 long-punch/lower-face-occlusion artwork. All9 other native sprites are unchanged fromv007. Sequence: dash → revised kick → grounded uppercut → left/right punch loop ×4 → palm finish. No opponent/effects.144×112 indexed native PNG, original16-entry palette,15 used colours, opaque teal RGB(88,120,120),6x nearest PNG and indexed BMP.

Built-in image_gen edit, repository pixel-looks ruler/lattice extraction, original-palette mapping and red-eye lock. No illustration resizing or source-code edits. Source, prompt and extraction records preserved; all previous versions retained. Game-import compatibility unverified.

'''+'Extraction warnings (verbatim):\n\n'+('\n'.join('- '+w for w in rec.get('warnings',[])) or 'None.')+'\n\nLineup verdict: '+lineup['verdict']+'. Standing body height101, tolerance1. Full per-file height flags are retained in processing/lineup/lineup.json; crouched/rotated poses require visual review rather than automatic approval.\n\nBoth full GIFs decoded and compared over all118 intended tick intervals. Normal5.9s, slow11.8s; integer whole-sprite movement with held key poses. Finish-to-start is an inspection replay reset.\n')
(o/'qa-report.json').write_text(json.dumps({'latest04':'exact byte copy ofv005','nine_other_native_files':'unchanged fromv007','07_extraction':rec,'lineup':lineup,'gif_decode':'passed118 intervals normal/slow','visual_review':'pending'},indent=2))
(o/'sha256.json').write_text(json.dumps({str(f.relative_to(o)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(o.rglob('*')) if f.is_file() and f.name!='sha256.json'},indent=2))
d=repo/'src/pixel-looks/mecha-candidate-2/actions/shin-ha-gou-shou-sen/v008';assert not d.exists();shutil.copytree(o,d)
