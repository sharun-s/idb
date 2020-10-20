import geopandas as gp
import matplotlib.pyplot as p
import pandas as pd
import sys
import shapely
import argparse

#args - filename - title - districts

parser = argparse.ArgumentParser(description='Basic 2D Tamil Nadu map generator')
parser.add_argument('--outfile', help='dump graph to OUTFILE, if not given enters interactive mode')
parser.add_argument('title', help='graph title')
parser.add_argument('districts', metavar='DistrictName', type=str, nargs='+',help='list of districts to plot')
parser.add_argument('--towns', metavar='Town Name', type=str, nargs='+',help='list of towns to plot')
parser.add_argument('-a',help='plot all towns',action="store_true")
parser.add_argument('-c',help='plot towngrade=muni corp',action="store_true")
parser.add_argument('-s1',help='plot towngrade=special grade',action="store_true")
parser.add_argument('-s2',help='plot towngrade=selection grade',action="store_true")
parser.add_argument('-g1',help='plot towngrade=first grade',action="store_true")
parser.add_argument('-g2',help='plot towngrade=second grade',action="store_true")

args = parser.parse_args()
print(args)

fig = p.figure(facecolor="#001f3f")
ax=fig.add_subplot(111, frameon=False)
fig.suptitle(args.title, color="#ffcc33", fontsize=16)
ax.set_facecolor("#002f4f")
ax.set_alpha(0.3)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.spines['bottom'].set_color('white')#'#ccc107')
ax.spines['top'].set_color('white') 
ax.spines['right'].set_color('white')
ax.spines['left'].set_color('white')

# setup data
#l1=gp.read_file('tn_boundary.json')
l2=gp.read_file('tn/geo/tn_dist.json')
l2.to_crs(epsg=4326,inplace=True)

munis=pd.read_csv('tn/geo/Munis.csv')
munis[['Lat','Lon']]=munis['LatLong'].str.split(";",expand=True)
munis[['Lat','Lon']]=munis[['Lat','Lon']].astype(float)
munis[['Type']]=munis[['Type']].astype(str)

g2=munis[munis['Type']=='Municipality Second grade']
g1=munis[munis['Type']=='Municipality First grade']
gsp=munis[munis['Type']=='Municipality Special grade']
gsl=munis[munis['Type']=='Municipality Selection grade']
corps=munis[munis['Type']=='Muni Corporation']

# setup base layer
#l1.plot(ax=ax, facecolor='#0099dd',edgecolor='blue',label='TN',alpha=.78)
l2.plot(ax=ax, facecolor='#0099dd',edgecolor='#002f4f',label='TN',alpha=.78, linewidth=.4)

# filter based on user choices
districts=l2[l2.Name.isin(args.districts)]

# tmphack if user spelling varies from whats in db just show possibilities  
if len(districts) < len(args.districts):
	print('Some districts not found. Check spelling. Did you mean -')
	print(l2[~l2.Name.isin(sys.argv[3:])].Name.sort_values().tolist())

districts.plot(ax=ax,facecolor='#ffcc66',edgecolor='#002f4f',label='TN'
	, linewidth=1)#,picker=5 

defaultdf=None
if args.a:
	munis.plot(ax=ax, kind='scatter',y='Lat',x='Lon',color='yellow',picker=True)
	defaultdf=munis
if args.c:
	corps.plot(ax=ax, kind='scatter',y='Lat',x='Lon',s=14,color='yellow',picker=True)
	defaultdf=corps
if args.s1:
	gsp.plot(ax=ax, kind='scatter',y='Lat',x='Lon',s=7,color='orange',picker=True)
	defaultdf=gsp
if args.s2:
	gsl.plot(ax=ax, kind='scatter',y='Lat',x='Lon',s=6,color='purple',picker=True)
	defaultdf=gsl
if args.g1:
	g1.plot(ax=ax, kind='scatter',y='Lat',x='Lon',s=6,color='red',picker=True)
	defaultdf=g1
if args.g2:
	g2.plot(ax=ax, kind='scatter',y='Lat',x='Lon',s=6,color='pink',picker=True)
	defaultdf=g2

#to debug - tmpevt=None
def onhover(event):
	axsub = event.inaxes
	#print(event)
	#global tmpevt
	#tmpevt=event
	if axsub:
		try:
			tmp = l2[l2.contains(shapely.geometry.Point(event.xdata,event.ydata))]['Name'].values[0]
			#print(munis[munis.District==tmp][['#Name','Type']])
			annote.xy=event.xdata,event.ydata
			annote.set_text(tmp)
			fig.canvas.draw_idle()
		except IndexError as e:
			pass
		#print(tmp)
		#global annote

#this works only by clicking specifically on the path within the tolerance level specified by 'picker' prop passed to plot
def on_pick(event):
	#print(event)
	#patchCollection = event.artist
	#print(patchCollection)
	ind = event.ind
	tmp=defaultdf.iloc[ind]['#Name'].values[0]
	if tmp:
		annote.set_text(tmp) 
	fig.canvas.draw_idle()

annote = ax.annotate("", xy=(0,0),xytext=(.1,.5), textcoords="figure fraction", color="#ffcc33", fontsize=14)
								#bbox=dict(boxstyle="round", fc="w"), 
								#arrowprops=dict(arrowstyle="->"))
#annote.set_visible(False)
fig.canvas.mpl_connect('pick_event', on_pick)
#fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('motion_notify_event', onhover)

if args.outfile:
	fig.savefig(args.outfile,format='png',facecolor=fig.get_facecolor())
else:
	p.show()

#ax.set_xscale('log')
# import numpy as np
# # Function Mercator transform
# def forward(a):
#     a = np.deg2rad(a)
#     return np.rad2deg(np.log(np.abs(np.tan(a) + 1.0 / np.cos(a))))

# def inverse(a):
#     a = np.deg2rad(a)
#     return np.rad2deg(np.arctan(np.sinh(a)))

# ax.set_yscale('function', functions=(forward, inverse))
