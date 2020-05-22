import sys
#print("files to process-", len(sys.argv)-1)
import pandas as p
import geopandas as gp
import matplotlib.pyplot as plt
df=p.read_csv(sys.argv[1])
if len(df) == 0:
	sys.exit()

fig = plt.figure(facecolor="#001f3f")

#l1=gp.read_file('../tn_boundary.json')
l2=gp.read_file('../../tn_dist.json')

ax3 = fig.add_subplot(111, frameon=False)
l2.plot(ax=ax3, facecolor='#0099dd',edgecolor='blue',label='TN',alpha=.78, linewidth=0)
ax3.get_xaxis().set_visible(False)
ax3.get_yaxis().set_visible(False)
ax3.set_facecolor("#002f4f")
ax3.set_alpha(0.3)
ax3.spines['bottom'].set_color('white')#'#ccc107')
ax3.spines['top'].set_color('white') 
ax3.spines['right'].set_color('white')
ax3.spines['left'].set_color('white')

#age dist binned
women=df[df.Gender=='F']
#women.groupby(p.cut(women.Age, [0,30,40,50,60,70])).Age.count()
men=df[df.Gender=='M']
#men.groupby(p.cut(men.Age, [0,30,40,50,60,70])).Age.count().plot('bar')

#plot districts with women
l2[l2.Name.isin(women.District)].plot(ax=ax3,facecolor='#ffcc55',edgecolor='blue')
