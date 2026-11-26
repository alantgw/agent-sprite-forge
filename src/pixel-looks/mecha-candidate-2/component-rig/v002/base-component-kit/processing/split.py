from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,colorsys
r=Path('/workspace/work/mecha-component-v001');o=r/'kit';o.mkdir(exist_ok=True)
for d in ['aligned','cropped','masks']:(o/d).mkdir(exist_ok=True)
source=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2/v001/mecha-final-1x.png');im=Image.open(source);a=np.array(im);rgb=np.array(im.convert('RGB'));fg=a!=0;labels=np.zeros(a.shape,np.uint8);labels[fg]=1
pieces=[('torso_core',None,[63,63]),
('rear_ribbons',[(80,73),(96,75),(109,78),(119,74),(129,77),(131,91),(127,98),(116,101),(95,102),(86,96),(89,88),(81,83)],[86,78]),
('near_shoulder_wing',[(22,36),(31,37),(33,27),(41,33),(49,42),(48,51),(43,57),(33,56),(24,55),(22,47)],[40,50]),
('far_shoulder_wing',[(72,54),(80,46),(92,41),(111,32),(120,31),(123,36),(128,33),(127,43),(128,47),(119,53),(105,57),(95,60),(83,58)],[87,50]),
('mane',[(39,42),(39,29),(44,18),(53,10),(63,8),(78,8),(94,11),(105,16),(109,25),(108,35),(101,40),(88,42),(76,39),(65,43),(54,43)],[65,36]),
('waist_skirt',[(44,65),(58,65),(66,67),(72,66),(78,72),(80,79),(77,85),(70,87),(61,85),(55,82),(48,83),(42,80),(38,76),(42,71)],[63,77]),
('near_thigh',[(40,78),(49,78),(54,83),(52,92),(48,95),(40,94),(34,89),(35,83)],[48,80]),
('far_thigh',[(73,78),(80,77),(87,81),(91,88),(89,93),(82,95),(77,91),(73,84)],[77,80]),
('near_shin_foot',[(34,87),(43,87),(49,94),(50,100),(46,104),(34,107),(28,109),(20,108),(15,105),(16,101),(22,98),(26,94),(29,90)],[42,90]),
('far_shin_foot',[(79,87),(87,87),(90,92),(91,96),(91,99),(96,102),(100,103),(102,109),(97,111),(84,110),(77,107),(74,101),(75,95)],[85,90]),
('near_upper_arm',[(37,50),(43,50),(48,55),(48,61),(45,68),(39,72),(34,72),(33,64),(36,58)],[41,54]),
('far_upper_arm',[(80,48),(89,48),(97,53),(98,60),(96,65),(91,68),(84,64),(79,58)],[87,53]),
('near_forearm',[(39,52),(40,55),(38,60),(39,67),(36,73),(32,79),(31,84),(26,84),(21,81),(19,76),(21,71),(24,66),(25,61),(26,55),(27,52),(29,52),(30,56),(33,55),(36,52)],[36,60]),
('far_forearm',[(86,48),(88,48),(91,53),(95,53),(100,54),(104,50),(107,51),(108,57),(105,64),(108,65),(108,71),(104,75),(99,78),(96,82),(91,83),(87,80),(85,77),(83,72),(86,68),(83,65),(84,59)],[89,59]),
('head_crests_face',[(46,53),(48,46),(44,43),(42,36),(46,34),(48,27),(49,28),(54,39),(60,35),(65,17),(70,6),(73,8),(70,27),(71,31),(90,23),(100,22),(81,39),(88,36),(112,24),(118,24),(100,36),(78,47),(70,53),(61,56),(54,55)],[60,48])]
for i,(name,poly,pivot) in enumerate(pieces,1):
 if poly:
  m=Image.new('1',im.size);ImageDraw.Draw(m).polygon(poly,fill=1);labels[np.array(m)&fg]=i
# Keep the chest/collar and mechanical rib block together, behind the face.
m=Image.new('1',im.size);ImageDraw.Draw(m).polygon([(45,54),(53,54),(60,53),(67,49),(78,44),(84,43),(87,45),(84,51),(78,57),(75,61),(80,64),(81,69),(76,72),(65,68),(59,67),(55,64),(48,65),(45,61)],fill=1);labels[np.array(m)&fg]=1
# Restore forearm masks above that chest patch.
for i,(name,poly,pivot) in enumerate(pieces,1):
 if name.endswith('_forearm'):
  m=Image.new('1',im.size);ImageDraw.Draw(m).polygon(poly,fill=1);labels[np.array(m)&fg]=i
# Include the far gauntlet thumb/claw edge rather than placing it on a rear ribbon.
m=Image.new('1',im.size);ImageDraw.Draw(m).polygon([(83,74),(90,73),(97,75),(99,78),(96,83),(91,84),(87,82),(83,79)],fill=1);labels[np.array(m)&fg]=14
# The short left-going crest belongs to the head, not the shoulder.
m=Image.new('1',im.size);ImageDraw.Draw(m).polygon([(34,28),(35,36),(43,44),(52,48),(53,42),(43,36)],fill=1);labels[np.array(m)&fg]=len(pieces)
# Split actual fingers from the forearm shell, without inventing any hidden pixels.
for arm,cut,pivot in [('near',75,[26,76]),('far',76,[94,77])]:
 id=next(i for i,q in enumerate(pieces,1) if q[0]==arm+'_forearm');newid=len(pieces)+1;pieces.append((arm+'_claw_hand',None,pivot));mask=(labels==id)&(np.indices(a.shape)[0]>=cut);labels[mask]=newid
# Visible contour cells outside the chest envelope belong to their adjacent component.
yy,xx=np.indices(a.shape);outside=(labels==1)&((yy<43)|(yy>73)|(xx<44)|(xx>84))
from scipy.ndimage import distance_transform_edt
_,where=distance_transform_edt(~((labels>1)&fg),return_indices=True)
labels[outside]=labels[where[0][outside],where[1][outside]]
# Tiny disconnected contour pixels outside the torso belong to the nearest part.
from scipy.ndimage import label, distance_transform_edt
components,n=label(labels==1)
for j in range(1,n+1):
 island=components==j
 if island.sum()>8:continue
 _,where=distance_transform_edt(~((labels>1)&fg),return_indices=True)
 labels[island]=labels[where[0][island],where[1][island]]
# Gold/brown pixels cannot be part of a red rear ribbon: keep these with hand/foot.
col=np.array(im.getpalette()).reshape(-1,3);gold=[i for i,(R,G,B) in enumerate(col) if R>G*1.15 and G>B*1.8 and G>35 and R>70]
for y,x in np.argwhere((labels==2)&np.isin(a,gold)):
 labels[y,x]=17 if y<85 else 10
# Keep the far boot's black heel attachment with the boot, beneath the rear ribbons.
yy,xx=np.indices(a.shape);heel=(labels==2)&(xx>=97)&(xx<=102)&(yy>=96)&(yy<=102)&np.isin(a,[1,2,4,5,7,8]);labels[heel]=10
records=[];recon=np.zeros_like(a);mapping=Image.new('RGB',im.size,(88,120,120));mp=np.array(mapping)
for id,(name,poly,pivot) in enumerate(pieces,1):
 m=labels==id;assert m.any(),name;y,x=np.where(m);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];rgba=np.zeros((112,144,4),np.uint8);rgba[m,:3]=rgb[m];rgba[m,3]=255;full=Image.fromarray(rgba);full.save(o/'aligned'/(name+'.png'));full.crop(box).save(o/'cropped'/(name+'.png'));Image.fromarray(m.astype('uint8')*255).save(o/'masks'/(name+'.png'));recon[m]=a[m];mp[m]=[int(c*255) for c in colorsys.hsv_to_rgb((id*.618034)%1,.65,.95)];records.append(dict(id=id,name=name,source_bounds=box,pivot_global=pivot,pivot_crop=[pivot[0]-box[0],pivot[1]-box[1]],pixel_count=int(m.sum()),source_index_histogram={str(k):int((a[m]==k).sum()) for k in np.unique(a[m])},source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),visible_pixels_only=True,aligned_file='aligned/'+name+'.png',cropped_file='cropped/'+name+'.png'))
assert np.array_equal(recon,a);assert sum(q['pixel_count'] for q in records)==int(fg.sum())
out=Image.fromarray(recon);out.putpalette(im.getpalette());out.save(o/'reassembled-base-1x.png',bits=4);out.resize((864,672),Image.Resampling.NEAREST).save(o/'reassembled-base-6x.png');Image.fromarray(labels).save(o/'ownership-index.png');Image.fromarray(mp).resize((864,672),Image.Resampling.NEAREST).save(o/'ownership-map-6x.png')
page=Image.new('RGB',(1200,((len(records)+3)//4)*240),(43,53,54));d=ImageDraw.Draw(page)
for i,q in enumerate(records):
 x=i%4*300;y=i//4*240;tile=Image.open(o/q['cropped_file']);w,h=tile.size;k=min(6,268//w,194//h);pic=tile.resize((w*k,h*k),Image.Resampling.NEAREST);page.paste(pic,(x+16,y+34),pic);d.text((x+8,y+8),q['name'],fill='white')
page.save(o/'parts-sheet.png');(o/'parts.json').write_text(json.dumps(dict(schema='mecha.component-kit.v1',canvas=[144,112],palette=im.getpalette(),background_rgb=[88,120,120],source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),anatomy='near=image-left/anatomical-right; far=image-right/anatomical-left',reconstruction_pixel_differences=int((recon!=a).sum()),overlap_pixels=0,covered_foreground_pixels=int(fg.sum()),note='Disjoint visible source pixels, no redrawn or resized artwork. Hidden surfaces are not fabricated. Parts need underpaint only when a new view exposes an occluded surface.',parts=records),indent=2));print('Split',len(records),'parts;',int(fg.sum()),'pixels covered once; reconstruction differences=0')
