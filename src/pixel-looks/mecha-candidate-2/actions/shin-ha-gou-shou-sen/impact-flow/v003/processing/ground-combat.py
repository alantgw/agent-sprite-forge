from pathlib import Path
from PIL import Image
import numpy as np,json,subprocess
r=Path('/workspace/work/mecha-impact-v003');old=Path('/workspace/work/mecha-impact-v002');a=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/actions');plan=json.loads((r/'plan.json').read_text());(r/'plan-before-no-jump.json').write_text(json.dumps(plan,indent=2))
poses={
'18':('ground-uppercut-two-drive','SECOND UPPERCUT drive upward-left with BOTH FEET FIRMLY PLANTED, knees bent opening into hip drive, torso forward, closed right fist from image-left at chin height, opposite clenched hand guards ribs. No leap, no tucked airborne knees.'),
'19':('ground-uppercut-two-impact','SECOND UPPERCUT IMPACT upward-left from grounded wide stance, both feet planted and rear heel drives, right closed fist just above forehead and bent elbow, hips/chest rotate upward with no jump. Opposite fist near ribs. Compact body, head between broad shoulders.'),
'21':('ground-combo-left-load','GROUND COMBO left punch LOAD: original common wide planted stance, both feet on floor in exactly same positions as seed. Left closed fist chambered near chest/shoulder, right clenched hand guards cheek, torso leans20degrees forward with waist coiled. No jump, no tucked knees.'),
'22':('ground-combo-left-hit','GROUND COMBO LEFT cross-body punch HIT toward image-left at chin height. Left arm from image-right shoulder crosses chest and lower face, short thick forearm, original curled gold knuckles lead left, opposite right hand pulled beside shoulder partly hidden. Both feet stay planted in seed common stance. Forward waist/shoulder drive, no jump.'),
'23':('ground-combo-right-load','GROUND COMBO right punch DRIVE halfway left at chin height, elbow bent, left hand retracts to shoulder/chest partly occluded. Original curled gold knuckles and forearm armour, original common stance with BOTH FEET PLANTED in same positions as seed. Waist turns into right punch, no jump.'),
'24':('ground-combo-right-hit','GROUND COMBO RIGHT punch HIT left at chin level, right hand from image-left shoulder nearly extends, original gold curled knuckles and forearm armour, left closed hand pulled near shoulder/ribs. SAME planted wide common stance and broad forward torso, both feet on floor, no jump.'),
'25':('ground-combo-left-pursuit','GROUND COMBO LEFT heavy cross punch slightly down-left at chest height; waist rotates more into strike, torso inclines forward25degrees, rear toe pushes and front foot plants a short follow-up STEP. Both feet stay close to floor, never flying. Active left forearm crosses chest, right closed hand at shoulder partly occluded. Original broad body and short thick arms.'),
'26':('ground-combo-right-pursuit','GROUND COMBO RIGHT heavy punch slightly up-left at lower-face height, waist rotates into strike, front knee bends and rear foot drives a short follow-up STEP with ground contact. Right fist has original gold curled knuckles, left hand chambered near ribs, same broad body and original planted stance. No jump or flight.')}
for row in plan:
 id=row['id']
 if id in poses:
  row['name'],row['pose']=poses[id];row['new']=True
  seed=a/('alternating-wave-punch/v004/left-punch-1x.png' if id in ['21','22','25'] else 'alternating-wave-punch/v004/right-punch-1x.png')
  if id in ['18','19']:seed=Path(plan[8]['source'])
  row['pose_seed']=str(seed);row['request']=str(r/'requests'/id)
  subprocess.run(['python',str(r/'ask.py'),'ask-view','--master',str(old/'ask-28/master.png'),'--cell','8','--key','green','--view-words',row['pose'],'--output-dir',row['request']],check=True,capture_output=True)
  im=Image.open(seed);arr=np.array(im);ys,xs=np.where(arr!=0);box=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1));crop=im.convert('RGB').crop(box);mask=Image.fromarray((arr!=0).astype('uint8')*255).crop(box);w,h=crop.size;out=Image.open(Path(row['request'])/'reference.png').convert('RGB');out.paste(crop.resize((w*8,h*8),Image.Resampling.NEAREST),(1024+(1024-w*8)//2,920-h*8),mask.resize((w*8,h*8),Image.Resampling.NEAREST));out.save(Path(row['request'])/'seed-reference.png')
 if id=='20':row['name']='ground-uppercut-two-follow';row['pose']='Grounded upward followthrough, both feet planted; source pose reused, stage remains grounded.'
(r/'plan.json').write_text(json.dumps(plan,indent=2));print('No jumping poses in revised plan. New22, reused8.')
