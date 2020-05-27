import matplotlib.pyplot as plt
import sys,squarify
import pandas as p
from itertools import cycle

master=p.read_csv('data/cag/csv/rev.csv',comment='#')
v=master[master['month']=='Jan'][['State','GST','Stamp','Sales','Excise','ShareOfUnion','Other','Grants','NTR']].set_index('State')

title=sys.argv[1]
s=title.split()[0] # assume first word in title is state name
if s=='Tamil':
	s='Tamil Nadu'
if s=='Andhra':
	s='Andhra Pradesh'	
outfile=sys.argv[2]

colnames=['GST', 'Stamp', 'Sales', 'Excise', 'ShareOfUnion', 'Other', 'Grants','NTR']
l2c={
	'GST':"#00d0ff",
	'Stamp':"#ffc107",
	'Excise':'#00ff88',
	'Sales':'#22eeaa',
	'ShareOfUnion':'#A6E22E',
	'Other':'#F92672',
	'Grants':'red',
	'NTR':'#AE81FF',
}

fig = plt.figure(facecolor="#001f3f")
fig.suptitle(title, color="#00efde", fontsize=16)
ax = fig.add_subplot(111, frameon=False)
ax.set_facecolor("#002f4f")
ax.set_alpha(0.1)
ax.spines['bottom'].set_color('white')#'#ccc107')
ax.spines['top'].set_color('white') 
ax.spines['right'].set_color('white')
ax.spines['left'].set_color('white')
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
results=v.loc[s].sort_values(ascending=True)

squarify.plot(ax=ax, sizes=results.values, label=results.index, color=[l2c[i] for i in results.index], alpha=0.8)
fig.savefig(r'data/cag/viz/'+outfile,format='png',facecolor=fig.get_facecolor())
#plt.show()