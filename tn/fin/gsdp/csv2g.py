import pandas as p
import matplotlib.pyplot as plt
import common

#NB: tmp hack because of import common run from parent dir - idb/tn/fin$python3 -m gsdp.csv2g

def newfig(title):
	fig = plt.figure(facecolor="#001f3f",figsize=(7.2,7.2))
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

# color inner and outer labels differently
def cleanup_pie(ax):
	for t in ax.texts:
		if t.get_text().find('%') > -1:
			t.set_color('#001f3f')
		else:
			t.set_color("#00efde")#efdecc")
	y=ax.get_yaxis()
	y.label.set_visible(False)


df=p.read_csv('gsdp/data/TamilNadu_GSDP_27-08-2020.csv',comment="#")
SectorsByYear=df[df['Head'].isna()].iloc[:,2:].set_index('Desc').T
SubSectorsByYear=df[df['Subhead'].isna()].iloc[:14,2:].set_index('Desc').T
SubSectorsByYear.drop(['Primary','Secondary','Tertiary'],axis=1,inplace=True)
#rename cols to make labels smaller
SubSectorsByYear.columns=['Agriculture Forestry Fishing', 'Mining',#'Primary',
    'Manufacturing','Electricity Gas Water & utility','Construction',#'Secondary', 
    'Trade Repair Hotels','Transport Storage Broadcasting','Finance','Real Estate','Public Administration', 'Other'#,'Tertiary'
]

#cmap = plt.get_cmap("tab20")
outer_colors = [#"#88ff44",
				'#00fd88',"#ffc107",'#ff2244']#,
inner_colors = [#"#44ff44","#00ff33",
				'#00fe66','#00cc55',
				'#f8b414','#ffcc33','#feab88',
				"#F92672","#dd3377",'#bb3377',"#bb4488",'#ee88c1','#AE81aa'
				]

def addGDPCalculationText(ax, year):
	tot=common.format_indian(100000.0*df.iloc[27][year])
	tax=common.format_indian(100000.0*df.iloc[28][year])
	subsidy=common.format_indian(100000.0*df.iloc[29][year])
	gsdp=common.format_indian(100000.0*df.iloc[30][year])
	
	#ax.plot([.5,.5],[1,1],".")
	ax.annotate('GVA', xytext=(.05,.9), xycoords='figure fraction', xy=(.45,.51), 
		arrowprops={'arrowstyle':"<-",'ec':'w','connectionstyle':"angle,angleA=-90,angleB=180,rad=0"}, 
		color='white')
	ax.annotate('+(Tax) '+tax, xycoords='figure fraction', xy=(.12,.9), color='white')
	ax.annotate('-(Subsidy) '+subsidy, xycoords='figure fraction', xy=(.33,.9), color='white')
	ax.annotate('= '+gsdp + ' (State GDP)', xycoords='figure fraction', xy=(.56,.9), fontsize=12, fontweight='heavy', 
		color='white')
	ax.annotate(tot + '\n\n'+ year, xycoords='figure fraction', xy=(.45,.48), fontweight='bold', 
		color='white')

def formatData(data):
	details={}
	for i in data.index:
		labelandamt=[ k +'\n'+common.format_indian(j*100000.0) for k,j in data.loc[i].items() ]
		#tot=common.format_indian(sum(i*100000.0 for i in data.loc[i].values))
		details[i]=labelandamt
	return details

details=formatData(SectorsByYear)
subdetails=formatData(SubSectorsByYear)

years=SectorsByYear.index

for year in years:
	fig,ax = newfig('Tamil Nadu GDP')
	w=SectorsByYear.loc[year].plot.pie(labels=details[year],#autopct='%1.1f%%'
		radius=.55, 
		colors=outer_colors, wedgeprops=dict(width=0.2))
	#cleanup_pie(w)

	w=SubSectorsByYear.loc[year].plot.pie(labels=subdetails[year],radius=1, colors=inner_colors,
		wedgeprops=dict(width=0.1, edgecolor='white'))
	cleanup_pie(w)

	addGDPCalculationText(w, year)
	plt.annotate('Data:http://mospi.nic.in/GSVA-NSVA', (0.,0), (0, -25), 
                xycoords='axes fraction', textcoords='offset points', 
                color='#E6DBff', va='top', fontstyle='italic')
	#plt.tight_layout()
	fig.savefig('gsdp/s-'+year+'.png',format='png',facecolor=fig.get_facecolor())
