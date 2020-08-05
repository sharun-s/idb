#!/usr/bin/env python3
# generates files in loan_explorer, investment_explorer, expense_explorer, income_explorer
# for income json breakup details file is parsed for sub head [A-Z][A-Z]
# for revex,capex,loan simple grep of the functional head across all demand files
# generates indexes - loan_index capex_index revex_index 


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

def ppIncomeByDepts(detailsfile,head):
	#Find all sub depts generating income
	o=subprocess.run(r"cat "+ shlex.quote(detailsfile.strip()) + ' | jq -r \'paths as $p|getpath($p) | select(scalars)| ($p | map(select(type=="string"))) + [.]|@csv\'' + r"| grep '\[.*\]\",\"Total'  | grep 2018 " ,shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	rows=[]
	for i in csv.reader(o.stdout.splitlines()):
		rows.append([i[2],i[5]])
	df=p.DataFrame(rows)
	#print(rows,file=sys.stderr)
	try:
		df[[0,2]]=df[0].str.split('[',expand=True)
		df[2]=df[2].str.replace(']','')
	except ValueError as e:
		print(f'check {detailsfile.strip()} - dept subdept code not found - probably no Income')
		return
	
	m={}
	for dept in df[2].unique():
		d=dept_map[dept_map[0] == int(dept[:2])]			
		subdept=dept[2:]
		if subdept.startswith('0'):
			subdept=subdept[1]
		m[dept]=d[d[1] == int(subdept)][2].iloc[0]
	df.columns=['head','amt','code']
	df['subdept']=df['code'].apply(lambda x:m[x])
	with open(f'income_explorer/{head}.html','w') as f:
		f.write('<body style="font-family:verdana,sans-serif;">')
		f.write(f'<br>--Income Sources (Revenue)<br>')
		f.write(df.to_html(index=False,border=0,columns=['head','amt','subdept']))
		f.write('</body>')	

def parseResults(o):
	d=[]
	v=[]
	totamt=0
	y=o.stdout.splitlines()
	for i in csv.reader(y):
		demand=i[0].split('.')[0].split('/')[-1]
		v=[]
		if len(demand)==2 or len(demand)==1: # hack: skips files not matching format xx.csv or x.csv
			v.append(dept_map[dept_map[0] == int(demand)].iloc[0][2])
			for amt in i[2:3]:
				if amt !='':
					v.append(format_indian(1000*atof(amt)))
					totamt=totamt+atof(amt)  
				else: 
					v.append('-')
			d.append(v)
		else:
			head=i[0].split(':')[1]
			subdeptname=i[0].split(':')[0].split('/')[-1].replace('.csv','')
			dept=subdeptname.split('-')[0]
			#print(i, head, i[1])
			if len(head)==2 and head.isupper():
				d.append([i[1],subdeptname.split('-')[1],dept])
				v.append('-')

	return (d,v,totamt)

def highlight(x):
    return ['font-weight: bold' for v in x]

def pp(d,v,ftitle,titleStr,detailsdir):		
	dk=p.DataFrame(d)#v,index=[i.title() for i in d])
	if(len(dk)==0):
		return False
	#dk.style.set_table_styles([dict(selector="td",props=[('max-width', '50px')])])

	with open(f'{detailsdir}/{ftitle}.html','w') as f:
		f.write('<body style="font-family:verdana,sans-serif;">')
		f.write(f'<b>--{titleStr}</b><br>')
		f.write(dk.to_html(header=False,index=False,border=0,bold_rows=False,na_rep=''))
		f.write('<br><a href="history_explorer/dummy.html">[Historic Data 2002-2018]</a>')
		f.write('</body>')
		f.write('\n')
	return True

def updateIndex(head,ta,indexfile,detailsdir):
	with open(indexfile,'a') as f:
		r=func_map[func_map[0]==int(head)].iloc[0]
		f.write(f'<div style="font-family:sans-serif;"><a href="{detailsdir}/{r[0]}.html" title="{ta}" target=details>{r[1].title()}</a></div>')

def SubDeptsBreakup(titleStr, head, indexfile, detailsdir):
	#note this catches head at start of line only
	#o=subprocess.run(r"grep -Ir '^"+head+"' data/expenditure --exclude-dir=tmp",shell=True, stdout=subprocess.PIPE, universal_newlines=True)	
	#this catches head anywhere - esp all occurrences within dpcode
	o=subprocess.run(r"grep -Ir '"+head+"' data/expenditure --exclude-dir=tmp",shell=True, stdout=subprocess.PIPE, universal_newlines=True)	
	d,v,ta=parseResults(o)
	if pp(d,v,head,titleStr,detailsdir):
		updateIndex(head,ta,indexfile,detailsdir)
	
	#print(f'<b>{format_indian(ta*1000)}</b>')

dept_map=p.read_csv('tn_dept2subdept_map',header=None)
#skipping error lines cause just interested in code to major head map, 3 col rows not reqd
func_map=p.read_csv('tn_func2dept_map',header=None,error_bad_lines=False,warn_bad_lines=False)

for head in func_map[0].astype(str):
	if head[0]=='0' or head[0]=='1':
		o=subprocess.run( ['ls -1 data/revenue/breakup/'+head+'*'],shell=True, stdout=subprocess.PIPE, universal_newlines=True)
		ppIncomeByDepts(o.stdout,head)
	elif head[0]=='2' or head[0]=='3':
		SubDeptsBreakup("Expenditure day to day (revex)", head,'revex_index.html','expense_explorer')
	elif head[0]=='4' or head[0]=='5':
		SubDeptsBreakup('Investments (capex)',head,'capex_index.html','investment_explorer')
	elif head[0]=='6' or head[0]=='7':
		SubDeptsBreakup('Loans',head,'loan_index.html','loan_explorer')
	else:
		print('Unrecognized head',head)
