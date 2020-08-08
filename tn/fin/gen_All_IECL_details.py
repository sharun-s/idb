#!/usr/bin/env python3
# generates files in loan_explorer, investment_explorer, expense_explorer, income_explorer
# for income json breakup details file is parsed for sub head [A-Z][A-Z]
# for revex,capex,loan simple grep of the functional head across all demand files TODO get amts pull code from gen_Innovation
# generates indexes - loan_index capex_index revex_index income_index

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
try:
	subprocess.run(r'rm income_index.html loan_index.html revex_index.html capex_index.html income_explorer/* investment_explorer/* expense_explorer/* loan_explorer/*',shell=True)
except Exception as e:
	pass

def get_amounts(filename,dpcode):
	g=p.read_csv(filename)
	#dpcode=dpcode.strip()
	#print(g.loc[:6])
	#print(g[g['dpcode']==dpcode])
	#print(g[g['dpcode']==dpcode].index)
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

def dumpIncomeDetails(detailsfile,head):
	#Find all sub depts generating income
	o=subprocess.run(r"cat "+ shlex.quote(detailsfile.strip()) + ' | jq -r \'paths as $p|getpath($p) | select(scalars)| ($p | map(select(type=="string"))) + [.]|@csv\'' + r"| grep '\[.*\]\",\"Total'  | grep 2018 " ,shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	rows=[]
	for i in csv.reader(o.stdout.splitlines()):
		descidx=2
		for idx,val in enumerate(i):
			if val.find('[') >-1:
				descidx=idx
				break
		rows.append([i[descidx],i[descidx+3]]) 
	df=p.DataFrame(rows)
	#get the dept subdept code generating the revenue
	try:
		df[[0,2]]=df[0].str.split('[',expand=True)
		df[2]=df[2].str.replace(']','')
	except ValueError as e:
		print(len(rows),f'check {detailsfile.strip()} - dept subdept code not found - probably no Income')
		raise e
	
	m={}
	# using the code get the names of the dept and subdept
	for dept in df[2].unique():
		#print(detailsfile,head,dept)
		d=dept_map[dept_map[0] == int(dept[:2])]			
		subdept=dept[2:]
		if subdept.startswith('0'):
			subdept=subdept[1]
		try:
			m[dept]=d[d[1] == int(subdept)][2].iloc[0]
		except Exception as e:
			print(dept, subdept, head, detailsfile)
			print(d)
			raise e
		
	df.columns=['Head','Amt','Code']
	df['subdept']=df['Code'].apply(lambda x:m[x])
	with open(f'income_explorer/{head}.html','w') as f:
		f.write('<body style="font-family:verdana,sans-serif;">')
		f.write(f'<a href=../startpage.html target=details>Home</a>&nbsp;<br>--Income Sources (Revenue)<br>')
		df.style.set_table_styles([dict(selector="th",props=[("text-align", "center")])])
		f.write(df.to_html(index=False,border=0,justify='center',columns=['Head','Amt','Code']))
		f.write('</body>')	
	try:
		r=func_map[func_map[0]==head].iloc[0]
		return (r[0],r[1],'') # TODO: get the total the way dept-summary2html does
	except Exception as e:
		print(head)
		raise e
    

def parseResults(o):
	d=[]
	v=[]
	totamt=0
	y=o.stdout.splitlines()
	for i in csv.reader(y):
		demand=i[0].split('.')[0].split('/')[-1]
		v=[]
		#this hacky condition cause of the 3 different types of files in the data/expenditure directory
		# eg: 22.csv has high level sub heads, 22-depts.csv has subdepts, while 22-1 22-2 etc are detail files for each sub dept
		# if the Head is found in 22.csv just show name and amount. if in a sub dept file- the line containing the 'Total' has to be located 
		if len(demand)==2 or len(demand)==1: 
			v.append(dept_map[dept_map[0] == int(demand)].iloc[0][2])
			for amt in i[2:3]:
				if amt !='':
					try:
						v.append(format_indian(1000*atof(amt)))
						totamt=totamt+atof(amt)
					except ValueError as e:
						print(i)
						raise e					  
				else: 
					v.append('-')
			#print(v)
			for k in range(len(v),6):
				v.append('')
			d.append(v)
		elif demand.find('-depts') > -1:
			continue
		else:
			head=i[0].split(':')[1]
			subdeptname=i[0].split(':')[0].split('/')[-1].replace('.csv','')
			dept=subdeptname.split('-')[0]
			#print(i, head, i[1])
			if len(head)==2 and head.isupper():
				try:
					row=[i[1],subdeptname.split('-')[1],dept]
					#print(i[0].split('.')[0]+'.csv',i[-1])
					row.extend(get_amounts(i[0].rsplit('.',maxsplit=1)[0]+'.csv', i[-1]))
					d.append(row)
					#v.append('-')# TODO v is not used by dumpdetails. remove it on next refactor
				except Exception as e:
					print('SKIPPING', i)
					print(head,subdeptname,dept)
					raise e
	return (d,v,totamt)

def highlight(x):
    return ['font-weight: bold' for v in x]

def dumpDetails(d,v,ftitle,titleStr,detailsdir):		
	dk=p.DataFrame(d)#v,index=[i.title() for i in d])
	if(len(dk)==0):
		return False
	#dk.style.set_table_styles([dict(selector="td",props=[('max-width', '50px')])])

	with open(f'{detailsdir}/{ftitle}.html','w') as f:
		f.write('<body style="font-family:verdana,sans-serif;">')
		f.write(f'<a href=../startpage.html target=details>Home</a>&nbsp;<b>--{titleStr}</b><br>')
		f.write(dk.to_html(header=False,index=False,border=0,bold_rows=False,na_rep='-'))
		f.write('<br><a href="history_explorer/dummy.html">[Historic Data 2002-2018]</a>')
		f.write('</body>')
		f.write('\n')
	return True
		
def writeIndex(index, indexfile,detailsdir):
	#remove None if any exist in index
	index=[i for i in index if i]
	with open(indexfile,'w') as f:
		f.write('<body style="font-family:sans-serif;">')
		f.write('<div>Sort by: <a target=ind href="#">Amount</a>&nbsp;&nbsp;<a target=ind href="#">A-Z</a>&nbsp;&nbsp;<a target=ind href="#">Code</a></div>')
		for detailsfile,funcname,totamt in sorted(index,key=lambda x:x[1]):
			# format total if its a float
			if isinstance(totamt,float):
				f.write(f'<div style="font-family:sans-serif;"><a href="{detailsdir}/{detailsfile}.html" title="{format_indian(1000*totamt)}" target=details>{funcname.title()}</a></div>')
			else:
				f.write(f'<div style="font-family:sans-serif;"><a href="{detailsdir}/{detailsfile}.html" title="{totamt}" target=details>{funcname.title()}</a></div>')
		f.write('</body>')

def SubDeptsBreakup(titleStr, head,detailsdir):
	#note this catches head at start of line only
	#o=subprocess.run(r"grep -Ir '^"+head+"' data/expenditure --exclude-dir=tmp",shell=True, stdout=subprocess.PIPE, universal_newlines=True)	
	#this catches head anywhere - esp all occurrences within dpcode
	o=subprocess.run(r"grep -Ir '"+head+"' data/expenditure --exclude-dir=tmp",shell=True, stdout=subprocess.PIPE, universal_newlines=True)	
	d,v,ta=parseResults(o)
	if dumpDetails(d,v,head,titleStr,detailsdir):
		try:
			r=func_map[func_map[0]==head].iloc[0]
			return (r[0],r[1],ta)
		except Exception as e:
			print(head)
			raise e
		#print('done',head)
	#NOTE no else so None gets returned in some cases and is removed from index in writeIndex
	#print(f'<b>{format_indian(ta*1000)}</b>')

dept_map=p.read_csv('tn_dept2subdept_map',header=None)
#skipping error lines cause just interested in code to major head map, 3 col rows not reqd
func_map=p.read_csv('tn_func2dept_map',dtype=str,header=None,error_bad_lines=False,warn_bad_lines=False)
revex_index=[]
capex_index=[]
loan_index=[]
rev_index=[]

for head in func_map[0]:
	if head[0]=='2' or head[0]=='3':
		revex_index.append(SubDeptsBreakup("Expenditure day to day (revex)", head, 'expense_explorer'))
	elif head[0]=='4' or head[0]=='5':
		capex_index.append(SubDeptsBreakup('Investments (capex)',head,'investment_explorer'))
	elif head[0]=='6' or head[0]=='7':
		loan_index.append(SubDeptsBreakup('Loans',head,'loan_explorer'))
	else:
		pass#print('Unrecognized head',head)

writeIndex(revex_index,'revex_index.html','expense_explorer')
writeIndex(capex_index,'capex_index.html','investment_explorer')
writeIndex(loan_index,'loan_index.html','loan_explorer')

revfiles=listdir('data/revenue/breakup/')
for f in revfiles:
	rev_index.append(dumpIncomeDetails(f'data/revenue/breakup/{f}', f[:4]))
writeIndex(rev_index,'income_index.html','income_explorer')
#print('done',f)