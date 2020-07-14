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

dept_map=p.read_csv('tn_function_dept_map',header=None)

rev_head=sys.argv[1]
revex_head='2'+sys.argv[1][1:]
capex_head='4'+sys.argv[1][1:]
loan_head='6'+sys.argv[1][1:]

rev_file='data/revenue/'+rev_head+'.csv'

with open(rev_file) as f:
	line=f.readline()
	title=line.split(',')[1].strip().replace('"','').title()
	print('\033[41m '+title.upper()+'\033[0m','Year: 2018-2019')

print('---Income---')
df=p.read_csv(rev_file,comment='#',header=None)
df[1]=df[1].apply(lambda x:str(x).replace('- ','-')).apply(lambda x:atof(x) if x!='nan' else 0)
df=df[df[1]!=0.0]
df.set_index(0,inplace=True)
df=df.sort_values(by=1,ascending=True)
tot=format_indian(1000*df[1].sum())
df[1]=df[1].apply(lambda z:format_indian(1000*z))
print(df[1].to_string(header=False))
print(f'Total Income \033[91m {tot}\033[0m')

#s=shlex.split('ls -1 "data/revenue/breakup/'+rev_head+'*"')
#print(s)

o=subprocess.run( ['ls -1 data/revenue/breakup/'+rev_head+'*'],shell=True, stdout=subprocess.PIPE, universal_newlines=True)
print('More details:',o.stdout)

#Find all sub depts generating income
o=subprocess.run(r"grep -Po '\[\d\d\d\d\]' "+ o.stdout.strip()+" | sort | uniq" ,shell=True, stdout=subprocess.PIPE, universal_newlines=True)
#print(o.stdout)
depts=o.stdout.replace('[','').replace(']','').split('\n')
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
print('----sub depts that generated income')
for i in d[d[1].isin(subdepts)][2].values:
	print(i, end=',')

print('\n')

print('--Expenditure day to day (revex)')
o=subprocess.run(r"grep -Ir '^"+revex_head+"' data/expenditure ",shell=True, stdout=subprocess.PIPE, universal_newlines=True)
#print('2018','2019 Estimate','2019 revised','2020',sep='\t')
r=csv.reader(o.stdout.splitlines())
#print(o.stdout)

demands=[i[0].split('.')[0].split('/')[-1] for i in csv.reader(o.stdout.splitlines())]
d=[ dept_map[dept_map[0] == int(i)].iloc[0][2] for i in demands ]
v=[format_indian(1000*atof(amt)) for v in r for amt in v[2:3] ]
if len(d)==1:
	print(f'\033[33m {v[0]}\033[0m')
else:
	for i in zip(d,v):
		print(i[0].title(),
			'\033[92m'+i[1]+'\033[0m', sep=' ')

print('\n--Investments (capex)')
o=subprocess.run(r"grep -Ir '^"+capex_head+"' data/expenditure ",shell=True, stdout=subprocess.PIPE, universal_newlines=True)
#print("\t".join(['2018','2019 Estimate','2019 revised','2020']))
#print(o.stdout)
r=csv.reader(o.stdout.splitlines())
#print("\t".join([format_indian(1000*atof(amt)) for v in r for amt in v[2:3] ]) )
demands=[i[0].split('.')[0].split('/')[-1] for i in csv.reader(o.stdout.splitlines())]
d=[ dept_map[dept_map[0] == int(i)].iloc[0][2] for i in demands ]
v=[format_indian(1000*atof(amt)) for v in r for amt in v[2:3] ]
if len(d)==1:
	print(f'\033[91m {v[0]}\033[0m')
else:
	for i in zip(d,v):
		print(i[0].title(),
			'\033[92m'+i[1]+'\033[0m', sep=' ')
		
print('\n--Loans')
o=subprocess.run(r"grep -Ihr '^"+loan_head+"' data/expenditure ",shell=True, stdout=subprocess.PIPE, universal_newlines=True)
print(o.stdout)
