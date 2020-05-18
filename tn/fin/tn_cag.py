import camelot
import locale
from locale import atof
import matplotlib.pyplot as plt
import sys
from itertools import cycle
locale.setlocale(locale.LC_NUMERIC, '')

#dec=camelot.read_pdf(r'/home/s/idb/tn/fin/201912.pdf')

fname=sys.argv[1]
pg=sys.argv[2]
title=sys.argv[3]
outfile=sys.argv[4]

#tables=camelot.read_pdf(r'/home/s/idb/tn/fin/20201.pdf',pages="1-2,17,18")
#summary=tables[0].df
#rec=tables[1].df
#exp=tables[2].df
fig = plt.figure(facecolor="#001f3f")
fig.suptitle(title, color="#00efde", fontsize=16)
ax = fig.add_subplot(111, frameon=False)
#ax.get_xaxis().set_visible(False)
#ax.get_yaxis().set_visible(False)
ax.set_facecolor("#002f4f")
ax.set_alpha(0.3)
ax.spines['bottom'].set_color('white')#'#ccc107')
ax.spines['top'].set_color('white') 
ax.spines['right'].set_color('white')
ax.spines['left'].set_color('white')
ax.tick_params(axis='y', colors='#E6DB74')#FD971F')
ax.tick_params(axis='x', colors='#E6DB74')#

tables=camelot.read_pdf(fname,pages=pg)

def cumulativeIncoming():
  rec[4][2:11].apply(atof).plot(color='green',label='18-19',legend=True)
  rec[2][2:11].apply(atof).plot(color='green',label='19-20',legend=True)
  plt.show()

def cumulativeOutgoing():
  exp[4][2:11].apply(atof).plot(color='green',label='18-19',legend=True)
  exp[2][2:11].apply(atof).plot(color='green',label='19-20',legend=True)
  plt.show()

c=cycle(["#ffc107","#00d0ff",'#00ff88'])
labels=cycle(sys.argv[5].split(','))
def cumulative():
	for i in range(0,len(tables)):
		df=tables[i].df
		fc=next(c)
		tl=next(labels)
		#df[[2,4]][2:14].applymap(lambda x:atof(x) if x else None).plot(kind='bar',ax=ax, color=[fc,None],label='FY19 '+tl, legend=True)
		df[4][2:14].apply(lambda x:atof(x) if x else None).plot(ax=ax, color=fc,label='FY19 '+tl, alpha=0.2, legend=True)		
		df[2][2:14].apply(lambda x:atof(x) if x else None).plot(ax=ax, color=fc,label='FY20 '+tl,legend=True)
	print(df[0][2:14].str.replace('\n','').str[:3].to_list())
	ax.set_xticks(range(2,14))
	ax.set_xticklabels(df[0][2:14].str.replace('\n','').str[:3].to_list(), rotation=0)
	#ax.set_xticks(df[0][2:14].str.replace('\n','').str[:3].to_list())
	l=ax.legend(loc='lower left', ncol=3, bbox_to_anchor=(0.0, .91), frameon=False, facecolor='none')
	for text in l.get_texts():
		text.set_color("#efdecc")
	#ax.set_ylim(ax.get_ylim()[::-1])
	fig.savefig(outfile,format='png',facecolor=fig.get_facecolor())

cumulative()