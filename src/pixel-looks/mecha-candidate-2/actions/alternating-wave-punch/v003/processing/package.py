from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,shutil,hashlib
r=Path('/workspace/work/mecha-punch-option2-v002');o=r/'deliverables';o.mkdir();root=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2');old=root/'actions/alternating-wave-punch/v001';base=Image.open(root/'v001/mecha-final-1x.png');original=Image.open(old/'B-left-punch-1x.png');pal=original.getpalette();p=np.array(pal,dtype=np.int32).reshape(-1,3);allowed=np.array([1,2]+list(range(4,16)));a=np.array(Image.open(r/'extracted/left-punch-extended.png').convert('RGBA'));idx=allowed[(((a[:,:,:3].astype(np.int32)[:,:,None,:]-p[None,None,allowed,:])**2).sum(-1)).argmin(-1)].astype('uint8');idx[a[:,:,3]==0]=0
full=np.zeros((112,144),dtype='uint8');full[7:109,25:136]=idx;arr=np.array(original);mask=np.zeros(arr.shape,bool);mask[38:80,28:118]=True;new=arr.copy();new[mask]=full[mask];assert np.array_equal(new[~mask],arr[~mask]);im=Image.fromarray(new);im.putpalette(pal);im.save(o/'B-left-punch-longer-right-arm-back-1x.png',bits=4);im.save(o/'B-left-punch-longer-right-arm-back.bmp');im.resize((864,672),Image.Resampling.NEAREST).save(o/'B-left-punch-longer-right-arm-back-6x.png',bits=4)
for n in ['A-right-punch-1x.png','A-right-punch-6x.png','A-right-punch.bmp','chi-wave-1x.png','chi-wave-6x.png']:shutil.copy2(old/n,o/n)
frames=[Image.open(o/'A-right-punch-1x.png'),im];fx=Image.open(o/'chi-wave-1x.png').convert('RGBA');anchors=[(16,55),(46,57)];stageframes=[]
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
for i,(f,s) in enumerate(zip([base,original,im],['Approved base / same 3x','Previous option 2: left punch','Revised option 2: longer punch / arm back'])):d.text((432*i+12,12),s,fill='white');page.paste(f.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(432*i,38))
page.save(o/'option-comparison.png');re=Image.open(o/'B-left-punch-longer-right-arm-back-1x.png');assert re.mode=='P' and re.size==(144,112) and re.getpalette()==pal and 'transparency' not in re.info;assert len(set(new.ravel()))<=16
assert (o/'A-right-punch-1x.png').read_bytes()==(old/'A-right-punch-1x.png').read_bytes()
g=Image.open(o/'firing-loop.gif');assert g.n_frames==20
for i,f in enumerate(stageframes):g.seek(i);assert g.convert('RGB').tobytes()==f.tobytes()
y,x=np.where(new!=0);record=json.loads((r/'extracted/left-punch-extended.json').read_text());meta={'option':2,'status':'for review; option 1 remains accepted final','canvas':[144,112],'palette_entries':16,'used_colours':len(set(new.ravel().tolist())),'occupied_bounds_exclusive':[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],'background_rgb':pal[:3],'change_mask_exclusive':[28,38,118,80],'pixels_changed_from_previous_option2':int((new!=arr).sum()),'all_pixels_outside_arm_chest_box_identical_to_previous_option2':True,'right_punch_frame_identical_bytes_to_option1':True,'art_source':'host_image','route':'built-in image_gen','extraction':record};(o/'specification.json').write_text(json.dumps(meta,indent=2))
(o/'README.md').write_text("""# Revised option 2 — longer left punch, right arm swept back

Left punch extends farther forward, requested approximately 40% greater reach. Opposite arm sweeps back behind torso with an open elbow rather than folding beside chest. Shoulder-root perspective changed, so 40% is an artistic target, not a measured anatomical guarantee. Body scale, head, waist and legs preserved outside documented arm/chest overlap box. Final option 1 remains untouched in ../v001/; previous option 2 remains in ../v002/.

![Revised attack loop](firing-loop.gif)

[Pose only](pose-only-loop.gif) · [Base / previous option 2 / revision](option-comparison.png)

[Revised native PNG](B-left-punch-longer-right-arm-back-1x.png) · [Nearest 6x PNG](B-left-punch-longer-right-arm-back-6x.png) · [Indexed BMP](B-left-punch-longer-right-arm-back.bmp)

144×112, exact original16-entry palette,15 colours used, opaque teal RGB(88,120,120). Right-punch companion frame and separate energy wave unchanged. Preview emits the projectile from the revised fist position; only two body drawings are used. Timing unchanged200ms/body pose and40ms projectile ticks.

Built-in image_gen edit, repository pixel-looks ask-pose/pose extraction using original master lattice; strict source match71.13%, master cells retained80.03%, no fallback pipeline. Final palette lock and arm/chest-only composite preserve all pixels outside box x28..117/y38..79. All intermediate generated takes retained: first reach overshot, then corrected twice. Two-frame loop has no recovery in-betweens. Visual anatomy requires review; numeric checks do not approve it. No game import compatibility claim. Original base and option1 unchanged.
""")
proc=o/'processing';proc.mkdir();shutil.copytree(r/'ask',proc/'ask-pose');shutil.copytree(r/'extracted',proc/'extracted');shutil.copy2(r/'package.py',proc/'package.py');shutil.copy2(r/'read.py',proc/'read.py');shutil.copy2('/workspace/generated_images/exec-7f98ad32-df2c-4f0e-836a-e8738f9d6dcc.png',proc/'generated-source.png')
(o/'sha256.json').write_text(json.dumps({str(f.relative_to(o)):hashlib.sha256(f.read_bytes()).hexdigest() for f in o.rglob('*') if f.is_file()},indent=2));print(json.dumps({k:v for k,v in meta.items() if k!='extraction'},indent=2))
