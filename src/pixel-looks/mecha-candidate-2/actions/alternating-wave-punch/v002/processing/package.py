from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,shutil,hashlib
r=Path('/workspace/work/mecha-punch-option2-v001');o=r/'deliverables';o.mkdir();root=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2');old=root/'actions/alternating-wave-punch/v001';base=Image.open(root/'v001/mecha-final-1x.png');original=Image.open(old/'B-left-punch-1x.png');pal=original.getpalette();p=np.array(pal,dtype=np.int32).reshape(-1,3);allowed=np.array([1,2]+list(range(4,16)));a=np.array(Image.open(r/'extracted/left-punch-retracted.png').convert('RGBA'));idx=allowed[(((a[:,:,:3].astype(np.int32)[:,:,None,:]-p[None,None,allowed,:])**2).sum(-1)).argmin(-1)].astype('uint8');idx[a[:,:,3]==0]=0
full=np.zeros((112,144),dtype='uint8');full[7:109,25:136]=idx;arr=np.array(original);mask=np.zeros(arr.shape,bool);mask[40:77,30:66]=True;new=arr.copy();new[mask]=full[mask];assert np.array_equal(new[~mask],arr[~mask]);im=Image.fromarray(new);im.putpalette(pal);im.save(o/'B-left-punch-right-arm-back-1x.png',bits=4);im.save(o/'B-left-punch-right-arm-back.bmp');im.resize((864,672),Image.Resampling.NEAREST).save(o/'B-left-punch-right-arm-back-6x.png',bits=4)
for n in ['A-right-punch-1x.png','A-right-punch-6x.png','A-right-punch.bmp','chi-wave-1x.png','chi-wave-6x.png']:shutil.copy2(old/n,o/n)
frames=[Image.open(o/'A-right-punch-1x.png'),im];fx=Image.open(o/'chi-wave-1x.png').convert('RGBA');anchors=[(16,55),(69,56)];stageframes=[]
for t in range(20):
 phase=(t//5)%2;stage=Image.new('RGB',(280,128),tuple(pal[:3]));ar=np.array(frames[phase].convert('RGBA'));ar[np.array(frames[phase])==0,3]=0;body=Image.fromarray(ar);stage.paste(body,(128,8),body)
 for birth in range(0,t+1,5):
  age=t-birth
  if age>8:continue
  ex,ey=anchors[(birth//5)%2];stage.paste(fx,(128+ex-fx.width-age*15,8+ey-fx.height//2),fx)
 stageframes.append(stage.resize((1120,512),Image.Resampling.NEAREST))
stageframes[0].save(o/'firing-loop.gif',save_all=True,append_images=stageframes[1:],duration=40,loop=0,optimize=False,disposal=2)
plain=[f.resize((576,448),Image.Resampling.NEAREST) for f in frames];plain[0].save(o/'pose-only-loop.gif',save_all=True,append_images=plain[1:],duration=200,loop=0,optimize=False,disposal=2)
page=Image.new('RGB',(1296,390),tuple(pal[:3]));d=ImageDraw.Draw(page)
for i,(f,s) in enumerate(zip([base,original,im],['Approved base / same 3x','Final option 1: left punch','Option 2: right arm pulled back'])):d.text((432*i+12,12),s,fill='white');page.paste(f.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(432*i,38))
page.save(o/'option-comparison.png');re=Image.open(o/'B-left-punch-right-arm-back-1x.png');assert re.mode=='P' and re.size==(144,112) and re.getpalette()==pal and 'transparency' not in re.info;assert len(set(new.ravel()))<=16
assert (o/'A-right-punch-1x.png').read_bytes()==(old/'A-right-punch-1x.png').read_bytes()
g=Image.open(o/'firing-loop.gif');assert g.n_frames==20
for i,f in enumerate(stageframes):g.seek(i);assert g.convert('RGB').tobytes()==f.tobytes()
y,x=np.where(new!=0);record=json.loads((r/'extracted/left-punch-retracted.json').read_text());meta={'option':2,'status':'for review; option 1 remains accepted final','canvas':[144,112],'palette_entries':16,'used_colours':len(set(new.ravel().tolist())),'occupied_bounds_exclusive':[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],'background_rgb':pal[:3],'change_mask_exclusive':[30,40,66,77],'pixels_changed_from_option1':int((new!=arr).sum()),'all_pixels_outside_inactive_arm_box_identical_to_option1':True,'right_punch_frame_identical_bytes_to_option1':True,'art_source':'host_image','route':'built-in image_gen','extraction':record};(o/'specification.json').write_text(json.dumps(meta,indent=2))
(o/'README.md').write_text('''# Option 2 — right arm chambered back during left punch

Option 1 remains the user-accepted final option, unchanged in `../v001/`. This alternative changes only the inactive right arm in the left-punch drawing: raised, bent and pulled back beside the ribs instead of hanging down. The left punch, head, body, proportions, legs, feet and hair retain the exact pixels of option 1 outside the documented inactive-arm box. The right-punch frame and separate projectile are copied byte-for-byte from option 1.

![Option 2 firing preview](firing-loop.gif)

[Pose-only loop](pose-only-loop.gif) · [Base and both options side by side](option-comparison.png)

- [Left punch with right arm back — native PNG](B-left-punch-right-arm-back-1x.png) · [6x](B-left-punch-right-arm-back-6x.png) · [BMP](B-left-punch-right-arm-back.bmp)
- [Unchanged right punch — native PNG](A-right-punch-1x.png) · [6x](A-right-punch-6x.png)

144×112; exact original 16-entry indexed palette, 15 entries used, opaque teal RGB(88,120,120). Nearest-neighbour previews. Exactly two character drawings; energy wave travels separately. Same preview timing as option 1: 200ms per body pose, 40ms projectile ticks. Built-in image_gen edit followed by repository pixel-looks ask-pose/pose on option 1's lattice. Strict source/master match 89.8%; extractor retained 93.06% master cells. Final composition additionally locks every pixel outside inactive-arm box x30..65/y40..76 to option 1. No fallback pipeline used. Numeric checks do not replace visual approval. No game-import compatibility claim.

Generated source, request and extraction records retained in processing/. Earlier options and original references are preserved.
''')
proc=o/'processing';proc.mkdir();shutil.copytree(r/'ask',proc/'ask-pose');shutil.copytree(r/'extracted',proc/'extracted');shutil.copy2(r/'package.py',proc/'package.py');shutil.copy2(r/'read.py',proc/'read.py');shutil.copy2('/workspace/generated_images/exec-1282dc35-a1af-4c1a-bfab-d948eba73016.png',proc/'generated-source.png')
(o/'sha256.json').write_text(json.dumps({str(f.relative_to(o)):hashlib.sha256(f.read_bytes()).hexdigest() for f in o.rglob('*') if f.is_file()},indent=2));print(json.dumps({k:v for k,v in meta.items() if k!='extraction'},indent=2))
