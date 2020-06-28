import matplotlib.pyplot as plt
import sys,squarify,locale
import pandas as p
from itertools import cycle
from locale import atof
locale.setlocale(locale.LC_NUMERIC, '')

df=p.read_csv(sys.argv[1],comment='#',header=None)
df[1]=df[1].apply(atof)

with open(sys.argv[1]) as f:
	title=f.readline().split(',')[1]

#colnames=df.loc[0]
# l2c={
# 	'GST':"#00d0ff",
# 	'Stamp':"#ffc107",
# 	'Excise':'#00ff88',
# 	'Sales':'#22eeaa',
# 	'ShareOfUnion':'#A6E22E',
# 	'Other':'#F92672',
# 	'Grants':'red',
# 	'NTR':'#AE81FF',
# }

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

df.set_index(0,inplace=True)
results=df.sort_values(by=1,ascending=True)

squarify.plot(ax=ax, sizes=results.values, label=results.index, alpha=0.8)
fig.savefig(sys.argv[1].replace('csv','png'),format='png',facecolor=fig.get_facecolor())
#plt.show()