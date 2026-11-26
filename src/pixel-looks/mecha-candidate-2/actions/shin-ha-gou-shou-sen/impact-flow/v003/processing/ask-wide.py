import sys
sys.path.insert(0,'/workspace/agent-sprite-forge/skills/generate2dsprite/scripts')
import pixel_look
# Preserve the original 112px-wide master at >=8 source px per native cell.
# Only the reference canvas is wider; exported native sprites stay144x112.
pixel_look.WIDE=(2304,1024)
pixel_look.main()
