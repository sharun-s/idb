import geopandas as gp
import matplotlib.pyplot as p
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d
from descartes import PolygonPatch
import numpy as np
import sys

#1. Big gap between axis and edge of screen?
#2. Setting xlim and ylim causes stretching

def Poly(ax, geom, forecolor, bordercolor, borderwidth=1, transparency=1., zheight=0):
	pp=PolygonPatch(geom, fc=forecolor, ec=bordercolor, lw=borderwidth,alpha=transparency, zorder=zheight )
	xy=pp.get_extents()
	ax.add_patch(pp)
	art3d.pathpatch_2d_to_3d(pp, z=zheight, zdir="z")
	return xy

BLUE = '#6699cc'

l1=gp.read_file('tn_boundary.json')
l2=gp.read_file('tn_dist.json')

alld=l2.geometry
districts=l2[l2.Name.isin(sys.argv[4:])].geometry
tn=l1.iloc[0].geometry
tnx=tn.centroid.x
tny=tn.centroid.y

fig = p.figure(facecolor="#001f3f",figsize=(10.24,7.68)) 
#fig.subplots_adjust(left=-0.4,right=1.4)
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax = fig.gca(projection='3d')
e=40 if int(sys.argv[2]) > 40 else int(sys.argv[2])  
azi=int(sys.argv[3]) or -90.
ax.set_axis_off()
ax.set_aspect(0.73*1.33)
ax.view_init(elev=e, azim=azi)

ax.set_facecolor('#001f3f')
#ax.get_proj=lambda:np.dot(Axes3D.get_proj(ax),np.diag([1.04,1.15,1,1])) 

window=Poly(ax,geom=tn,forecolor='#22aacc', bordercolor=BLUE, transparency=0.3, zheight=0)
#ax.plot([tnx],[tny],[1],'go')
print(window.xmin, window.xmax, window.xmax-window.xmin)
print(window.ymin, window.ymax, window.ymax-window.ymin)
print(10.24/7.68)
print((window.xmax-window.xmin)/(window.ymax-window.ymin))
ax.set_xlim3d(window.xmin-70000, window.xmax-150000) #8600000, 8800000)
ax.set_ylim3d(window.ymin, window.ymax-150000)#1360000, 1440000)
ax.set_zlim3d(0, 3)
#ax.margins(1.1,.1,0.,tight=True)
print(ax.get_proj())
print(ax.get_w_lims())
zh=0
for j in districts:
	#base
	if int(sys.argv[2]) > 40:
		zh=(int(sys.argv[2])-40)/90.0
	Poly(ax,geom=j,forecolor='yellow', bordercolor='#002f4f', borderwidth=1, zheight=1+zh)
	ax.plot([j.centroid.x, j.centroid.x],[j.centroid.y, j.centroid.y],[1,1+zh],'y',linewidth=4)
	#top
	#Poly(ax,geom=j,forecolor='yellow', bordercolor='yellow', borderwidth=0.5, zheight=2)

	# zinc=0
	# end=6
	# for i in range(0,2*end):
	# 	pbase=PolygonPatch(j, fc='yellow', ec=BLUE, alpha=0.2, lw=0, zorder=1 )
	# 	ax.add_patch(pbase)
	# 	art3d.pathpatch_2d_to_3d(pbase, z=i/(1.0*end), zdir="z")	

for j in alld:
	Poly(ax,geom=j,forecolor='yellow', bordercolor='#001f3f', transparency=0.2, borderwidth=1, zheight=1)
	#ax.plot([tnx, j.centroid.x],[tny, j.centroid.y],[1],'r')	

bbox = fig.bbox_inches.from_bounds(2, 1, 8, 7)
fig.savefig(sys.argv[1],format='png', bbox_inches=bbox, facecolor=fig.get_facecolor())


from matplotlib.colors import LightSource
# Get colormaps to use with lighting object.
from matplotlib import cm

# Use Lighting
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

#p.show()

