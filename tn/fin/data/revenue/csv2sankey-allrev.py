import matplotlib.pyplot as plt
import sys,squarify,locale
import pandas as p
from itertools import cycle
from locale import atof
from matplotlib.sankey import Sankey
locale.setlocale(locale.LC_NUMERIC, '')

from os import listdir
allfiles=listdir('.')
csv=[i for i in allfiles if i.endswith('csv') ][:int(sys.argv[1])]#and i.startswith('02')]
print(csv)
fig = plt.figure(facecolor="#001f3f",figsize=(12,6))
#fig.suptitle(title.replace('"','').capitalize(), color="#00efde", fontsize=12)

ax = fig.add_subplot(111, frameon=False)
ax.set_facecolor("#002f4f")
ax.set_alpha(0.1)
ax.spines['bottom'].set_color('white')#'#ccc107')
ax.spines['top'].set_color('white') 
ax.spines['right'].set_color('white')
ax.spines['left'].set_color('white')
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
sk=Sankey(ax=ax,head_angle=180, scale=0.000000001)
sink=[]
sinklabel=[]
try:
	for c in csv:
		df=p.read_csv(c,comment='#',header=None)

		df[1]=df[1].apply(lambda x:str(x).replace('- ','-')).apply(lambda x:atof(x) if x!='nan' else 0)
		
		with open(c) as f:
			title=f.readline().split(',')[1].strip()
		
		df.set_index(0,inplace=True)
		results=df.sort_values(by=1,ascending=True)
		if all([True if r==0 else False for r in results[1]]):
			print("skipping",c)
			continue 
		sink.append(-1*df[1].sum())
		sinklabel.append(title.replace('"','').capitalize())
	print(sink+[-1*sum(sink)])
	sk.add(
		#pathlengths=[100]*results.values,
	    flows=sink+[-1*sum(sink)],
		labels=['']*len(sinklabel)+['total'], 
		orientations=[1.]*len(sink) + [-1.],
		color="#027368")
	cnt=0
	for c in csv:
		df=p.read_csv(c,comment='#',header=None)

		df[1]=df[1].apply(lambda x:str(x).replace('- ','-')).apply(lambda x:atof(x) if x!='nan' else 0)
		
		df.set_index(0,inplace=True)
		results=df.sort_values(by=1,ascending=True)
		if all([True if r==0 else False for r in results[1]]):
			print("skipping",c)
			continue 
		print([-1*k for k in results[1].tolist()] + [df[1].sum()])
		print('connecting',cnt, len(results))
		sk.add(
			#pathlengths=[100]*results.values,
		    flows=[-1*k for k in results[1].tolist()] + [df[1].sum()],
			#labels=[i[:10] for i in results.index]+[title.replace('"','').capitalize()[:10]], 
			orientations=[1. if i > 0 else -1. for i in results.values]+[0.],
			color="#ffc107", prior=0, connect=(cnt, len(results)))
		cnt=cnt+1
		#fig.savefig('sk_'+sys.argv[1].replace('csv','png'),format='png',facecolor=fig.get_facecolor())
		#plt.show()

	dia=sk.finish()
	for d in range(0,len(dia)):
		for i in range(0,len(dia[d].texts)):
			dia[d].texts[i].set_color('#E6DB74')
	fig.savefig('grow_'+sys.argv[1]+'.png',format='png',facecolor=fig.get_facecolor())
except Exception as e:
	print("error in ",c)
	raise e
