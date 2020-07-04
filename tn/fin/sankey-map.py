import matplotlib.pyplot as plt
from matplotlib import transforms
import sys,locale,re
from pprint import pprint
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

def format_hack(l,v):
	vcnt=0
	vals=[]
	for i in l:
		vals.append(i+' '+format_indian(v[vcnt]))
		vcnt=vcnt+1
	return (l,vals)

flat=False # false produces a forest true produces fallen trees
# When long labels have to be fit between branches either set this option to True or increase gap parameter of Sankey
alternateLeaves=False
fig = plt.figure(facecolor="#001f3f",figsize=(12,6))
fig.suptitle('Map of Income, Expense, Loans Flows of TN Govt', color="#00efde", fontsize=12)
title=''
ax = fig.add_subplot(111, frameon=False)
ax.set_facecolor("#002f4f")
#ax.get_xaxis().set_visible(False)
#ax.get_yaxis().set_visible(False)

sk=Sankey(ax=ax,head_angle=270, scale=0.000000001, unit=None,
	offset=0.25, shoulder=0., margin=2.,gap=.45)

sk.add(
	flows=[-607286000,-24533000,-11000000,-111020000,-77324000,-273250000,-51857000,1156270000],
	labels=['d1','d1', 'd1','d2','d2','d2', 'd2','T'],
	orientations=[1,1,1,1,1,1,1,0])

#d1 financials
d=([607286000,24533000,11000000,-631868000],
	['2011 State Legis', '2059 Public Works', 
		#'2235 Social Security and Welfare', 
		'7610 Loan to Govt Servants','Total'])
fd=format_hack(d[1],d[0])
d2=([111020000,77324000,273250000,51857000,-514066000],
	['2012 Governor', '2013 Council of Ministers', 
		'2052 Secretariat - General Services', 
		'2059 Public Works','Total'])
fd2=format_hack(d2[1],d2[0])


sk.add(flows=d[0],
		labels=fd[1], 
		orientations=[1,1,1,0],
		color="#027368", prior=0,connect=(0,0))

#d1 depts
sk.add(patchlabel='State Legislature',
	flows=[631868000,-631868000],
	labels=['', ''],
	orientations=[1,-1],
	prior=1,connect=[3,0])

offset = transforms.ScaledTranslation(3., 0.0, fig.dpi_scale_trans)
new_transform = ax.transData + offset

sk.add(flows=d2[0],
		labels=fd2[1], 
		orientations=[1,1,1,1,0],
		color="#027368", prior=0,connect=(3,0))#, transform=new_transform)

#d2 depts
sk.add(
	flows=[514066000,-30410000,-133056000,-350600000],
	labels=['','Gov Sec', 'Gov House','C o M'],
	orientations=[1,-1,-1,-1],
	prior=3,connect=[4,0])#, transform=new_transform)



dia=sk.finish()
#for i in dia:
#	i.texts[-1].set_text('') # totals at joins hide them
#	# handle total formating

for i in dia:
	i.text.set_color('#dddd88')
	x,y=i.text.get_position()
	i.text.set_position((x,y+.35))
#t=dia[0].texts[-1]
#text = t.get_text()
#pos=text.find('\n')
#if pos > -1:
#	t.set_text(text[:pos]+'\n TOTAL REVENUE')
#	t.set_color('#ffcc33')	
#hide all intermediate text
for i in dia[1:-1]:
	for t in i.texts:
		t.set_text('')
#in the final dia
c=cycle(['left','right'])
for t in dia[0].texts:
	t.set_color('#ffcc33')
	# if alternateLeaves:
	# 	# alternateLeaves creates more space between label so fontsize can be larger
	# 	t.set_fontsize(10)
	# else:
	# 	t.set_fontsize(8)
	text=t.get_text()
	pos=text.find('\n')
	if pos > -1:
		if not flat:
			negative=re.search(r'\-\d+',text[:pos])
			#print(text)
			t.set_text(tw.fill(tw.dedent(text[:pos]),50).title())
			if alternateLeaves:
				if negative !=None:
					print('negative',text)
					t.set_ha('left')
					#next(c)
				else:
					t.set_ha(next(c))
			else:
				t.set_ha('left')
			t.set_wrap('True')
		else:
			t.set_text(tw.fill(tw.dedent(text[:pos]),10).title())
	else:
		t.set_text(tw.fill(tw.dedent(text),15).title())
	t.set_wrap(True)
#hide join total val
#dia[-1].texts[-1].set_text('')	

fig.savefig('map.png',format='png',facecolor=fig.get_facecolor())