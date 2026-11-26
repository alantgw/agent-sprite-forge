from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np
r=Path('/workspace/work/mecha-thirty-v001');p=r/'provisional';eye={'04':[46,61,49,64],'06':[58,43,61,45],'10':[48,43,51,46],'11':[52,40,56,43],'21':[57,54,60,57],'24':[56,55,60,58],'26':[58,41,62,43],'28':[67,50,71,53],'30':[62,40,65,43]};records={}
for id,box in eye.items():
 im=Image.open(p/(id+'.png'));a=np.array(im);x,y,X,Y=box;e=a[y:Y,x:X].copy()
 for src,dst in [(8,6),(13,11),(9,10),(12,10),(14,10),(15,10)]:e[e==src]=dst
 # Orange sampling in the eye core is remapped to the original red, never armour elsewhere.
 if 11 not in e:
  where=np.argwhere(np.isin(e,[6,10]))
  if len(where):e[tuple(where[len(where)//2])]=11
 assert 11 in e,(id,box,e.tolist());a[y:Y,x:X]=e;out=Image.fromarray(a);out.putpalette(im.getpalette());out.save(p/(id+'.png'),bits=4);records[id]={'eye_box_exclusive':box}
masterfile=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/actions/shin-ha-gou-shou-sen/v010/native/03-combo-chamber-left.png');im=Image.open(masterfile);master=np.array(im);head=Image.new('1',(144,112));poly=[(46,17),(113,17),(115,25),(106,31),(98,45),(83,62),(58,71),(44,64),(32,50),(38,37)];ImageDraw.Draw(head).polygon(poly,fill=1);head=np.array(head);match=head&(master!=0);mask=np.zeros((112,144),bool);mask[28:83]=True;mask&=~head;mask[62:70,42:80]=True;mask[59:62,51:54]=False;mask[70:,105:]=False
for id in ['21','24']:
 generated=np.array(Image.open(p/(id+'.png')));best=None
 for dy in range(-9,10):
  for dx in range(-9,10):
   shifted=np.zeros_like(master);x0=max(0,dx);X=min(144,144+dx);y0=max(0,dy);Y=min(112,112+dy);shifted[y0:Y,x0:X]=generated[y0-dy:Y-dy,x0-dx:X-dx];score=int(((master==shifted)&match).sum());rank=(score,-abs(dx)-abs(dy))
   if best is None or rank>best[0]:best=(rank,dx,dy,shifted)
 _,dx,dy,shifted=best;out=master.copy();out[mask]=shifted[mask];assert np.array_equal(out[~mask],master[~mask]);o=Image.fromarray(out);o.putpalette(im.getpalette());o.save(p/(id+'.png'),bits=4);records[id].update(common_body_source=str(masterfile),arm_mask_rows=[28,83],head_polygon=poly,lower_face_occlusion_box=[42,62,80,70],protected_eye=[51,59,54,62],protected_tail_box=[105,70,144,112],alignment_shift=[dx,dy],head_match_cells=best[0][0],outside_arm_mask_exact=True)
(r/'art-processing.json').write_text(json.dumps(records,indent=2));page=Image.new('RGB',(1728,380),(88,120,120));d=ImageDraw.Draw(page)
for j,id in enumerate(['20','21','24','25']):
 if id in ['21','24']:f=p/(id+'.png')
 else:f=Path(next(q['source'] for q in json.loads((r/'plan.json').read_text()) if q['id']==id))
 pic=Image.open(f);page.paste(pic.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(j*432,32));d.text((j*432+8,8),id,fill='white')
page.save(r/'combo-art-review.png')
