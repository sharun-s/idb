import pandas as p
import matplotlib.pyplot as plt
from locale import atof
import numpy as np
#names is added cause rows have variable number of vals, 5 is possible max if not update it.
df=p.read_csv(r'south_summary.csv',header=None,names = list(range(0,5)))

df['filename']=df[0].str.split(':').str[0]
df['state']=df[0].str.split(':').str[1]
df['indicator_no']=df['filename'].str.split('_').str[0]
df['indicator_name']=df['filename'].str.split('_').str[1].str.split('.').str[0]
df.drop(0,axis=1,inplace=True)
indi=df['indicator_name'].unique()
numofcols_nonnull=lambda d:d[[1,2,3,4]].isnull().sum().value_counts(0)[0]

def getSource(indicatorname):
	fname=df[df['indicator_name']==indicatorname].filename.unique()
	print(fname[0])
	fdf=open(fname[0])
	l=fdf.readlines()[-1]
	fdf.close()
	if l.find('Source')>-1:
		print(i,l)
		return l
	return ''

def getFilename(indicatorname):
	fname=df[df['indicator_name']==indicatorname].filename.unique()
	print(fname[0])
	return fname[0].replace('csv','png')
kind='bar'
for i in indi:
	fig = plt.figure(facecolor="#001f3f",figsize=(8.,6.4))
	fig.suptitle('Southern States '+i, x=0.35,color="#E6DB74", fontsize=16)
	ax = fig.add_subplot(111, frameon=False)
	ax.set_facecolor("#002f4f")
	ax.set_alpha(0.1)
	ax.spines['bottom'].set_color('white')#'#ccc107')
	ax.spines['top'].set_color('white') 
	ax.spines['right'].set_color('white')
	ax.spines['left'].set_color('white')
	ax.tick_params(axis='y', colors='#E6DB74')#FD971F')
	ax.tick_params(axis='x', colors='#E6DB74')
	#ax.set_xlim(0,175000)
	ax.set_ylabel('',visible=False)

	tmp=df[df['indicator_name']==i]
	print(tmp)
	cols=numofcols_nonnull(tmp)
	if cols==1:
		kind='bar'
	else:
		kind='line'
	print(cols)
	print(getSource(i))
	colstoplot=list(range(1,cols+1))
	tmp=tmp[colstoplot+['state']].set_index('state')
	print(tmp.dtypes)
	#convert obj cols to float - if already float dont convert
	for j in colstoplot:
		if tmp[j].dtypes == np.object:
			tmp[j]=tmp[j].apply(lambda x:atof(x) if x else None)
	print(tmp.dtypes)
	if kind=='bar':
		#stmp=tmp[colstoplot].sort_values(ascending=True,by=[1])		
		#plt.xticks(x, tmp.index.to_list(), rotation='horizontal')
		ax.set_xlabel('',visible=False)
		ax.bar(list(range(0,len(tmp.index))), height=tmp[1].to_list(), tick_label=tmp.index.to_list(), width=0.04, color=['#0266B4','orange','tomato','green','pink'])
		yticks = [int(t) for t in ax.get_yticks().tolist()] # get list of ticks
		print(yticks)
		ly=len(yticks)-2
		print(yticks[ly])
		for t in range(0,len(yticks)-2):
			yticks[t] = ''
		ax.set_yticks([yticks[ly]])
		ax.set_yticklabels([yt for yt in yticks if yt])
		
		
		ax.set_xticklabels(tmp.index.to_list(), rotation=0)
	else:
		tmp[colstoplot].sort_index().T.plot(ax=ax,kind=kind)
	plt.annotate(getSource(i).replace(',',''), (0.,0), (0, -25), xycoords='axes fraction', textcoords='offset points', color='#E6DBff', va='top', fontstyle='italic')
	prefix=''
	if kind=='bar':
		prefix='b_'
	fig.savefig(r'viz/'+prefix+getFilename(i),format='png',facecolor=fig.get_facecolor())

