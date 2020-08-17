import matplotlib.pyplot as plt
import sys,locale,re
import pandas as p
from itertools import cycle
from locale import atof
from matplotlib.sankey import Sankey
locale.setlocale(locale.LC_NUMERIC, '')
from decimal import Decimal
import textwrap as tw
from os import listdir

def fexp(number):
    (sign, digits, exponent) = Decimal(number).as_tuple()
    return len(digits) + exponent - 1

def fman(number):
    return Decimal(number).scaleb(-fexp(number)).normalize()


def format_indian(t):
	dic = {
		3:('K',1),
	    4:('K',10), 
	    5:('Lak',1),
	    6:('Lak',10),
	    7:('Cr',1),
	    8:('Cr',10),# 10 cr
	    9:('Cr',100), # 100 cr
	    10:('K Cr',1), # 1000 cr
	    11:('K Cr',10), # 10k cr
	    12:('Lk Cr',1) # 1 L cr
	}
	ex=fexp(t)
	m=fman(t)
	return "{:.2f}".format(m*dic[ex][1])+" "+dic[ex][0]

COLUMN_TO_PLOT=2
flat=False # false produces a forest true produces fallen trees
# When long labels have to be fit between branches either set this option to True or increase gap parameter of Sankey
alternateLeaves=False

titlemap=p.read_csv('demand_dept.csv')

allfiles=listdir('.')
csv=[str(i)+'.csv' for i in range(10,55)][:int(sys.argv[1])]
fig = plt.figure(facecolor="#001f3f",figsize=(12,16))
#fig.suptitle(title.replace('"','').capitalize(), color="#00efde", fontsize=12)
title=''
ax = fig.add_subplot(111, frameon=False)
ax.set_facecolor("#002f4f")
ax.set_alpha(0.1)
ax.spines['bottom'].set_color('white')#'#ccc107')
ax.spines['top'].set_color('white') 
ax.spines['right'].set_color('white')
ax.spines['left'].set_color('white')
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
sk=Sankey(ax=ax,head_angle=90, scale=0.000000001, offset=0.25, shoulder=0., margin=0,gap=.45)
sink=[]
sinklabel=[]
skippedfiles=0
try:
	for c in csv:
		df=p.read_csv(c,comment='#',header=None)
		code=c.replace('.csv','')
		title=titlemap[titlemap['h']==int(code)]['dept'].item().partition('(')[0].strip()
		df[COLUMN_TO_PLOT]=df[COLUMN_TO_PLOT].apply(lambda x:str(x).replace('- ','-')).apply(lambda x:atof(x) if x!='nan' else 0)
		df=df[df[COLUMN_TO_PLOT]!=0.0]
		df.set_index(1,inplace=True)
		results=df.sort_values(by=COLUMN_TO_PLOT,ascending=True)
		if all([True if r==0 else False for r in results[COLUMN_TO_PLOT]]):
			#print("skipping",c)
			skippedfiles=skippedfiles+1
			continue
		sink.append(-1*df[COLUMN_TO_PLOT].sum())
		sinklabel.append(title.replace('"','').title())
	#print(sink+[-1*sum(sink)])
	sk.add(
		#pathlengths=[100]*results.values,
	    flows=sink+[-1*sum(sink)],
		labels=['']*len(sinklabel)+[format_indian(-1000*sum(sink))], 
		orientations=[1.]*len(sink) + [-1.],
		color="#027368",rotation=270)
	cnt=0
	for c in csv:
		#with open(c) as f:
		#	line=f.readline()
		#	title=line.split(',')[1].strip().replace('"','').title()
		#	code=line.split(',')[0][1:].strip()
		#title=titlemap['h']=code
		
		df=p.read_csv(c,comment='#',header=None)
		df[COLUMN_TO_PLOT]=df[COLUMN_TO_PLOT].apply(lambda x:str(x).replace('- ','-')).apply(lambda x:atof(x) if x!='nan' else 0)
		df=df[df[COLUMN_TO_PLOT]!=0.0]# drop all empty rows
		df.set_index(1,inplace=True)
		results=df.sort_values(by=COLUMN_TO_PLOT,ascending=True)
		if all([True if r==0 else False for r in results[COLUMN_TO_PLOT]]):
			#print("skipping",c)
			#hack - this test shld really be run at the begining. i.e. start processing only if last file in csv list has values
			if cnt+1==len(csv):
				# file is empty AND final one in list so no point saving image
				sys.exit()
			continue 
		#vals being added to labels so actual vals coming from flow which get displayed but hard to edit can be hidden
		vals=[]
		v=results[COLUMN_TO_PLOT].tolist()
		vcnt=0
		for i in results.index:
			vals.append(i+' '+format_indian(1000*v[vcnt]))
			vcnt=vcnt+1
		if flat==True:
			orios=[1. if i > 0 else 1. for i in results[COLUMN_TO_PLOT].values]+[-1.]
		else:
			if alternateLeaves:
				ct=cycle([-1.,1.])
				orios=[next(ct) if i > 0 else -1. for i in results[COLUMN_TO_PLOT].values]+[0.]
			else:
				orios=[-1. if i > 0 else -1. for i in results[COLUMN_TO_PLOT].values]+[0.]
		if cnt==len(csv)-1-skippedfiles:
			alpha=1
		else:
			alpha=.6
		sk.add(
		    flows=[-1*k for k in v] + [1*df[COLUMN_TO_PLOT].sum()],
			labels=vals+[''],
			orientations=orios,
			#color="#ddcc33",
			color="#027368",
			facecolor="#ffc107",
			alpha=alpha, prior=0, connect=(cnt, len(results)))
		cnt=cnt+1
	dia=sk.finish()
	#print([i.tips for i in dia])
	for i in dia[0].texts[:-1]:
		i.set_text('') # totals at joins hide them
	# handle total formating
	t=dia[0].texts[-1]
	text = t.get_text()
	pos=text.find('\n')
	if pos > -1:
		explabel='Expenditure '+text[:pos]
		t.set_text('')#(explabel)
		#t.set_color('#ffcc33')	
	#hide all intermediate text
	#for i in dia[1:-1]:
	for i in dia:
		for t in i.texts:
			t.set_text('')
	#in the final dia
	c=cycle(['right','left'])
	for t in dia[-1].texts:
		t.set_color('#ffcc33')
		if alternateLeaves:
			# alternateLeaves creates more space between label so fontsize can be larger
			t.set_fontsize(10)
		else:
			t.set_fontsize(8)
		text=t.get_text()
		pos=text.find('\n')
		if pos > -1:
			if not flat:
				negative=re.search(r'\-\d+',text[:pos])
				#print(text)
				#t.set_text(tw.fill(tw.dedent(text[:pos]),50).title())
				if alternateLeaves:
					if negative !=None:
						#print('negative',text)
						t.set_ha('right')
						#next(c)
					else:
						t.set_ha(next(c))
				else:
					t.set_ha('right')
				t.set_wrap('True')
			else:
				pass
				#t.set_text(tw.fill(tw.dedent(text[:pos]),10).title())
		else:
			pass
			#t.set_text(tw.fill(tw.dedent(text),15).title())
		t.set_wrap(True)
	#hide join total val
	dia[-1].texts[-1].set_text('')
	xl,yl=dia[0].tips[-1]	
	#plt.text(0.8, 0.1,title+' ['+code+']', color='#E6DB74', fontsize=14, ha='center', va='center', transform=ax.transAxes, wrap=True)
	plt.text(xl, yl,explabel, color='#ffc107', fontsize=16, ha='left', va='center', wrap=True)
	cnt=0
	for tp in dia[0].tips[:-1]:
		xl,yl=tp
		plt.text(xl, yl, sinklabel[cnt].replace('Department','')[:30], color='#f89909', fontsize=12, ha='left', va='bottom'
			)
		cnt=cnt+1

	fig.savefig('big_'+sys.argv[1]+'.png',format='png',facecolor=fig.get_facecolor())
except Exception as e:
	print("error in ",c)
	raise e
