import geopandas as gp
import matplotlib.pyplot as p
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d
from descartes import PolygonPatch
import numpy as np
import sys
from matplotlib.transforms import Affine2D
from matplotlib.patches import PathPatch
from matplotlib.text import TextPath
import matplotlib as matp

matp.use('TkAgg')
p.ion()
#TODO
#1. Big gap between axis and edge of screen?
#2. Setting xlim and ylim causes stretching
#args
# output filename, elevation, azimuth, list of districts
def Path3D(ax, geom, forecolor, bordercolor, borderwidth=1, transparency=1., zheight=0):
	# descartes.PolygonPatch converts a shapely or geojson like obj (geom in this case) to a matplotlib pathpatch
	pp=PolygonPatch(geom, fc=forecolor, ec=bordercolor, lw=borderwidth,alpha=transparency, zorder=zheight )
	xy=pp.get_extents()
	ax.add_patch(pp)
	art3d.pathpatch_2d_to_3d(pp, z=zheight, zdir="z")
	return xy

def Path3D_transform(ax, geom, forecolor, bordercolor, angle,borderwidth=1, transparency=1., 
	z=0,zdir='z'):
	# descartes.PolygonPatch converts a shapely or geojson like obj (geom in this case) to a matplotlib pathpatch
	pp=PolygonPatch(geom, fc=forecolor, ec=bordercolor, 
		lw=borderwidth,alpha=transparency, zorder=z )
	ptmp=pp.get_path()
	x=geom.centroid.x
	y=geom.centroid.y
	if zdir == "y":
		xy1, z1 = (x, z), y
	elif zdir == "x":
		xy1, z1 = (y, z), x
	else:
		xy1, z1 = (x, y), z
	trans = Affine2D().rotate_deg(0).translate(0,0)#xy1[0], xy1[1])
	print(xy1[0], xy1[1])#len(ptmp.cleaned(simplify=True)))
	tmp=PathPatch(trans.transform_path(ptmp))
	ax.add_patch(tmp)
	print(z1)
	art3d.pathpatch_2d_to_3d(tmp, z=z1, zdir='z')#zdir)
	#print(tmp.get_extents())

def text3d(ax, xyz, s, zdir="z", size=None, angle=0, usetex=False, **kwargs):
    '''
    Plots the string 's' on the axes 'ax', with position 'xyz', size 'size',
    and rotation angle 'angle'.  'zdir' gives the axis which is to be treated
    as the third dimension.  usetex is a boolean indicating whether the string
    should be interpreted as latex or not.  Any additional keyword arguments
    are passed on to transform_path.

    Note: zdir affects the interpretation of xyz.
    '''
    x, y, z = xyz
    if zdir == "y":
        xy1, z1 = (x, z), y
        #xy1, z1 = (x, window.ymax-140000), 2
    elif zdir == "x":
        xy1, z1 = (y, z), x
    else:
        xy1, z1 = (x, y), z

    text_path = TextPath((window.xmin-70000, window.ymin), s, size=size, usetex=usetex)
    #trans = Affine2D().rotate_deg(angle).translate(xy1[0], xy1[1])
    trans = Affine2D().rotate(angle).translate(xy1[0], xy1[1])
    p1 = PathPatch(trans.transform_path(text_path), **kwargs)
    ax.add_patch(p1)
    art3d.pathpatch_2d_to_3d(p1, z=z1, zdir=zdir)

BLUE = '#6699cc'

l1=gp.read_file('tn_boundary.json')
l2=gp.read_file('tn_dist.json')

alld=l2.geometry
districts=l2[l2.Name.isin(sys.argv[4:])].geometry
tn=l1.iloc[0].geometry
tnx=tn.centroid.x
tny=tn.centroid.y

fig = p.figure(facecolor="#001f3f",figsize=(10.24,7.68)) 
fig.subplots_adjust(left=0,right=1,bottom=0, top=1)
#fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax = fig.gca(projection='3d')
e=40 if int(sys.argv[2]) > 40 else int(sys.argv[2])  
azi=int(sys.argv[3]) or -90.
#ax.set_axis_off()
#ax.set_aspect(0.73*1.33)
#ax.view_init(elev=e, azim=azi)
ax.set_facecolor('#001f3f')
#ax.get_proj=lambda:np.dot(Axes3D.get_proj(ax),np.diag([1.04,1.15,1,1])) 

window=Path3D(ax,geom=tn,forecolor='#001f3f',#'#22aacc', 
	bordercolor='#001f3f',#,BLUE, 
	transparency=0, zheight=0)
#ax.plot([tnx],[tny],[1],'go')
#print(window.xmin, window.xmax, window.xmax-window.xmin)
#print(window.ymin, window.ymax, window.ymax-window.ymin)
#print(10.24/7.68)
#print((window.xmax-window.xmin)/(window.ymax-window.ymin))
ax.set_xlim3d(window.xmin-120000, window.xmax) #8600000, 8800000)
ax.set_ylim3d(window.ymin, window.ymax)#1360000, 1440000)
ax.set_zlim3d(0, 3)
#ax.margins(1.1,.1,0.,tight=True)
#print(ax.get_proj())
#print(ax.get_w_lims())
zh=0
for j in districts:
	#base
	if int(sys.argv[2]) > 40:
		zh=(int(sys.argv[2])-40)/90.0
	Path3D(ax,geom=j,forecolor='yellow', bordercolor='#002f4f', borderwidth=1, zheight=1+zh)
	ax.plot([j.centroid.x, j.centroid.x],[j.centroid.y, j.centroid.y],[1,1+zh],'y',linewidth=4)
	#top
	#Poly(ax,geom=j,forecolor='yellow', bordercolor='yellow', bordegrwidth=0.5, zheight=2)

	# zinc=0
	# end=6
	# for i in range(0,2*end):
	# 	pbase=PolygonPatch(j, fc='yellow', ec=BLUE, alpha=0.2, lw=0, zorder=1 )
	# 	ax.add_patch(pbase)
	# 	art3d.pathpatch_2d_to_3d(pbase, z=i/(1.0*end), zdir="z")	

#print(j.centroid.x,j.centroid.y)
#trans = Affine2D().rotate_deg(1).translate(100000,-200000)#j.centroid.x,(window.ymax-window.ymin)/2)#j.centroid.y)
Path3D_transform(ax,j, forecolor="#ffcc33", bordercolor="black",angle=np.pi/2,zdir='z')#, lw=1,alpha=0.6, zorder=1)
#p1 = PathPatch(trans.transform_path(polypath.get_path()))
#ax.add_patch(p1)
#art3d.pathpatch_2d_to_3d(p1, z=z1, zdir=zdir)

for j in alld:
	Path3D(ax,geom=j,forecolor='#E6DB74', bordercolor='#E6DB74', transparency=.8, borderwidth=1, zheight=0)
	#ax.plot([tnx, j.centroid.x],[tny, j.centroid.y],[1],'r')	

# text3d(ax, (-1000, 0, 0), "X-axis", 
# 	zdir="z", size=50000, usetex=False, angle=0,
#        ec="yellow", fc="orange")
# text3d(ax, (window.xmax-window.xmin, window.ymax-window.ymin, 0), "Y-axis", zdir="z", size=50000, usetex=False,
#         angle=np.pi/80, ec="red", fc="red")
# text3d(ax, (window.xmax-window.xmin,window.ymax-window.ymin, 2 ), "Z axis", zdir="z", size=50000, usetex=False,
#         angle=0, ec="blue", fc="orange")

# Write a Latex formula on the z=0 'floor'
#text3d(ax, (tnx, tny, 3),"test sjdk jit",zdir="x", size=51000, usetex=False,ec="none", fc="green")

ax.zaxis.set_pane_color((.0,.2,.39,.21))
ax.xaxis._axinfo['grid']['linewidth']=0
ax.yaxis._axinfo['grid']['linewidth']=0
ax.zaxis._axinfo['grid']['color']=(0.,0.,0.,0.)
#ax.xaxis.set_label_text("District Names")

ax.tick_params(colors='#E6DB74')
xmt=ax.get_xmajorticklabels()
ymt=ax.get_ymajorticklabels()
ax.set_xticklabels(l2.iloc[:len(xmt)]['Name'])
ax.set_yticklabels(l2.iloc[len(xmt)-2:len(xmt)+len(xmt)]['Name'])
ax.set_zticklabels(l2.iloc[len(xmt)+len(xmt):len(xmt)+len(xmt)+len(xmt)]['Name'])
print(xmt[0].get_position()[0],ymt[int(len(ymt)/2)].get_position()[0])
center_y=ymt[int(len(ymt)/2)].get_position()[0]
center_x=xmt[int(len(xmt)/2)].get_position()[0]
print(center_x,ymt[-1].get_position()[0])
print(ymt)
ax.text(xmt[0].get_position()[0], center_y,1,"X-Axis",zdir='y',fontsize=20,color='yellow')
ax.text(center_x, ymt[-1].get_position()[0],1,"Y-Axis",zdir='x',fontsize=20,color='green')

#fig.savefig(sys.argv[1],format='png',facecolor=fig.get_facecolor())

#print(l2['Name'].to_list())
# bbox = fig.bbox_inches.from_bounds(2, 1, 8, 7)
# fig.savefig(sys.argv[1],format='png', 
# 	#bbox_inches=bbox, 
# 	facecolor=fig.get_facecolor())
#p.show()

#debug
#print(ax.zaxis.get_view_interval())
#print(ax.yaxis.get_data_interval())
#print(ax.get_xticklabels())
#print(ax.xaxis.get_ticklabels(minor=True))
#print(ax.xaxis.get_ticklocs())

#ax.tick_params(axis='x',grid_linewidth=0,grid_color='#E6DB74') # doesnt work
#for i in range(len(xmt)):
#	print(xmt[i])
#	xmt[i].set_text(l2.iloc[i]['Name'])

# doesnt work
#mt=ax.xaxis.get_major_ticks()
#mt=ax.xaxis.get_ticklabels()# has not label1
#mt=ax.get_xmajorticklabels()
#i=mt[0]
#print(mt[0].label1,mt[0].label2,mt[0].label)
#print([j for j in dir(i) if j.find("set")>-1 ])
# for i in range(len(mt)):
# 	mt[i].set_label(l2.iloc[i]['Name'])
# 	mt[i].set_label1(l2.iloc[i]['Name'])
# 	mt[i].set_label2(l2.iloc[i]['Name'])
# 	print(mt[i].get_label(),l2.iloc[i]['Name'])

# doesnt set tick labels
# tl=ax.xaxis.get_ticklabels()
# for i in range(len(tl)):
# 	tl[i].set_text(l2.iloc[i]['Name'])
# 	print(tl[i],l2.iloc[i]['Name'])
#ax.figure.canvas.draw()

#from matplotlib.colors import LightSource
# Get colormaps to use with lighting object.
#from matplotlib import cm

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

