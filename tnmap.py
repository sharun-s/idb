import geopandas as gp
import matplotlib.pyplot as p
import sys

#args - filename - title - districts

fig = p.figure(facecolor="#001f3f")
#l1=gp.read_file('tn_boundary.json')

ax=fig.add_subplot(111, frameon=False)
l2=gp.read_file('tn_dist.json')

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


districts=l2[l2.Name.isin(sys.argv[3:])]
print(len(districts))
print('Missing-')
print(l2[~l2.Name.isin(sys.argv[3:])].Name)
districts.plot(ax=ax,facecolor='orange',edgecolor='#002f4f',label='TN',alpha=.73, linewidth=1) 
#fig.savefig(sys.argv[1],format='png',facecolor=fig.get_facecolor())
p.show()
