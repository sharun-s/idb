import argparse,sys
import common
from locale import atof
import pandas as p
import matplotlib.pyplot as plt
#NB: tmp hack because of import common run from parent dir - idb/tn/fin$python3 -m district_banking.csv2g

parser = argparse.ArgumentParser(description='Aggregate Deposits Credit Grapher')
parser.add_argument('-csv', default="district_banking/districtwise_deposits_credit.csv",help='input csv file')
parser.add_argument('-pie', default=False, help='show only latest quarter districtwise', action='store_true')
parser.add_argument('-cdr', default=False, help='show credit deposit ratio districtwise', action='store_true')
parser.add_argument('-std', default=False, help='show deviation from avg cdr', action='store_true')
parser.add_argument('-logscale', default=False, help='show in logscale', action='store_true')
parser.add_argument('-south', default=True, help='plot Southern States total', action='store_false')
parser.add_argument('-india', default=True, help='plot all India total', action='store_false')

parser.add_argument('-dumpall',action="store_true", help='show all data dump all districts')
parser.add_argument('--outfile', help='output filename specify extn')
parser.add_argument('--type',default='deposit',help="deposit or credit")

args = parser.parse_args()
print(args)

alldata=p.read_csv(args.csv,skiprows=2)

depcol=[i for i in alldata.columns if i.find('Deposit') > -1]
credcol=[i for i in alldata.columns if i.find('Credit') > -1]
branchcol=[i for i in alldata.columns if i.find('Offices') > -1]

d=alldata[depcol].T
d.columns=alldata['District']
c=alldata[credcol].T
c.columns=alldata['District']
b=alldata[branchcol].T
b.columns=alldata['District']

if args.type == 'deposit':
	selected=d
	Title='Deposits'
	Key='Deposit'
else:
	selected=c
	Title='Credit'
	Key='Credit'

if args.pie:
	tot=common.format_indian(10000000.0*selected.loc['2020-21:Q1 '+Key]['Total'])
	#print(tot)
	#drop state total so it doesn't get plotted
	selected.drop('Total',axis=1,inplace=True)

	fig,ax=common.newfig('TN Districts - '+Title+' in Scheduled Banks - 2020')

	latest=selected.loc['2020-21:Q1 '+Key].T.sort_values(ascending=False)
	latestlabels=common.formatLabelAmts(latest)
	latest.plot(kind='pie',ax=ax,autopct='%1.1f%%',
		labels=latestlabels, #cmap=plt.get_cmap("Paired"),
		colors=common.get_regional_colors(latest), 
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
elif args.cdr:
	year='2020-21:Q1'
	fig,a = common.newfig('TN Districts CreditDeposit Ratio '+ year)
	alldata['cdr']=alldata[year+' Credit']/alldata[year+' Deposit'] * 100.0
	cdr=alldata['cdr']
	if args.std:
		alldata['cdrstd']=(cdr- cdr.mean())/cdr.std()
		alldata['colors'] = ['#cc3107' if x < 0 else '#22bb66' for x in alldata['cdrstd']]
		alldata.sort_values('cdrstd',inplace=True)
		alldata.reset_index(inplace=True)
		a.hlines(y=alldata.index, xmin=0, xmax=alldata.cdrstd, color=alldata.colors, linewidth=5)
	else:
		alldata['colors'] = ['#cc3107' if x < cdr.mean() else '#22bb66' for x in cdr]
		alldata.sort_values('cdr',inplace=True)
		alldata.reset_index(inplace=True)
		a.hlines(y=alldata.index, xmin=0, xmax=alldata.cdr, color=alldata.colors, linewidth=5)
	
	a.set_ylabel('$District$',color="#E6DB74")
	a.set_xlabel('$District Credit Deposit Ratio$' ,color="#E6DB74")
	#(STATE Total=)'+str(d[d['District']=='STATE'][year][0])

	#bbox_inches='tight'
	a.set_yticks(alldata.index)
	a.set_yticklabels(alldata.District.values)
	plt.grid(ax=a,linestyle='--', alpha=0.2)
	plt.tight_layout(ax=a)

else:
	if args.dumpall:
		for i in d.columns:
			fig,a=common.newfig(i+' - Deposits/Credit 2017-20')
			d[i].plot(ax=a, label="Deposits", legend=True, color='darkorange')
			c[i].plot(ax=a, label="Credit", legend=True, color='limegreen')
			a.invert_xaxis();
			a.set_ylabel('CRORES',color="#d6cB74")
			#print(dir(a.get_xticklabels()[2]))
			a.fill_between(range(0,13),d[i].values,c[i].values,where=d[i].values > c[i].values, facecolor='orange', alpha=0.4)
			a.fill_between(range(0,13),d[i].values,c[i].values,where=d[i].values < c[i].values, facecolor='limegreen', alpha=0.4)
			dlatest=d[i]['2020-21:Q1 Deposit']
			clatest=c[i]['2020-21:Q1 Credit']
			cdr=clatest/dlatest * 100.0
			a.annotate(f"{cdr:.2f}%", xy=(.9,clatest), xytext=(0,0), color='#d6cB74', 
				xycoords = a.get_yaxis_transform(), 
        		textcoords="offset points",
				size=15)
			a.set_xticklabels([xt.get_text().split(' ')[0] for xt in a.get_xticklabels() if xt])
			fig.savefig('deposits_credit_2017-2020'+i+'.png',format='png',facecolor=fig.get_facecolor())
	else:
		fig,ax=common.newfig('TN Districts - '+Title+' '+ selected.index[-1].replace(Key,'')[:4]+'-'+selected.index[0].replace(Key,'')[:4])
		selected.drop('Total',axis=1,inplace=True)
		if args.south:
			selected.drop('Southern Region',axis=1,inplace=True,errors='ignore')
		if args.india:
			selected.drop('All India',axis=1,inplace=True,errors='ignore')

		#if args.droptopN:
		selected.drop(['CHENNAI','COIMBATORE','KANCHEEPURAM'],axis=1,inplace=True)

		selected.plot(ax=ax,legend=False)
		if args.logscale:
			ax.set_yscale('log')
		ax.invert_xaxis()
		for line in ax.lines:
			y = line.get_ydata()[0]
			ax.annotate(line.get_label().title(), xy=(1,y), xytext=(0,0), color=line.get_color(), 
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
