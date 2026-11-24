from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,shutil,hashlib
r=Path('/workspace/work/mecha-sequence-v004');o=r/'deliverables';o.mkdir(exist_ok=True);repo=Path('/workspace/agent-sprite-forge');old=repo/'src/pixel-looks/mecha-candidate-2/actions/shin-ha-gou-shou-sen/v003';pal=Image.open(repo/'src/pixel-looks/mecha-candidate-2/v001/mecha-final-1x.png').getpalette()
for n in ['native','previews','bmp','comparisons','processing']:(o/n).mkdir(exist_ok=True)
records=json.loads((r/'generation-records.json').read_text());spec=[];frames=[]
for i,f in enumerate(sorted((old/'native').glob('*.png'))):
 id=f.name[:2];name={'07':'07-low-forward-kick','08':'08-grounded-uppercut'}.get(id,f.stem);unchanged=id not in ['04','07','08'];row={'id':id,'file':'native/'+name+'.png','byte_unchanged_from_v003':unchanged}
 if unchanged:shutil.copy2(f,o/'native'/f.name);im=Image.open(f).copy()
 else:
  im=Image.open(r/'provisional'/('04-arms.png' if id=='04' else id+'.png'));a=np.array(im)
  if id in ['07','08']:
   box={'07':(56,65,60,68),'08':(59,41,62,43)}[id];x,y,X,Y=box;e=a[y:Y,x:X].copy()
   for s,d in [(8,6),(13,11),(9,10),(12,10),(14,10),(15,10)]:e[e==s]=d
   if id=='07':e[1,2]=11
   a[y:Y,x:X]=e;assert 11 in e;row['eye_box_exclusive']=box
  im=Image.fromarray(a);im.putpalette(pal);im.save(o/'native'/(name+'.png'),bits=4)
  p=o/'processing'/id;p.mkdir(exist_ok=True);shutil.copytree(r/('ask-'+id),p/'ask',dirs_exist_ok=True);shutil.copytree(r/('extracted-'+id),p/'extracted',dirs_exist_ok=True);rec=next(q for q in records if q['id']==id);shutil.copy2(rec['source'],p/'generated-source.png');(p/'prompt.txt').write_text(rec['prompt'])
  row['extraction']=json.loads((r/('extracted-'+id)/('pose-'+id+'.json')).read_text())
  page=Image.new('RGB',(864,380),tuple(pal[:3]));d=ImageDraw.Draw(page);d.text((10,8),'v003 '+id,fill='white');d.text((442,8),'v004 '+id,fill='white');page.paste(Image.open(f).convert('RGB').resize((432,336),Image.Resampling.NEAREST),(0,35));page.paste(im.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(432,35));page.save(o/'comparisons'/(name+'.png'))
 im.save(o/'bmp'/(name+'.bmp'));im.resize((864,672),Image.Resampling.NEAREST).save(o/'previews'/(name+'-6x.png'));a=np.array(im);y,x=np.where(a!=0);row.update(canvas=[144,112],palette_entries=16,used_colours=len(np.unique(a)),occupied_bounds_exclusive=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]);assert im.mode=='P' and im.size==(144,112) and im.getpalette()==pal and 'transparency' not in im.info;frames.append(im);spec.append(row)
a,b=np.array(frames[2]),np.array(frames[3]);assert np.array_equal(a[51:76,14:48],b[51:76,14:48])
page=Image.new('RGB',(864,380),tuple(pal[:3]));d=ImageDraw.Draw(page)
for j,k in enumerate([2,3]):d.text((j*432+10,8),f'{k+1:02d} - identical right guard pixels',fill='white');page.paste(frames[k].convert('RGB').resize((432,336),Image.Resampling.NEAREST),(j*432,35));d.rectangle((j*432+14*3,35+51*3,j*432+48*3-1,35+76*3-1),outline='cyan')
page.save(o/'comparisons/03-04-right-guard.png')
for fn,ms in [('combo-loop.gif',100),('combo-loop-slow.gif',220)]:
 big=[im.resize((720,560),Image.Resampling.NEAREST) for im in frames[2:6]];big[0].save(o/fn,save_all=True,append_images=big[1:],duration=ms,loop=0,optimize=False,disposal=2);g=Image.open(o/fn);assert g.n_frames==4
 for k,im in enumerate(big):g.seek(k);assert g.convert('RGB').tobytes()==im.convert('RGB').tobytes()
page=Image.new('RGB',(1440,508),tuple(pal[:3]));d=ImageDraw.Draw(page)
for i,(row,im) in enumerate(zip(spec,frames)):
 x=i%5*288;y=i//5*254;d.text((x+7,y+7),Path(row['file']).stem,fill='white');page.paste(im.convert('RGB').resize((288,224),Image.Resampling.NEAREST),(x,y+28))
page.save(o/'all-ten-poses.png')
meta={'version':'v004','status':'for visual review','sequence':['dash','07 kick','08 grounded uppercut','03/04/05/06 loop x4','09/10 palm'],'new_ids':['04','07','08'],'byte_unchanged_ids':['01','02','03','05','06','09','10'],'right_guard_lock_box_exclusive':[14,51,48,76],'right_guard_pixels_equal_03':True,'background_rgb':pal[:3],'frames':spec,'game_import_compatibility':'not verified'};(o/'specification.json').write_text(json.dumps(meta,indent=2))
for f in ['ask.py','read.py','read-pose-safe.py','read-left-arm.py','arm-read-records.json','generation-records.json','package.py']:shutil.copy2(r/f,o/'processing'/f)
(o/'processing/limitations.md').write_text('The default pose statistics reader fails for a contracted silhouette. The runtime wrapper only pads its comparison array; strict lattice gates are unchanged. Full changed-arm sampling on the same verified lattice removes stale withdrawn-arm remnants. Head, feet and right-guard rectangle are restored from03. Repository source unchanged. An extra04 attempt created an additional limb and was rejected. New view height warnings remain:07=85 versus master101;08=97 versus101. These require visual review; numerical checks do not constitute art approval. Eye colour is explicitly corrected to original dark red. Sources are preserved. Private screenshot references are not redistributed.')
shutil.copy2('/workspace/generated_images/exec-70e558a0-bcc0-41f3-b8e4-6919701a8348.png',o/'processing/rejected-04-extra-limb.png')
print('Packaged 10 sprites;7 byte-identical;04 guard exact; palette and combo GIF readback passed.')
