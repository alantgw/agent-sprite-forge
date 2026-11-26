from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np
r=Path('/workspace/work/mecha-impact-v003');p=r/'provisional';p.mkdir(exist_ok=True);pal=Image.open('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/v001/mecha-final-1x.png').getpalette();colors=np.array(pal).reshape(-1,3);allow=np.array([1,2]+list(range(4,16)));plan=json.loads((r/'plan.json').read_text());new=[row for row in plan if row['new']];page=Image.new('RGB',(2160,2232),(88,120,120));d=ImageDraw.Draw(page)
for j,row in enumerate(new):
 id=row['id'];f=r/f'extracted-{id}/pose-{id}.png'
 if not f.exists():continue
 im=Image.open(f).convert('RGBA');a=np.array(im);idx=allow[((a[:,:,:3].astype('int32')[:,:,None,:]-colors[None,None,allow,:])**2).sum(-1).argmin(-1)].astype('uint8');idx[a[:,:,3]==0]=0;h,w=idx.shape;assert w<=140 and h<=112,(id,w,h);x=(144-w)//2;y=max(0,109-h);out=np.zeros((112,144),'uint8');out[y:y+h,x:x+w]=idx;im=Image.fromarray(out);im.putpalette(pal);im.save(p/(id+'.png'),bits=4);cx=j%5*432;cy=j//5*372;d.text((cx+5,cy+5),id+' '+row['name'],fill='white');page.paste(im.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(cx,cy+32))
page.save(r/'new-poses-review.png')
