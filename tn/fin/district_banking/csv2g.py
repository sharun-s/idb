import matplotlib.pyplot as plt;import pandas as p
import argparse,sys
import common
from locale import atof
from matplotlib.colors import Normalize
import matplotlib.cm as cm
#NB: tmp hack because of import common run from parent dir - idb/tn/fin$python3 -m district_banking.csv2g
norm = Normalize(vmin=0.0, vmax=4.0)

def newfig(title):
	fig = plt.figure(facecolor="#001f3f",figsize=(7.2,7.2), dpi= 80)#figsize=(7.2,7.2))
	fig.suptitle(title, color="#E6DB74", fontsize=16)
	ax = fig.add_subplot(111, frameon=False)
	ax.set_facecolor("#002f4f")
	ax.set_alpha(0.1)
	ax.spines['bottom'].set_color('white')#'#ccc107')
	ax.spines['top'].set_color('white') 
	ax.spines['right'].set_color('white')
	ax.spines['left'].set_color('white')
	ax.tick_params(axis='y', colors='#E6DB74')#FD971F')
	ax.tick_params(axis='x', colors='#E6DB74')#
	return fig,ax

def formatData(data):
	#details={}
	labelandamt=[]
	cnt=0
	for k,j in data.items():
		cnt=cnt+1
		if cnt>10:
			labelandamt.append(k +' '+common.format_indian(j*10000000.0))
		else:
			labelandamt.append(k +'\n'+common.format_indian(j*10000000.0))
	return labelandamt

parser = argparse.ArgumentParser(description='Total Deposits Grapher')
parser.add_argument('-csv', default="district_banking/districtwise_deposits_credit.csv",help='input csv')
parser.add_argument('-pie', default=False, help='show only latest quarter districtwise', action='store_true')
parser.add_argument('-dumpall',action="store_true", help='show all data dump all districts')
parser.add_argument('--outfile', help='output filename specify extn')

args = parser.parse_args()
print(args)

coldict={'North':'violet','West':'darkorange','South':'green',
'Chennai':'dodgerblue','East':'crimson'}

disam={'tiruppur':'West',
'tirunelvali':'South',
'kanyakumari':'South',
'toothukudi':'South',
'sivaganga':'South',
'nagapattinam':'East',
'tiruvannamalai':'North',
'pudukkottai':'East',
'nilgiris':'West'} 

alldata=p.read_csv(args.csv,skiprows=2)

region=p.read_csv('gsdp/data/ddp-currentprices.csv',skiprows=2)
rmap=region[['District','Region']]

depcol=[i for i in alldata.columns if i.find('Deposit') > -1]
credcol=[i for i in alldata.columns if i.find('Credit') > -1]
branchcol=[i for i in alldata.columns if i.find('Offices') > -1]

d=alldata[depcol].T
d.columns=alldata['District']
c=alldata[credcol].T
c.columns=alldata['District']
b=alldata[branchcol].T
b.columns=alldata['District']

tot=common.format_indian(10000000.0*d.loc['2020-21:Q1 Deposit']['Total'])
print(tot)
#drop state total so it doesn't get plotted
d.drop('Total',axis=1,inplace=True)

def get_colors(data):
	colors=[]
	for i in data.index:
		if i.title() in rmap['District'].values:
			#colors.append(cm.Paired(norm(coldict[rmap[ rmap['District']==i.title()]['Region'].values[0]])))
			colors.append(coldict[rmap[ rmap['District']==i.title()]['Region'].values[0]])
		else:
			print(i.lower(),'not found using disam')
			colors.append(coldict[disam[i.lower()]])
	return colors

if args.pie:
	fig,ax=newfig('TN Districts - Deposits in Scheduled Banks - 2020')

	latest=d.loc['2020-21:Q1 Deposit'].T.sort_values(ascending=False)
	latestlabels=formatData(latest)
	latest.plot(kind='pie',ax=ax,autopct='%1.1f%%',
		labels=latestlabels, #cmap=plt.get_cmap("Paired"),
		colors=get_colors(latest), 
		wedgeprops=dict(width=0.3,edgecolor='#444444'))
	prev=None
	for tx in ax.texts:
		tx.set_color("#E6DB74")
		label=tx.get_text()
		if label.find('%') > -1:
			#tx.set_color('#001f3f')
			perc=atof(label[:-2])
			if perc<0.3:
				tx.set_fontsize(3)
				prev.set_fontsize(3)
			if perc<1:
				tx.set_fontsize(4)
				prev.set_fontsize(4)
			elif perc<3:
				tx.set_fontsize(5)
				prev.set_fontsize(6)
			elif perc<4:
				tx.set_fontsize(6)
				prev.set_fontsize(8)
			elif perc<7:
				tx.set_fontsize('small')
				prev.set_fontsize(10)
			else:
				tx.set_fontsize('medium')
				prev.set_fontsize(12)
		else:
			prev=tx

	y=ax.get_yaxis()
	y.label.set_visible(False)
	ax.annotate('TN Total \n\n'+ tot , xycoords='figure fraction', xy=(.45,.48), fontweight='bold', 
		color='white')
else:
	if args.dumpall:
		for i in d.columns:
			fig,a=newfig(i+' - Deposits/Credit 2020')
			d[i].plot(ax=a, label="Deposits", legend=True, color='limegreen')
			c[i].plot(ax=a, label="Credit", legend=True, color='red')
			a.invert_xaxis();
			a.set_ylabel('CRORES',color="#d6cB74")
			#print(dir(a.get_xticklabels()[2]))
			a.fill_between(range(0,13),d[i].values,c[i].values,where=d[i].values > c[i].values, facecolor='green', alpha=0.7)
			a.fill_between(range(0,13),d[i].values,c[i].values,where=d[i].values < c[i].values, facecolor='salmon', alpha=0.4)
			
			a.set_xticklabels([xt.get_text().split(' ')[0] for xt in a.get_xticklabels() if xt])
			fig.savefig('deposits_credit_2017-2020'+i+'.png',format='png',facecolor=fig.get_facecolor())
	else:
		fig,ax=newfig('TN Districts - Credit - 2020')
		c.plot(ax=ax,legend=False)
		ax.set_yscale('log')
		ax.invert_xaxis()
		for line in ax.lines:
			y = line.get_ydata()[0]
			ax.annotate(line.get_label().title(), xy=(1,y), xytext=(0,0), color='#d6cB74',#line.get_color(), 
        		xycoords = ax.get_yaxis_transform(), 
        		textcoords="offset points",
        		size=8)


plt.annotate('Data:rbi.org.in (Quarterly Deposit Stats)', (0.,0), (0, -25), 
                xycoords='axes fraction', textcoords='offset points', 
                color='#E6DBff', va='top', fontstyle='italic')

if args.outfile:
	fig.savefig(args.outfile,format='png',facecolor=fig.get_facecolor())
elif args.dumpall:
	pass
else:
	plt.show()
