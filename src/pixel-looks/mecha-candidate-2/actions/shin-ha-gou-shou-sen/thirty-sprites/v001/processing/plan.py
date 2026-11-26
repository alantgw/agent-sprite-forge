from pathlib import Path
import json,shutil
r=Path('/workspace/work/mecha-thirty-v001');repo=Path('/workspace/agent-sprite-forge/src/pixel-looks/mecha-candidate-2');act=repo/'actions';current=act/'shin-ha-gou-shou-sen/v010/native';v2=act/'shin-ha-gou-shou-sen/v002/native'
# id,name, source file or newly generated pose description
plan=[
(1,'standing',repo/'v001/mecha-final-1x.png'),(2,'ready-guard',current/'01-ready-guard.png'),(3,'power-crouch',current/'02-power-crouch.png'),
(4,'dash-coil','Low coiled forward dash anticipation toward image-left. Hips low, torso leans forward25degrees, rear leg bent and loaded, lead foot touching ahead, both original beast gauntlets tucked near ribs. A short powerful takeoff pose, not running with long legs.'),
(5,'low-dash',v2/'03-low-dash.png'),
(6,'kick-chamber','Anatomical left knee raised high across lower chest ready for rising kick, left shin folded tightly with clawed foot below knee and pointed forward-left, right foot planted. Torso forward not leaning back. Both beast gauntlets guard cheeks. Face looks image-left. Same body width and thick short limbs as master.'),
(7,'forward-kick',act/'shin-ha-gou-shou-sen/v008/native/07-forward-far-side-kick.png'),(8,'turning-kick',current/'07-selected-turning-kick.png'),
(9,'back-landing','Kick follow-through into LANDING FACING AWAY from viewer, three-quarter BACK view turned toward image-right. Both clawed feet grounded, left foot just landing slightly forward, bent knees, lowered hips, back angular shoulder plates visible, gauntlets low beside ribs. Full pale lavender mane and red ribbons sweep sideways in a right-turning arc. No face/eyes visible from back; head size unchanged. Compact body.'),
(10,'unwind-front','After back-facing landing, pivot back toward image-left into three-quarter SIDE LEFT, hips still partly turned away, upper torso comes around first. Both knees flexed, left beast gauntlet guarding near cheek, right beast gauntlet near waist. Forward inclined upper body, complete mane/ribbons swinging around shoulders.'),
(11,'uppercut-coil','LOW UPPERCUT WINDUP facing image-left. Knees deeply bent, torso inclines forward, striking image-left beast gauntlet lowered beside hip with elbow back ready to drive upward. Other beast gauntlet stays beside upper chest. Feet planted wide, head looks toward upper-left, not head-down.'),
(12,'grounded-uppercut',current/'08-grounded-uppercut.png'),(13,'rising-uppercut',v2/'05-rising-uppercut.png'),(14,'pursuit-launch',v2/'06-pursuit-launch.png'),(15,'airborne-rush',v2/'07-airborne-rush.png'),(16,'air-turn-back',act/'spin-follow-up-kick/v001/spin-kick-2-1x.png'),(17,'air-turn-side',act/'spin-follow-up-kick/v001/spin-kick-3-1x.png'),(18,'followup-kick',act/'spin-follow-up-kick/v001/spin-kick-4-1x.png'),(19,'landing-brace',v2/'08-landing-brace.png'),(20,'left-windup',current/'03-combo-chamber-left.png'),
(21,'left-half-strike','Midway LEFT PUNCH toward image-left: anatomical left arm from image-right shoulder swings forward across chest; elbow still bent90degrees, long thick forearm parallel to ground with original beast gauntlet at lower-face level halfway extended. Right beast guard beside cheek partly occluded behind left forearm. Crouch planted same wide feet and head position as SECOND reference left-punch endpoint. No human fist.'),
(22,'left-full-strike',current/'04-combo-left-hit.png'),(23,'right-windup',current/'05-combo-chamber-right.png'),
(24,'right-half-strike','Midway RIGHT PUNCH toward image-left: anatomical right arm from image-left shoulder drives forward at lower-face level, elbow still bent90degrees with thick lavender forearm and original beast gauntlet halfway extended. Left beast guard pulls to shoulder partly hidden by torso. Crouched planted feet, same body/head size and location as SECOND right-punch endpoint. No human fist.'),
(25,'right-full-strike',current/'06-combo-right-hit.png'),
(26,'palm-settle','Transition from rapid punches into final palm: both forearms retract toward lower ribs, elbows drawn back, beast gauntlets partly open with original short claws. Torso straightens a little in same wide planted crouch, shoulders square three-quarter left, looking image-left. Hair settles back while rear ribbons remain to image-right.'),
(27,'palm-charge',current/'09-palm-charge.png'),
(28,'palm-half-release','Halfway final PALM THRUST toward image-left. Image-left beast gauntlet extends halfway out from chest, elbow partly bent, open armoured mechanical palm directed left and short original claws spread. Other gauntlet retracted shoulder beside chest. Torso leans forward, feet planted same wide stance. Keep original beast gauntlet not human hand. Same body proportions as SECOND final palm endpoint. No energy or effects.'),
(29,'palm-full-release',current/'10-palm-release.png'),
(30,'palm-recovery','Recovery after final palm: striking image-left arm pulled back halfway, elbow bends and beast gauntlet lowers beside chest with claws relaxed, other beast gauntlet guards near ribs. Torso rises slightly from wide braced stance, feet remain planted, head faces image-left. Hair and red ribbons relax backward. Quiet recovery, no effects.')]
rows=[]
for id,name,src in plan:
 row={'id':f'{id:02}','name':name,'new':isinstance(src,str)}
 if row['new']:
  row['pose']=src;shutil.copytree('/workspace/work/mecha-sequence-v010/ask-07',r/f'ask-{id:02}');req=r/f'ask-{id:02}/request.json';j=json.loads(req.read_text());j['viewWords']=src;req.write_text(json.dumps(j,indent=2))
 else:row['source']=str(src);assert src.exists(),src
 rows.append(row)
(r/'plan.json').write_text(json.dumps(rows,indent=2));print('30frames:10new,20existing.')
