from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,shutil,json,hashlib
r=Path('/workspace/work/mecha-sequence-v007');o=r/'deliverables';o.mkdir();old=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/actions/shin-ha-gou-shou-sen/v006')
for n in ['native','previews','bmp','comparisons','processing']:(o/n).mkdir()
rows=[];frames=[]
for f in sorted((old/'native').glob('*.png')):
 changed=f.name.startswith('07-');name='07-left-cross-rising-kick' if changed else f.stem
 if changed:
  original=Image.open(f);im=Image.open(r/'provisional/07.png');arr=np.array(im);arr[41:43,73:77][arr[41:43,73:77]==8]=6;im=Image.fromarray(arr);im.putpalette(original.getpalette());im.save(o/'native'/(name+'.png'),bits=4);assert im.getpalette()==original.getpalette()
  page=Image.new('RGB',(864,380),(88,120,120));d=ImageDraw.Draw(page)
  for j,(pic,label) in enumerate([(original,'v006'),(im,'v007 - cross-body rising kick')]):page.paste(pic.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(j*432,35));d.text((j*432+10,8),label,fill='white')
  page.save(o/'comparisons/07-redesigned-kick.png')
 else:shutil.copy2(f,o/'native'/f.name);im=Image.open(f).copy();assert (o/'native'/f.name).read_bytes()==f.read_bytes()
 im.resize((864,672),Image.Resampling.NEAREST).save(o/'previews'/(name+'-6x.png'));im.save(o/'bmp'/(name+'.bmp'));a=np.array(im);y,x=np.where(a!=0);rows.append({'id':f.name[:2],'file':'native/'+name+'.png','byte_unchanged_from_v006':not changed,'canvas':[144,112],'palette_entries':16,'used_colours':len(np.unique(a)),'occupied_bounds_exclusive':[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]});assert im.mode=='P' and im.size==(144,112) and 'transparency' not in im.info;frames.append(im)
for fn in ['combo-loop.gif','combo-loop-slow.gif']:shutil.copy2(old/fn,o/fn)
page=Image.new('RGB',(1440,508),(88,120,120));d=ImageDraw.Draw(page)
for i,(row,im) in enumerate(zip(rows,frames)):
 x=i%5*288;y=i//5*254;d.text((x+7,y+7),Path(row['file']).stem,fill='white');page.paste(im.convert('RGB').resize((288,224),Image.Resampling.NEAREST),(x,y+28))
page.save(o/'all-ten-poses.png');meta={'version':'v007','change':'07 regenerated from unmirrored base: anatomical left-leg cross-body kick to body-relative right-front-up, in front of head. Face remains left and rear mane trails right.','source_version':'v006','unchanged_native_count':9,'frames':rows,'palette_and_eye_colours':'original16-entry palette; red-eye shadow corrected to original palette','background_rgb':[88,120,120],'game_import_compatibility':'not verified'};(o/'specification.json').write_text(json.dumps(meta,indent=2));shutil.copy2(r/'package.py',o/'processing/package.py')
rec=json.loads((r/'extracted-07/pose-07.json').read_text());meta['extraction_07']=rec;meta['latest04']='exact native PNG from v005, copied unchanged through v006';(o/'specification.json').write_text(json.dumps(meta,indent=2));shutil.copytree(r/'ask-07',o/'processing/07/ask');shutil.copytree(r/'extracted-07',o/'processing/07/extracted');shutil.copy2(rec['source']['image'],o/'processing/07/generated-source.png');shutil.copy2(r/'read.py',o/'processing/read.py')
s=Path('/workspace/work/mecha-sequence-v006/build-demo.py').read_text().replace('mecha-sequence-v006','mecha-sequence-v007').replace("'source_version':'v006'","'source_version':'v007'").replace('UPWARD KICK - FACING LEFT','LEFT CROSS-BODY RISING KICK');(r/'build-demo.py').write_text(s)
assert (o/'native/04-combo-left-hit.png').read_bytes()==Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/actions/shin-ha-gou-shou-sen/v005/native/04-combo-left-hit.png').read_bytes()
print('Latest04 and8 other sprites unchanged.07 extracted on original master lattice.')
