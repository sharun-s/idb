import matplotlib.pyplot as plt
import sys
import pandas as p
from itertools import cycle
import common

df=p.read_csv(sys.argv[1],header=None,comment='#')
if len(df) == 0:
	sys.exit()

title=sys.argv[2]
outfile=sys.argv[3]
colnames=sys.argv[4].split(',')
plotallyears=True if sys.argv[5] == 'all' else False

fig,ax=common.newfig(title)

c=cycle(["#00d0ff","#ffc107",'#00ff88','#AE81FF','#A6E22E','#F92672'])
labels=cycle(colnames)

def getlatest(columnno):
	latest=df[p.notna(df[columnno])][columnno]
	return latest.index[-1],latest.iloc[-1]

def fy_all():
	for i in range(0,len(df.columns),3):
		fc=next(c)
		tl=next(labels)
		df[i].plot(ax=ax, color=fc,label='2020 '+tl,legend=False)
		df[i+1].plot(ax=ax, color=fc,label='2019 '+tl,alpha=0.5, legend=False)
		df[i+2].plot(ax=ax, color=fc,label='2018 '+tl, alpha=0.4, legend=False)		

	ax.set_xticks([2,5,8,11])
	ax.set_xticklabels(['Jun', 'Sep', 'Dec', 'Mar'])
	lcnt=0
	for line in ax.lines:
		y = line.get_ydata()[-1]
		if y:
			x=1
			xt=0
			pass
		else:
			x,y=getlatest(lcnt)
			xt=32
			x=x/13.0
		lcnt=lcnt+1
		ax.annotate(line.get_label().upper(), xy=(x,y), xytext=(xt,0), 
			color=line.get_color(),alpha=line.get_alpha(),#'#d6cB74',#line.get_color(), 
    		xycoords = ax.get_yaxis_transform(), 
    		textcoords="offset pixels",
    		size=12)
	plt.annotate('DATA: Comptroller and Auditor General of India - State Accounts Monthly Key Indicators', (0.02,.0), (0, -25), 
                xycoords='axes fraction', 
                textcoords='offset points', 
                color='#d6cB74', va='top', fontsize=9)

	fig.savefig(r'data/cag/viz/'+outfile,format='png',facecolor=fig.get_facecolor(),bbox_inches='tight')

def fy2019():
	for i in range(0,len(colnames)):
		fc=next(c)
		tl=next(labels)
		#df[i+1].plot(ax=ax, color=fc,label='FY18 '+tl, alpha=0.2, legend=True)		
		df[i].plot(ax=ax, color=fc,label='FY19'+tl,legend=True)
	if len(df) == 13:
		#ax.set_xticks(range(0,13))
		#ax.set_xticklabels(['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar-P', 'Mar-S'])
		ax.set_xticks([2,5,8,11,12])
		ax.set_xticklabels(['Jun', 'Sep', 'Dec', 'Mar-P', 'Mar-S'])
	else:
		ax.set_xticks([2,5,8,11])
		ax.set_xticklabels(['Jun', 'Sep', 'Dec', 'Mar'])
	nc=4
	if len(df.columns)%3==0:
		nc=3
	l=ax.legend(loc='lower left', ncol=nc, bbox_to_anchor=(.2, .97), frameon=False, facecolor='none')
	for text in l.get_texts():
		text.set_color("#efdecc")
	fig.savefig(r'data/cag/viz/'+outfile,format='png',facecolor=fig.get_facecolor())

if plotallyears:
	fy_all()
else:
	fy2019()