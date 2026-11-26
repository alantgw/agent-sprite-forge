import sys
sys.path.insert(0,'/workspace/agent-sprite-forge/skills/generate2dsprite/scripts')
import pixel_look
fit=pixel_look.pg.fit_lattice
wide=any('requests-wide' in q for q in sys.argv)
def local(rgb,ruler,cell,at=(0,0),**kwargs):
 # Wider palm canvases were returned with a larger positional shift of the ruler.
 # Search a larger window (still within upstream default36px/1px scale spread).
 # The original strict nine-point equality and60% acceptance gate are unchanged.
 return fit(rgb,ruler,cell,at,spread=.3 if wide else .15,reach=24 if wide else 6)
pixel_look.pg.fit_lattice=local
pixel_look.main()
