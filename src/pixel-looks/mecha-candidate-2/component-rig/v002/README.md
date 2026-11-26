# Component action review v002

30 unique native sprite poses assembled from reusable parts. Review version, not artistically approved or game-import verified.

Sequence: two dash poses → forward heavy punch → uppercut → grounded roundhouse → uppercut → alternating left/right punches (three cycles) → palm strike. No enemy, effects, jump or 360-degree spin. The roundhouse uses a left-rear view and sweeps toward image-right at roughly waist height.

## Files

- `native/`: 30 individual 144×112 indexed PNGs, opaque teal RGB (88,120,120).
- `previews/`: exact 6× nearest-neighbour PNGs.
- `action-4x.gif`, `action-slow-4x.gif`, `action-1x.gif`: 42 playback samples using the 30 poses; the six combo poses repeat three times.
- `layers-ora/`: 30 independently editable OpenRaster files; each layer composite exactly matches its native PNG.
- `base-component-kit/`: immutable 17-part original-pixel kit.
- `new-parts/`: reusable kick-angle components with transparent PNGs and original-palette indexed versions.
- `poses.json`, `playback.json`: transforms, bounds, colour counts and timings.

## Method and checks

Art sources: existing approved base and selected v010 kick/palm, plus one host_image generation restricted to a new lower-body angle. No paid image API used. The generated upper body, head, eyes, arms and mane were discarded. Pixel-looks `ask-pose`/`pose` measured the generation at native scale; the retained lower-body region was mapped to the original palette and split into kicking-leg and pelvis/support components. An unrelated 29-pixel arm remnant was removed from the kick-part mask. The new lower-body angle alone was mirrored to match the previously selected left-rear upper-body view; the frontal character base was not mirrored.

Front-view frames reuse original head, eyes, mane, wings, torso, waist and leg sources at scale 1. Both original forearm armour shells retain their complete source index histograms in all 24 frontal frames (48 checks). Side-view kick frames reuse selected v010 upper-body parts, remove the old raised leg and human-like guard, then attach an original-base beast-arm guard and the new leg parts. Small exposed elbow and wrist connections are drawn under the armour with original palette entries. Processing scripts are archival records of this workspace, not changes to editor/tool source.

16 palette entries in every PNG: frontal frames use all 16; the six side-view frames use 15. The background is opaque teal. Frame 29 and 30 have exactly identical head, mane, torso, wings, waist and leg layers; the final palm body does not enlarge. All 30 native images are different. The GIFs were decoded and compared pixel-for-pixel against their intended frames. All 30 ORA composites were checked against native PNGs. Pixel-look lineup verdict: `same`, master body height 101, frames 100–101. See `qa.json` and `processing/lineup-final/`.

## Visual review limits

Numerical checks do not establish animation quality. The frontal-to-side-view change at the roundhouse is a deliberate view change, with a return to the frontal stance at frame 16; it is not a fully interpolated body turn. Original exposed-surface cutouts limit how far elbows and shoulders can move. Review fist silhouette, the roundhouse transition, and palm readability before calling this an approved action. No ROM/disc/editor source modified. All earlier versions preserved.
