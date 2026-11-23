from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,shutil,hashlib,zipfile
r=Path('/workspace/work/mecha-video-ten-v001');o=r/'deliverables';o.mkdir();repo=Path('/workspace/agent-sprite-forge');basepath=repo/'src/pixel-looks/mecha-candidate-2/v001/mecha-final-1x.png';base=Image.open(basepath);pal=base.getpalette();p=np.array(pal,dtype=np.int32).reshape(-1,3);allowed=np.array([1,2]+list(range(4,16)));plan=json.loads((r/'generation-records.json').read_text());frames=[];spec=[];warnings=[];proc=o/'processing';proc.mkdir();preview=o/'previews';preview.mkdir();comparisons=o/'comparisons';comparisons.mkdir();native=o/'native';native.mkdir();bmps=o/'bmp';bmps.mkdir();dur=[360,450,150,140,200,150,150,240,450,650];lift=[0,0,0,0,0,10,9,0,0,0]
for i,q in enumerate(plan):
 id=q['id'];n=f"{id}-{q['name']}";folder=r/f'extracted-{id}';rec=json.loads((folder/f'pose-{id}.json').read_text());a=np.array(Image.open(folder/f'pose-{id}.png').convert('RGBA'));idx=allowed[(((a[:,:,:3].astype(np.int32)[:,:,None,:]-p[None,None,allowed,:])**2).sum(-1)).argmin(-1)].astype('uint8');idx[a[:,:,3]==0]=0;h,w=idx.shape;assert w<=140 and h<=109;at=((144-w)//2,109-lift[i]-h);assert at[1]>=0
 canvas=np.zeros((112,144),dtype='uint8');canvas[at[1]:at[1]+h,at[0]:at[0]+w]=idx;im=Image.fromarray(canvas);im.putpalette(pal);im.save(native/f'{n}.png',bits=4);im.save(bmps/f'{n}.bmp');big=im.resize((864,672),Image.Resampling.NEAREST);big.save(preview/f'{n}-6x.png',bits=4);frames.append(im)
 re=Image.open(native/f'{n}.png');assert re.mode=='P' and re.size==(144,112) and re.getpalette()==pal and 'transparency' not in re.info;assert Image.open(preview/f'{n}-6x.png').convert('RGB').tobytes()==re.convert('RGB').resize((864,672),Image.Resampling.NEAREST).tobytes();assert len(set(canvas.ravel()))<=16
 yy,xx=np.where(canvas!=0);row={'id':id,'pose':q['name'],'file':f'native/{n}.png','canvas':[144,112],'occupied_bounds_exclusive':[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)],'used_colours':len(set(canvas.ravel().tolist())),'stored_palette_entries':16,'placement_xy':list(at),'airborne_lift_px':lift[i],'preview_hold_ms':dur[i],'reference_part':q['part'],'reference_time_s':q['time'],'strict_ruler_equal_share':rec['rulerEqualShare'],'body_height_rows':rec['heightRows'],'master_body_height_rows':rec['masterHeightRows'],'warnings':rec.get('warnings',[])};spec.append(row)
 for warning in rec.get('warnings',[]):warnings.append({'file':f'native/{n}.png','warning':warning})
 sub=proc/id;sub.mkdir();shutil.copytree(r/f'ask-{id}',sub/'ask-view');shutil.copytree(folder,sub/'extracted');shutil.copy2(q['source'],sub/'generated-source.png');(sub/'host-prompt.txt').write_text(q['host_prompt']);
 # Generation beside extracted native on same page (not a runtime sprite sheet).
 src=Image.open(q['source']).convert('RGB');src.thumbnail((900,450));review=Image.new('RGB',(900,820),(88,120,120));d=ImageDraw.Draw(review);review.paste(src,((900-src.width)//2,0));d.text((12,460),n+' / generated source above, base and native at 3x below',fill='white');review.paste(base.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(10,480));review.paste(im.convert('RGB').resize((432,336),Image.Resampling.NEAREST),(458,480));review.save(comparisons/f'{n}-source-base-native.png')
# Contact preview, not a runtime sprite sheet.
page=Image.new('RGB',(1440,508),(88,120,120));d=ImageDraw.Draw(page)
for i,(q,im) in enumerate(zip(plan,frames)):
 x=(i%5)*288;y=(i//5)*254;d.text((x+7,y+7),q['id']+' '+q['name'],fill='white');page.paste(im.convert('RGB').resize((288,224),Image.Resampling.NEAREST),(x,y+28))
page.save(o/'all-ten-poses.png')
for name,times in [('sequence-preview.gif',dur),('sequence-slow.gif',[550]*10)]:
 big=[im.resize((720,560),Image.Resampling.NEAREST) for im in frames];big[0].save(o/name,save_all=True,append_images=big[1:],duration=times,loop=0,optimize=False,disposal=2);g=Image.open(o/name);assert g.n_frames==10
 for k,im in enumerate(big):g.seek(k);assert g.convert('RGB').tobytes()==im.convert('RGB').tobytes()
# Preserve known authoritative files unchanged, omit private video and screenshots.
refs=o/'references';refs.mkdir();shutil.copy2(basepath,refs/'approved-base-1x.png');style=repo/'src/pixel-looks/mecha-candidate-2/v001/references/reference-a.png'
if style.exists():shutil.copy2(style,refs/'reference-A-style.png')
meta={'version':'v001','status':'draft for visual review','asset':'ten condensed key poses for Shin Ha Gou Shou Sen sequence','art_source':'host_image','route':'built-in image_gen, no paid API invoked','method':'ten individual ask-view/custom pose generations beside approved base ruler, strict lattice extraction, exact original-palette mapping, integer placement only; no native resize','body_palette_exactly_matches_approved_base':True,'opaque_teal_rgb':pal[:3],'frames':spec,'warnings':warnings,'source_video_handling':'six user-provided Drive segments inspected locally in provided order; original videos and screenshots private, not in repository','source_display_rotation':'video metadata90deg rotation honoured before pose inspection','timing':'condensed illustration, not original44second playback','motion_limits':'ten distinct key poses, no interpolated in-betweens, no enemy or effects, fast obscured pursuit reconstructed from visible entry/exit','game_import_compatibility':'not verified'};(o/'specification.json').write_text(json.dumps(meta,indent=2))
rows='\n'.join(f"| {q['id']} {q['name']} | [PNG](native/{q['id']}-{q['name']}.png) | [6x](previews/{q['id']}-{q['name']}-6x.png) | {s['occupied_bounds_exclusive']} | {s['used_colours']} |" for q,s in zip(plan,spec))
warntext='\n'.join('- `'+x['file']+'`: '+x['warning'] for x in warnings)
(o/'README.md').write_text('''# Ten mecha key poses — video sequence v001

Draft for visual review: ten individual native sprites derived from approved Candidate2 v001, representing the supplied six-part sequence: ready guard → power crouch → low rush → close strike → rising strike → pursuit launch → airborne rush → landing brace → palm windup → final palm thrust. The six recordings total about43.7s; camera closeups, long flashes, opponent reactions and finishing explosion are omitted. Fast pursuit is frequently obscured by streaks; poses06–07 are readable reconstructions of that passage, not exact tracing of every hidden joint.

![Ten poses](all-ten-poses.png)

[Sequence preview](sequence-preview.gif) · [Slow inspection](sequence-slow.gif)

| Pose | Native144x112 | Nearest preview | Occupied bounds x0,y0,x1,y1 | Used colours |
| --- | --- | --- | --- | --- |
'''+rows+'''

All files use the exact approved16-entry indexed palette;15 colours used, opaque teal RGB(88,120,120). Unused green entry excluded from foreground mapping. Native sprites are generated-grid cells read at1x, never a resized illustration. All previews nearest-neighbour. Individual indexed BMPs in bmp/. No opponent, energy, scenery, aura, text or screen UI in the sprites. Existing approved assets unchanged; no editor/game files modified. No game-import compatibility claim.

The preview is ten key drawings with holds, not smooth60fps animation or a literal44s recreation. Both preview GIFs loop for inspection; the attack itself is a one-shot sequence. Grounded poses share floor109; two flight poses are raised9–10px. Horizontal positioning centres each silhouette on canvas, rather than claiming a verified runtime root/collider. Native placement and timing are documented in specification.json.

## Method and provenance

Built-in image_gen, approved base as unchanged left ruler, one reposed figure per separate image on right. Repository generate2dsprite pixel-looks ask-view/view custom-pose workflow.2048x1024 request layout; returned1774x887 sources. Each source's strict ruler fit determines grid, and new figure is read on its own lattice. Narrowed fitter retains the original gate; no failed ruler was patched or bypassed. Intermediate extra shades then nearest mapping to the original palette, excluding the original green foreground entry; cells are not resized. Original anatomy, gauntlets, contours and simplified mechanical details still need visual review: a numerical gate is not artistic approval.

Every source, host prompt, request, extracted1x and source-versus-native review is retained in processing/ and comparisons/. Source videos/screenshots remain private outside the repository. References contains unchanged approved native base and original style reference.

## Height warnings — retained verbatim

The extractor compares the occupied central-column body height with a standing ruler. Crouches, leaning strikes and tucked flight poses change that measurement. These drafts retain the warnings instead of claiming all checks passed. Each must be judged at equal scale against the approved body; this set is not automatically approved.

'''+warntext+'\n')
(o/'qa-report.txt').write_text('Native PNG readback:144x112/P/exact original16-entry palette/no transparency.15 used foreground/background entries. All6x PNGs are exact nearest-neighbour images. GIF decoded frames equal intended enlarged native frames;10 frames each. Strict ruler gate passed for all ten sources; per-source match values and every height warning retained in specification.json. No anatomical correctness claim from numeric checks. Source image compare pages retained. Two flight sprites use explicit upward placement; no per-frame scaling.\n'+warntext+'\n')
shutil.copy2(r/'read.py',proc/'read.py');shutil.copy2(r/'package.py',proc/'package.py');(proc/'pose-plan.json').write_text(json.dumps([{k:v for k,v in q.items() if k not in ['host_prompt','source']} for q in plan],indent=2))
(o/'sha256.json').write_text(json.dumps({str(f.relative_to(o)):hashlib.sha256(f.read_bytes()).hexdigest() for f in o.rglob('*') if f.is_file() and f.name!='sha256.json'},indent=2));print(json.dumps({'frames':[{k:s[k] for k in ['id','occupied_bounds_exclusive','used_colours']} for s in spec],'height_warnings':len(warnings)},indent=2))
