# v010 — user-selected right-facing turning kick

User preferred the earlier right-facing kicking gesture (source exec-471c5011), so that exact generated source is now extracted as07 without regeneration. v008 andv009 remain intact. Native extraction and original palette mapping simplify some generated fine detail; review at1x. Red-eye colour locked.

![Kick](previews/07-selected-turning-kick-6x.png)

![Full animation](moveset-demonstration.gif)

[Slow animation](moveset-demonstration-slow.gif) · [Latest04 punch](previews/04-combo-left-hit-6x.png) · [All10 poses](all-ten-poses.png)

Latest04 is byte-identical tov005 long-punch/lower-face-occlusion artwork. All9 other native sprites are unchanged fromv009. Sequence: dash → revised kick → grounded uppercut → left/right punch loop ×4 → palm finish. No opponent/effects.144×112 indexed native PNG, original16-entry palette,15 used colours, opaque teal RGB(88,120,120),6x nearest PNG and indexed BMP.

Existing built-in image_gen source selected by user (no new generation this revision), repository pixel-looks ruler/lattice extraction, original-palette mapping and red-eye lock. No illustration resizing or source-code edits. Source, prompt and extraction records preserved; all previous versions retained. Game-import compatibility unverified.

Extraction warnings (verbatim):

- the new view's body is 99 rows tall, the master's 101: it is not the same height; generate again

Lineup verdict: differs. Standing body height101, tolerance1. Full per-file height flags are retained in processing/lineup/lineup.json; crouched/rotated poses require visual review rather than automatic approval.

Both full GIFs decoded and compared over all118 intended tick intervals. Normal5.9s, slow11.8s; integer whole-sprite movement with held key poses. Finish-to-start is an inspection replay reset.
