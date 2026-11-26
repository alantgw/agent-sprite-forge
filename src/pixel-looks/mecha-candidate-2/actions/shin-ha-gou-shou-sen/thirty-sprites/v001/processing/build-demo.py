from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib
r=Path('/workspace/work/mecha-thirty-v001');o=r/'deliverables';files=sorted((o/'native').glob('*.png'));sprites=[Image.open(f).copy() for f in files];pal=sprites[0].getpalette();masks=[Image.fromarray((np.array(s)!=0).astype('uint8')*255) for s in sprites];before={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files};steps=[]
def add(p,ms,a,b,phase):steps.append((p,ms,a,b,phase))
add(1,450,(290,148),(290,148),'READY');add(2,350,(290,148),(290,148),'GUARD');add(3,500,(290,148),(290,148),'POWER COIL');add(4,150,(290,148),(280,148),'DASH ANTICIPATION');add(5,300,(280,148),(225,148),'CLOSE THE DISTANCE');add(6,150,(225,148),(215,148),'KICK CHAMBER');add(7,150,(215,148),(210,148),'RISING KICK');add(8,150,(210,148),(205,148),'TURNING KICK');add(9,200,(205,148),(200,148),'BACK LANDING');add(10,150,(200,148),(195,148),'UNWIND');add(11,200,(195,148),(195,148),'UPPERCUT WINDUP');add(12,200,(195,148),(190,148),'UPPERCUT');add(13,200,(190,148),(185,132),'RISING FOLLOWTHROUGH');add(14,150,(185,132),(175,121),'PURSUIT LAUNCH');add(15,200,(175,121),(165,116),'AIRBORNE PURSUIT');add(16,150,(165,116),(158,119),'TURN BACK');add(17,150,(158,119),(150,124),'TURN SIDE');add(18,200,(150,124),(142,133),'FOLLOWUP KICK');add(19,250,(142,133),(138,148),'LANDING BRACE')
for cycle in range(4):
 for p,ms,label in [(20,100,'LEFT WINDUP'),(21,50,'LEFT HALF'),(22,100,'LEFT HIT'),(23,100,'RIGHT WINDUP'),(24,50,'RIGHT HALF'),(25,100,'RIGHT HIT')]:add(p,ms,(138,148),(138,148),f'COMBO {cycle+1}/4 : '+label)
add(26,250,(138,148),(138,148),'SETTLE');add(27,600,(138,148),(138,148),'PALM WINDUP');add(28,150,(138,148),(134,148),'PALM EXTENSION');add(29,150,(134,148),(128,148),'PALM RELEASE');add(29,600,(128,148),(128,148),'FINISH HOLD');add(30,400,(128,148),(128,148),'RECOVERY');add(1,400,(128,148),(128,148),'REPLAY')
tick=50;clean=[];labelled=[];timeline=[];font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',21);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13);elapsed=0
for pose,ms,start,end,phase in steps:
 n=ms//tick;assert n*tick==ms
 for k in range(n):
  u=k/max(1,n-1);x=round(start[0]+(end[0]-start[0])*u);y=round(start[1]+(end[1]-start[1])*u);idx=pose-1;at=(x-72,y-108);s=sprites[idx];ys,xs=np.where(np.array(masks[idx])!=0);assert 0<=xs.min()+at[0] and xs.max()+at[0]<384 and 0<=ys.min()+at[1] and ys.max()+at[1]<160,(pose,at)
  stage=Image.new('P',(384,160));stage.putpalette(pal);stage.paste(s,at,masks[idx]);stage=stage.resize((1152,480),Image.Resampling.NEAREST);clean.append(stage);page=Image.new('RGB',(1152,580),(29,39,42));page.paste(stage.convert('RGB'),(0,50));d=ImageDraw.Draw(page);d.text((16,12),phase,font=font,fill='white');d.text((965,16),f'POSE {pose:02d} / 30',font=small,fill='white')
  for j in range(30):
   bx=17+j*37;d.rectangle((bx,543,bx+28,569),fill=(227,202,246) if j==idx else (88,120,120));d.text((bx+4,549),f'{j+1:02d}',font=small,fill=(17,19,56) if j==idx else 'white')
  labelled.append(page);timeline.append({'t_ms':elapsed,'pose':pose,'root_xy':[x,y],'phase':phase});elapsed+=tick
# UI colours do not enter clean sprite GIF. Labelled GIF reserves original16 palette entries.
ui=[(29,39,42),(255,255,255),(227,202,246),(17,19,56)];colour=pal[:48]+[v for c in ui for v in c];colour=(colour+[0]*768)[:768];pim=Image.new('P',(1,1));pim.putpalette(colour);labelled=[f.quantize(palette=pim,dither=Image.Dither.NONE) for f in labelled]
checks=[]
for fn,frames,speed in [('moveset-30.gif',clean,1),('moveset-30-slow.gif',clean,2),('moveset-30-labelled.gif',labelled,1)]:
 frames[0].save(o/fn,save_all=True,append_images=frames[1:],duration=tick*speed,loop=0,optimize=False,disposal=2);g=Image.open(o/fn);wanted=0
 for i in range(g.n_frames):
  g.seek(i);actual=g.convert('RGB').tobytes();repeat=g.info['duration']//(tick*speed)
  for j in range(repeat):assert actual==frames[wanted].convert('RGB').tobytes(),(fn,i,wanted);wanted+=1
 assert wanted==len(frames);checks.append({'file':fn,'encoded_frames':g.n_frames,'checked_time_intervals':wanted,'duration_ms':elapsed*speed,'readback_matches':True})
# Six pose overview uses exact clean stages, no pixel interpolation.
page=Image.new('RGB',(1152,3*280),(29,39,42));d=ImageDraw.Draw(page)
for j,pose in enumerate([5,8,9,12,22,29]):
 i=next(i for i,t in enumerate(timeline) if t['pose']==pose);x=j%2*576;y=j//2*280;page.paste(clean[i].convert('RGB').resize((576,240),Image.Resampling.NEAREST),(x,y+32));d.text((x+8,y+8),timeline[i]['phase'],fill='white')
page.save(o/'motion-overview.png');(o/'timeline.json').write_text(json.dumps({'unique_drawings':30,'newly_generated_drawings':10,'stage_native':[384,160],'display_scale':3,'tick_ms':tick,'duration_ms':elapsed,'combo_repeats':4,'combo_pose_cycle':[20,21,22,23,24,25],'method':'original static sprites, held timing and integer whole-sprite translation; no effects/morphing; inspection replay resets after recovery','steps':[{'pose':p,'ms':ms,'start_root':a,'end_root':b,'phase':s} for p,ms,a,b,s in steps],'timeline':timeline,'gif_checks':checks},indent=2));assert all(hashlib.sha256(f.read_bytes()).hexdigest()==before[f.name] for f in files);print(json.dumps({'duration_ms':elapsed,'tick_intervals':len(clean),'unique_native_poses':30,'gif_checks':checks},indent=2))
