from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,shutil,zipfile
r=Path('/workspace/work/mecha-combo-v003');o=r/'deliverables';o.mkdir();repo=Path('/workspace/agent-sprite-forge');old=repo/'src/pixel-looks/mecha-candidate-2/actions/shin-ha-gou-shou-sen/v002';pal=Image.open(repo/'src/pixel-looks/mecha-candidate-2/v001/mecha-final-1x.png').getpalette();plan=[('01','ready-guard'),('02','power-crouch'),('03','combo-chamber-left'),('04','combo-left-hit'),('05','combo-chamber-right'),('06','combo-right-hit'),('07','rising-launch'),('08','diving-followthrough'),('09','palm-charge'),('10','palm-release')];frames=[];spec=[]
for n in ['native','previews','bmp','comparisons','processing']:(o/n).mkdir()
recordmap={q['id']:q for q in json.loads((r/'generation-records.json').read_text())};oldspec=json.loads((old/'specification.json').read_text());armrec=json.loads((r/'arm-read-records.json').read_text());eyes={'03':(51,59,54,62),'07':(60,36,64,38),'08':(45,66,48,69)}
for i,(id,name) in enumerate(plan):
 unchanged=id in ['01','02','09','10'];n=id+'-'+name;row={'id':id,'name':name,'file':f'native/{n}.png','unchanged_from_v002':unchanged}
 if unchanged:
  for f,dest in [(old/f'native/{n}.png',o/f'native/{n}.png'),(old/f'previews/{n}-6x.png',o/f'previews/{n}-6x.png'),(old/f'bmp/{n}.bmp',o/f'bmp/{n}.bmp')]:shutil.copy2(f,dest)
  im=Image.open(o/f'native/{n}.png');assert (o/f'native/{n}.png').read_bytes()==(old/f'native/{n}.png').read_bytes()
 else:
  f=r/f"provisional/{id}{'-arms' if id in ['04','05','06'] else ''}.png";a=np.array(Image.open(f));box=eyes['03' if id in ['03','04','05','06'] else id];x0,y0,x1,y1=box;eye=a[y0:y1,x0:x1].copy()
  for src,dst in [(8,6),(13,11),(9,10),(12,10),(14,10),(15,10)]:eye[eye==src]=dst
  a[y0:y1,x0:x1]=eye;assert 11 in set(eye.ravel()) and not(set(eye.ravel())&{8,9,12,13,14,15});im=Image.fromarray(a);im.putpalette(pal);im.save(o/f'native/{n}.png',bits=4);im.save(o/f'bmp/{n}.bmp');im.resize((864,672),Image.Resampling.NEAREST).save(o/f'previews/{n}-6x.png',bits=4);row['eye_box_exclusive']=box
  folder=r/('extracted-'+id+('-safe' if id in ['04','05','06'] else '-compact' if id=='07' else ''));rec=json.loads((folder/f'pose-{id}.json').read_text());row['extraction_record']=rec;row['warnings']=rec.get('warnings',[]);p=o/'processing'/id;p.mkdir();shutil.copytree(r/f'ask-{id}',p/'ask');shutil.copytree(folder,p/'extracted');shutil.copy2(recordmap[id]['source'],p/'generated-source.png');(p/'host-prompt.txt').write_text(recordmap[id]['host_prompt']);
  if id=='07':(p/'compact-edit-prompt.txt').write_text(recordmap[id]['compact_prompt'])
  before=Image.open(sorted((old/'native').glob(id+'-*.png'))[0]);page=Image.new('RGB',(864,380),tuple(pal[:3]));d=ImageDraw.Draw(page);d.text((10,10),id+' before',fill='white');d.text((442,10),id+' redesigned',fill='white');page.paste(before.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(0,36));page.paste(im.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(432,36));page.save(o/f'comparisons/{n}.png')
 a=np.array(im);y,x=np.where(a!=0);row.update({'canvas':[144,112],'palette_entries':16,'used_colours':len(set(a.ravel().tolist())),'occupied_bounds_exclusive':[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]});assert im.size==(144,112) and im.mode=='P' and im.getpalette()==pal and 'transparency' not in im.info;frames.append(im.copy());spec.append(row)
# Common body is exact for the four-frame combo outside the explicitly documented arm mask.
common=np.array(frames[2]);mask=np.zeros((112,144),bool);mask[slice(*armrec['arm_rows'])]=True;head=Image.new('1',(144,112));ImageDraw.Draw(head).polygon(armrec['protected_head_polygon'],fill=1);mask&=~np.array(head)
for im in frames[3:6]:assert np.array_equal(np.array(im)[~mask],common[~mask])
for name,ms in [('combo-loop.gif',100),('combo-loop-slow.gif',220)]:
 big=[im.resize((720,560),Image.Resampling.NEAREST) for im in frames[2:6]];big[0].save(o/name,save_all=True,append_images=big[1:],duration=ms,loop=0,optimize=False,disposal=2);g=Image.open(o/name);assert g.n_frames==4
 for k,im in enumerate(big):g.seek(k);assert g.convert('RGB').tobytes()==im.convert('RGB').tobytes()
page=Image.new('RGB',(1440,508),tuple(pal[:3]));d=ImageDraw.Draw(page)
for i,((id,n),im) in enumerate(zip(plan,frames)):
 x=(i%5)*288;y=(i//5)*254;d.text((x+7,y+7),id+' '+n,fill='white');page.paste(im.convert('RGB').resize((288,224),Image.Resampling.NEAREST),(x,y+28))
page.save(o/'all-ten-poses.png');meta={'version':'v003','status':'redesigned middle for visual review','unique_sprite_count':10,'newly_redesigned_ids':['03','04','05','06','07','08'],'byte_unchanged_ids':['01','02','09','10'],'combo_sequence':['03','04','05','06'],'combo_ms_per_frame':100,'combo_slow_ms_per_frame':220,'combo_repeats_in_full_demo':4,'palette_exactly_matches_original':True,'background_rgb':pal[:3],'frames':spec,'common_body_mask':armrec,'method':'host image_gen;03/07/08 ask-view/view beside original ruler;04-06 ask-pose/pose against03; full changed-arm lattice read to remove stale withdrawn-arm pixels, head/legs protected. Same strict fits retained.','processing_limitations':'default pose statistics crashes on contracting silhouette; runtime-only comparison-array fix. Default connected-change retention left old rear-arm cells; complete arm-region sampling uses same verified lattice, repository key cleaner and contour rule. No editor or repository source change.','eye_policy':'original red core184,21,14, shadow46,11,19; no orange/white eyes','game_import_compatibility':'not verified'};(o/'specification.json').write_text(json.dumps(meta,indent=2));(o/'README.md').write_text('''# v003 — four-frame combo loop and redesigned pursuit

Exactly10 unique native sprites.03–06 form a repeatable **windup → left hit → counter-windup → right hit** loop, rather than spending each drawing once.07 rises with a compact uppercut,08 dives diagonally down-left.01/02 and the approved09/10 palm ending are copied byte-for-byte from v002.

![Combo loop](combo-loop.gif)

[Slow combo](combo-loop-slow.gif) · [Complete moveset demonstration](moveset-demonstration.gif) · [Ten poses](all-ten-poses.png)

144×112 indexed PNGs, original16-entry palette,15 colours used, opaque teal RGB(88,120,120). Nearest-neighbour previews in previews/, indexed BMPs in bmp/. No opponent or effects. Red eyes explicitly palette-locked. Head and legs remain identical across03–06 outside the documented arm/head mask. Full-demo loop count is adjustable (default4 cycles); repeating the four drawings does not introduce extra unique sprites.

Built-in image_gen, repository pixel-looks workflows; same native grid, no illustration resize. One uppercut source was too tall112rows; regenerated into98rows without rescaling body or changing native canvas. Strict master-fit records and all height warnings retained in specification.json. Height warnings reflect low stance and aerial poses and still require visual review, not automatic approval. Default pose reader had a contracted-bounds statistics error; external runtime wrapper fixes only its comparison array after art extraction. Its partial-change merge also retained withdrawn-arm remnants; the final changed-arm region is read on the SAME passed lattice with the repository sampler/key-cleaner/outline rules, then original03 head/legs are restored outside a documented mask. Strict fit threshold is unchanged; no failed gate bypass or different art pipeline. Repository/editor source untouched. Processing sources, prompts and wrappers retained.

The full GIF is a condensed staging demonstration, not literal60fps source-video reconstruction. Two aerial drawings cannot show every hidden attack between camera cuts. No game-import compatibility claim; previous revisions preserved.
''');
for f in ['read.py','ask.py','read-pose-safe.py','read-combo-arms.py','package.py']:shutil.copy2(r/f,o/'processing'/f)
(o/'processing/arm-read-records.json').write_text(json.dumps(armrec,indent=2));(r/'package-files.json').write_text(json.dumps([{'id':id,'name':n} for id,n in plan],indent=2));print('Ten frames ready; four-frame combo body/palette/eyes/GIF checks passed. Full demonstration pending.')
