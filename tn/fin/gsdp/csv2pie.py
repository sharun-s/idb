import pandas as p
import matplotlib.pyplot as plt

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
		t.set_color("#efdecc")
	y=ax.get_yaxis()
	y.label.set_visible(False)
	
df=p.read_csv('data/TamilNadu_GSDP_27-08-2020.csv',comment="#")
Sectors=df[df['Head'].isna()].iloc[:,2:].set_index('Desc').T
SubSectors=df[df['Subhead'].isna()].iloc[:14,2:].set_index('Desc').T
SubSectors.columns=['Agriculture, forestry, fishing', 'Mining','Primary',
       'Manufacturing','Electricity, gas, water supply & utility','Construction','Secondary', 
       'Trade, repair, hotels','Transport, storage, broadcasting','Finance','Real estate','Public administration', 'Other','Tertiary'
       ]

for i in Sectors.index:
	fig,ax = newfig(i)
	w=Sectors.loc[i].plot(kind='pie',autopct='%1.1f%%',radius=.7,wedgeprops=dict(width=0.3, edgecolor='w'))
	cleanup_pie(w)
	cols = ['Agriculture, forestry, fishing', 'Mining',
       'Manufacturing','Electricity, gas, water supply & utility','Construction', 
       'Trade, repair, hotels','Transport, storage, broadcasting','Finance','Real estate','Public administration', 'Other']
	w=SubSectors.loc[i][cols].plot(kind='pie',radius=1,wedgeprops=dict(width=0.3, edgecolor='w'))
	cleanup_pie(w)
	
	fig.savefig(i+'.png',format='png',facecolor=fig.get_facecolor())
