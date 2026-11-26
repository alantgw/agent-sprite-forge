from pathlib import Path
from PIL import Image
import numpy as np,subprocess,json
r=Path('/workspace/work/mecha-impact-v002');o=r/'deliverables';p=o/'processing/lineup-inputs';p.mkdir();master=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/v001/mecha-final-1x.png')
for f in [*sorted((o/'native').glob('*.png')),master]:
 im=Image.open(f);a=np.array(im);im=im.convert('RGBA');im.putalpha(Image.fromarray((a!=0).astype('uint8')*255));im.save(p/f.name)
args=['python','/workspace/agent-sprite-forge/skills/generate2dsprite/scripts/pixel_look.py','lineup','--master',str(p/master.name)]
for f in sorted(p.glob('[0-9]*.png')):args+=['--item',str(f)]
args+=['--output-dir',str(o/'processing/lineup')];result=subprocess.run(args,check=True,capture_output=True,text=True);record=json.loads(result.stdout);print(json.dumps({'verdict':record['verdict'],'masterHeight':record['masterHeight'],'heights':{Path(k).name:v for k,v in record['heights'].items()}},indent=2))
