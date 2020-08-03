#!/usr/bin/env python3
#To turn on revenue code autocompletion on shell
#complete -W "`find data/revenue/*.csv -printf "%f "| tr -d ".csv"`" ./summary.py

import sys
import pandas as p
import subprocess
import shlex, locale
from locale import atof
locale.setlocale(locale.LC_NUMERIC, '')
from decimal import Decimal
import textwrap as tw
from os import listdir
import csv

# prevents text columns in dumped html getting trimmed
p.set_option('display.max_colwidth', -1)

def fexp(number):
    (sign, digits, exponent) = Decimal(number).as_tuple()
    return len(digits) + exponent - 1

def fman(number):
    return Decimal(number).scaleb(-fexp(number)).normalize()


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
	    12:('Lk Cr',1) # 1 L cr
	}
	ex=fexp(t)
	m=fman(t)
	return "{:.2f}".format(m*dic[ex][1])+" "+dic[ex][0]

def parseResults(o):
	d=[]
	v=[]
	totamt=0
	y=o.stdout.splitlines()
	for i in csv.reader(y):
		demand=i[0].split('.')[0].split('/')[-1]
		if len(demand)==2 or len(demand)==1: # hack: skips files not matching format xx.csv or x.csv
			d.append(dept_map[dept_map[0] == int(demand)].iloc[0][2])
			for amt in i[2:3]:
				if amt !='':
					v.append(format_indian(1000*atof(amt)))
					totamt=totamt+atof(amt)  
				else: 
					v.append('-')
		else:
			head=i[0].split(':')[1]
			#print(i, head, i[1])
			if len(head)==2 and head.isupper():
				d.append(i[1])
				v.append('-')

	return (d,v,totamt)

def parseHistory(o):
	v=[]
	for i in csv.reader(o.stdout.splitlines()):
		#print(i)
		for amt in i[2:]:
			if amt !='':
				try:
					v.append(format_indian(100000*atof(amt)))
				except ValueError as e:
					v.append('xx')  
			else: 
				v.append('-')
	return ",".join(v)

def highlight(x):
    return ['font-weight: bold' for v in x]

def pp(d,v,ftitle,titleStr):
	with open(f'func_explorer/{ftitle}-depts.html','w') as f:
		f.write('<body style="font-family:verdana,sans-serif;">')
		f.write(f'<br>--{titleStr}<br>')
		dk=p.DataFrame(v,index=[i.title() for i in d])
		f.write(dk.to_html(header=False,border=0,bold_rows=False))
		f.write('</body>')

def ppIncomeByDepts(detailsfile):
	#Find all sub depts generating income
	o=subprocess.run(r"cat "+ shlex.quote(detailsfile.strip()) + ' | jq -r \'paths as $p|getpath($p) | select(scalars)| ($p | map(select(type=="string"))) + [.]|@csv\'' + r"| grep '\[.*\]\",\"Total'  | grep 2018 " ,shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	rows=[]
	for i in csv.reader(o.stdout.splitlines()):
		rows.append([i[2],i[5]])
	df=p.DataFrame(rows)
	#print(rows)
	df[[0,2]]=df[0].str.split('[',expand=True)
	df[2]=df[2].str.replace(']','')
	m={}
	for dept in df[2].unique():
		d=dept_map[dept_map[0] == int(dept[:2])]			
		subdept=dept[2:]
		if subdept.startswith('0'):
			subdept=subdept[1]
		m[dept]=d[d[1] == int(subdept)][2].iloc[0]
	df.columns=['head','amt','code']
	df['subdept']=df['code'].apply(lambda x:m[x])
	with open(f'func_explorer/{rev_head}-depts.html','w') as f:
		f.write('<body style="font-family:verdana,sans-serif;">')
		f.write(f'<br>--Income Sources (Revenue)<br>')
		f.write(df.to_html(index=False,border=0,columns=['head','amt','subdept']))
		f.write('</body>')	

def SubDeptsBreakup(titleStr, head):
	#note this catches head at start of line only
	#o=subprocess.run(r"grep -Ir '^"+head+"' data/expenditure --exclude-dir=tmp",shell=True, stdout=subprocess.PIPE, universal_newlines=True)	
	#this catches head anywhere - esp all occurrences within dpcode
	o=subprocess.run(r"grep -Ir '"+head+"' data/expenditure --exclude-dir=tmp",shell=True, stdout=subprocess.PIPE, universal_newlines=True)	
	d,v,ta=parseResults(o)
	pp(d,v,head,titleStr)
	#print(f'<b>{format_indian(ta*1000)}</b>')

dept_map=p.read_csv('tn_function_dept_map',header=None)
rev_head=None
if int(sys.argv[1][0])%2 == 0:
	rev_head='0'+sys.argv[1][1:]
	revex_head='2'+sys.argv[1][1:]
	capex_head='4'+sys.argv[1][1:]
	loan_head='6'+sys.argv[1][1:]
if int(sys.argv[1][0])%2==1:
	rev_head='1'+sys.argv[1][1:]
	revex_head='3'+sys.argv[1][1:]
	capex_head='5'+sys.argv[1][1:]
	loan_head='7'+sys.argv[1][1:]
# todo handle 8 ? 


#if len(sys.argv) > 2:
#	if sys.argv[2] == 'Expenditure':
SubDeptsBreakup("Expenditure day to day (revex)", revex_head)

#	if sys.argv[2] == 'Investment':
SubDeptsBreakup('Investments (capex)',capex_head)

#	if sys.argv[2] == 'Loans':
SubDeptsBreakup('Loans',loan_head)
#else:
o=subprocess.run( ['ls -1 data/revenue/breakup/'+rev_head+'*'],shell=True, stdout=subprocess.PIPE, universal_newlines=True)
ppIncomeByDepts(o.stdout)

