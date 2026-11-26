from pathlib import Path
from PIL import Image,ImageDraw
import json
r=Path('/workspace/work/mecha-video-rebuild-v001');guesses={'02':(59,46),'04':(40,63),'05':(31,66),'06':(55,55),'07':(72,47),'10':(61,38),'11':(52,42),'13':(65,34),'14':(40,49),'15':(69,34),'16':(73,44),'17':(54,63),'18':(50,60),'19':(63,75),'20':(55,61),'21':(55,61),'23':(64,46),'25':(58,39),'27':(72,45),'29':(62,53),'30':(59,44)};rows=(len(guesses)+3)//4;page=Image.new('RGB',(1120,rows*248),(60,60,60));d=ImageDraw.Draw(page)
for j,(id,(x,y)) in enumerate(guesses.items()):
 im=Image.open(r/'provisional'/(id+'.png'));box=(x-8,y-6,x+8,y+8);px=j%4*280+25;py=j//4*248+25;page.paste(im.crop(box).convert('RGB').resize((224,196),Image.Resampling.NEAREST),(px,py));d.text((px,py-18),id+' '+str(box),fill='white')
 for k in range(14):d.text((px-22,py+k*14),str(box[1]+k),fill='yellow')
 for k in range(0,16,2):d.text((px+k*14,py+198),str(box[0]+k),fill='yellow')
page.save(r/'eyes-review.png')
