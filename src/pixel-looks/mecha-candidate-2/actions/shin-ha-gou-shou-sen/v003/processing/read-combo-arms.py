"""Read complete changed-arm cells on the already verified master lattice.
Avoid the default pose reader leaving disconnected negative changes of withdrawn arms.
No repository source changes; same forge_pixelgrid sampler/key cleaner/outline rules.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np,sys
sys.path.insert(0,'/workspace/agent-sprite-forge/skills/generate2dsprite/scripts')
import pixel_look as pl
r=Path('/workspace/work/mecha-combo-v003');pal=Image.open('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/v001/mecha-final-1x.png').getpalette();p=np.array(pal,dtype=np.int32).reshape(-1,3);allow=np.array([1,2]+list(range(4,16)));master=np.array(Image.open(r/'provisional/03.png'));mask=np.zeros((112,144),bool);mask[28:83]=True;head=Image.new('1',(144,112));ImageDraw.Draw(head).polygon([(46,17),(113,17),(115,25),(106,31),(98,45),(83,62),(58,71),(44,64),(32,50),(38,37)],fill=1);protected=np.array(head);mask&=~protected
records=[]
for id in ['04','05','06']:
 rec=json.loads((r/f'extracted-{id}-safe/pose-{id}.json').read_text());req=json.loads((r/f'ask-{id}/request.json').read_text());assert rec['lattice']['share']>=.60;source=np.array(Image.open(rec['source']['image']).convert('RGB'));cols=req['canvas'][0]//req['cell'];rows=req['canvas'][1]//req['cell'];fit=rec['lattice'];cells=pl.pg.read_lattice(source,fit['cell'],fit['offset'],cols,rows);key=pl.pg.measure_key(source.astype(np.float32));on=np.sqrt(((cells-key)**2).sum(axis=2))>=pl.pg.KEY_DISTANCE;rgba=np.zeros((rows,cols,4),dtype='uint8');rgba[on,:3]=np.round(cells[on]).clip(0,255).astype('uint8');rgba[on,3]=255;edge=pl.clean_edge(rgba,key,'rule');canvas=np.zeros((112,144,4),dtype='uint8');dx=14-req['masterAt'][0];dy=17-req['masterAt'][1];sx0=max(0,-dx);sy0=max(0,-dy);sx1=min(cols,144-dx);sy1=min(rows,112-dy);canvas[dy+sy0:dy+sy1,dx+sx0:dx+sx1]=rgba[sy0:sy1,sx0:sx1];closed,outline=pl.close_outline(canvas,(0,0,24),'rule');filled=np.zeros_like(canvas);ox=-outline['offset'][0];oy=-outline['offset'][1];h,w=closed.shape[:2];assert ox>=0 and oy>=0 and ox+w<=144 and oy+h<=112;filled[oy:oy+h,ox:ox+w]=closed;idx=allow[((filled[:,:,:3].astype(np.int32)[:,:,None,:]-p[None,None,allow,:])**2).sum(-1).argmin(-1)].astype('uint8');idx[filled[:,:,3]==0]=0;final=master.copy();final[mask]=idx[mask];assert np.array_equal(final[~mask],master[~mask]);im=Image.fromarray(final);im.putpalette(pal);im.save(r/f'provisional/{id}-arms.png',bits=4);records.append({'id':id,'verified_lattice':fit,'edge':edge,'outline':outline,'source':rec['source'],'pixels_outside_arm_mask_equal_common_master':True})
(r/'arm-read-records.json').write_text(json.dumps({'arm_rows':[28,83],'protected_head_polygon':[(46,17),(113,17),(115,25),(106,31),(98,45),(83,62),(58,71),(44,64),(32,50),(38,37)],'poses':records},indent=2));page=Image.new('RGB',(1152,254),(88,120,120));d=ImageDraw.Draw(page)
for i,id in enumerate(['03','04','05','06']):
 im=Image.open(r/f"provisional/{id}{'-arms' if id!='03' else ''}.png");page.paste(im.convert('RGB').resize((288,224),Image.Resampling.NEAREST),(288*i,26));d.text((288*i+8,7),id,fill='white')
page.save(r/'combo-check.png');print('Read complete arm regions on verified lattice; head/lower body locked.')
