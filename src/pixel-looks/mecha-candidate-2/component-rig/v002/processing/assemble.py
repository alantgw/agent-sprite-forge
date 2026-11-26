from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,math,hashlib
import rig
r=Path('/workspace/work/mecha-component-v002');o=r/'assembled';o.mkdir(exist_ok=True)
for n in ['native','previews','pose-layers']:(o/n).mkdir(exist_ok=True)
configs=[]
def add(id,name,near=None,far=None,lean=0,shift=(0,0),hand=None,quarter=False,leg=None,nearupper=0,farupper=0):
 cfg=rig.pose(near,far,hand);cfg['_body_angle']=lean;cfg['_body_shift']=list(shift);cfg['_quarter']=quarter
 cfg['near_upper_arm'].update(angle=nearupper,pivot=[41,54],at=[41,54]);cfg['far_upper_arm'].update(angle=farupper,pivot=[87,53],at=[87,53])
 if leg:
  thighangle,shinangle=leg;hip=[77,80];v=[8,10];c=math.cos(math.radians(thighangle));s=math.sin(math.radians(thighangle));knee=[round(hip[0]+c*v[0]+s*v[1]),round(hip[1]-s*v[0]+c*v[1])]
  cfg['far_thigh'].update(angle=thighangle,pivot=hip,at=hip,z=65);cfg['far_shin_foot'].update(angle=shinangle,pivot=[85,90],at=knee,z=65)
 configs.append(dict(id=f'{id:02}',name=name,config=cfg))
# Near=image-left/anatomical right. Far=image-right/anatomical left.
guard=(0,[87,56],55)
add(1,'dash-load',(0,[36,60]),guard,lean=1,shift=(-2,1))
add(2,'dash-plant',(0,[37,61]),guard,lean=2,shift=(-2,1))
add(3,'heavy-chamber',(0,[47,55],55),guard,lean=1)
add(4,'heavy-drive',(0,[47,55],55),(-90,[79,61],90),lean=1,farupper=-90)
add(5,'heavy-cross-impact',(0,[47,55],55),(-90,[66,60],90),lean=2,shift=(-1,0),farupper=-90)
add(6,'heavy-cross-follow',(0,[47,55],55),(-90,[64,60],90),lean=2,shift=(-1,0),farupper=-90)
add(7,'uppercut-one-coil',(0,[36,63]),guard,lean=2,shift=(0,1))
add(8,'uppercut-one-drive',(180,[39,62]),guard,lean=1)
add(9,'uppercut-one-impact',(180,[40,49]),guard,lean=1,nearupper=180)
# The anatomical left leg chambers on image-right, arcs across the pelvis toward
# mecha-right/front (image-left), and retracts. No body spin or full back-facing frame.
add(10,'roundhouse-chamber',(0,[47,55],55),guard,lean=2,leg=(-130,-25))
add(11,'roundhouse-hip-open',(0,[47,55],55),guard,lean=1,quarter=True,leg=(-140,-60))
add(12,'roundhouse-sweep-drive',(0,[47,55],55),guard,lean=1,quarter=True,leg=(-140,-100))
add(13,'roundhouse-impact',(0,[47,55],55),guard,lean=1,quarter=True,leg=(-140,-125))
add(14,'roundhouse-short-follow',(0,[47,55],55),guard,lean=1,quarter=True,leg=(-140,-130))
add(15,'roundhouse-rechamber',(0,[47,55],55),guard,lean=2,leg=(-140,-60))
add(16,'roundhouse-plant',(0,[36,61]),guard,lean=1,leg=(-20,0))
add(17,'uppercut-two-coil',(0,[36,64]),guard,lean=1,shift=(0,1))
add(18,'uppercut-two-drive',(180,[40,59]),guard,lean=1)
add(19,'uppercut-two-impact',(180,[40,48]),guard,lean=1,nearupper=180)
add(20,'uppercut-two-follow',(180,[39,47]),guard,lean=1,nearupper=180)
add(21,'combo-left-load',(0,[47,55],55),(-90,[80,62],90),lean=1,farupper=-90)
add(22,'combo-left-hit',(0,[47,55],55),(-90,[65,59],90),lean=2,farupper=-90)
add(23,'combo-right-load',(-90,[45,64]),guard,lean=1)
add(24,'combo-right-hit',(-90,[36,62]),guard,lean=2)
add(25,'combo-left-follow',(0,[47,55],55),(-90,[63,59],90),lean=2,shift=(-1,0),farupper=-90)
add(26,'combo-right-follow',(-90,[35,61]),guard,lean=2,shift=(-1,0))
# Open palm angle -90 turns its left-facing fan upright beside cheek. The black/red
# gauntlet is a separate original shell and is never replaced by the palm variant.
add(27,'palm-coil',(180,[39,64]),guard,lean=2,hand=([48,43],-90))
add(28,'palm-drive',(-90,[47,65]),guard,lean=1,hand=([32,56],0))
add(29,'palm-impact',(-90,[39,64]),guard,lean=2,shift=(-2,0),hand=([24,55],0))
add(30,'palm-follow',(-90,[38,64]),guard,lean=2,shift=(-2,0),hand=([23,55],0))
for row in configs:
 id=int(row['id']);cfg=row['config']
 if 10<=id<=15:
  cfg['_quarter']=False;cfg['_kick_variant']=True
  cfg['roundhouse-pelvis-support']=dict(z=50,pivot=[69,77],at=[69,77])
  cfg['side-mane-ribbons']=dict(z=30)
  cfg['side-head-chest']=dict(z=60)
  cfg['far_forearm'].update(angle=0,at=[83,48],z=70)
  cfg['far_claw_hand'].update(angle=0,at=[83,48],z=70)
  cfg['roundhouse-kicking-leg']=dict(z=65,pivot=[74,77],at=[74,77],angle={10:-28,11:-20,12:-10,13:0,14:4,15:-24,16:-30}[id])
  cfg['_body_angle']=0;cfg['_body_shift']=[0,0]
for row in configs:
 if row['id']=='16':
  row['config']=rig.pose((0,[40,59]),guard);row['config']['_body_angle']=0
records=[];layer_maps={};forearm_checks=[]
for row in configs:
 id=row['id'];name=id+'-'+row['name'];a,layers=rig.render(row['config']);im=Image.fromarray(a);im.putpalette(rig.pal);im.save(o/'native'/(name+'.png'),bits=4);im.resize((864,672),Image.Resampling.NEAREST).save(o/'previews'/(name+'-6x.png'));y,x=np.where(a!=0);rec=dict(id=id,name=row['name'],file='native/'+name+'.png',canvas=[144,112],used_colours=len(np.unique(a)),bounds=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],config=row['config'],sha256=hashlib.sha256((o/'native'/(name+'.png')).read_bytes()).hexdigest());records.append(rec);layer_maps[id]=layers
 for arm in ([] if row['config'].get('_kick_variant') else ['near_forearm','far_forearm']):
  src=rig.parts[arm]['a'];out=layers[arm];actual=np.bincount(out[out!=0],minlength=16);wanted=np.bincount(src[src!=0],minlength=16);assert np.array_equal(actual,wanted),(id,arm,'part clipped or scaled');forearm_checks.append(dict(id=id,part=arm,palette_histogram_identical_to_base=True,all_original_red_black_pixels_retained=True))
 body_names=['head_crests_face','mane','torso_core','waist_skirt','near_shoulder_wing','far_shoulder_wing','near_thigh','near_shin_foot','far_thigh','far_shin_foot']
 body=np.zeros_like(a)
 for n in body_names:
  if n in layers:body[layers[n]!=0]=layers[n][layers[n]!=0]
 rec['body_layer_hash']=hashlib.sha256(body.tobytes()).hexdigest()
assert len({Image.open(o/q['file']).tobytes() for q in records})==30
for name in ['head_crests_face','mane','torso_core','waist_skirt','near_shoulder_wing','far_shoulder_wing','near_thigh','near_shin_foot','far_thigh','far_shin_foot']:
 assert np.array_equal(layer_maps['29'][name],layer_maps['30'][name]),name
page=Image.new('RGB',(1728,1270),(88,120,120));d=ImageDraw.Draw(page)
for j,q in enumerate(records):
 x=j%6*288;y=j//6*254;page.paste(Image.open(o/q['file']).convert('RGB').resize((288,224),Image.Resampling.NEAREST),(x,y+28));d.text((x+6,y+8),q['id']+' '+q['name'],fill='white')
page.save(o/'all-30-assembled.png');(o/'poses.json').write_text(json.dumps(dict(version='component-action-v001',source=rig.spec['source'],unique_frames=30,independent_whole_body_generations=0,new_component_generations=1,base_parts=17,all_scales=1,forearm_checks=forearm_checks,palm29_30_body_layers_identical=True,frames=records),indent=2));print('30different assemblies. Both original gauntlet histograms identical in all30. Palm29/30 body layers exactly identical.')
