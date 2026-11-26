from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib
r=Path('/workspace/work/mecha-impact-v003');o=r/'deliverables';meta=json.loads((o/'specification.json').read_text());rows=meta['frames'];sprites=[Image.open(o/q['file']).copy() for q in rows];pal=sprites[0].getpalette();masks=[Image.fromarray((np.array(s)!=0).astype('uint8')*255) for s in sprites];steps=[]
def add(p,ms,a,b,label):steps.append(dict(pose=p,ms=ms,start_root=[a,145],end_root=[b,145],phase=label))
add(1,200,290,240,'GROUND DASH');add(2,120,240,230,'GROUND PLANT');add(3,160,230,230,'HEAVY / CHAMBER');add(4,80,230,222,'HEAVY / DRIVE');add(5,160,222,218,'HEAVY / IMPACT');add(6,120,218,212,'HEAVY / FOLLOW')
add(7,160,212,208,'UPPERCUT 1 / COIL');add(8,80,208,202,'UPPERCUT 1 / DRIVE');add(9,160,202,200,'UPPERCUT 1 / IMPACT')
for p,ms,label in [(10,160,'LOAD'),(11,120,'LEFT-REAR TURN'),(12,80,'HORIZONTAL DRIVE'),(13,160,'SWEEP IMPACT'),(14,120,'BACK FOLLOWTHROUGH'),(15,120,'BACK RECOVERY'),(16,160,'PIVOT LANDING')]:add(p,ms,200,200,'ROTATING KICK / '+label)
add(17,160,200,196,'UPPERCUT 2 / COIL');add(18,80,196,190,'UPPERCUT 2 / DRIVE');add(19,160,190,184,'UPPERCUT 2 / IMPACT');add(20,120,184,180,'UPPERCUT 2 / GROUNDED FOLLOW')
for cycle in range(3):
 x=180-cycle*20
 for p,dx,X,label in [(21,0,2,'LEFT LOAD'),(22,2,6,'LEFT HIT'),(23,6,8,'RIGHT DRIVE'),(24,8,12,'RIGHT HIT'),(25,12,16,'LEFT FOLLOW'),(26,16,20,'RIGHT FOLLOW')]:add(p,80,x-dx,x-X,f'GROUND COMBO {cycle+1}/3 / '+label)
# Palm roots refer to the planted REAR foot. Combo roots refer to canvas centre.
# Keeping the rear foot still lets the drawn hip/shoulder lunge show the force.
add(27,440,150,150,'PALM / DEEP COIL');add(28,80,150,150,'PALM / HIP DRIVE');add(29,280,150,150,'PALM / HEEL IMPACT');add(30,440,150,150,'PALM / COMMITTED FOLLOW')
assert len({s['pose'] for s in steps})==30
assert all(s['start_root'][1]==s['end_root'][1]==145 for s in steps)
tick=40;elapsed=0;frames=[];labelled=[];timeline=[];font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',21)
def render(p,x,y,size):
 idx=p-1;anchor=rows[idx]['ground_anchor'];at=(x-anchor[0],y-anchor[1]);ys,xs=np.where(np.array(masks[idx])!=0);assert 0<=xs.min()+at[0] and xs.max()+at[0]<size[0] and 0<=ys.min()+at[1] and ys.max()+at[1]<size[1],(p,at,anchor)
 stage=Image.new('P',size);stage.putpalette(pal);stage.paste(sprites[idx],at,masks[idx]);return stage
for step in steps:
 n=step['ms']//tick;assert n*tick==step['ms']
 for k in range(n):
  u=k/max(1,n-1)
  if 'IMPACT' in step['phase']:u=max(0,(u-.5)*2)
  x=round(step['start_root'][0]+(step['end_root'][0]-step['start_root'][0])*u);p=step['pose'];stage=render(p,x,145,(360,160)).resize((1440,640),Image.Resampling.NEAREST);frames.append(stage)
  page=Image.new('RGB',(1440,690),(29,39,42));page.paste(stage.convert('RGB'),(0,50));ImageDraw.Draw(page).text((15,12),step['phase']+f'   / POSE {p:02d}',font=font,fill='white');labelled.append(page);timeline.append(dict(t_ms=elapsed,pose=p,root_xy=[x,145],anchor=rows[p-1]['ground_anchor'],phase=step['phase']));elapsed+=tick
pim=Image.new('P',(1,1));pim.putpalette((pal[:48]+[29,39,42,255,255,255]+[0]*768)[:768]);labelled=[im.quantize(palette=pim,dither=Image.Dither.NONE) for im in labelled]
checks=[]
def save(fn,ims,ms):
 ims[0].save(o/fn,save_all=True,append_images=ims[1:],duration=ms,loop=0,optimize=False,disposal=2);g=Image.open(o/fn);wanted=0
 for i in range(g.n_frames):
  g.seek(i);actual=g.convert('RGB').tobytes();repeat=g.info['duration']//ms
  for j in range(repeat):assert actual==ims[wanted].convert('RGB').tobytes(),(fn,i,wanted);wanted+=1
 assert wanted==len(ims);checks.append(dict(file=fn,encoded_frames=g.n_frames,checked_time_intervals=wanted,duration_ms=len(ims)*ms,readback_matches=True))
save('moveset-30.gif',frames,40);save('moveset-30-slow.gif',frames,80);save('moveset-30-labelled.gif',labelled,40)
# Detail clips contain the exact same native drawings, no morphing or effects.
for name,which,size,scale,root in [('rotating-kick-detail.gif',list(range(10,17)),(220,140),6,(110,125)),('palm-detail.gif',[27,28,29,30],(240,140),5,(150,125))]:
 clips=[]
 for s in steps:
  if s['pose'] not in which:continue
  im=render(s['pose'],*root,size).resize((size[0]*scale,size[1]*scale),Image.Resampling.NEAREST)
  clips += [im]*(s['ms']//40)
 if name.startswith('rotating'):clips += [clips[-1]]*8
 save(name,clips,80)
# Key motion proof at exact 3x native, with labels outside sprites.
page=Image.new('RGB',(1296,736),(88,120,120));d=ImageDraw.Draw(page)
for j,p in enumerate([1,5,13,14,22,29]):
 x=j%3*432;y=j//3*368;page.paste(sprites[p-1].convert('RGB').resize((432,336),Image.Resampling.NEAREST),(x,y+28));d.text((x+6,y+7),rows[p-1]['id']+' '+rows[p-1]['name'],fill='white')
page.save(o/'key-poses.png');(o/'timeline.json').write_text(json.dumps(dict(unique_drawings=30,new_drawings=22,retained_drawings=8,dash_drawings=2,attack_drawings=28,kick_drawings=7,stage_native=[360,160],display_scale=4,tick_ms=40,duration_ms=elapsed,no_jump_attacks=True,ground_baseline=145,combo_repeats=3,combo_pose_cycle=[21,22,23,24,25,26],sequence=['heavy','uppercut1','rotating_horizontal_kick','uppercut2','ground_left_right_combo','palm'],method='Static native drawings, held impacts and integer ground translation. Kick is anchored at support foot; palm anchored at rear foot. No vertical lift, morphing or effects. Last-to-first is inspection replay reset.',steps=steps,timeline=timeline,gif_checks=checks),indent=2));print(json.dumps(dict(duration_ms=elapsed,checks=checks),indent=2))
