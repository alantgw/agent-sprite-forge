import sys
sys.path.insert(0,'/workspace/agent-sprite-forge/skills/generate2dsprite/scripts')
import pixel_look
fit=pixel_look.pg.fit_lattice
def local(rgb,ruler,cell,at=(0,0),**kwargs):
 return fit(rgb,ruler,cell,at,spread=.15,reach=6)
pixel_look.pg.fit_lattice=local
pixel_look.main()
