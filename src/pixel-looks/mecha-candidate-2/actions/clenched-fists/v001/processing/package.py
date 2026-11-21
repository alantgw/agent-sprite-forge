from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,shutil,hashlib
r=Path('/workspace/work/mecha-fists-v001');out=r/'deliverables';out.mkdir(exist_ok=False)
base=Image.open('/workspace/work/mecha-action-v001/deliverables/mecha-raised-claws-1x.png');pal=base.getpalette();palette=np.array(pal,dtype=np.int32).reshape(-1,3);pose=Image.open(r/'pose/mecha-fists.png').convert('RGBA');assert pose.size==(112,102)
a=np.array(pose);dist=((a[:,:,:3].astype(np.int32)[:,:,None,:]-palette[None,None,1:,:])**2).sum(-1);idx=dist.argmin(-1).astype(np.uint8)+1;idx[a[:,:,3]==0]=0
proposed=np.zeros((112,144),dtype=np.uint8);proposed[7:109,16:128]=idx
original=np.array(base);mask=np.zeros(original.shape,dtype=bool)
boxes=[(21,27,44,53),(84,36,112,60)]
for x0,y0,x1,y1 in boxes:mask[y0:y1,x0:x1]=True
final=original.copy();final[mask]=proposed[mask];assert np.array_equal(final[~mask],original[~mask])
im=Image.fromarray(final);im.putpalette(pal);im.save(out/'mecha-clenched-fists-1x.png',bits=4);im.save(out/'mecha-clenched-fists.bmp');im.resize((864,672),Image.Resampling.NEAREST).save(out/'mecha-clenched-fists-6x.png',bits=4)
page=Image.new('RGB',(1152,490),tuple(pal[:3]));d=ImageDraw.Draw(page);d.text((18,10),'Previous open hands',fill='white');d.text((594,10),'Corrected: tightly clenched fists',fill='white');page.paste(base.convert('RGB').resize((576,448),Image.Resampling.NEAREST),(0,32));page.paste(im.convert('RGB').resize((576,448),Image.Resampling.NEAREST),(576,32));page.save(out/'hand-correction-comparison.png')
re=Image.open(out/'mecha-clenched-fists-1x.png');assert re.size==(144,112) and re.getpalette()==pal and len(set(re.get_flattened_data()))==16 and 'transparency' not in re.info
assert Image.open(out/'mecha-clenched-fists-6x.png').convert('RGB').tobytes()==re.convert('RGB').resize((864,672),Image.Resampling.NEAREST).tobytes()
record={'canvas':[144,112],'palette_entries':16,'used_entries':16,'palette_identical_to_approved_base':True,'background_rgb':pal[:3],'opaque':True,'changed_pixels':int((final!=original).sum()),'changes_confined_to_hand_boxes_xyxy_exclusive':boxes,'all_pixels_outside_boxes_identical':True,'method':'repository ask-pose/pose; original palette lock; hand-region-only compositing','art_source':'host_image','game_import_compatible':'not verified','pose_record':json.loads((r/'pose/mecha-fists.json').read_text())};(out/'specification.json').write_text(json.dumps(record,indent=2))
(out/'report.txt').write_text('Correction: both raised hands are tightly clenched punching fists, rather than an open grabbing gesture.\n144x112 indexed PNG with the exact approved 16-entry palette, all entries used; opaque teal RGB(88,120,120). Exact 6x nearest-neighbour preview and indexed BMP included.\nRepository pixel-looks ask-pose/pose generated the hand correction, with the existing runtime ruler-fit search and temporary one-colour extraction workaround. Final pixels are locked to the approved palette. Only the two documented hand regions are composited into the prior action sprite; every other pixel is verified identical. No editor or repository source changes; no game-import compatibility claim.\n')
proc=out/'processing';proc.mkdir();shutil.copy2('/workspace/generated_images/exec-b6e086da-defc-42f9-84dd-d5fa884c1bcc.png',proc/'generated-source.png');shutil.copytree(r/'ask',proc/'ask');shutil.copytree(r/'pose',proc/'pose');shutil.copy2(r/'package.py',proc/'package.py');shutil.copy2(r/'pose_fit.py',proc/'pose_fit.py')
(out/'sha256.json').write_text(json.dumps({str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*') if p.is_file()},indent=2));print(json.dumps({k:v for k,v in record.items() if k!='pose_record'}))
