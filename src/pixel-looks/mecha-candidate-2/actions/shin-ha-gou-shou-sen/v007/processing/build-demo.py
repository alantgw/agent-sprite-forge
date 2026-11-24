from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,shutil
r=Path('/workspace/work/mecha-sequence-v007');o=r/'demo-build';o.mkdir(exist_ok=True);src=r/'deliverables';files=sorted((src/'native').glob('*.png'));sprites=[Image.open(f).copy() for f in files];pal=sprites[0].getpalette();rgb=tuple(pal[:3]);hashes={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files};masks=[Image.fromarray((np.array(s)!=0).astype('uint8')*255) for s in sprites]
# id, ms, root start/end: only whole-sprite movement; no pose interpolation.
steps=[(1,350,(284,148),(284,148),'1  GUARD'),(2,450,(284,148),(284,148),'1  BRACE'),(3,300,(284,148),(210,148),'2  DASH TO ENEMY'),(7,350,(210,148),(195,148),'3  LEFT CROSS-BODY RISING KICK'),(8,400,(195,148),(190,148),'4  GROUNDED UPPERCUT')]
for cycle in range(4):
 for pose,label in [(3,'WINDUP'),(4,'LEFT HIT'),(5,'COUNTER WINDUP'),(6,'RIGHT HIT')]:
  steps.append((pose,100,(190,148),(190,148),f'5  COMBO {cycle+1}/4 : '+label))
steps.extend([(9,900,(190,148),(190,148),'6  PALM WINDUP'),(10,200,(190,148),(182,148),'7  PALM STRIKE'),(10,800,(182,148),(182,148),'7  FINISH HOLD'),(1,550,(182,148),(182,148),'REPLAY')])

font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16);frames=[];timeline=[];tick=50;elapsed=0;scale=3;W,H=384,160
for si,(pose,ms,start,end,label) in enumerate(steps):
 count=ms//tick;assert count*tick==ms
 for k in range(count):
  u=k/max(1,count-1);x=round(start[0]+(end[0]-start[0])*u);y=round(start[1]+(end[1]-start[1])*u);at=(x-72,y-109);idx=pose-1;s=sprites[idx];box=np.array(masks[idx]).nonzero();xmin,xmax=int(box[1].min())+at[0],int(box[1].max())+at[0];ymin,ymax=int(box[0].min())+at[1],int(box[0].max())+at[1];assert 0<=xmin<=xmax<W and 0<=ymin<=ymax<H
  stage=Image.new('P',(W,H));stage.putpalette(pal);stage.paste(s,at,masks[idx]);stage=stage.convert('RGB').resize((W*scale,H*scale),Image.Resampling.NEAREST);page=Image.new('RGB',(W*scale,H*scale+104),(29,39,42));page.paste(stage,(0,50));d=ImageDraw.Draw(page);d.text((18,12),label,font=font,fill='white');d.text((W*scale-150,16),f'POSE {pose:02d} / 10',font=small,fill='white');
  for j in range(10):
   bx=18+j*46;by=H*scale+63;colour=(227,202,246) if j==idx else (88,120,120);d.rectangle((bx,by,bx+34,by+27),fill=colour);d.text((bx+7,by+3),f'{j+1:02d}',font=small,fill=(17,19,56) if j==idx else 'white')
  d.text((520,H*scale+70),'10 original poses | position + timing only',font=small,fill=(220,220,220));frames.append(page);timeline.append({'t_ms':elapsed,'pose':pose,'root_xy':[x,y],'phase':label});elapsed+=tick
# Preserve sprite palette exactly; reserve extra palette slots only for labels outside stage.
from collections import Counter
ui=Counter()
for f in frames[::max(1,len(frames)//20)]:ui.update(f.crop((0,0,f.width,50)).getdata());ui.update(f.crop((0,530,f.width,f.height)).getdata())
extra=[list(c) for c,_ in ui.most_common(230) if list(c) not in [pal[i:i+3] for i in range(0,48,3)]];colors=pal[:48]+[v for c in extra for v in c];colors=(colors+[0]*768)[:768];palette=Image.new('P',(1,1));palette.putpalette(colors);indexed=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
for name,speed in [('moveset-demonstration.gif',1),('moveset-demonstration-slow.gif',2)]:
 indexed[0].save(o/name,save_all=True,append_images=indexed[1:],duration=tick*speed,loop=0,optimize=False,disposal=2);g=Image.open(o/name)
 # GIF can coalesce identical holds. Validate all decoded time intervals, including pose and movement.
 decoded=[]
 for k in range(g.n_frames):g.seek(k);decoded.extend([g.convert('RGB').copy()]*(g.info['duration']//(tick*speed)))
 assert len(decoded)==len(indexed),(len(decoded),len(indexed))
 for actual,wanted in zip(decoded,indexed):assert actual.tobytes()==wanted.convert('RGB').tobytes()
# Five panels demonstrate the main motion phrases, using the exact rendered frames.
poses=[2,4,7,9,10];shots=[]
for p in poses:shots.append(frames[next(i for i,t in enumerate(timeline) if t['pose']==p)])
contact=Image.new('RGB',(1152,5*292),(29,39,42))
for i,f in enumerate(shots):contact.paste(f.resize((576,292),Image.Resampling.NEAREST),(0,i*292))
# Compact2-column stage overview retains stage at integer scale1 for embedded inspection.
contact=Image.new('RGB',(768,3*210),(29,39,42));d=ImageDraw.Draw(contact)
for i,p in enumerate([3,7,8,4,6,10]):
 t=next(t for t in timeline if t['pose']==p);idx=p-1;stage=Image.new('P',(384,160));stage.putpalette(pal);x,y=t['root_xy'];stage.paste(sprites[idx],(x-72,y-109),masks[idx]);at=((i%2)*384,(i//2)*210);d.text((at[0]+8,at[1]+8),t['phase'],font=small,fill='white');contact.paste(stage.convert('RGB'),(at[0],at[1]+40))
contact.save(o/'motion-overview.png');frames[next(i for i,t in enumerate(timeline) if t['pose']==7)].save(o/'demonstration-still.png')
meta={'source_version':'v007','source_commit':'packaged separately','source_hashes':hashes,'source_sprite_count':10,'added_character_drawings':0,'native_sprite_canvas':[144,112],'stage_native':[384,160],'stage_display_scale':3,'render_tick_ms':tick,'duration_ms':elapsed,'normal_duration_ms':elapsed,'slow_duration_ms':elapsed*2,'loop':'infinite inspection replay; finish-to-start resets deliberately','effects':'none; no opponent or new FX','method':'opaque teal keyed for compositing only; native sprite pixels unchanged; integer position lerp and held key poses; no body morphing','combo_repeats':4,'steps':[{'pose':p,'duration_ms':ms,'start_root':st,'end_root':en,'phase':s} for p,ms,st,en,s in steps],'timeline':timeline,'limits':'compressed staging of the six-part video, not literal44-second timing or60fps character animation'};(o/'timeline.json').write_text(json.dumps(meta,indent=2));(o/'README.md').write_text('''# Ten-pose moveset demonstration

Uses the amended v002 sprites unchanged: guard/powerup → low dash and close/rising strikes → launch and airborne pursuit → landing/palm windup → palm finish. Whole-sprite translation, jump height, repeated close-strike poses and held anticipation show how the ten drawings can represent the video move.

![Moveset demonstration](moveset-demonstration.gif)

[Slow demonstration](moveset-demonstration-slow.gif) · [Overview](motion-overview.png) · [Source sprites](../../v002/README.md)

No added character drawings, opponent, aura, beam, hit flash or scenery. The original ten native PNGs are unchanged, including red-eye lock and angular armour. Stage is384×160 logical pixels displayed3x nearest-neighbour; each mecha frame stays144×112 at1x. Labels and the numbered pose indicator are outside the stage. Whole sprite positions move in integer pixels; poses snap rather than morph. The last-to-first loop is a deliberate replay reset, not a claimed seamless recovery.

Compressed demonstration timing, not a literal44-second/60fps recreation. Only the existing ten poses are used; close/rising strikes reuse04/05 to indicate the rapid combo. Position and timing values are in timeline.json. Original source hashes recorded and checked unchanged. GIF readback was verified over every encoded time interval. Earlier v002 height review flags remain documented in the source set; no new anatomy approval or game-import compatibility claim.
''');shutil.copy2(r/'build-demo.py',o/'build.py');(o/'sha256.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in o.iterdir() if p.is_file() and p.name!='sha256.json'},indent=2));assert all(hashlib.sha256(f.read_bytes()).hexdigest()==hashes[f.name] for f in files);print(json.dumps({'duration_ms':elapsed,'ticks':len(frames),'source_sprites':10,'added_poses':0,'output':str(o)},indent=2))
