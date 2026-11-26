from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
r=Path('/workspace/work/mecha-component-v002');o=r/'new-parts';base=Image.open('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/v001/mecha-final-1x.png');pal=base.getpalette()
src=Image.open('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/actions/shin-ha-gou-shou-sen/v010/native/07-selected-turning-kick.png');v=np.array(src)
# Only previously selected left-rear upper body and ribbons; old raised leg and human-like guard excluded.
m=Image.new('1',(144,112));ImageDraw.Draw(m).polygon([(4,1),(89,1),(89,34),(81,41),(79,50),(85,55),(79,65),(72,73),(68,80),(59,87),(36,91),(19,81),(10,64)],fill=1);mask=np.array(m)
for n,sel in [('side-mane-ribbons',(np.indices(v.shape)[1]<38)|((np.indices(v.shape)[0]>69)&(np.indices(v.shape)[1]<72))),('side-head-chest',None)]:
 if sel is None:sel=~(((np.indices(v.shape)[1]<38)|((np.indices(v.shape)[0]>69)&(np.indices(v.shape)[1]<72))))
 a=np.where(mask&sel,v,0).astype('uint8');im=Image.fromarray(a);im.putpalette(pal);im.save(o/(n+'-indexed.png'),transparency=0,bits=4);im.convert('RGBA').save(o/(n+'.png'))
# Mirror only the NEW lower-body angle, not the character's frontal base.
for n in ['roundhouse-kicking-leg','roundhouse-pelvis-support']:
 im=Image.open(o/(n+'-indexed.png'));im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT);im.save(o/(n+'-indexed.png'),transparency=0,bits=4);im.convert('RGBA').save(o/(n+'.png'))
