from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,shutil,hashlib
r=Path('/workspace/work/mecha-impact-v002');o=r/'deliverables';o.mkdir(exist_ok=True)
for n in ['native','previews','bmp','processing']:(o/n).mkdir(exist_ok=True)
plan=json.loads((r/'plan.json').read_text());gen={q['id']:q for q in json.loads((r/'generation-records.json').read_text())};base=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/v001/mecha-final-1x.png');pal=Image.open(base).getpalette();spec=[]
for row in plan:
 id=row['id'];name=id+'-'+row['name'];dest=o/'native'/(name+'.png');rec=dict(row)
 shutil.copy2(r/'provisional'/(id+'.png') if row['new'] else row['source'],dest)
 if row['new']:
  p=o/'processing'/id;p.mkdir(exist_ok=True);shutil.copytree(r/f'ask-{id}',p/'ask',dirs_exist_ok=True);shutil.copytree(r/f'extracted-{id}',p/'extracted',dirs_exist_ok=True);shutil.copy2(gen[id]['source'],p/'generated-source.png');(p/'host-prompt.txt').write_text(gen[id]['prompt'] or '');rec['extraction']=json.loads((r/f'extracted-{id}/pose-{id}.json').read_text())
 im=Image.open(dest);a=np.array(im);assert im.mode=='P' and im.size==(144,112) and im.getpalette()==pal and 'transparency' not in im.info
 im.resize((864,672),Image.Resampling.NEAREST).save(o/'previews'/(name+'-6x.png'));im.save(o/'bmp'/(name+'.bmp'));y,x=np.where(a!=0);rec.update(file='native/'+name+'.png',canvas=[144,112],palette_entries=16,used_colours=len(np.unique(a)),occupied_bounds_exclusive=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],sha256=hashlib.sha256(dest.read_bytes()).hexdigest());spec.append(rec)
assert len({Image.open(o/q['file']).tobytes() for q in spec})==30
page=Image.new('RGB',(1728,1270),(88,120,120));d=ImageDraw.Draw(page)
for i,row in enumerate(spec):
 x=i%6*288;y=i//6*254;d.text((x+5,y+6),row['id']+' '+row['name'],fill='white');page.paste(Image.open(o/row['file']).convert('RGB').resize((288,224),Image.Resampling.NEAREST),(x,y+28))
page.save(o/'all-30-poses.png');(o/'specification.json').write_text(json.dumps({'version':'impact-flow-v002','status':'draft for visual review','unique_sprite_count':30,'newly_generated_pose_count':23,'reused_dash_sprites':2,'reused_approved_attack_endpoints':5,'attack_pose_count':28,'sequence':['heavy','uppercut1','kick','uppercut2','combo','palm'],'background_rgb':pal[:3],'native_canvas':[144,112],'palette_entries':16,'frames':spec,'game_import_compatibility':'not verified'},indent=2))
print('Packaged',len(spec))
