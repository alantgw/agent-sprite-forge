from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np,shutil,hashlib
r=Path('/workspace/work/mecha-video-rebuild-v001');o=r/'deliverables';o.mkdir();byid={q['id']:q for q in json.loads((r/'plan.json').read_text())};gen={q['id']:q for q in json.loads((r/'generation-records-final.json').read_text())};art=json.loads((r/'art-processing.json').read_text());order=[1,2,3,4,5,20,21,22,23,24,6,7,8,9,10,11,12,13,14,15,16,17,18,19,25,26,27,28,29,30];pal=Image.open('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/v001/mecha-final-1x.png').getpalette()
for n in ['native','previews','bmp','processing']:(o/n).mkdir()
frames=[];spec=[]
for i,slot in enumerate(order,1):
 row=byid[f'{slot:02}'];sid=row['id'];id=f'{i:02}';name=id+'-'+row['name'];dest=o/'native'/(name+'.png');rec=dict(row);rec['source_slot']=sid;rec['id']=id;rec['new_generation']=row['new'];rec['adapted_common_body']=slot in [20,21,22,23,24]
 if row['new'] or rec['adapted_common_body']:shutil.copy2(r/'provisional'/(sid+'.png'),dest);rec['art_processing']=art.get(sid,{})
 else:shutil.copy2(row['source'],dest);assert dest.read_bytes()==Path(row['source']).read_bytes();rec['byte_identical_to_source']=True
 if row['new']:
  p=o/'processing'/id;p.mkdir();shutil.copytree(r/f'ask-{sid}',p/'ask');shutil.copytree(r/f'extracted-{sid}',p/'extracted');shutil.copy2(gen[sid]['source'],p/'generated-source.png');(p/'host-prompt.txt').write_text(gen[sid]['prompt']);rec['extraction']=json.loads((r/f'extracted-{sid}/pose-{sid}.json').read_text())
  if gen[sid].get('rejected_source'):shutil.copy2(gen[sid]['rejected_source'],p/'rejected-oversized-gauntlet.png');rec['rejected_source_reason']=gen[sid]['rejected_reason']
 im=Image.open(dest);a=np.array(im);assert im.mode=='P' and im.size==(144,112) and im.getpalette()==pal and 'transparency' not in im.info;im.resize((864,672),Image.Resampling.NEAREST).save(o/'previews'/(name+'-6x.png'));im.save(o/'bmp'/(name+'.bmp'));y,x=np.where(a!=0);rec.update(file='native/'+name+'.png',canvas=[144,112],palette_entries=16,used_colours=len(np.unique(a)),occupied_bounds_exclusive=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],sha256=hashlib.sha256(dest.read_bytes()).hexdigest());assert rec['used_colours']<=16;spec.append(rec);frames.append(im.copy())
assert len({im.tobytes() for im in frames})==30
page=Image.new('RGB',(1728,1270),(88,120,120));d=ImageDraw.Draw(page)
for i,(row,im) in enumerate(zip(spec,frames)):
 x=i%6*288;y=i//6*254;d.text((x+5,y+6),row['id']+' '+row['name'],fill='white');page.paste(im.convert('RGB').resize((288,224),Image.Resampling.NEAREST),(x,y+28))
page.save(o/'all-30-poses.png');meta={'version':'video-rebuild-v001','status':'draft for visual review','unique_sprite_count':30,'newly_generated_pose_count':22,'reused_key_pose_sources':8,'byte_unchanged_whole_sprites':6,'existing_punch_arm_endpoints_adapted_to_shared_body':2,'base':'approved Candidate2v001','background_rgb':pal[:3],'native_canvas':[144,112],'palette_entries':16,'frames':spec,'art_source':'host image_gen; existing approved base and8key poses used only where appropriate','motion_design':'new video-based close combat -> turning kick -> uppercut -> alternating airborne pursuit -> landing -> palm finish; no previous spin-followup cycle','game_import_compatibility':'not verified'};(o/'specification.json').write_text(json.dumps(meta,indent=2))
for f in ['plan.py','plan.json','generation-records-all.json','generation-records-final.json','doctor.json','read.py','extract.py','prepare.py','finish-art.py','art-processing.json','package.py']:shutil.copy2(r/f,o/'processing'/f)
print('30different native poses;22 new;6exact endpoint copies;2reused punch-arm poses adapted. Same144x112 palette and opaque teal verified.')
