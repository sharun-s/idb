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
	r=csv.reader(o.stdout.splitlines())
	d=[]
	v=[]
	for i in csv.reader(o.stdout.splitlines()):
		demand=i[0].split('.')[0].split('/')[-1]
		if len(demand)==2 or len(demand)==1: # hack: skips files not matching format xx.csv or x.csv
			d.append(dept_map[dept_map[0] == int(demand)].iloc[0][2])
			for amt in i[2:3]:
				if amt !='':
					v.append(format_indian(1000*atof(amt)))  
				else: 
					v.append('-')
	return (d,v)

def pp(d,v):
	print('<ul>')
	for i in zip(d,v):
		wrapped=tw.wrap(tw.dedent(i[0]),60)
		for l in wrapped[:-1]: 
			print('<li>'+l.title() +' ')
		print(wrapped[-1].title().rjust(60," "),
			''+i[1]+'</li>', sep=' ')
	print('</ul>')

def ppIncome():
	df=p.read_csv(rev_file,comment='#',header=None)
	df[1]=df[1].apply(lambda x:str(x).replace('- ','-')).apply(lambda x:atof(x) if x!='nan' else 0)
	df=df[df[1]!=0.0]
	df.set_index(0,inplace=True)
	df=df.sort_values(by=1,ascending=True)
	tot=format_indian(1000*df[1].sum())
	df[1]=df[1].apply(lambda z:format_indian(1000*z))
	print(df[1].to_string(header=False))
	print(f'<h4>Total Income {tot} </h4>')

def ppIncomeByDepts(detailsfile):
	#Find all sub depts generating income
	o=subprocess.run(r"grep -Po '\[\d\d\d\d\]' "+ shlex.quote(detailsfile.strip()) +" | sort | uniq" ,shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	print(o.stdout)
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
		print('<h4>Income by SubDepts</h4>')
		print(",".join(d[d[1].isin(subdepts)][2].values.tolist()))
		#print(d[d[1].isin(subdepts)][2].values.tolist())


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

rev_file='data/revenue/'+rev_head+'.csv'
try:
	with open(rev_file) as f:
		line=f.readline()
		title=line.split(',')[1].strip().replace('"','').title()
		print('<h3>'+title.upper()+'  Year:2018-2019 </h3>')
		print('<h4>Income</h4>')

		ppIncome()
	
		o=subprocess.run( ['ls -1 data/revenue/breakup/'+rev_head+'*'],shell=True, stdout=subprocess.PIPE, universal_newlines=True)
		print('<a href="'+ o.stdout+'">details</a>')

		ppIncomeByDepts(o.stdout)

except FileNotFoundError as e:
	# todo: derive and check if rev code exists from whatever code that has been passed. 
	# check in rev dir cag dir and hist csv files
	print('Income data not found or No income reported') 
	pass

print('')
print('<h4>Expenditure day to day (revex)</h4>')
o=subprocess.run(r"grep -Ir '^"+revex_head+"' data/expenditure --exclude-dir=tmp",shell=True, stdout=subprocess.PIPE, universal_newlines=True)
#print('2018','2019 Estimate','2019 revised','2020',sep='\t')
d,v=parseResults(o)
pp(d,v)

print('<h4>Investments (capex)</h4>')
o=subprocess.run(r"grep -Ir '^"+capex_head+"' data/expenditure --exclude-dir tmp ",shell=True, stdout=subprocess.PIPE, universal_newlines=True)
#print("\t".join(['2018','2019 Estimate','2019 revised','2020']))
d,v=parseResults(o)
pp(d,v)

print('<h4>--Loans<h4>')
o=subprocess.run(r"grep -Ir '^"+loan_head+"' data/expenditure --exclude-dir=tmp",shell=True, stdout=subprocess.PIPE, universal_newlines=True)
d,v=parseResults(o)
pp(d,v)

print('<h4>--Historic Trend 2002-2018 (in laks)</h4>')
o=subprocess.run(r'grep -P "'+rev_head+'" data/*.csv',shell=True, stdout=subprocess.PIPE, universal_newlines=True)
print(o.stdout)
o=subprocess.run(r'grep -P "'+revex_head+'" data/*.csv',shell=True, stdout=subprocess.PIPE, universal_newlines=True)
print(o.stdout)
o=subprocess.run(r'grep -P "'+capex_head+'" data/*.csv',shell=True, stdout=subprocess.PIPE, universal_newlines=True)
print(o.stdout)


print('<h4>Compared to Other States</h4>')
o=subprocess.run(r'grep -Pi "'+title+'" ../../ke/data/*.csv' ,shell=True, stdout=subprocess.PIPE, universal_newlines=True)
print(o.stdout)


