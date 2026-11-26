from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,math,hashlib
r=Path('/workspace/work/mecha-component-v002');kit=Path('/workspace/work/mecha-component-v001/kit');spec=json.loads((kit/'parts.json').read_text());base=Image.open(spec['source']);a=np.array(base);pal=base.getpalette();labels=np.array(Image.open(kit/'ownership-index.png'));parts={q['name']:dict(q,a=np.where(labels==q['id'],a,0).astype('uint8')) for q in spec['parts']}
# This is the previously approved OPEN HAND only, not a replacement forearm.
source=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/actions/shin-ha-gou-shou-sen/v010/native/10-palm-release.png');im=Image.open(source);v=np.array(im);m=Image.new('1',im.size);ImageDraw.Draw(m).polygon([(8,37),(14,37),(15,39),(19,39),(22,43),(23,49),(24,54),(23,62),(20,65),(10,65),(7,63),(9,60),(10,58),(6,56),(6,51),(8,48),(6,47),(6,44),(9,42)],fill=1);m=np.array(m)&(v!=0);parts['open_hand']=dict(name='open_hand',a=np.where(m,v,0).astype('uint8'),pivot_global=[23,55],source=str(source))
parts['quarter_torso']=dict(name='quarter_torso',a=np.array(Image.open(kit/'variants/quarter_torso-indexed.png')),pivot_global=[63,77])
for n in ['roundhouse-kicking-leg','roundhouse-pelvis-support','side-mane-ribbons','side-head-chest']:
 parts[n]=dict(name=n,a=np.array(Image.open(r/'new-parts'/(n+'-indexed.png'))),pivot_global=[69,77])
# All rotations sample the original part directly, never a previously transformed frame.
def transform(arr,p,q,angle=0):
 c=math.cos(math.radians(angle));s=math.sin(math.radians(angle));px,py=p[0]+.5,p[1]+.5;qx,qy=q[0]+.5,q[1]+.5
 return np.array(Image.fromarray(arr).transform((144,112),Image.Transform.AFFINE,(c,-s,px-c*qx+s*qy,s,c,py-s*qx-c*qy),resample=Image.Resampling.NEAREST,fillcolor=0))
def render(config):
 layers=[];by={};body_angle=config.get('_body_angle',0);body_shift=config.get('_body_shift',[0,0]);root=[63,77]
 def parent(q):
  c=math.cos(math.radians(body_angle));ss=math.sin(math.radians(body_angle));dx=q[0]-root[0];dy=q[1]-root[1]
  return [round(root[0]+c*dx+ss*dy+body_shift[0]),round(root[1]-ss*dx+c*dy+body_shift[1])]

 for name,part in parts.items():
  if name=='open_hand':continue
  if (name.startswith('roundhouse-') or name.startswith('side-')) and not config.get('_kick_variant'):continue
  if name=='quarter_torso' and not config.get('_quarter'):continue
  if config.get('_quarter') and name in ['torso_core','waist_skirt']:continue
  tr=config.get(name,{})
  if tr.get('hide'):continue
  if config.get('_kick_variant') and name in ['waist_skirt','near_thigh','far_thigh','near_shin_foot','far_shin_foot','quarter_torso','mane','rear_ribbons','head_crests_face','near_shoulder_wing','far_shoulder_wing','torso_core','near_upper_arm','far_upper_arm','near_forearm','near_claw_hand']:continue
  pivot=tr.get('pivot',part['pivot_global']);at=tr.get('at',part['pivot_global']);angle=tr.get('angle',0);z=tr.get('z',40)
  isleg='thigh' in name or 'shin_foot' in name or name.startswith('roundhouse-')
  if not isleg and name!='rear_ribbons':
   at=parent(at)
   # Keep head/mane and the red-black forearm assemblies pixel-stable in world orientation.
   if name not in ['head_crests_face','mane'] and 'forearm' not in name and 'claw_hand' not in name:angle+=body_angle
  arr=transform(part['a'],pivot,at,angle);layers.append((z,name,arr));by[name]=arr
 if config.get('_open_hand'):
  tr=config['_open_hand'];arr=transform(parts['open_hand']['a'],[23,55],parent(tr['at']),tr.get('angle',0));layers.append((tr.get('z',95),'open_hand',arr));by['open_hand']=arr
 # Draw compact joint underlays at scale 1, using original palette indices.
 # These are newly exposed elbow connections, never replacement hand armour.
 for side,shoulder in ([] if config.get('_kick_variant') else [('near',[43,54]),('far',[85,53])]):
  tr=config.get(side+'_forearm',{});pivot=tr.get('pivot',parts[side+'_forearm']['pivot_global']);at=parent(tr.get('at',parts[side+'_forearm']['pivot_global']));angle=math.radians(tr.get('angle',0));dx=0;dy=-5
  elbow=[round(at[0]+math.cos(angle)*dx+math.sin(angle)*dy),round(at[1]-math.sin(angle)*dx+math.cos(angle)*dy)];shoulder=parent(shoulder)
  im=Image.new('L',(144,112),0);d=ImageDraw.Draw(im)
  d.line([tuple(shoulder),tuple(elbow)],fill=2,width=10)
  d.line([tuple(shoulder),tuple(elbow)],fill=4,width=6)
  d.line([(shoulder[0]-1,shoulder[1]-2),(elbow[0]-1,elbow[1]-2)],fill=7,width=3)
  d.rectangle((elbow[0]-3,elbow[1]-3,elbow[0]+3,elbow[1]+3),fill=2)
  d.line([(elbow[0]-2,elbow[1]-2),(elbow[0]+2,elbow[1]-2)],fill=9,width=2)
  ar=np.array(im);by[side+'_elbow_underlay']=ar;layers.append((38,side+'_elbow_underlay',ar))
 if config.get('_open_hand'):
  wrist=parent(config['_open_hand']['at']);im=Image.new('L',(144,112),0);d=ImageDraw.Draw(im)
  # A short cuff reconnects the approved open hand to the original beast-arm shell.
  if config['_open_hand'].get('angle',0)==0:
   d.rectangle((wrist[0]-1,wrist[1]-2,wrist[0]+7,wrist[1]+3),fill=2)
   d.line([(wrist[0],wrist[1]-1),(wrist[0]+6,wrist[1]-1)],fill=7,width=2)
   ar=np.array(im);layers.append((89,'open-palm-cuff',ar));by['open-palm-cuff']=ar
 out=np.zeros_like(a)
 for _,name,arr in sorted(layers,key=lambda t:t[0]):out[arr!=0]=arr[arr!=0]
 return out,by
# Layer order moves the inactive arm behind the torso; active forearm can cover lower face.
def pose(near=None,far=None,openhand=None):
 cfg={}
 for name in parts:
  if name=='open_hand':continue
  z=50 if name=='quarter_torso' else 40
  if name=='rear_ribbons':z=0
  elif name.startswith('far_') and ('arm' in name or 'hand' in name):z=15
  elif 'thigh' in name or 'shin_foot' in name:z=25
  elif name=='mane':z=30
  elif 'shoulder_wing' in name:z=35
  elif name=='waist_skirt':z=50
  elif name=='head_crests_face':z=60
  elif name.startswith('near_') and ('arm' in name or 'hand' in name):z=80
  cfg[name]=dict(z=z)
 for side,state in [('near',near),('far',far)]:
  if not state:continue
  angle,at=state[:2];z=state[2] if len(state)>2 else 90;pivot=parts[side+'_forearm']['pivot_global']
  for suffix in ['forearm','claw_hand']:cfg[side+'_'+suffix].update(angle=angle,pivot=pivot,at=at,z=z)
 if openhand:
  cfg['near_claw_hand']['hide']=True;cfg['_open_hand']=dict(at=openhand[0],angle=openhand[1],z=95)
 return cfg
