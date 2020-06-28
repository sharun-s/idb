import matplotlib.pyplot as plt
import sys,squarify,locale
import pandas as p
from itertools import cycle
from locale import atof
from matplotlib.sankey import Sankey
locale.setlocale(locale.LC_NUMERIC, '')
try:

	df=p.read_csv(sys.argv[1],comment='#',header=None)

	df[1]=df[1].apply(lambda x:str(x).replace('- ','-')).apply(lambda x:atof(x) if x!='nan' else 0)
	#.apply(lambda x:atof(x) if not p.isna(x) else 0.)
	#df[1].str.replace('- ','-').apply(atof)

	with open(sys.argv[1]) as f:
		title=f.readline().split(',')[1].strip()

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
	fig.suptitle(title.replace('"','').capitalize(), color="#00efde", fontsize=12)

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

	#squarify.plot(ax=ax, sizes=results.values, label=results.index, alpha=0.8)
	dia=Sankey(ax=ax,head_angle=180, scale=0.0000001,
		#pathlengths=[100]*results.values,
	    flows=results[1].tolist() + [-1*df[1].sum()],
		labels=[i[:10] for i in results.index]+[title.replace('"','').capitalize()[:10]], 
		orientations=[1. if i > 0 else -1. for i in results.values]+[0.],
		color="#ffc107").finish()
	for i in range(0,len(dia[0].texts)):
		dia[0].texts[i].set_color('#E6DB74')
	fig.savefig('sk_'+sys.argv[1].replace('csv','png'),format='png',facecolor=fig.get_facecolor())
	#plt.show()
except Exception as e:
	print("error in ",sys.argv[1])
	print(e)
