from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
r=Path('/workspace/work/mecha-component-v002');o=r/'new-parts';o.mkdir(exist_ok=True)
base=Image.open('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/v001/mecha-final-1x.png');pal=base.getpalette();colors=np.array(pal).reshape(-1,3);allowed=np.array([1,2]+list(range(4,16)))
src=Image.open(r/'extracted-roundhouse/roundhouse.png').convert('RGBA');full=Image.new('RGBA',(144,112));full.paste(src,(17,7));v=np.array(full);idx=allowed[((v[:,:,:3].astype(int)[:,:,None]-colors[None,None,allowed])**2).sum(-1).argmin(-1)].astype('uint8');idx[v[:,:,3]==0]=0
poly=[(16,64),(66,64),(77,69),(89,85),(92,111),(60,111),(47,89),(16,83)]
m=Image.new('1',(144,112));ImageDraw.Draw(m).polygon(poly,fill=1);low=np.where(np.array(m),idx,0).astype('uint8')
m=Image.new('1',(144,112));ImageDraw.Draw(m).polygon([(16,63),(58,63),(70,69),(71,78),(60,84),(16,83)],fill=1);kick=np.where(np.array(m),low,0).astype('uint8');pelvis=np.where(np.array(m),0,low).astype('uint8')
for n,a in [('roundhouse-kicking-leg',kick),('roundhouse-pelvis-support',pelvis)]:
 im=Image.fromarray(a);im.putpalette(pal);im.save(o/(n+'-indexed.png'),transparency=0,bits=4);im.convert('RGBA').save(o/(n+'.png'))
(o/'provenance.json').write_text(json.dumps(dict(art_source='host_image',source='/workspace/generated_images/exec-e314a167-7c53-4a98-9d26-24c40ce843cf.png',extraction='pixel_look ask-pose / pose',only_imported='masked pelvis and legs; generated head, eyes, shoulders, arms and hair discarded',native_mapping=[17,7],palette='nearest original palette, no new colours',lower_body_polygon=poly),indent=2))
