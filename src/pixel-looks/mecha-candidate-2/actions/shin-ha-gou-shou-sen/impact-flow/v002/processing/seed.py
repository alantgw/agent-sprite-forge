from pathlib import Path
from PIL import Image
import numpy as np,json
r=Path('/workspace/work/mecha-impact-v002');a=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/actions');plan=json.loads((r/'plan.json').read_text())
for row in plan:
 if not row['new']:continue
 id=row['id'];n=int(id)
 if n in range(3,8):source=a/'shin-ha-gou-shou-sen/v010/native/04-combo-left-hit.png'
 elif n in [8,9,11,17,18,19,20]:source=a/'shin-ha-gou-shou-sen/v010/native/08-grounded-uppercut.png'
 elif n in [12,13,15,16]:source=a/'shin-ha-gou-shou-sen/v008/native/07-forward-far-side-kick.png'
 elif n in [21,22,25]:source=a/'alternating-wave-punch/v004/left-punch-1x.png'
 elif n in [23,24,26]:source=a/'alternating-wave-punch/v004/right-punch-1x.png'
 else:source=a/'shin-ha-gou-shou-sen/v010/native/10-palm-release.png'
 im=Image.open(source);arr=np.array(im);ys,xs=np.where(arr!=0);box=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1));cropped=im.convert('RGB').crop(box);mask=Image.fromarray((arr!=0).astype('uint8')*255).crop(box);w,h=cropped.size;out=Image.open(r/f'ask-{id}/reference.png').convert('RGB');at=(1024+(1024-w*8)//2,920-h*8);out.paste(cropped.resize((w*8,h*8),Image.Resampling.NEAREST),at,mask.resize((w*8,h*8),Image.Resampling.NEAREST));out.save(r/f'ask-{id}/seed-reference.png');row['pose_seed']=str(source)
(r/'plan.json').write_text(json.dumps(plan,indent=2))
