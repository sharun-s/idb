import pandas as p
import matplotlib.pyplot as plt

def newfig(title):
	fig = plt.figure(facecolor="#001f3f",figsize=(10,10), dpi= 80)
	fig.suptitle(title, color="#00efde", fontsize=12)
	ax = fig.add_subplot(111, frameon=False)
	ax.set_title('Deviation from Average',color="#00efde", fontsize=12)
	ax.set_facecolor("#002f4f")
	ax.set_alpha(0.1)
	ax.spines['bottom'].set_color('white')#'#ccc107')
	ax.spines['top'].set_color('white') 
	ax.spines['right'].set_color('white')
	ax.spines['left'].set_color('white')
	ax.tick_params(axis='y', colors='#E6DB74')#FD971F')
	ax.tick_params(axis='x', colors='#E6DB74')#
	return fig,ax

d=p.read_csv('data/ddp.csv',skiprows=2)
def dumpChart(year):
	f,a = newfig('TN - District Domestic Product '+ year)

	v=d[['District',year]][1:]
	ddp=v[year]
	v['ddp']=(ddp - ddp.mean())/ddp.std()
	v['colors'] = ['#cc3107' if x < 0 else '#22bb66' for x in v['ddp']]
	v.sort_values('ddp',inplace=True)
	v.reset_index(inplace=True)
	a.hlines(y=v.index, xmin=0, xmax=v.ddp, color=v.colors, linewidth=5)
	a.set_ylabel('$District$',color="#E6DB74")
	a.set_xlabel('$District Domestic Product$',color="#E6DB74")
	#bbox_inches='tight'
	a.set_yticks(v.index)
	a.set_yticklabels(v.District.values)
	plt.grid(linestyle='--', alpha=0.2)
	plt.tight_layout()
	f.savefig('ddp'+str(year)+'.png',format='png',facecolor=f.get_facecolor())

dumpChart('2013-14')
dumpChart('2012-13')
dumpChart('2011-12')
dumpChart('2010-11')
dumpChart('2009-10')
dumpChart('2008-09')
dumpChart('2007-08')
dumpChart('2006-07')

