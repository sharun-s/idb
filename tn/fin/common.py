import pandas as p
import sys,re,os
import subprocess
import shlex, locale
locale.setlocale(locale.LC_NUMERIC, '')
from locale import atof
from decimal import Decimal
import textwrap as tw
from os import listdir
import csv

# prevents text columns in dumped html getting trimmed
p.set_option('display.max_colwidth', -1)

def get_amounts(filename,dpcode):
	g=p.read_csv(filename)
	tmp=g[g['dpcode']==dpcode].index[0]
	head=g.ix[tmp]['head']
	idx=tmp
	while True:
		idx=idx+1
		try:
			if g.ix[idx]['head']==head:
				if g.ix[idx]['desc'].startswith('Total '+head): # maybe charged/voted or neither
					return g.ix[idx][['2018','2019Rev','2020Est']]
			if idx>tmp+60:
				return ['?','?','?']
		except Exception as e:
			print(f'{filename}:{dpcode}')
			raise e

def amt2flt(x):
	if x=='' or x=='nan' or x=='?':
		return 0
	return 1000*atof(x)

def fexp(number):
    (sign, digits, exponent) = Decimal(number).as_tuple()
    return len(digits) + exponent - 1

def fman(number):
    return Decimal(number).scaleb(-fexp(number)).normalize()

dept_map=p.read_csv('tn_dept2subdept_map',header=None)
#skipping error lines cause just interested in code to major head map, 3 col rows not reqd
func_map=p.read_csv('tn_func2dept_map',dtype=str,header=None,error_bad_lines=False,warn_bad_lines=False)


def format_indian(t):
	if t==0:
		return '--'
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
	    12:('Lk Cr',1), # 1 L cr
	    13:('Lk Cr',10)
	}
	ex=fexp(t)
	m=fman(t)
	return "{:.2f}".format(m*dic[ex][1])+" "+dic[ex][0]

def format_indian_cr(t):
	if t==0:
		return '--'
	dic = {
		1:('Cr',10),
	    2:('Cr',100),# 100 cr
	    3:('Cr',1000), # 1000 cr
	    4:('K Cr',10), # 10000 cr
	    5:('Lk Cr',1)#, # 10k cr
	    #6:('Lk Cr',1) # 1 L cr
	}
	ex=fexp(t)
	m=fman(t)
	#print(m,dic[ex][1],ex)
	return "{:.2f}".format(m*dic[ex][1])+" "+dic[ex][0]

import matplotlib.cm as cm
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
import pandas as p

norm = Normalize(vmin=0.0, vmax=4.0)

region=p.read_csv('gsdp/data/ddp-currentprices.csv',skiprows=2)
rmap=region[['District','Region']]
coldict={	
			'North':'violet',
			'West':'darkorange',
			'South':'green',
			'Chennai':'dodgerblue',
			'East':'crimson'
		}

#fill as and when spelling variations show up
disam={'tiruppur':'West',
'tirunelvali':'South',
'kanyakumari':'South',
'toothukudi':'South',
'sivaganga':'South',
'nagapattinam':'East',
'tiruvannamalai':'North',
'pudukkottai':'East',
'nilgiris':'West'
} 


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

def formatLabelAmts(data):
	#details={}
	labelandamt=[]
	cnt=0
	for k,j in data.items():
		cnt=cnt+1
		if cnt>10:
			labelandamt.append(k +' '+format_indian(j*10000000.0))
		else:
			labelandamt.append(k +'\n'+format_indian(j*10000000.0))
	return labelandamt

def get_regional_colors(data):
	colors=[]
	for i in data.index:
		if i.title() in rmap['District'].values:
			#colors.append(cm.Paired(norm(coldict[rmap[ rmap['District']==i.title()]['Region'].values[0]])))
			colors.append(coldict[rmap[ rmap['District']==i.title()]['Region'].values[0]])
		else:
			print(i.lower(),'not found using disam')
			colors.append(coldict[disam[i.lower()]])
	return colors

