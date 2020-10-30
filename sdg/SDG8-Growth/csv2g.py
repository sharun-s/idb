import pandas as p
import matplotlib.pyplot as plt
from locale import atof
import numpy as np
import json 

with open('national_sdg8.json') as f:
	national=json.load(f)
meta=p.read_csv(r'sdg8_meta.csv')
meta_idx=meta.Indicator.str.split(':').str[0].str.replace('.','')

ligo=['#0266B4','orange','tomato','green','pink']
pigo=["#00d0ff","#ffc107",'tomato','#00cc88','pink']
#names is added cause rows have variable number of vals, 5 is possible max if not update it.
df=p.read_csv(r'south_summary.csv',header=None,names = list(range(0,5)))

df['filename']=df[0].str.split(':').str[0]
df['state']=df[0].str.split(':').str[1]
df['indicator_no']=df['filename'].str.split('_').str[0]
df['indicator_name']=df['filename'].str.split('_').str[1].str.split('.').str[0]
df.drop(0,axis=1,inplace=True)
indi=df['indicator_name'].unique()
numofcols_nonnull=lambda d:len([col for col in [1,2,3,4] if d.loc[:, col].notna().any()])

def getYears(indicatorname):
	fname=df[df['indicator_name']==indicatorname].filename.unique()
	#print(fname[0])
	fdf=open(fname[0])
	l=fdf.readlines()[0]
	fdf.close()
	#print(l)
	#if l.find('Source')>-1:
	#	print(l)
	#	return l
	return l

def getFilename(indicatorname):
	fname=df[df['indicator_name']==indicatorname].filename.unique()
	print(fname[0])
	return fname[0].replace('csv','png')

def getMeta(indicator_no):
	idx=meta_idx[meta_idx==indicator_no].index[0]
	return meta.ix[idx]

def pad(bothsides=True):
	if bothsides:
		ax.set_xticks([xt for xt in range(0,cols+2)])
		if useYears:
			ax.set_xticklabels(['']+yrs[1:]+[''])
		else:
			ax.set_xticklabels(['']+tmp.columns.to_list()+[''])
	else:
		ax.set_xticks([.9]+[xt for xt in range(1,cols)]+[cols+.1])
		if useYears:
			ax.set_xticklabels(['']+yrs[1:]+[''])
		else:
			ax.set_xticklabels(['']+tmp.columns.to_list()+[''])

def styleLegend():
	l=ax.legend(loc='lower left', ncol=5, bbox_to_anchor=(-0.05, 1.01), frameon=False, facecolor='none')
	lc=0
	for text in l.get_texts():
		text.set_color(pigo[lc])#"#efdecc")
		lc=lc+1

kind='bar'
for i in indi:
	fig = plt.figure(facecolor="#001f3f",figsize=(8.,6.4))
	ax = fig.add_subplot(111, frameon=False)
	ax.set_facecolor("#002f4f")
	ax.set_alpha(0.1)
	ax.spines['bottom'].set_color('white')#'#ccc107')
	ax.spines['top'].set_color('white') 
	ax.spines['right'].set_color('white')
	ax.spines['left'].set_color('white')
	ax.tick_params(axis='y', colors='#E6DB74')#FD971F')
	ax.tick_params(axis='x', colors='#E6DB74')#001f3f
	#ax.set_xlim(0,175000)
	#ax.set_ylabel('',visible=False)

	tmp=df[df['indicator_name']==i]
	#print(tmp)
	mi=getMeta(tmp.indicator_no.unique()[0])
	#fig.suptitle(mi.Indicator,color="#E6DB74", fontsize=16)
	fig.suptitle(i,color="#E6DB74", fontsize=16)
	
	cols=numofcols_nonnull(tmp)
	if cols==1:
		kind='bar'
	else:
		kind='gbar'
	#print(cols)
	
	yrs=getYears(i).split(',')
	useYears=False
	if cols+1== len(yrs):
		useYears=True
		#print('Using years -',yrs)
	addPercToTickLabel=False
	if mi['Unit of Measurement'] == 'Percentage':
		addPercToTickLabel=True

	if useYears:
		plt.annotate('Data: '+','.join(yrs[1:]),
		(0.,1.), (0.,25), xycoords='axes fraction',
		color='#E6DBff', textcoords='offset points',va='top', fontstyle='italic')
	else:
		plt.annotate('Reference Period:'+ 
		' '.join(yrs),
		#str(mi['Data Reference Period'])+
		#' '+mi['Periodicity']+
		#'  Latest Data:'+str(mi['Latest Data Availability']),
		(0.,1.), (0.,25), xycoords='axes fraction',
		color='#E6DBff', textcoords='offset points',va='top', fontstyle='italic')


	colstoplot=list(range(1,cols+1))
	tmp=tmp[colstoplot+['state']].set_index('state')
	#print(tmp.dtypes)
	#convert obj cols to float - if already float dont convert
	for j in colstoplot:
		if tmp[j].dtypes == np.object:
			tmp[j]=tmp[j].apply(lambda x:atof(x) if x else None)
	#print(tmp.dtypes)
	if kind=='bar':
		#stmp=tmp[colstoplot].sort_values(ascending=True,by=[1])		
		#plt.xticks(x, tmp.index.to_list(), rotation='horizontal')
		#if addPercToTickLabel:
		ax.set_ylabel(mi['Unit of Measurement'],color="#d6cB74")
		#else:
		ax.set_xlabel('',visible=False)
		ax.bar(list(range(0,len(tmp.index))), height=tmp[1].to_list(), tick_label=tmp.index.to_list(), width=0.04, color=ligo)
		yticks = [int(t) for t in ax.get_yticks().tolist()] # get list of ticks
		#print(yticks)
		ly=len(yticks)-2
		#print(yticks[ly])
		for t in range(0,len(yticks)-2):
			yticks[t] = ''
		ax.set_yticks([yticks[ly]])	
		ax.set_yticklabels([yt for yt in yticks if yt])
		ax.set_xticklabels(tmp.index.to_list(), rotation=0)
	elif kind=='barh':
		ax.set_ylabel('',visible=False)
		ax.barh(list(range(0,len(tmp.index))), width=tmp[1].to_list(), tick_label=tmp.index.to_list(), height=0.04, color=ligo)
		xticks = [int(t) for t in ax.get_xticks().tolist()] 
		lx=len(xticks)-2
		for t in range(0,len(xticks)-2):
			xticks[t] = ''
		ax.set_xticks([xticks[lx]])
		ax.set_xticklabels([xt for xt in xticks if xt])
		ax.set_yticklabels(tmp.index.to_list(), rotation=0)
	elif kind=='line':
		#tmp[colstoplot].sort_index().T.plot(ax=ax,kind=kind,marker = 'o',linestyle=(0,(1,20)) , color=pigo, legend=False)
		sorttmp=tmp[colstoplot].sort_index().T
		sorttmp.plot(ax=ax,kind=kind,marker = 'o', linestyle='None',color=pigo, legend=False, clip_on=False)
		for line, name in zip(ax.lines, sorttmp.columns.to_list()):
			y = line.get_ydata()[-1]
			ax.annotate(name, xy=(1,y), xytext=(6,0), color=line.get_color(), 
                xycoords = ax.get_yaxis_transform(), textcoords="offset points",
                size=12, va="center")
		ax.set_ylabel(mi['Unit of Measurement'],color="#d6cB74")
		pad(False)
	else:
		# grouped bar
		sorttmp=tmp[colstoplot].sort_index()
		#print(sorttmp)
		ax.set_ylabel(mi['Unit of Measurement'],color="#d6cB74")
		ax.set_xlabel('',visible=False)
		#sorttmp.plot(ax=ax,kind='bar')
		x = range(0,len(sorttmp.columns))  # the label locations
		width = 0.1
		idx=0
		for si in sorttmp.index:
			#print(sorttmp.ix[si].values)
			#print([idx+(xx*width) for xx in x])
			ax.bar([idx+(xx*width) for xx in x], height=sorttmp.ix[si].values, width=0.1, color=ligo[idx])
			idx=idx+1
		ax.set_xticks(range(0,len(sorttmp.index)))
		ax.tick_params(axis='x', colors='#001f3f')
		ax.set_xticklabels(sorttmp.index.to_list(), rotation=0, color="#E6DB74")

	plt.annotate(mi.Source+'\n'+str(mi.url), (0.,0), (0, -25), 
		xycoords='axes fraction', textcoords='offset points', 
		color='#E6DBff', va='top', fontstyle='italic')#, fontsize=14)
	#plt.annotate(mi['Target'], (-.3,0), (-1, -160), xycoords='axes fraction', textcoords='offset points', color="#bbbB74", fontsize=16)
	#plt.annotate(mi['Desc'],(-1.,-0.2), (0, 0), xycoords='axes fraction', textcoords='offset points', color="#E6DB74", fontsize=16)
	
	prefix=''
	#if kind=='bar':
	#	prefix='b_'
	fig.savefig(r'viz/'+prefix+getFilename(i),format='png',facecolor=fig.get_facecolor(), bbox_inches='tight')

