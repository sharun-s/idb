import matplotlib.pyplot as plt
import sys
import pandas as p
from itertools import cycle

states=p.read_csv('States')
m=['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar-P', 'Mar-S']
master=[]
for s in range(0,len(states)):

	df=p.read_csv(r'data/cag/csv/'+states.prefix.iloc[s]+sys.argv[1],header=None,comment='#')
	if len(df) == 0:
		print(states.prefix.iloc[s] + 'no data found')
		sys.exit()
	df['month']=m[:len(df)]
	df['State']=states.name.iloc[s]
	master.append(df)
	title=states.name.iloc[s] #sys.argv[2]
	outfile=states.prefix.iloc[s]+sys.argv[3]
	colnames=sys.argv[4].split(',')
	incFY2018=True if sys.argv[5] == 'incFY2018' else False

master=p.concat(master, ignore_index=True, sort=False)
master=master.rename(columns={0:'GST',1:'Stamp',2:'Land',3:'Sales',4:'Excise',5:'ShareOfUnion',6:'Other'})
cats=['GST','Stamp','Sales','Excise','ShareOfUnion','Other']
colors=["#ffc107","#33ccff",'#F95733','#00ff88','#F9e792',"#ff1122",'#A6E22E']

for i in range(0,len(cats)):
	fig = plt.figure(facecolor="#001f3f")
	fig.suptitle('Southern States Tax Revenue Breakup FY19 (upto Jan)', x=0.35,color="#E6DB74", fontsize=16)
	ax = fig.add_subplot(111, frameon=False)
	ax.set_facecolor("#002f4f")
	ax.set_alpha(0.1)
	ax.spines['bottom'].set_color('white')#'#ccc107')
	ax.spines['top'].set_color('white') 
	ax.spines['right'].set_color('white')
	ax.spines['left'].set_color('white')
	ax.tick_params(axis='y', colors='#E6DB74')#FD971F')
	ax.tick_params(axis='x', colors='#E6DB74')
	ax.set_xlim(0,110000)
	ax.set_ylabel('',visible=False)
	bars=master[master['month']=='Jan'][['State']+cats[:i+1]].set_index('State')
	sorted_idx=bars.transpose().sum().sort_values(ascending=True).index
	ax.set_yticklabels(bars.index.to_list(), rotation=0)
	bars.ix[sorted_idx].plot(ax=ax,kind='barh',stacked=True,color=colors[:i+1], width=0.06)	
	l=ax.legend(loc='lower left', ncol=6, bbox_to_anchor=(-0.35, .97), frameon=False, facecolor='none')
	for text in l.get_texts():
		text.set_color("#efdecc")
	fig.savefig(r'data/cag/viz/'+str(i)+outfile,format='png',facecolor=fig.get_facecolor(),bbox_inches='tight')
