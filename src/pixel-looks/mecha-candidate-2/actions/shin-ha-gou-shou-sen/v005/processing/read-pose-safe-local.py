"""Runtime-only pose statistics fix; repository source and sprite pixels unchanged."""
import sys,inspect
sys.path.insert(0,'/workspace/agent-sprite-forge/skills/generate2dsprite/scripts')
import pixel_look
fit=pixel_look.pg.fit_lattice
def local(rgb,ruler,cell,at=(0,0),**kwargs):
 return fit(rgb,ruler,cell,at,spread=.025,reach=2)
pixel_look.pg.fit_lattice=local
source=inspect.getsource(pixel_look.cmd_pose)
needle='    part = sprite[where[1]:where[1] + mh, where[0]:where[0] + mw]\n'
replacement='''    # Compare contracted silhouettes on a transparent master-sized statistics canvas.
    # This is AFTER art extraction/outline and never changes sprite or fitting gate.
    part = np.zeros_like(master)
    sx0, sy0 = max(0, where[0]), max(0, where[1])
    sx1, sy1 = min(sprite.shape[1], where[0] + mw), min(sprite.shape[0], where[1] + mh)
    if sx1 > sx0 and sy1 > sy0:
        dx0, dy0 = sx0 - where[0], sy0 - where[1]
        part[dy0:dy0+sy1-sy0, dx0:dx0+sx1-sx0] = sprite[sy0:sy1, sx0:sx1]
'''
assert source.count(needle)==1
exec(source.replace(needle,replacement),pixel_look.__dict__)
pixel_look.main()
