from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib
r=Path('/workspace/work/mecha-video-rebuild-v001');o=r/'deliverables';files=sorted((o/'native').glob('*.png'));sprites=[Image.open(f).copy() for f in files];pal=sprites[0].getpalette();masks=[Image.fromarray((np.array(s)!=0).astype('uint8')*255) for s in sprites];before={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files};steps=[]
def add(p,ms,a,b,phase):steps.append((p,ms,a,b,phase))
add(1,350,(290,148),(290,148),'READY');add(2,300,(290,148),(290,148),'TIGHTEN GUARD');add(3,700,(290,148),(290,148),'GATHER POWER');add(4,150,(290,148),(280,148),'LAUNCH LOAD');add(5,300,(280,148),(230,146),'FORWARD RUSH')
for cycle in range(2):
 for p,ms,label in [(6,100,'LEFT CHAMBER'),(7,100,'LEFT HALF'),(8,100,'LEFT HIT'),(9,100,'RIGHT LOAD'),(10,100,'RIGHT HIT')]:add(p,ms,(230,148),(230,148),f'CLOSE COMBAT {cycle+1}/2 : '+label)
add(11,150,(230,148),(222,148),'PLANT FOR KICK');add(12,150,(222,148),(217,148),'KICK CHAMBER');add(13,200,(217,148),(210,148),'TURNING RISING KICK');add(14,200,(210,148),(205,148),'TURNING LANDING');add(15,150,(205,148),(200,148),'UNWIND');add(16,150,(200,148),(200,148),'UPPERCUT LOAD');add(17,200,(200,148),(195,148),'UPPERCUT HIT');add(18,150,(195,148),(190,132),'RISING FOLLOWTHROUGH');add(19,150,(190,132),(180,120),'COIL FOR PURSUIT')
for cycle in range(2):
 add(20,150,(180-cycle*15,120-cycle*2),(172-cycle*15,118-cycle*2),'AIR LEAD STRIKE');add(21,150,(172-cycle*15,118-cycle*2),(165-cycle*15,118-cycle*2),'AIR COUNTER STRIKE')
add(22,200,(150,116),(142,132),'DOWNWARD PURSUIT');add(23,150,(142,132),(138,140),'AIR RECOVERY');add(24,250,(138,140),(135,148),'LANDING ABSORB');add(25,200,(135,148),(135,148),'SET PALM STANCE');add(26,550,(135,148),(135,148),'PALM WINDUP');add(27,150,(135,148),(132,148),'PALM DRIVE');add(28,150,(132,148),(126,148),'PALM HIT');add(28,450,(126,148),(126,148),'PALM HOLD');add(29,250,(126,148),(123,148),'PALM FOLLOWTHROUGH');add(30,350,(123,148),(123,148),'RECOVER GUARD');add(1,350,(123,148),(123,148),'REPLAY')

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
for j,pose in enumerate([5,8,13,17,21,28]):
 i=next(i for i,t in enumerate(timeline) if t['pose']==pose);x=j%2*576;y=j//2*280;page.paste(clean[i].convert('RGB').resize((576,240),Image.Resampling.NEAREST),(x,y+32));d.text((x+8,y+8),timeline[i]['phase'],fill='white')
page.save(o/'motion-overview.png');(o/'timeline.json').write_text(json.dumps({'unique_drawings':30,'newly_generated_drawings':22,'stage_native':[384,160],'display_scale':3,'tick_ms':tick,'duration_ms':elapsed,'combo_repeats':2,'combo_pose_cycle':[6,7,8,9,10], 'air_cycle':[20,21], 'air_repeats':2,'method':'original static sprites, held timing and integer whole-sprite translation; no effects/morphing; inspection replay resets after recovery','steps':[{'pose':p,'ms':ms,'start_root':a,'end_root':b,'phase':s} for p,ms,a,b,s in steps],'timeline':timeline,'gif_checks':checks},indent=2));assert all(hashlib.sha256(f.read_bytes()).hexdigest()==before[f.name] for f in files);print(json.dumps({'duration_ms':elapsed,'tick_intervals':len(clean),'unique_native_poses':30,'gif_checks':checks},indent=2))
