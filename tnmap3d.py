import geopandas as gp
import matplotlib.pyplot as p
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d
from descartes import PolygonPatch
import numpy as np
import sys

from matplotlib.colors import LightSource
# Get colormaps to use with lighting object.
from matplotlib import cm

BLUE = '#6699cc'

l1=gp.read_file('tn_boundary.json')
l2=gp.read_file('tn_dist.json')

#fig = p.figure(facecolor='white')
fig = p.figure(facecolor="#001f3f") 
ax = fig.gca(projection='3d')
districts=l2[l2.Name.isin(['Coimbatore','Erode','Kanyakumari'])].geometry
alld=l2.geometry
tn=l1.iloc[0].geometry

pp=PolygonPatch(tn, fc='#22aacc', ec=BLUE, alpha=0.3, zorder=0 )
xy=pp.get_window_extent()
ax.add_patch(pp)
art3d.pathpatch_2d_to_3d(pp, z=0, zdir="z")

for j in districts:
	pbase=PolygonPatch(j, fc='yellow', ec='#002f4f', lw=1, zorder=2 )
	ax.add_patch(pbase)
	art3d.pathpatch_2d_to_3d(pbase, z=0, zdir="z")	

	pp=PolygonPatch(j, fc='#001f3f', ec="yellow", alpha=1., lw=.5, zorder=2 )
	ax.add_patch(pp)
	art3d.pathpatch_2d_to_3d(pp, z=2, zdir="z")

	zinc=0
	end=6
	for i in range(0,2*end):
		pbase=PolygonPatch(j, fc='yellow', ec=BLUE, alpha=0.2, lw=0, zorder=1 )
		ax.add_patch(pbase)
		art3d.pathpatch_2d_to_3d(pbase, z=i/(1.0*end), zdir="z")	

for j in alld:
	pp=PolygonPatch(j, fc='yellow', ec="#001f3f", alpha=0.1, lw=1, zorder=2 )
	ax.add_patch(pp)
	art3d.pathpatch_2d_to_3d(pp, z=2, zdir="z")



# pp=PolygonPatch(tn, fc='#001f3f', ec='#ffff00', alpha=0.2, zorder=0 )
# ax.add_patch(pp)
# art3d.pathpatch_2d_to_3d(pp, z=2, zdir="z")

#ax.set_top_view()
ax.set_xlim3d(xy.xmin, xy.xmax) #8600000, 8800000)
ax.set_ylim3d(xy.ymin, xy.ymax)#1360000, 1440000)
ax.set_zlim3d(0, 4)

#ax=l1.plot(facecolor='#0099dd',edgecolor='blue',label='TN',alpha=.78)
e=int(sys.argv[2])
azi=int(sys.argv[3]) or -90.
ax.set_axis_off()
ax.view_init(elev=e, azim=azi)
ax.set_facecolor('#001f3f')
#l2[l2.Name=='Tiruppur'].plot(ax=ax,facecolor='orange',edgecolor='blue',label='TN',alpha=.73, linewidth=1) 
#p.ison()

# y = np.linspace(xy.ymin, xy.ymax)
# x = np.linspace(xy.xmin, xy.xmax)
# yy, xx = np.meshgrid(y, x)
# def f(x,t):
#     return t/t*2
# zz = f(yy,xx)

# # Create an instance of a LightSource and use it to illuminate the surface.
# light = LightSource(315, 45)
# white = np.zeros((zz.shape[0], zz.shape[1], 3))
# illuminated_surface = light.shade_rgb(white*(0.2,0.6,1.), zz)

# ax.plot_surface(xx, yy, zz,
#                 cstride=100, rstride=100,
#                 alpha=1., color='#ffff00', #facecolors=illuminated_surface,
#                 linewidth=0,
#                 zorder=10)

p.show()
#fig.savefig(sys.argv[1],format='png',facecolor=fig.get_facecolor())

