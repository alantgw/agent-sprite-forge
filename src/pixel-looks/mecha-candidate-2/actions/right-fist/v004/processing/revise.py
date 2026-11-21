from PIL import Image,ImageDraw
from pathlib import Path
import numpy as np
r=Path('/workspace/work/mecha-exact-arm-v001');root=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2');base=Image.open(root/'v001/mecha-final-1x.png');old=Image.open(root/'actions/right-fist/v002/mecha-right-fist-1x.png');pal=base.getpalette();b=np.array(base);a=np.array(old)
mask=Image.new('1',(144,112));ImageDraw.Draw(mask).polygon([(39,52),(40,55),(38,60),(39,67),(36,73),(32,79),(31,84),(26,84),(21,81),(19,76),(21,71),(24,66),(25,61),(26,55),(27,52),(29,52),(30,56),(33,55),(36,52)],fill=1)
m=np.array(mask)&(b!=0);crop=b[51:85,18:41];cm=m[51:85,18:41]
f=a.copy();f[27:69,20:43]=0
# Preserve the exact base armour clusters, reflected vertically as the forearm raises.
tile=np.flipud(crop);tm=np.flipud(cm);x,y=22,29
region=f[y:y+tile.shape[0],x:x+tile.shape[1]];region[tm]=tile[tm]
im=Image.fromarray(f);im.putpalette(pal);im.save(r/'draft.png',bits=4);im.resize((864,672),Image.Resampling.NEAREST).save(r/'draft-6x.png',bits=4)
cut=Image.fromarray(np.where(cm,crop,0).astype('uint8'));cut.putpalette(pal);cut.resize((230,340),Image.Resampling.NEAREST).save(r/'source-arm.png')
