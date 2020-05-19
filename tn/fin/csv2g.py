import matplotlib.pyplot as plt
import sys
import pandas as p
from itertools import cycle

df=p.read_csv(sys.argv[1],header=None)
if len(df) == 0:
	sys.exit()

title=sys.argv[2]
outfile=sys.argv[3]
colnames=sys.argv[4].split(',')
incFY2018=True if sys.argv[5] == 'incFY2018' else False

fig = plt.figure(facecolor="#001f3f", figsize=(8.,6.))
fig.suptitle(title, color="#00efde", fontsize=16)
ax = fig.add_subplot(111, frameon=False)
ax.set_facecolor("#002f4f")
ax.set_alpha(0.1)
ax.spines['bottom'].set_color('white')#'#ccc107')
ax.spines['top'].set_color('white') 
ax.spines['right'].set_color('white')
ax.spines['left'].set_color('white')
ax.tick_params(axis='y', colors='#E6DB74')#FD971F')
ax.tick_params(axis='x', colors='#E6DB74')#

c=cycle(["#00d0ff","#ffc107",'#00ff88'])
labels=cycle(colnames)

def fy2018_19():
	for i in range(0,len(df.columns),2):
		fc=next(c)
		tl=next(labels)
		df[i+1].plot(ax=ax, color=fc,label='FY18 '+tl, alpha=0.2, legend=True)		
		df[i].plot(ax=ax, color=fc,label='FY19 '+tl,legend=True)
	if len(df) == 13:
		#ax.set_xticks(range(0,13))
		#ax.set_xticklabels(['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar-P', 'Mar-S'])
		ax.set_xticks([2,5,8,11,12])
		ax.set_xticklabels(['Jun', 'Sep', 'Dec', 'Mar-P', 'Mar-S'])
	else:
		ax.set_xticks([2,5,8,11])
		ax.set_xticklabels(['Jun', 'Sep', 'Dec', 'Mar'])
		#ax.set_xticks(range(0,12))
		#ax.set_xticklabels(['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar'])

	#print(df[0][2:14].str.replace('\n','').str[:3].to_list())
	#ax.set_xticks(range(2,14))
	#ax.set_xticklabels(df[0][2:14].str.replace('\n','').str[:3].to_list(), rotation=0)
	
	#ax.set_xticks(df[0][2:14].str.replace('\n','').str[:3].to_list())
	nc=4
	if len(df.columns)%3==0:
		nc=3
	l=ax.legend(loc='lower left', ncol=nc, bbox_to_anchor=(-0.1, 1.01), frameon=False, facecolor='none')
	for text in l.get_texts():
		text.set_color("#efdecc")
	#ax.set_ylim(ax.get_ylim()[::-1])
	fig.savefig(r'data/cag/viz/'+outfile,format='png',facecolor=fig.get_facecolor())

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
	l=ax.legend(loc='lower left', ncol=nc, bbox_to_anchor=(.2, 1.01), frameon=False, facecolor='none')
	for text in l.get_texts():
		text.set_color("#efdecc")
	fig.savefig(r'data/cag/viz/'+outfile,format='png',facecolor=fig.get_facecolor())

if incFY2018:
	fy2018_19()
else:
	fy2019()