from pathlib import Path
from PIL import Image,ImageDraw,ImageSequence
import numpy as np,json,shutil,zipfile,io,xml.etree.ElementTree as E,sys
sys.path.insert(0,str(Path(__file__).parent));import rig
r=Path(__file__).parent;s=r/'assembled';o=r/'deliverables';o.mkdir(exist_ok=True)
for name in ['native','previews']:shutil.copytree(s/name,o/name,dirs_exist_ok=True)
shutil.copy2(s/'poses.json',o/'poses.json');shutil.copy2(s/'all-30-assembled.png',o/'all-30-poses.png')
records=json.loads((s/'poses.json').read_text());fs=records['frames'];ims=[Image.open(s/q['file']) for q in fs]
order=list(range(1,21))+list(range(21,27))*3+list(range(27,31))
times={1:100,2:70,3:160,4:50,5:130,6:60,7:100,8:60,9:160,10:90,11:70,12:60,13:140,14:80,15:60,16:90,17:90,18:50,19:130,20:70,21:50,22:70,23:50,24:70,25:70,26:70,27:220,28:70,29:170,30:450}
for scale in [1,4]:
 frames=[ims[i-1].resize((144*scale,112*scale),Image.Resampling.NEAREST) for i in order]
 frames[0].save(o/f'action-{scale}x.gif',save_all=True,append_images=frames[1:],duration=[times[i] for i in order],loop=0,optimize=False,disposal=2)
slow=[ims[i-1].resize((576,448),Image.Resampling.NEAREST) for i in order];slow[0].save(o/'action-slow-4x.gif',save_all=True,append_images=slow[1:],duration=[times[i]*2 for i in order],loop=0,optimize=False,disposal=2)
# Every pose also has independently editable, aligned part layers.
(o/'layers-ora').mkdir(exist_ok=True)
def png(im):
 b=io.BytesIO();im.save(b,format='PNG');return b.getvalue()
for q,merged in zip(fs,ims):
 a,layers=rig.render(q['config']);cfg=q['config'];root=E.Element('image',w='144',h='112',name=q['id']+' '+q['name']);stack=E.SubElement(root,'stack')
 def z(n):
  if 'elbow_underlay' in n:return 38
  if n=='open-palm-cuff':return 89
  if n=='open_hand':return cfg['_open_hand'].get('z',95)
  return cfg.get(n,{}).get('z',40)
 with zipfile.ZipFile(o/'layers-ora'/(q['id']+'-'+q['name']+'.ora'),'w',compression=zipfile.ZIP_DEFLATED) as zf:
  zf.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
  for n in reversed(sorted(layers,key=z)):
   ar=layers[n];im=Image.fromarray(ar);im.putpalette(rig.pal);rgba=im.convert('RGBA');rgba.putalpha(Image.fromarray((ar!=0).astype('uint8')*255));path='data/'+n+'.png';zf.writestr(path,png(rgba));E.SubElement(stack,'layer',{'name':n,'src':path,'opacity':'1','visibility':'visible','composite-op':'svg:src-over','x':'0','y':'0'})
  zf.writestr('data/background.png',png(Image.new('RGBA',(144,112),(88,120,120,255))));E.SubElement(stack,'layer',{'name':'opaque teal','src':'data/background.png','opacity':'1','visibility':'visible','composite-op':'svg:src-over','x':'0','y':'0'})
  zf.writestr('stack.xml',E.tostring(root));zf.writestr('mergedimage.png',png(merged));zf.writestr('Thumbnails/thumbnail.png',png(merged.convert('RGBA')))
qa={'canvas':[144,112],'palette_entries':16,'used_colours_by_frame':{},'opaque_teal':True,'unique_native_frames':len({im.tobytes() for im in ims}),'all_part_scales':1,'palm29_30_body_layers_identical':records['palm29_30_body_layers_identical'],'exact_source_forearm_histogram_checks_non_kick':len(records['forearm_checks']),'kick_view':'reused selected v010 left-rear upper-body parts + new horizontal roundhouse lower-body angle','gif_frame_readback':[]}
for q,im in zip(fs,ims):
 assert im.size==(144,112) and im.mode=='P';assert len(im.getpalette())==48;assert 'transparency' not in im.info;assert tuple(im.getpalette()[:3])==(88,120,120);qa['used_colours_by_frame'][q['id']]=len(im.getcolors());prev=Image.open(o/'previews'/(Path(q['file']).stem+'-6x.png')).convert('RGB');assert np.array_equal(np.array(prev),np.repeat(np.repeat(np.array(im.convert('RGB')),6,0),6,1))
for name in ['action-1x.gif','action-4x.gif','action-slow-4x.gif']:
 gif=Image.open(o/name);scale=gif.width//144;frames=[f.copy() for f in ImageSequence.Iterator(gif)];assert len(frames)==len(order)
 for k,(frame,id) in enumerate(zip(frames,order)):
  want=ims[id-1].convert('RGB').resize((144*scale,112*scale),Image.Resampling.NEAREST);assert np.array_equal(np.array(frame.convert('RGB')),np.array(want)),(name,k)
 qa['gif_frame_readback'].append({'file':name,'frames':len(frames),'pixels_exact':True})
(o/'qa.json').write_text(json.dumps(qa,indent=2));(o/'playback.json').write_text(json.dumps({'order':order,'duration_ms':times,'sequence':['dash (2 poses)','forward heavy punch','uppercut','roundhouse','uppercut','alternating punches repeated 3 times','palm strike'],'effects':False,'opponent':False,'jump':False},indent=2))
print(json.dumps(qa,indent=2))
