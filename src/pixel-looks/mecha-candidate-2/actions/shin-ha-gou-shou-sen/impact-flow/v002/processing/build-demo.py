from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,math,hashlib
r=Path('/workspace/work/mecha-impact-v002');o=r/'deliverables';files=sorted((o/'native').glob('*.png'));sprites=[Image.open(f).copy() for f in files];pal=sprites[0].getpalette();masks=[Image.fromarray((np.array(s)!=0).astype('uint8')*255) for s in sprites];steps=[];target=(227,163,0)
def add(p,ms,a,b,phase,to=None,hit=False):
 global target
 end=target if to is None else to;steps.append(dict(pose=p,ms=ms,start_root=a,end_root=b,phase=phase,target_start=target,target_end=end,hit=hit));target=end
add(1,200,(390,195),(335,195),'DASH / 2 drawings only')
add(2,120,(335,195),(322,195),'PLANT INTO HEAVY PUNCH')
add(3,80,(322,195),(319,195),'1  HEAVY STRAIGHT / lead strike')
add(4,80,(319,195),(306,195),'1  HEAVY STRAIGHT / drive')
add(5,160,(306,195),(300,195),'1  HEAVY STRAIGHT / IMPACT',(205,158,-10),True)
add(6,120,(300,195),(291,195),'1  HEAVY STRAIGHT / follow')
add(7,120,(291,195),(260,195),'1  HEAVY STRAIGHT / link')
add(8,160,(260,195),(255,195),'2  UPPERCUT / coil')
add(9,80,(255,195),(248,195),'2  UPPERCUT / drive')
add(10,160,(248,195),(245,195),'2  UPPERCUT / IMPACT',(195,122,-18),True)
add(11,120,(245,195),(251,195),'2  UPPERCUT / lift')
add(12,160,(251,195),(268,195),'3  TURNING KICK / chamber')
add(13,80,(268,195),(267,195),'3  TURNING KICK / drive')
add(14,160,(267,195),(260,195),'3  TURNING KICK / IMPACT',(165,96,-30),True)
add(15,120,(260,195),(244,195),'3  TURNING KICK / turn through')
add(16,120,(244,195),(228,195),'3  TURNING KICK / attack link')
add(17,160,(228,195),(223,195),'4  SECOND UPPERCUT / coil')
add(18,80,(223,195),(219,182),'4  SECOND UPPERCUT / drive')
add(19,160,(219,182),(215,160),'4  SECOND UPPERCUT / IMPACT',(145,62,-22),True)
add(20,160,(215,160),(225,132),'4  SECOND UPPERCUT / rising pursuit')
for c in range(3):
 dx=c*32;sx=145-c*32
 add(21,80,(225-dx,132 if c==0 else 114),(222-dx,120),f'5  AIR COMBO {c+1}/3 / left load')
 add(22,80,(222-dx,120),(218-dx,115),f'5  AIR COMBO {c+1}/3 / LEFT HIT',(sx-8,68,-12),True)
 add(23,80,(218-dx,115),(214-dx,114),f'5  AIR COMBO {c+1}/3 / right drive')
 add(24,80,(214-dx,114),(210-dx,112),f'5  AIR COMBO {c+1}/3 / RIGHT HIT',(sx-16,60,-20),True)
 add(25,80,(210-dx,112),(202-dx,120),f'5  AIR COMBO {c+1}/3 / LEFT FOLLOW',(sx-24,68,-10),True)
 add(26,80,(202-dx,120),(194-dx,114),f'5  AIR COMBO {c+1}/3 / RIGHT FOLLOW',(sx-32,62,-18),True)
add(27,320,(130,114),(132,195),'6  PALM / plant and load',(49,147,-5))
add(28,120,(132,195),(129,195),'6  PALM / drive',(49,163,0))
add(29,200,(129,195),(126,195),'6  PALM / IMPACT',(-5,145,-38),True)
add(30,480,(126,195),(122,195),'6  PALM / committed followthrough',(-65,125,-60))
# At most two dash drawings; every remaining drawing is an attack phase.
assert len({s['pose'] for s in steps})==30
assert [s['pose'] for s in steps if s['phase'].startswith('DASH')]==[1]
tick=40;scale=3;stage_size=(480,220);clean=[];reference=[];timeline=[];elapsed=0
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
for step in steps:
 n=step['ms']//tick;assert n*tick==step['ms'];p=step['pose'];a=step['start_root'];b=step['end_root'];ta=step['target_start'];tb=step['target_end']
 for k in range(n):
  u=k/max(1,n-1);v=max(0,(u-.5)*2) if step['hit'] and n>2 else u
  x=round(a[0]+(b[0]-a[0])*v);y=round(a[1]+(b[1]-a[1])*v);tx=round(ta[0]+(tb[0]-ta[0])*v);ty=round(ta[1]+(tb[1]-ta[1])*v);angle=ta[2]+(tb[2]-ta[2])*v;idx=p-1;at=(x-72,y-108);ys,xs=np.where(np.array(masks[idx])!=0)
  assert 0<=xs.min()+at[0] and xs.max()+at[0]<480 and 0<=ys.min()+at[1] and ys.max()+at[1]<220,(p,at)
  stage=Image.new('P',stage_size);stage.putpalette(pal);stage.paste(sprites[idx],at,masks[idx]);clean.append(stage.resize((1440,660),Image.Resampling.NEAREST))
  # This box is an explanatory target, never an opponent sprite or a sprite effect.
  ref=Image.new('RGB',stage_size,(88,120,120));d=ImageDraw.Draw(ref);rad=math.radians(angle);co=math.cos(rad);si=math.sin(rad)
  pts=[(round(tx+xx*co-yy*si),round(ty+xx*si+yy*co)) for xx,yy in [(-18,-32),(18,-32),(18,32),(-18,32)]];d.line(pts+[pts[0]],fill=(250,245,209),width=1);d.line([(tx-4,ty),(tx+4,ty)],fill=(250,245,209));d.line([(tx,ty-4),(tx,ty+4)],fill=(250,245,209));ref.paste(sprites[idx].convert('RGB'),at,masks[idx]);ref=ref.resize((1440,660),Image.Resampling.NEAREST)
  page=Image.new('RGB',(1440,740),(29,39,42));page.paste(ref,(0,45));d=ImageDraw.Draw(page);d.text((15,10),step['phase'],font=font,fill='white');d.text((1250,15),f'POSE {p:02d}/30',font=small,fill='white');d.text((15,713),'Outlined box = enemy displacement reference only. No enemy / effects in native sprites.',font=small,fill=(250,245,209));reference.append(page);timeline.append(dict(t_ms=elapsed,pose=p,root_xy=[x,y],target_xy=[tx,ty],target_angle=angle,phase=step['phase']));elapsed+=tick
ui=[(29,39,42),(255,255,255),(250,245,209)];colour=pal[:48]+[v for c in ui for v in c];colour=(colour+[0]*768)[:768];pim=Image.new('P',(1,1));pim.putpalette(colour);reference=[f.quantize(palette=pim,dither=Image.Dither.NONE) for f in reference]
checks=[]
for fn,frames,speed in [('moveset-30.gif',clean,1),('moveset-30-slow.gif',clean,2),('hit-reference.gif',reference,1),('hit-reference-slow.gif',reference,2)]:
 frames[0].save(o/fn,save_all=True,append_images=frames[1:],duration=tick*speed,loop=0,optimize=False,disposal=2);g=Image.open(o/fn);wanted=0
 for i in range(g.n_frames):
  g.seek(i);actual=g.convert('RGB').tobytes();repeat=g.info['duration']//(tick*speed)
  for j in range(repeat):assert actual==frames[wanted].convert('RGB').tobytes(),(fn,i,wanted);wanted+=1
 assert wanted==len(frames);checks.append(dict(file=fn,encoded_frames=g.n_frames,checked_time_intervals=wanted,duration_ms=elapsed*speed,readback_matches=True))
page=Image.new('RGB',(1440,1155),(29,39,42));d=ImageDraw.Draw(page)
for j,p in enumerate([5,10,14,19,24,29]):
 i=next(i for i,t in enumerate(timeline) if t['pose']==p);x=j%2*720;y=j//2*385;page.paste(reference[i].convert('RGB').resize((720,370),Image.Resampling.NEAREST),(x,y))
page.save(o/'six-hit-overview.png');(o/'timeline.json').write_text(json.dumps(dict(unique_drawings=30,newly_generated_drawings=23,dash_drawings=2,attack_drawings=28,stage_native=stage_size,display_scale=scale,tick_ms=tick,duration_ms=elapsed,combo_repeats=3,combo_pose_cycle=[21,22,23,24,25,26],sequence=['heavy','uppercut1','kick','uppercut2','combo','palm'],method='Held drawings, hit stops and integer whole-sprite pursuit. Target reference is diagram-only approximate recoil, not measured physics. Last-to-first is replay reset.',steps=steps,timeline=timeline,gif_checks=checks),indent=2));print(json.dumps(dict(duration_ms=elapsed,tick_intervals=len(clean),gif_checks=checks),indent=2))
