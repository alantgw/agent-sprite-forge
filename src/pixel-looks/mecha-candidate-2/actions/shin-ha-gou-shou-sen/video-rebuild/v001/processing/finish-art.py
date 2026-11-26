from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np
r=Path('/workspace/work/mecha-video-rebuild-v001');p=r/'provisional';eyes={'02':[[60,45,63,47]],'04':[[38,63,41,65]],'05':[[29,65,32,68]],'06':[[54,53,57,56]],'07':[[71,46,75,48]],'10':[[59,38,62,40]],'11':[[51,42,54,44]],'13':[[63,34,65,36]],'14':[[39,48,43,50]],'15':[[69,37,72,39]],'16':[[71,48,75,50]],'17':[[54,60,57,63]],'18':[[57,47,61,50]],'19':[[62,58,66,61]],'20':[[53,60,56,62]],'21':[[53,60,56,62]],'23':[[62,45,65,47]],'25':[[59,37,62,39]],'27':[[69,45,72,47],[77,45,80,47]],'29':[[61,52,65,54]],'30':[[57,45,60,47]]};records={}
for id,boxes in eyes.items():
 im=Image.open(p/(id+'.png'));a=np.array(im)
 for box in boxes:
  x,y,X,Y=box;e=a[y:Y,x:X].copy();hadred=11 in e;hadorange=8 in e
  for src,dst in [(8,6 if hadred else 11),(13,11),(9,10),(12,10),(14,10),(15,10)]:e[e==src]=dst
  if 11 not in e:
   loc=np.argwhere(e==10)
   if len(loc):e[tuple(loc[len(loc)//2])]=11
  assert 11 in e,(id,box,e.tolist());a[y:Y,x:X]=e
 out=Image.fromarray(a);out.putpalette(im.getpalette());out.save(p/(id+'.png'),bits=4);records[id]={'eye_boxes_exclusive':boxes}
# Stabilize the NEW close-combat crouch, not the prior sprite body's pixels.
canonical=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/actions/shin-ha-gou-shou-sen/v010/native/03-combo-chamber-left.png');im=Image.open(canonical);master=np.array(im);head=Image.new('1',(144,112));poly=[(46,17),(113,17),(115,25),(106,31),(98,45),(83,62),(58,71),(44,64),(32,50),(38,37)];ImageDraw.Draw(head).polygon(poly,fill=1);head=np.array(head);match=head&(master!=0);mask=np.zeros((112,144),bool);mask[28:83]=True;mask&=~head;mask[62:70,42:80]=True;mask[59:62,51:54]=False;mask[70:,105:]=False;mask[78:91,43:107]=False
plan={q['id']:q for q in json.loads((r/'plan.json').read_text())}
for id in ['20','21','22','23','24']:
 if plan[id]['new']:source=r/'arm-raw'/ (id+'.png')
 else:source=Path(plan[id]['source'])
 generated=np.array(Image.open(source));best=None
 for dy in range(-12,13):
  for dx in range(-16,17):
   shifted=np.zeros_like(master);x0=max(0,dx);X=min(144,144+dx);y0=max(0,dy);Y=min(112,112+dy);shifted[y0:Y,x0:X]=generated[y0-dy:Y-dy,x0-dx:X-dx];score=int(((master==shifted)&match).sum());rank=(score,-abs(dx)-abs(dy))
   if best is None or rank>best[0]:best=(rank,dx,dy,shifted)
 _,dx,dy,shifted=best;out=master.copy();out[mask]=shifted[mask];assert np.array_equal(out[~mask],master[~mask]);o=Image.fromarray(out);o.putpalette(im.getpalette());o.save(p/(id+'.png'),bits=4);records.setdefault(id,{}).update(common_body_source=str(canonical),new_arm_design=plan[id]['new'],arm_mask_rows=[28,83],head_polygon=poly,lower_face_occlusion_box=[42,62,80,70],eye_lock_box=[51,59,54,62],tail_lock_box=[105,70,144,112],waist_lock_box=[43,78,107,91],integer_alignment=[dx,dy],head_match_cells=best[0][0],outside_mask_exact=True,arm_source=str(source))
(r/'art-processing.json').write_text(json.dumps(records,indent=2));page=Image.new('RGB',(2160,380),(88,120,120));d=ImageDraw.Draw(page)
for j,id in enumerate(['20','21','22','23','24']):
 pic=Image.open(p/(id+'.png'));page.paste(pic.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(j*432,32));d.text((j*432+8,8),id+' shared body / new arm pose',fill='white')
page.save(r/'combat-loop-review.png')
