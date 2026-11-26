from pathlib import Path
import json,subprocess,shutil
r=Path('/workspace/work/mecha-impact-v003');old=Path('/workspace/work/mecha-impact-v002');pub=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/actions/shin-ha-gou-shou-sen/impact-flow/v002');prior=json.loads((pub/'specification.json').read_text())['frames'];initial=json.loads((r/'plan.json').read_text());(r/'plan-initial.json').write_text(json.dumps(initial,indent=2));plan=[]
kicks={
'10':('sweep-kick-load','Kick LOAD immediately after uppercut. Face image-left, torso inclines forward; left knee just crosses pelvis at waist height, hands close to ribs, planted right knee bends. Waist starts turning to its right, shoulders lag. Original FRONT-LEFT body mostly visible, but left back shoulder edge begins to turn into view. No high kick, foot not extended.'),
'11':('sweep-kick-left-rear','Quarter-turn COIL of sweep kick: LEFT-REAR half of body and large left back shoulder plane now visible, chest mostly hidden. Head still looks over left shoulder toward image-left. Waist/pelvis have rotated to mecha own right more than shoulders. Left knee held across LOW waist, shin folded. Supporting right foot pivots; both closed hands guard shoulders. Foot stays below waist/chest, no vertical kick.'),
'12':('sweep-kick-drive','DRIVE horizontal rotating kick LEFT TO RIGHT: camera sees LEFT-REAR body as waist and torso turn right together. Head follows toward image-right, left leg partly extends laterally RIGHT at waist height with knee still bent. Foot and shin point right together below chin; angular support leg and broad planted foot. Most chest hidden, actual left back armour visible.'),
'13':('sweep-kick-impact','Horizontal rotating sweep IMPACT to image-right from LEFT-REAR view. Pelvis/torso turned right, left leg extends at waist/lower-chest height below head, supporting right knee bent, torso forward. This is the new rear-left pilot, not prior high kick.'),
'14':('sweep-kick-back-through','Sweep FOLLOWTHROUGH: turn farther to its right until FULL BACK faces viewer, head face hidden. Left kicking leg continues its rightward horizontal arc AWAY from camera beyond body, foreshortened and partly occluded by right rear waist armour. Foot stays at waist height, never above shoulders. Support right foot pivots, torso/hips rotate together, mane and red ribbons lag toward left. Actual back shoulder planes, not front chest or orb.'),
'15':('sweep-kick-back-retract','RETRACT after rotational sweep, full back/left-rear predominant. Left knee folds after sweeping right, foot drops toward ground, right planted knee absorbs torque. Torso continues rotation and head starts looking around toward image-left, only small left cheek edge visible. No second kick; closed hands by ribs. Correct base back armour, thick segmented limbs.'),
'16':('sweep-kick-land-link','LAND after rotating sweep: back-left quarter still visible, head turns over shoulder toward LEFT target again, torso begins pivot into the next leftward uppercut. Left foot lowers into a wide grounded stance, right support leg braced. Right closed hand drops near hip to load uppercut, left guards cheek. No jump, no high foot, no neutral pause.')}
for i in range(1,31):
 id=f'{i:02}';srcslot=i
 if i in [7,8,9]:srcslot=i+1
 q=prior[srcslot-1];row=dict(id=id,name=q['name'],group=q['group'],new=False,source=str(pub/q['file']),previous_slot=f'{srcslot:02}')
 if i in [1,2,3,27,28,29,30]:
  init=next(z for z in initial if z['id']==id);row.update(name=init['name'],pose=init['pose'],new=True,pose_seed=init['pose_seed'])
 if id in kicks:
  name,pose=kicks[id];row.update(name=name,pose=pose,new=True,group='kick',pose_seed='/workspace/generated_images/exec-61e2e02c-3bd1-4568-b289-d765cefc0324.png')
 if i in [7,8,9]:row['group']='uppercut1'
 if row['new']:
  req=r/'requests'/id
  subprocess.run(['python',str(r/'ask.py'),'ask-view','--master',str(old/'ask-28/master.png'),'--cell','8','--key','green','--view-words',row['pose'],'--output-dir',str(req)],check=True,capture_output=True)
  row['request']=str(req)
 plan.append(row)
(r/'plan.json').write_text(json.dumps(plan,indent=2))
# Reader uses authoritative request path, not the initial request names.
(r/'extract.py').write_text("from pathlib import Path\nimport subprocess,sys\nr=Path('/workspace/work/mecha-impact-v003');id=sys.argv[1];source=sys.argv[2]\nsubprocess.run(['python',str(r/'read.py'),'view','--image',source,'--request',str(r/'requests'/id),'--name','pose-'+id,'--output-dir',str(r/f'extracted-{id}')],check=True)\n")
print('Final distribution:2dash,4heavy,3uppercut,7sweep,4uppercut,6combo,4palm; new14, reused16')
