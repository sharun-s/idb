import matplotlib.pyplot as plt
import sys,squarify
import pandas as p
from itertools import cycle

colnames=['Expenditure','Interest Payments','Wages','Pensions','Subsidies','CapEx','LoansGiven']
l2c={
	'Expenditure':"#00d0ff",
	'Interest Payments':"#ffc107",
	'Wages':'#00ff88',
	'Pensions':'#22eeaa',
	'Subsidies':'#A6E22E',
	'CapEx':'#F92672',
	'LoansGiven':'#AE81FF',
}

master=p.read_csv(sys.argv[3],comment='#')
v=master[master['month']=='Feb'][['State']+colnames].set_index('State')

title=sys.argv[1]
s=title.split()[0] # assume first word in title is state name
if s=='Tamil':
	s='Tamil Nadu'
if s=='Andhra':
	s='Andhra Pradesh'	
outfile=sys.argv[2]

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