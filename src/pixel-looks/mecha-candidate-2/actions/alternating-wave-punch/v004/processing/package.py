from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,shutil,hashlib
r=Path('/workspace/work/mecha-option1-branch-v001');o=r/'selected-loop-v001';o.mkdir();repo=Path('/workspace/agent-sprite-forge');base=Image.open(repo/'src/pixel-looks/mecha-candidate-2/v001/mecha-final-1x.png');pal=base.getpalette();p=np.array(pal,dtype=np.int32).reshape(-1,3);allowed=np.array([1,2]+list(range(4,16)));arrays=[];records=[]
for folder,name in [('selected-extracted','selected-left-punch'),('right-extracted','selected-right-punch')]:
 rec=json.loads((r/f'{folder}/{name}.json').read_text());a=np.array(Image.open(r/f'{folder}/{name}.png').convert('RGBA'));idx=allowed[(((a[:,:,:3].astype(np.int32)[:,:,None,:]-p[None,None,allowed,:])**2).sum(-1)).argmin(-1)].astype('uint8');idx[a[:,:,3]==0]=0
 mx,my=rec['masterAt'];at=(25-mx,7-my);h,w=idx.shape;full=np.zeros((112,144),dtype='uint8');full[at[1]:at[1]+h,at[0]:at[0]+w]=idx;arrays.append(full);records.append(rec)
# Only arms/chest overlap change. Selected left drawing supplies the common head and stance.
mask=np.zeros((112,144),bool);mask[38:79]=True;arrays[1][~mask]=arrays[0][~mask];assert np.array_equal(arrays[0][~mask],arrays[1][~mask]);frames=[];spec=[]
for name,a in zip(['left-punch','right-punch'],arrays):
 im=Image.fromarray(a);im.putpalette(pal);im.save(o/f'{name}-1x.png',bits=4);im.save(o/f'{name}.bmp');im.resize((864,672),Image.Resampling.NEAREST).save(o/f'{name}-6x.png',bits=4);frames.append(im);y,x=np.where(a!=0);re=Image.open(o/f'{name}-1x.png');assert re.mode=='P' and re.size==(144,112) and re.getpalette()==pal and 'transparency' not in re.info
 spec.append({'file':name+'-1x.png','occupied_bounds_exclusive':[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],'used_colours':len(set(a.ravel().tolist()))})
for filename,ms in [('alternating-loop.gif',180),('alternating-loop-slow.gif',350)]:
 enlarged=[im.resize((720,560),Image.Resampling.NEAREST) for im in frames];enlarged[0].save(o/filename,save_all=True,append_images=enlarged[1:],duration=ms,loop=0,optimize=False,disposal=2);g=Image.open(o/filename);assert g.n_frames==2
 for i,expected in enumerate(enlarged):g.seek(i);assert g.convert('RGB').tobytes()==expected.convert('RGB').tobytes()
page=Image.new('RGB',(864,380),tuple(pal[:3]));d=ImageDraw.Draw(page)
for i,(f,txt) in enumerate(zip(frames,['Selected first image: left punch','Companion: right punch'])):d.text((i*432+12,10),txt,fill='white');page.paste(f.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(i*432,35))
page.save(o/'two-poses.png');meta={'source_selection':'user attached first generated image exec-885e0b6d, not the later shortened revisions','canvas':[144,112],'palette_entries':16,'background_rgb':pal[:3],'frames':spec,'sequence':['left-punch-1x.png','right-punch-1x.png'],'normal_ms_per_pose':180,'slow_ms_per_pose':350,'shared_body':'every pixel outside rows38..78 identical between frames','effects':'none','route':'built-in image_gen','art_source':'host_image','extraction_records':records,'game_import_compatibility':'not verified'};(o/'specification.json').write_text(json.dumps(meta,indent=2))
(o/'README.md').write_text('''# Selected first image — alternating left/right punch loop

Uses the first image explicitly reattached by the user (generated source exec-885e0b6d), not subsequent shortened-punch attempts. A reciprocal right punch was generated from that image, exchanging the arms without mirroring the character. The selected longer left reach is deliberately retained; no claim that it matches the superseded20% target.

![Alternating punches](alternating-loop.gif)

[Slow inspection loop](alternating-loop-slow.gif) · [Both poses](two-poses.png)

| Pose | Native PNG | 6x nearest preview | Indexed BMP |
| --- | --- | --- | --- |
| Selected left punch | [PNG](left-punch-1x.png) | [Preview](left-punch-6x.png) | [BMP](left-punch.bmp) |
| Right punch | [PNG](right-punch-1x.png) | [Preview](right-punch-6x.png) | [BMP](right-punch.bmp) |

Exactly two body frames, 144×112, original16-entry palette,15 colours used, opaque teal RGB(88,120,120). No energy or effects in this motion preview. Normal180ms/pose; slow350ms/pose. All enlargements nearest-neighbour. Head, mane, waist/lower body and feet share fixed pixels outside rows38..78; shoulder/arm/chest overlap changes with each punch.

Art route: built-in image_gen; repository pixel-looks ask-pose/pose extraction on approved option1 lattice. Strict master match79.14% (left),76.44% (right), retained master81.89% and79.79%. Generated pictures are sampled on measured grid, then mapped to approved palette without rescaling cells. Pose extraction retains master cells outside detected changes, so native sprites are processed derivatives rather than literal downscales of source images. Reciprocal drawing uses selected image as design reference; extractor still registers to original option1 master. No fallback route. Numeric QA does not approve anatomy. Two drawings snap directly between punches; no recovery in-betweens or interpolation are claimed.

Final option1 and all previous revisions remain untouched. No game import compatibility claim. Generated source pictures, requests and extraction records retained in processing/.
''')
proc=o/'processing';proc.mkdir();shutil.copytree(r/'ask',proc/'ask-pose');shutil.copytree(r/'selected-extracted',proc/'left-extracted');shutil.copytree(r/'right-extracted',proc/'right-extracted');shutil.copy2(r/'read.py',proc/'read.py');shutil.copy2(r/'loop-package.py',proc/'package.py')
for dest,n in [('selected-left-source.png','exec-885e0b6d-9e08-4107-b1ab-1ce1268c092a.png'),('generated-right-source.png','exec-323c3ee1-8f4b-4cee-bea9-281e7ff4ec31.png')]:shutil.copy2(Path('/workspace/generated_images')/n,proc/dest)
print(json.dumps(spec,indent=2))
