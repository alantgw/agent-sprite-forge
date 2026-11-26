from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np,shutil,hashlib
r=Path('/workspace/work/mecha-thirty-v001');o=r/'deliverables';o.mkdir();plan=json.loads((r/'plan.json').read_text());gen={q['id']:q for q in json.loads((r/'generation-records.json').read_text())};art=json.loads((r/'art-processing.json').read_text());pal=Image.open('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/v001/mecha-final-1x.png').getpalette()
for n in ['native','previews','bmp','processing']:(o/n).mkdir()
frames=[];spec=[]
for row in plan:
 id=row['id'];name=id+'-'+row['name'];dest=o/'native'/(name+'.png');rec=dict(row)
 if row['new']:
  f=r/'provisional'/(id+'.png');shutil.copy2(f,dest);p=o/'processing'/id;p.mkdir();shutil.copytree(r/f'ask-{id}',p/'ask');shutil.copytree(r/f'extracted-{id}',p/'extracted');shutil.copy2(gen[id]['source'],p/'generated-source.png');(p/'host-prompt.txt').write_text(gen[id]['prompt']);rec['extraction']=json.loads((r/f'extracted-{id}/pose-{id}.json').read_text());rec['processing']=art.get(id,{})
 elif id in ['17','18']:
  im=Image.open(row['source']);a=np.array(im);box={'17':[89,31,94,35],'18':[73,43,79,47]}[id];x,y,X,Y=box;e=a[y:Y,x:X].copy()
  for s,d in [(8,6),(13,11),(9,10),(12,10),(14,11),(15,11)]:e[e==s]=d
  a[y:Y,x:X]=e;im=Image.fromarray(a);im.putpalette(pal);im.save(dest,bits=4);rec['eye_palette_correction_box']=box
 else:shutil.copy2(row['source'],dest);assert dest.read_bytes()==Path(row['source']).read_bytes();rec['byte_identical_to_source']=True
 im=Image.open(dest);a=np.array(im);assert im.mode=='P' and im.size==(144,112) and im.getpalette()==pal and 'transparency' not in im.info;im.resize((864,672),Image.Resampling.NEAREST).save(o/'previews'/(name+'-6x.png'));im.save(o/'bmp'/(name+'.bmp'));y,x=np.where(a!=0);rec.update(file='native/'+name+'.png',canvas=[144,112],palette_entries=16,used_colours=len(np.unique(a)),occupied_bounds_exclusive=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],sha256=hashlib.sha256(dest.read_bytes()).hexdigest());assert rec['used_colours']<=16;spec.append(rec);frames.append(im.copy())
assert len({im.tobytes() for im in frames})==30,'must be30different drawings'
# Accepted long-punch and palm endpoints remain exact copies, despite new numbering.
assert next(q for q in spec if q['id']=='22')['byte_identical_to_source']
page=Image.new('RGB',(1728,1270),(88,120,120));d=ImageDraw.Draw(page)
for i,(row,im) in enumerate(zip(spec,frames)):
 x=i%6*288;y=i//6*254;d.text((x+5,y+6),row['id']+' '+row['name'],fill='white');page.paste(im.convert('RGB').resize((288,224),Image.Resampling.NEAREST),(x,y+28))
page.save(o/'all-30-poses.png');(o/'specification.json').write_text(json.dumps({'version':'thirty-v001','unique_sprite_count':30,'newly_generated_count':10,'existing_drawing_count':20,'existing_byte_unchanged_count':18,'existing_eye_palette_corrected_count':2,'base':'approved Candidate2v001','background_rgb':pal[:3],'native_canvas':[144,112],'palette_entries':16,'frames':spec,'art_source':'host image_gen + existing base-derived sprites','motion_method':'held key drawings with integer whole-sprite position;6pose repeated punch cycle','game_import_compatibility':'not verified'},indent=2))
for f in ['plan.py','plan.json','generation-records.json','doctor.json','read.py','extract.py','prepare.py','finish-art.py','art-processing.json','package.py']:shutil.copy2(r/f,o/'processing'/f)
print('30 unique sprites packaged:10 new;18 exact source copies;2 legacy spin eye colour corrections. Original palette/canvas passed.')
