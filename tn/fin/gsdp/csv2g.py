import pandas as p
import matplotlib.pyplot as plt
import common

#NB: tmp hack because of import common run from parent dir - idb/tn/fin$python3 -m gsdp.csv2g

def newfig(title):
	fig = plt.figure(facecolor="#001f3f")#,figsize=(8.,6.4))
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
	return fig,ax

def cleanup_pie(ax):
	for t in ax.texts:
		if t.get_text().find('%') > -1:
			t.set_color('#001f3f')
		else:
			t.set_color("#00efde")#efdecc")
	y=ax.get_yaxis()
	y.label.set_visible(False)


df=p.read_csv('gsdp/data/TamilNadu_GSDP_27-08-2020.csv',comment="#")
Sectors=df[df['Head'].isna()].iloc[:,2:].set_index('Desc').T
SubSectors=df[df['Subhead'].isna()].iloc[:14,2:].set_index('Desc').T
SubSectors.columns=['Agriculture, forestry, fishing', 'Mining','Primary',
       'Manufacturing','Electricity, gas, water supply & utility','Construction','Secondary', 
       'Trade, repair, hotels','Transport, storage, broadcasting','Finance','Real estate','Public administration', 'Other','Tertiary'
       ]

for i in Sectors.index:
	fig,ax = newfig('TN GDP ' + str(i))
	q=[ k +'\n'+common.format_indian(j*100000.0) for k,j in Sectors.loc[i].items() ]
	tot=common.format_indian(sum(i*100000.0 for i in Sectors.loc[i].values))
	w=Sectors.loc[i].plot.pie(labels=q,autopct='%1.1f%%',wedgeprops=dict(width=0.6))
	#w=Sectors.loc[i].plot(kind='pie',autopct='%1.1f%%',radius=.7,wedgeprops=dict(width=0.3, edgecolor='w'))
	cleanup_pie(w)
	tax=common.format_indian(100000.0*df.iloc[28][i])
	subsidy=common.format_indian(100000.0*df.iloc[29][i])
	gsdp=common.format_indian(100000.0*df.iloc[30][i])
	w.annotate('GVA', xytext=(.05,.5), xycoords='figure fraction', xy=(.45,.51), 
		arrowprops={'arrowstyle':'<-','ec':'w'}, 
		color='white')
	w.annotate('+(Tax) '+tax, xycoords='figure fraction', xy=(.051,.4), color='white')
	w.annotate('-(Subsidy) '+subsidy, xycoords='figure fraction', xy=(.051,.3), color='white')
	w.annotate('= '+gsdp + '\n(State GDP)', xycoords='figure fraction', xy=(.051,.17), fontsize=12, fontweight='heavy', 
		color='#00effe')
	w.annotate(tot, xycoords='figure fraction', xy=(.45,.5), fontweight='bold', color='white')
	# cols = ['Agriculture, forestry, fishing', 'Mining',
 #       'Manufacturing','Electricity, gas, water supply & utility','Construction', 
 #       'Trade, repair, hotels','Transport, storage, broadcasting','Finance','Real estate','Public administration', 'Other']
	# w=SubSectors.loc[i][cols].plot(kind='pie',radius=1,wedgeprops=dict(width=0.3, edgecolor='w'))
	# cleanup_pie(w)
	
	fig.savefig('gsdp/s-'+i+'.png',format='png',facecolor=fig.get_facecolor())
