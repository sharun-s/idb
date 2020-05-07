import geopandas as gp
import matplotlib.pyplot as p
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d
from descartes import PolygonPatch
import numpy as np

BLUE = '#6699cc'

l1=gp.read_file('tn_boundary.json')

l2=gp.read_file('tn_dist.json')

fig = p.figure() 
ax = fig.gca(projection='3d')
krishnagiri=l2.iloc[23].geometry
tn=l1.iloc[0].geometry

pp=PolygonPatch(krishnagiri, fc='yellow', ec='orange', alpha=0.7, lw=0, zorder=2 )
ax.add_patch(pp)
art3d.pathpatch_2d_to_3d(pp, z=2, zdir="z")

pbase=PolygonPatch(krishnagiri, fc='yellow', ec='#002f4f', lw=1.5, zorder=2 )
ax.add_patch(pbase)
art3d.pathpatch_2d_to_3d(pbase, z=0, zdir="z")	

zinc=0
end=4
for i in range(0,2*end):
	pbase=PolygonPatch(krishnagiri, fc='yellow', ec=BLUE, alpha=0.2, lw=0, zorder=1 )
	ax.add_patch(pbase)
	art3d.pathpatch_2d_to_3d(pbase, z=i/(1.0*end), zdir="z")	

pp=PolygonPatch(tn, fc='#22aacc', ec=BLUE, alpha=0.5, zorder=0 )
pp.get_window_extent()
xy=pp.get_window_extent()
ax.add_patch(pp)
art3d.pathpatch_2d_to_3d(pp, z=0, zdir="z")

#ax.set_top_view()
ax.set_xlim3d(xy.xmin, xy.xmax) #8600000, 8800000)
ax.set_ylim3d(xy.ymin, xy.ymax)#1360000, 1440000)
ax.set_zlim3d(0, 4)

#ax=l1.plot(facecolor='#0099dd',edgecolor='blue',label='TN',alpha=.78)
ax.set_axis_off()
ax.view_init(elev=60., azim=-90.)
ax.set_facecolor('#002f4f')
#l2[l2.Name=='Tiruppur'].plot(ax=ax,facecolor='orange',edgecolor='blue',label='TN',alpha=.73, linewidth=1) 
#p.ison()
p.show()
