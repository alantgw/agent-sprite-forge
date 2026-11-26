# Component kit v001 — construction prototype

17 transparent, individually editable components cut from the approved Candidate 2 base. Reassembling their aligned layers reproduces all 7,846 foreground pixels with zero differences. Original source preserved.

Open `base-parts.ora` in an OpenRaster editor, or use `aligned/` PNG layers and `parts.json` pivot coordinates. `cropped/` provides smaller individual parts. `near` means image-left/anatomical right; `far` means image-right/anatomical left.

These are visible-pixel cutouts, not complete anatomical drawings. Previously hidden joints and rear surfaces still need dedicated drawings before large turns can be accepted. The 30-frame assembly experiment has visible connection problems and is not included as an approved action.

The repository pixel-looks `ask-pose`/`pose` workflow preserves unchanged master pixels and extracts changed areas. It does not automatically segment anatomy, supply a bone rig, or reconstruct hidden surfaces. Segmentation, pivots and layer assembly here are additional project work.

The original black/red forearm armour remains a distinct reusable part; hands must not replace that armour. Frame-to-frame scaling is forbidden. Future action work should use this kit plus carefully drawn angle variants, rather than independent full-character redraws.
