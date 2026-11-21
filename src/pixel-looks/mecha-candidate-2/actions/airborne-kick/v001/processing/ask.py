import sys
sys.path.insert(0,'/workspace/agent-sprite-forge/skills/generate2dsprite/scripts')
import pixel_look
pixel_look.WIDE=(2048,1024)
sys.argv=['pixel_look.py','ask-view','--master','/workspace/work/mecha-action-v001/master.png','--view-words','airborne kicking toward the viewers left, body leaning diagonally, front leg thrust out left, other leg bent below the waist, arms braced, complete flowing rear strands extending right','--cell','8','--key','green','--output-dir','/workspace/work/mecha-kick-v001/ask']
pixel_look.main()
