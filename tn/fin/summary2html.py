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
	#r=csv.reader(o.stdout.splitlines())
	d=[]
	v=[]
	totamt=0
	for i in csv.reader(o.stdout.splitlines()):
		demand=i[0].split('.')[0].split('/')[-1]
		if len(demand)==2 or len(demand)==1: # hack: skips files not matching format xx.csv or x.csv
			d.append(dept_map[dept_map[0] == int(demand)].iloc[0][2])
			for amt in i[2:3]:
				if amt !='':
					try:
						v.append(format_indian(1000*atof(amt)))
					except ValueError as e:
						print('error in', dept_map[dept_map[0] == int(demand)].iloc[0][2],file=sys.stderr)
						raise e
					
					totamt=totamt+atof(amt)  
				else: 
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

def pp(d,v):
	dk=p.DataFrame(v,index=[i.title() for i in d])
	if len(dk)==1:
		print('<b>'+dk.ix[0][0] +'</b><br>')
	else:
		#df.style.set_properties(color="red")
		#df.style.apply(highlight)
		#print(dk)
		print(dk.to_html(header=False,border=0,bold_rows=False))
	#for i in zip(d,v):
	#	wrapped=tw.wrap(tw.dedent(i[0]),60)
	#	for l in wrapped[:-1]: 
	#		print('<br>'+l.title() +' ')
	#	print(wrapped[-1].title().rjust(60," "),
	#		'<b>'+i[1]+'</b><br>', sep=' ')


def ppIncome():
	df=p.read_csv(rev_file,comment='#',header=None)
	df[1]=df[1].apply(lambda x:str(x).replace('- ','-')).apply(lambda x:atof(x) if x!='nan' else 0)
	df=df[df[1]!=0.0]
	#df.set_index(0,inplace=True)
	df=df.sort_values(by=1,ascending=True)
	tot=format_indian(1000*df[1].sum())
	df[1]=df[1].apply(lambda z:format_indian(1000*z))
	#if len(df)>1:
	#	print(df.to_html(header=False,index=False,border=0))
	print(f'<b>{tot}</b>')

def ppIncomeByDepts(detailsfile):
	#Find all sub depts generating income
	o=subprocess.run(r"grep -Po '\[\d\d\d\d\]' "+ shlex.quote(detailsfile.strip()) +" | sort | uniq" ,shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	#print(o.stdout)
	depts=o.stdout.replace('[','').replace(']','').split('\n')[:-1]
	if True:# temp hack check here for empty/errors in depts
		d=dept_map[dept_map[0] == int(depts[0][:2])]
		subdepts=[]
		for dept in depts:
			if dept:
				subdept=dept[2:]
				if subdept.startswith('0'):
					subdept=subdept[1]
			else:
				continue
			subdepts.append(subdept)
		print('<br><b>SubDepts producing Income</b>')
		#print("<a href='#'>[E] </a>,".join(d[d[1].isin(subdepts)][2].values.tolist()))
		print(d[d[1].isin(subdepts)].to_html(index=False,header=False,columns=[2],border=0))#[2].values.tolist())


print('<body style="font-family:verdana,sans-serif;">')

dept_map=p.read_csv('tn_dept2subdept_map',header=None)
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

rev_file='data/revenue/'+rev_head+'.csv'
try:
	with open(rev_file) as f:
		line=f.readline()
		title=line.split(',')[1].strip().replace('"','').title()
		print('<h3>'+title.upper()+'  Year:2018-2019 </h3>')
		print('--Income (revenue)<br>')

		ppIncome()
	
		o=subprocess.run( ['ls -1 data/revenue/breakup/'+rev_head+'*'],shell=True, stdout=subprocess.PIPE, universal_newlines=True)
		print('[<a target="_top" href="../'+ o.stdout+'">Details</a>][<a target="details" href=../func_explorer/'+rev_head+'-depts.html>Dept-wise</a>]')

		#ppIncomeByDepts(o.stdout)

except FileNotFoundError as e:
	# todo: derive and check if rev code exists from whatever code that has been passed. 
	# check in rev dir cag dir and hist csv files
	print('Income data not found or No income reported') 
	pass

print('<br>--Expenditure day to day (revex)<br>')
o=subprocess.run(r"grep -Ir '^"+revex_head+"' data/expenditure --exclude-dir=tmp",shell=True, stdout=subprocess.PIPE, universal_newlines=True)
#print('2018','2019 Estimate','2019 revised','2020',sep='\t')
d,v,ta=parseResults(o)
#pp(d,v)
print(f'<b>{format_indian(ta*1000)}</b> [<a target="details" href=../func_explorer/'+revex_head+'-depts.html>Dept-wise</a>]')


print('<br>--Investments (capex)<br>')
o=subprocess.run(r"grep -Ir '^"+capex_head+"' data/expenditure --exclude-dir tmp ",shell=True, stdout=subprocess.PIPE, universal_newlines=True)
#print("\t".join(['2018','2019 Estimate','2019 revised','2020']))
d,v,ta=parseResults(o)
#pp(d,v)
print(f'<b>{format_indian(ta*1000)}</b>  [<a target="details" href=../func_explorer/'+capex_head+'-depts.html>Dept-wise</a>]')


print('<br>--Loans<br>')
o=subprocess.run(r"grep -Ir '^"+loan_head+"' data/expenditure --exclude-dir=tmp",shell=True, stdout=subprocess.PIPE, universal_newlines=True)
d,v,ta=parseResults(o)
#pp(d,v)
print(f'<b>{format_indian(ta*1000)}</b> [<a target="details" href=../func_explorer/'+loan_head+'-depts.html>Dept-wise</a>]<br>')

print('<br><b>--Historic Trend 2002-2018 (in laks)</b>')
o=subprocess.run(r'grep -Ph "'+rev_head+'" data/*.csv',shell=True, stdout=subprocess.PIPE, universal_newlines=True)
print('<br><b>Income</b>')
print(parseHistory(o))
o=subprocess.run(r'grep -Ph "'+revex_head+'" data/*.csv',shell=True, stdout=subprocess.PIPE, universal_newlines=True)
print('<br><b>Expenses</b>')
print(parseHistory(o))
o=subprocess.run(r'grep -Ph "'+capex_head+'" data/*.csv',shell=True, stdout=subprocess.PIPE, universal_newlines=True)
print('<br><b>Investments</b>')
print(parseHistory(o))

print('<br><b>Compared to Other States (Kerala)</b><br>')
o=subprocess.run(r'grep -Pi "'+title+'" ../../ke/data/*.csv' ,shell=True, stdout=subprocess.PIPE, universal_newlines=True)
print(parseHistory(o))
print('<br><a href="../startpage.html" target=details>Explore</a>')

print('</body>')
