import geopandas as gp
import matplotlib.pyplot as p

l1=gp.read_file('tn_boundary.json')

l2=gp.read_file('tn_dist.json')

ax=l1.plot(facecolor='#0099dd',edgecolor='blue',label='TN',alpha=.78)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.spines['bottom'].set_color('white')#'#ccc107')
ax.spines['top'].set_color('white') 
ax.spines['right'].set_color('white')
ax.spines['left'].set_color('white')


l2[l2.Name=='Tiruppur'].plot(ax=ax,facecolor='orange',edgecolor='blue',label='TN',alpha=.73, linewidth=1) 
p.ison()
p.show()
