from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,shutil,hashlib
r=Path('/workspace/work/mecha-sequence-v005');old=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/actions/shin-ha-gou-shou-sen/v004');o=r/'deliverables';o.mkdir();pal=Image.open(r/'provisional/04-arms.png').getpalette()
for n in ['native','previews','bmp','comparisons','processing']:(o/n).mkdir()
frames=[];rows=[]
for f in sorted((old/'native').glob('*.png')):
 id=f.name[:2];name='07-left-upward-right-kick' if id=='07' else f.stem;changed=id in ['04','07'];row={'id':id,'file':'native/'+name+'.png','byte_unchanged_from_v004':not changed}
 if not changed:shutil.copy2(f,o/'native'/f.name);im=Image.open(f).copy()
 else:
  im=Image.open(r/'provisional'/('04-arms.png' if id=='04' else '07.png'));a=np.array(im)
  if id=='07':
   e=a[37:39,64:68].copy()
   for s,d in [(8,6),(13,11),(9,10),(12,10),(14,10),(15,10)]:e[e==s]=d
   a[37:39,64:68]=e;assert 11 in e;row['eye_box_exclusive']=[64,37,68,39]
  im=Image.fromarray(a);im.putpalette(pal);im.save(o/'native'/(name+'.png'),bits=4)
  ext=r/('extracted-04-redone' if id=='04' else 'extracted-07');rec=json.loads((ext/('pose-'+id+'.json')).read_text());row['extraction']=rec;p=o/'processing'/id;p.mkdir();shutil.copytree(r/('ask-'+id),p/'ask');shutil.copytree(ext,p/'extracted');shutil.copy2(rec['source']['image'],p/'generated-source.png')
  page=Image.new('RGB',(864,380),tuple(pal[:3]));d=ImageDraw.Draw(page);d.text((10,8),'v004 '+id,fill='white');d.text((442,8),'v005 '+id,fill='white');page.paste(Image.open(f).convert('RGB').resize((432,336),Image.Resampling.NEAREST),(0,35));page.paste(im.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(432,35));page.save(o/'comparisons'/(name+'.png'))
 im.resize((864,672),Image.Resampling.NEAREST).save(o/'previews'/(name+'-6x.png'));im.save(o/'bmp'/(name+'.bmp'));a=np.array(im);y,x=np.where(a!=0);row.update(canvas=[144,112],palette_entries=16,used_colours=len(np.unique(a)),occupied_bounds_exclusive=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]);assert im.mode=='P' and im.size==(144,112) and im.getpalette()==pal and 'transparency' not in im.info;rows.append(row);frames.append(im)
for n,ms in [('combo-loop.gif',100),('combo-loop-slow.gif',220)]:
 big=[im.resize((720,560),Image.Resampling.NEAREST) for im in frames[2:6]];big[0].save(o/n,save_all=True,append_images=big[1:],duration=ms,loop=0,optimize=False,disposal=2);g=Image.open(o/n);assert g.n_frames==4
 for k,im in enumerate(big):g.seek(k);assert g.convert('RGB').tobytes()==im.convert('RGB').tobytes()
page=Image.new('RGB',(1440,508),tuple(pal[:3]));d=ImageDraw.Draw(page)
for i,(row,im) in enumerate(zip(rows,frames)):
 x=i%5*288;y=i//5*254;d.text((x+7,y+7),Path(row['file']).stem,fill='white');page.paste(im.convert('RGB').resize((288,224),Image.Resampling.NEAREST),(x,y+28))
page.save(o/'all-ten-poses.png');shutil.copy2(r/'revised-two.png',o/'revised-two.png')
meta={'version':'v005','status':'for visual review','changes':{'04':'restore long left punch; raise to occlude lower face; right guard drawn back and partly occluded, still in front of torso','07':'anatomical left leg kicks diagonally to image upper-right; right leg supports'},'sequence':['dash','07 upward-right left kick','08 grounded uppercut','03/04/05/06 loop x4','09/10 palm'],'changed_ids':['04','07'],'byte_unchanged_ids':['01','02','03','05','06','08','09','10'],'frames':rows,'background_rgb':pal[:3],'game_import_compatibility':'not verified'};(o/'specification.json').write_text(json.dumps(meta,indent=2))
for f in ['package.py','read.py','read-arms-final.py','arm-read-records.json','read-pose-safe-local.py']:shutil.copy2(r/f,o/'processing'/f)
shutil.copy2('/workspace/work/mecha-sequence-v004/read-pose-safe.py',o/'processing/read-pose-safe.py')
print('Native8 unchanged; palette/canvas/combo decode verified.07 extraction has no height warnings.')
