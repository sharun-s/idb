import geopandas as gp
import matplotlib.pyplot as p
import pandas as pd
import sys

#args - filename - title - districts

fig = p.figure(facecolor="#001f3f")
#l1=gp.read_file('tn_boundary.json')

ax=fig.add_subplot(111, frameon=False)
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


fig.suptitle(sys.argv[2], color="#ffcc33", fontsize=16)

l2.plot(ax=ax, facecolor='#0099dd',edgecolor='#002f4f',label='TN',alpha=.78, linewidth=.4)
#ax.get_xaxis().set_visible(False)
#ax.get_yaxis().set_visible(False)
ax.set_facecolor("#002f4f")
ax.set_alpha(0.3)

#ax=l1.plot(facecolor='#0099dd',edgecolor='blue',label='TN',alpha=.78)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.spines['bottom'].set_color('white')#'#ccc107')
ax.spines['top'].set_color('white') 
ax.spines['right'].set_color('white')
ax.spines['left'].set_color('white')
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

districts=l2[l2.Name.isin(sys.argv[3:])]
print(len(districts))
print('Missing-')
print(l2[~l2.Name.isin(sys.argv[3:])].Name)
districts.plot(ax=ax,facecolor='orange',edgecolor='#002f4f',label='TN'
	,alpha=.73, linewidth=1)#,picker=5 
#fig.savefig(sys.argv[1],format='png',facecolor=fig.get_facecolor())

#munis.plot(ax=ax, kind='scatter',y='Lat',x='Lon',color='yellow')
corps.plot(ax=ax, kind='scatter',y='Lat',x='Lon',s=14,color='yellow')
gsp.plot(ax=ax, kind='scatter',y='Lat',x='Lon',s=7,color='orange')
gsl.plot(ax=ax, kind='scatter',y='Lat',x='Lon',s=5,color='purple')
g1.plot(ax=ax, kind='scatter',y='Lat',x='Lon',s=3,color='red')
g2.plot(ax=ax, kind='scatter',y='Lat',x='Lon',s=1,color='pink')



import shapely
#to debug - tmpevt=None
def onclick(event):
	axsub = event.inaxes
	#print(event)
	#global tmpevt
	#tmpevt=event
	if axsub:
		tmp = l2[l2.contains(shapely.geometry.Point(event.xdata,event.ydata))]['Name'].values[0]
		#print(tmp)
		#global annote
		annote.xy=event.xdata,event.ydata
		annote.set_text(tmp)
		fig.canvas.draw_idle()

#this works only by clicking specifically on the path within the tolerance level specified by 'picker' prop passed to plot
def on_pick(event):
	print(event)
	patchCollection = event.artist
	print(patchCollection) 

annote = ax.annotate("", xy=(0,0),xytext=(.1,.5), textcoords="figure fraction", color="#ffcc33", fontsize=14)
								#bbox=dict(boxstyle="round", fc="w"), 
								#arrowprops=dict(arrowstyle="->"))
#annote.set_visible(False)

#cid = fig.canvas.mpl_connect('pick_event', on_pick)
#fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('motion_notify_event', onclick)

p.show()
