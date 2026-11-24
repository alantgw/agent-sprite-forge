from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,shutil,json,hashlib
r=Path('/workspace/work/mecha-sequence-v006');o=r/'deliverables';o.mkdir();old=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/actions/shin-ha-gou-shou-sen/v005')
for n in ['native','previews','bmp','comparisons','processing']:(o/n).mkdir()
rows=[];frames=[]
for f in sorted((old/'native').glob('*.png')):
 changed=f.name.startswith('07-');name='07-upward-kick-facing-left' if changed else f.stem
 if changed:
  original=Image.open(f);im=original.transpose(Image.Transpose.FLIP_LEFT_RIGHT);im.save(o/'native'/(name+'.png'),bits=4);assert np.array_equal(np.array(im),np.array(original)[:,::-1]);assert im.getpalette()==original.getpalette()
  page=Image.new('RGB',(864,380),(88,120,120));d=ImageDraw.Draw(page)
  for j,(pic,label) in enumerate([(original,'v005'),(im,'v006 - horizontal flip')]):page.paste(pic.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(j*432,35));d.text((j*432+10,8),label,fill='white')
  page.save(o/'comparisons/07-horizontal-flip.png')
 else:shutil.copy2(f,o/'native'/f.name);im=Image.open(f).copy();assert (o/'native'/f.name).read_bytes()==f.read_bytes()
 im.resize((864,672),Image.Resampling.NEAREST).save(o/'previews'/(name+'-6x.png'));im.save(o/'bmp'/(name+'.bmp'));a=np.array(im);y,x=np.where(a!=0);rows.append({'id':f.name[:2],'file':'native/'+name+'.png','byte_unchanged_from_v005':not changed,'canvas':[144,112],'palette_entries':16,'used_colours':len(np.unique(a)),'occupied_bounds_exclusive':[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]});assert im.mode=='P' and im.size==(144,112) and 'transparency' not in im.info;frames.append(im)
for fn in ['combo-loop.gif','combo-loop-slow.gif']:shutil.copy2(old/fn,o/fn)
page=Image.new('RGB',(1440,508),(88,120,120));d=ImageDraw.Draw(page)
for i,(row,im) in enumerate(zip(rows,frames)):
 x=i%5*288;y=i//5*254;d.text((x+7,y+7),Path(row['file']).stem,fill='white');page.paste(im.convert('RGB').resize((288,224),Image.Resampling.NEAREST),(x,y+28))
page.save(o/'all-ten-poses.png');meta={'version':'v006','change':'07 exact horizontal pixel reflection; robot faces image-left and raised foot points upper-left. Mirrored pose, not a new anatomical left/right redesign.','source_version':'v005','unchanged_native_count':9,'frames':rows,'palette_and_eye_colours':'identical to v005; no interpolation or recolouring','background_rgb':[88,120,120],'game_import_compatibility':'not verified'};(o/'specification.json').write_text(json.dumps(meta,indent=2));shutil.copy2(r/'flip.py',o/'processing/flip.py')
s=Path('/workspace/work/mecha-sequence-v005/build-demo.py').read_text().replace('mecha-sequence-v005','mecha-sequence-v006').replace("'source_version':'v005'","'source_version':'v006'").replace('LEFT LEG KICKS UP-RIGHT','UPWARD KICK - FACING LEFT');(r/'build-demo.py').write_text(s)
print('07 exact reflection verified;9 other native files byte-identical.')
