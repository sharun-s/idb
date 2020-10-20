import geopandas as gp
import matplotlib.pyplot as p
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.mplot3d import proj3d
from descartes import PolygonPatch
#import descartes.patch as dp
import numpy as np
import sys
from matplotlib.transforms import Affine2D
from matplotlib.patches import PathPatch
from matplotlib.text import TextPath
import matplotlib as matp

#uncomment for interactive debug
#matp.use('TkAgg')
#p.ion()

#args
# output filename, elevation, azimuth, list of districts
def Path3D(ax, geom, name, forecolor, bordercolor, borderwidth=1, transparency=1., zheight=0):
	# descartes.PolygonPatch converts a shapely or geojson like obj (geom in this case) to a matplotlib pathpatch
	pp=PolygonPatch(geom, fc=forecolor, ec=bordercolor, lw=borderwidth,alpha=transparency, zorder=zheight )
	xy=pp.get_extents()
	pp.dname=name
	#store 2D path
	#pp.dpath=dp.PolygonPath(geom)
	pp.dpath=PolygonPatch(geom, fc=forecolor, ec=bordercolor, lw=borderwidth,alpha=transparency, zorder=zheight )
	pp.g=geom
	ax.add_patch(pp)
	art3d.pathpatch_2d_to_3d(pp, z=zheight, zdir="z")
	return xy

def Path3D_transform(ax, geom, forecolor, bordercolor, angle, trans, borderwidth=1, transparency=1., 
	z=0,zdir='z',scale=1):
	# descartes.PolygonPatch converts a shapely or geojson like obj (geom in this case) to a matplotlib pathpatch
	s = Affine2D().scale(scale) + ax.transData
	pp=PolygonPatch(geom, ec=bordercolor, 
		lw=borderwidth,alpha=transparency, zorder=z )
	ptmp=pp.get_path()
	x=geom.centroid.x
	y=geom.centroid.y
	if zdir == "y":
		xy1, z1 = (center_yz_x, center_yz_y),1 #(x, z), y
	elif zdir == "x":
		xy1, z1 = (y, z), x
	else:
		xy1, z1 = (x, y), z
	#print(xy1[0], xy1[1],z1)#len(ptmp.cleaned(simplify=True)))
	tmp=PathPatch(trans.transform_path(ptmp),color=forecolor,transform=s)
	ax.add_patch(tmp)
	art3d.pathpatch_2d_to_3d(tmp, z=z, zdir=zdir)
	#print(tmp.get_extents())

def get_proj_scale(self):
    """                                                                                                                                                                                                                                    
    Create the projection matrix from the current viewing position.                                                                                                                                                                        

    elev stores the elevation angle in the z plane                                                                                                                                                                                         
    azim stores the azimuth angle in the x,y plane                                                                                                                                                                                         

    dist is the distance of the eye viewing point from the object                                                                                                                                                                          
    point.                                                                                                                                                                                                                                 

    """
    relev, razim = np.pi * self.elev/180, np.pi * self.azim/180

    xmin, xmax = self.get_xlim3d()
    ymin, ymax = self.get_ylim3d()
    zmin, zmax = self.get_zlim3d()

    # transform to uniform world coordinates 0-1.0,0-1.0,0-1.0                                                                                                                                                                             
    worldM = proj3d.world_transformation(
        xmin, xmax,
        ymin, ymax,
        zmin, zmax)

    # look into the middle of the new coordinates                                                                                                                                                                                          
    R = np.array([0.5, 0.5, 0.5])

    xp = R[0] + np.cos(razim) * np.cos(relev) * self.dist
    yp = R[1] + np.sin(razim) * np.cos(relev) * self.dist
    zp = R[2] + np.sin(relev) * self.dist
    E = np.array((xp, yp, zp))

    self.eye = E
    self.vvec = R - E
    self.vvec = self.vvec / proj3d.mod(self.vvec)

    if abs(relev) > np.pi/2:
    # upside down                                                                                                                                                                                                                          
      V = np.array((0, 0, -1))
    else:
      V = np.array((0, 0, 1))
    zfront, zback = -self.dist, self.dist

    viewM = proj3d.view_transformation(E, R, V)
    perspM = proj3d.persp_transformation(zfront, zback)
    M0 = np.dot(viewM, worldM)
    M = np.dot(perspM, M0)

    return np.dot(M, scale);

distshape=None

def onhover(event):
	global distshape
	#incase zoom/pan happens min max changes
	xmin, xmax = ax.xaxis.get_view_interval() #or xlim_changed and ylim_changed 
	# if distshape:
	# 	ax.patches[-1].remove()
	# 	distshape.remove()	
	axsub = event.inaxes
	print(axsub.get_w_lims())
	#print(event)
	if axsub:
		for i in axsub.patches:
			i.set_fc('#E6DB74')
			# from patches.Patch.contains_point
			data_cords=i.get_transform().transform((event.xdata, event.ydata))
			if i.contains_point(data_cords):
				if i.dname=='TN' or i.dname=='selected':
					continue
				dlabel.set_text(i.dname)
				i.set_fc('red')
				#distshape=Path3D_transform(ax,i.g, trans=Affine2D().translate(-1.2,-9),forecolor="#d40000d0", bordercolor="red",angle=np.pi/2,zdir='y',z=12.7,scale=2.4)#, 

				fig.canvas.draw_idle()
			

BLUE = '#6699cc'

l1=gp.read_file('tn/geo/tn_boundary.json')
l1.to_crs(epsg=4326,inplace=True)

l2=gp.read_file('tn/geo/tn_dist.json')
l2.to_crs(epsg=4326,inplace=True)

districts=l2[l2.Name.isin(sys.argv[4:])].geometry
tn=l1.iloc[0].geometry
tnx=tn.centroid.x
tny=tn.centroid.y

fig = p.figure(facecolor="#001f3f",figsize=(10.24,7.68)) 
#fig.subplots_adjust(left=0,right=1,bottom=0, top=1)
ax = fig.gca(projection='3d')

e=40 if int(sys.argv[2]) > 40 else int(sys.argv[2])  
azi=int(sys.argv[3]) or -90.
ax.set_facecolor('#001f3f')

window=Path3D(ax,geom=tn,name='TN',forecolor='#001f3f',#'#22aacc', 
	bordercolor='#001f3f',#,BLUE, 
	transparency=0, zheight=0)
ax.set_xlim3d(window.xmin-1, window.xmax+1) #window.xmin-120000, window.xmax) #8600000, 8800000)
ax.set_ylim3d(window.ymin-1, window.ymax+1) #window.ymin, window.ymax)#1360000, 1440000)
ax.set_zlim3d(0, 3)
#print(window.xmin-1, window.xmax+1, window.ymin-1, window.ymax+1)
#75-81 - 6 
#7-14 - 7
#0-3 - 4

zh=0
for j in districts:
	#base
	if int(sys.argv[2]) > 40:
		zh=(int(sys.argv[2])-40)/90.0
	Path3D(ax,geom=j,name='selected',forecolor='yellow', bordercolor='#002f4f', borderwidth=1, zheight=1+zh)
	#ax.plot([j.centroid.x, j.centroid.x],[j.centroid.y, j.centroid.y],[1,1+zh],'y',linewidth=4)

for j in l2.itertuples():
	#print(j)
	Path3D(ax,geom=j.geometry,name=j.Name,forecolor='#E6DB74', bordercolor='#E6DB74', transparency=.8, borderwidth=1, zheight=0)
	#ax.plot([tnx, j.centroid.x],[tny, j.centroid.y],[1],'r')	

ax.zaxis.set_pane_color((.0,.2,.39,.21))
ax.xaxis.set_pane_color((.0,.2,.39,.21))
ax.yaxis.set_pane_color((.0,.2,.39,.21))

ax.xaxis._axinfo['grid']['linewidth']=0
ax.yaxis._axinfo['grid']['linewidth']=0
ax.zaxis._axinfo['grid']['color']=(0.,0.,0.,0.)

ax.xaxis.set_label_text("Longitude",color='#E6DB74')
ax.yaxis.set_label_text("Latitude",color='#E6DB74')

ax.tick_params(colors='#E6DB74')
xticlocs=ax.xaxis.get_majorticklocs()
yticlocs=ax.yaxis.get_majorticklocs()

center_yz_y=yticlocs[int(len(yticlocs)/2)]
center_yz_x=xticlocs[0]
center_xz_x=xticlocs[int(len(xticlocs)/2)]
center_xz_y=yticlocs[-1]
#ax.set_xticklabels([])
#ax.set_yticklabels([])
#ax.set_zticklabels([])

#ax.text3D(center_yz_x, center_yz_y,1,"Some Data",zdir='y',fontsize=20,color='yellow')
ax.text(center_yz_x, center_yz_y,1,"Not3d",zdir='y',fontsize=20,color='pink')

dlabel=ax.text(center_xz_x, center_xz_y,1,"Hover Over A District",zdir='x',fontsize=20,color='orange')

t=ax.zaxis.get_transform()
p1 = PathPatch(t.transform_path(ax.patches[13].dpath.get_path()))
ax.add_patch(p1)
art3d.pathpatch_2d_to_3d(p1, z=1, zdir='z')

#trans = Affine2D().rotate_deg(1).translate(100000,-200000)#j.centroid.x,(window.ymax-window.ymin)/2)#j.centroid.y)
# Path3D_transform(ax,j.geometry, trans = Affine2D().translate(1,2),
# 	forecolor="red", bordercolor="red",angle=np.pi/2,zdir='z')#, 
# Path3D_transform(ax,j.geometry, trans = Affine2D().translate(-1,-9),
# 	forecolor="pink", bordercolor="pink",angle=np.pi/2,zdir='y',z=14)#,
# Path3D_transform(ax,j.geometry, trans = Affine2D().translate(0,-5),
# 	forecolor="green", bordercolor="green",angle=np.pi/2,zdir='y',z=7)#yneg is down z is forward backward, lw=1,alpha=0.6, zorder=1)
# Path3D_transform(ax,j.geometry, trans = Affine2D().translate(0,-7),scale=2.4,
# 	forecolor="blue", bordercolor="blue",angle=np.pi/2,zdir='y',z=7)#, lw=1,alpha=0.6, zorder=1)
#for xx in range(-60,0,20):
xx=-55
#zz=70-90
for yy in range(-20,-10,1):
	#for zz in range(70,90,10):
	zz=70
	Path3D_transform(ax,j.geometry, trans = Affine2D().translate(xx,yy),scale=1,
			forecolor='red', bordercolor="red",angle=np.pi/2,zdir='x',z=zz)#, 


#print(ax.patches[-1].get_extents() )
print(ax.patches[-1] )
#ax.set_top_view()

# from matplotlib.patches import Circle
# circle = Circle((78,5), .4,color='#ffcc33') #z=4, zdir='y'
# #trans = Affine2D().rotate_deg(0).translate(78,11)
# #circle = Circle((0,0), .5,color='#ffcc33') #zd=z
# ax.add_patch(circle)
# art3d.pathpatch_2d_to_3d(circle, z=3, zdir='y')

#print(p.get(ax.patches[-1]))
#print(dir(p1))
#print(p1.get_window_extent())
#print(p1.get_visible())

#p1=art3d.PathPatch3D(ax.patches[13], zs=1, zdir='z')
#ax.add_patch(p1)

fig.canvas.mpl_connect('motion_notify_event', onhover)
#ax.get_proj=lambda:np.dot(Axes3D.get_proj(ax),np.diag([6/7.,7/7.,4/7.,1]))

p.show()

#adds random labels along xyz axis
# xmt=ax.get_xmajorticklabels()
# ymt=ax.get_ymajorticklabels()
# print(xmt)
# # tick label test
# ax.set_xticklabels(l2.iloc[:len(xmt)]['Name'])
# ax.set_yticklabels(l2.iloc[len(xmt)-2:len(xmt)+len(xmt)]['Name'])
# ax.set_zticklabels(l2.iloc[len(xmt)+len(xmt):len(xmt)+len(xmt)+len(xmt)]['Name'])
# print(xmt)
# #print(xmt[0].get_position()[0],ymt[int(len(ymt)/2)].get_position()[0])

#print(ax.xaxis.get_major_locator()) # Auto locator
#print(ax.xaxis.get_minor_locator()) # Null locator

#print([j for j in dir(ax.xaxis) if j.find("get")>-1 ])
#fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
#ax.set_axis_off()
#ax.set_aspect(0.73*1.33)
#ax.view_init(elev=e, azim=azi)

#ax.get_proj=lambda:np.dot(Axes3D.get_proj(ax),np.diag([1.04,1.15,1,1])) 

#ax.plot([tnx],[tny],[1],'go')
#print(window.xmin, window.xmax, window.xmax-window.xmin)
#print(window.ymin, window.ymax, window.ymax-window.ymin)
#print((window.xmax-window.xmin)/(window.ymax-window.ymin))

#ax.margins(1.1,.1,0.,tight=True)
#print(ax.get_proj())
#print(ax.get_w_lims())

	#top
	#Poly(ax,geom=j,forecolor='yellow', bordercolor='yellow', bordegrwidth=0.5, zheight=2)

	# zinc=0
	# end=6
	# for i in range(0,2*end):
	# 	pbase=PolygonPatch(j, fc='yellow', ec=BLUE, alpha=0.2, lw=0, zorder=1 )
	# 	ax.add_patch(pbase)
	# 	art3d.pathpatch_2d_to_3d(pbase, z=i/(1.0*end), zdir="z")	



#p1 = PathPatch(trans.transform_path(polypath.get_path()))
#ax.add_patch(p1)
#art3d.pathpatch_2d_to_3d(p1, z=z1, zdir=zdir)
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

