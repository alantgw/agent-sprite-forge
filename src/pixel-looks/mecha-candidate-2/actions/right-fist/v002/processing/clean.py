from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,shutil
from scipy.ndimage import label,find_objects
root=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2');src=root/'actions/right-fist/v001';out=Path('/workspace/work/mecha-right-fist-v002/deliverables');out.mkdir(exist_ok=False)
im=Image.open(src/'mecha-right-fist-1x.png');a=np.array(im);old=a.copy();lab,n=label(a!=0,structure=np.ones((3,3)));box=(22,82,31,85);target=[]
for i,sl in enumerate(find_objects(lab),1):
 b=(sl[1].start,sl[0].start,sl[1].stop,sl[0].stop)
 if b==box:target.append(i)
assert len(target)==1
remove=lab==target[0];assert int(remove.sum())==18
a[remove]=0;assert np.array_equal(a[~remove],old[~remove])
new=Image.fromarray(a);new.putpalette(im.getpalette());new.save(out/'mecha-right-fist-1x.png',bits=4);new.save(out/'mecha-right-fist.bmp');new.resize((864,672),Image.Resampling.NEAREST).save(out/'mecha-right-fist-6x.png',bits=4)
base=Image.open(root/'v001/mecha-final-1x.png');page=Image.new('RGB',(1152,500),(88,120,120));d=ImageDraw.Draw(page);d.text((18,10),'Approved base',fill='white');d.text((594,10),'Right fist / detached pin removed',fill='white');page.paste(base.convert('RGB').resize((576,448),Image.Resampling.NEAREST),(0,36));page.paste(new.convert('RGB').resize((576,448),Image.Resampling.NEAREST),(576,36));page.save(out/'base-right-fist-comparison.png')
re=Image.open(out/'mecha-right-fist-1x.png');assert re.size==(144,112) and re.getpalette()==im.getpalette() and len(set(re.get_flattened_data()))==16 and 'transparency' not in re.info
assert label(a!=0,structure=np.ones((3,3)))[1]==1
meta={'canvas':[144,112],'palette_entries':16,'used_entries':16,'palette_identical_to_v001':True,'background_rgb':[88,120,120],'opaque':True,'removed_component_bounds_xyxy_exclusive':box,'removed_pixels':18,'all_other_pixels_unchanged':True,'method':'remove only the detached connected component explicitly identified by the user; replace its indices with background index 0','previous_version':'../v001','game_import_compatibility':'not verified'};(out/'specification.json').write_text(json.dumps(meta,indent=2));(out/'report.txt').write_text('Removed the detached dark pin in front of the anatomical right leg (viewers left). Exactly 18 foreground pixels within [22,82,31,85) replaced with background palette index 0. All other pixels and palette entries match right-fist v001 exactly.\nNative 144x112, same 16 stored and used palette entries, opaque teal RGB(88,120,120). Preview uses exact 6x nearest-neighbour. Indexed BMP included. Original v001 retained. No additional generation or editor/game-file changes. Game-import compatibility not verified.\n')
proc=out/'processing';proc.mkdir();shutil.copy2('/workspace/work/mecha-right-fist-v002/clean.py',proc/'clean.py');(out/'sha256.json').write_text(json.dumps({str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*') if p.is_file()},indent=2));shutil.copytree(out,root/'actions/right-fist/v002');print(json.dumps(meta))
