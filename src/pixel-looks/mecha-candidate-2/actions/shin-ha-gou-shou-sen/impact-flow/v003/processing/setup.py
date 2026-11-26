from pathlib import Path
import json,subprocess,shutil
r=Path('/workspace/work/mecha-impact-v003');old=Path('/workspace/work/mecha-impact-v002');published=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/actions/shin-ha-gou-shou-sen/impact-flow/v002');prior=json.loads((published/'specification.json').read_text());plan=[]
poses={
'01':('ground-dash-drive','Low forward grounded dash into first heavy punch, facing image-left, leading foot skims ground and rear toe pushes; body forward with both actual closed fists chambered, no jumping or flying.'),
'02':('ground-dash-plant','Plant the forward step facing image-left, both feet close to ground, wide compact low body, left shoulder loaded for heavy cross; no separate jab.'),
'03':('heavy-chamber','Grounded heavy cross WINDUP, no jab: left fist pulled near shoulder/ribs, right hand guards cheek, knees bent and hips coiled to drive forward. Keep short thick arms and broad base proportions.'),
'12':('rotation-kick-coil','Start clockwise rotating sweep kick: waist starts turning to mecha own right, LEFT-REAR quarter comes into view, left knee crosses low across pelvis; support right knee bent, torso forward. This is horizontal rotation, not high upward kicking.'),
'13':('rotation-kick-drive','Drive lateral sweeping left leg from left to right about waist height as hips rotate right; camera mainly sees LEFT-REAR body and back shoulder armour, chest hidden, torso also turns. Foot stays below chin and knee follows sweep.'),
'14':('rotation-kick-impact','Rotating horizontal sweep kick IMPACT: left-rear view, waist and torso turning right together, left leg extends laterally at waist/lower-chest height below chin; no rising high kick.'),
'15':('rotation-kick-through','Follow through clockwise sweep kick, back and left-rear body predominant, pelvis and torso turn farther right with leg sweeping across low, foot below chest. Supporting shin short angular and foot broad; no lean backward.'),
'16':('rotation-kick-land','Land after sweep kick with back/left-rear still visible, left leg retracting down from waist height, right support knee absorbs torque, shoulder and waist turn into next uppercut. No extra kick or jump.'),
'27':('palm-deep-coil','Power palm windup, facing image-left: clear wide grounded low lunge, torso twisted away, active mechanical palm pulled close beside rear ribs, fingers open, opposite hand guards cheek. The palm is NOT already extended. Rear leg loads and hips coil.'),
'28':('palm-hip-drive','Power palm drive facing image-left: rear foot pushes, hips rotate forward and shoulder follows; open articulated palm moves halfway out at chest height, wrist straight, elbow still bent. Keep original gauntlet behind wrist, visibly separated open fingers and gold claw tips, no forearm-nose substitute.'),
'29':('palm-root-impact','Power palm IMPACT facing image-left: broad deep braced lunge, front knee bent, rear leg drives straight through hip, strong forward torso; active arm nearly extended horizontal at face height, PALM HEEL leading left with open articulated clawed hand upright and clear at native scale. Fingers spread, short gold tips, original mechanical hand and forearm from approved palm. Opposite fist tight by ribs. Head/chin partly behind upper arm, not leaning back. No beam or hit FX.'),
'30':('palm-driven-follow','Power palm committed followthrough left: same open palm fully forward, body lower and shoulder/waist turned farther into hit, rear heel drives, near knee braced and chest forward. Keep actual articulated palm open, no pointed armour tip as hand; complete mane/ribbons stream right. Hold attack, not idle.')}
for q in prior['frames']:
 id=q['id'];row=dict(id=id,name=q['name'],group=q['group'],new=id in poses,source=str(published/q['file']))
 if id in poses:
  row['name'],row['pose']=poses[id]
  if id in ['01','02','03']:seed=published/prior['frames'][3]['file']
  elif id in ['12','13','14','15','16']:seed=published/prior['frames'][13]['file']
  else:seed=published/prior['frames'][28]['file']
  row['pose_seed']=str(seed)
  subprocess.run(['python',str(r/'ask.py'),'ask-view','--master',str(old/'ask-28/master.png'),'--cell','8','--key','green','--view-words',row['pose'],'--output-dir',str(r/f'ask-{id}')],check=True,capture_output=True)
 plan.append(row)
(r/'plan.json').write_text(json.dumps(plan,indent=2))
for f in ['extract.py','batch-extract.py','prepare.py','package.py','check-lineup.py']:
 s=(old/f).read_text().replace('mecha-impact-v002','mecha-impact-v003');(r/f).write_text(s)
(r/'revision-notes.json').write_text(json.dumps({'corrections':['ground dash into heavy punch, no extra lead jab','waist+torso clockwise rotation and left-rear body planes, horizontal sweep below head','palm deep windup, hip/shoulder drive, leg bracing and distinct palm heel'], 'not_changed':'144x112 original palette, opaque teal, no effects/enemy inside sprites; earlier versions and original references preserved','reference_canvas':'2048x1024 to fit original112x102 ruler at8px cells; native canvas unchanged'},indent=2))
print('Prepared',len(poses),'new pose requests,',30-len(poses),'unchanged slots')
