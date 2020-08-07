#!/usr/bin/env python3
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

dept_map=p.read_csv('tn_dept2subdept_map',header=None)
sdfiles=listdir('subd_render/')
sdfilesmap=dict([(i.replace('_','').replace('-','').replace(' ','').replace(',','').replace('.html',''),i)for i in sdfiles])
found=0
def getSubDFilename(dcode,subcode,subname):
	key=str(int(dcode))+str(int(subcode))+subname.replace(' ','').replace('-','').replace('_','').replace(',','')
	if key in sdfilesmap:
		global found
		found=found+1
		return sdfilesmap[key]
	else:
		key=str(int(dcode))+'0'+str(int(subcode))+subname.replace(' ','').replace('-','').replace(',','')
		if key in sdfilesmap:
			found=found+1
			return sdfilesmap[key]
		else:
			print(key, 'didnt match filenames')
			return ''

def makeIndex():
	with open('dept_index.html','a') as f:
		f.write('<body style="font-family:sans-serif;"><div>Dept Index</div>')
		for code,name in dept_map[dept_map[1].isna()][[0,2]].itertuples(index=False):
			f.write(f'<div><a href="dept_summaries/{code}.html" target="details">{name.strip().title()}</a></div>')
		f.write('</body>')

def makeSummaries():
	for code,name in dept_map[dept_map[1].isna()][[0,2]].itertuples(index=False):
		with open(f'dept_summaries/{code}.html','a') as f:
			f.write(f'<body style="font-family:sans-serif;"><div><a href=../startpage.html target=details>Home</a>&nbsp;<b>{name.strip().title()}</b></div>')
			#get subdepts and link to them
			for dcode,subcode,subname in dept_map[dept_map[0]==code].iloc[1:].itertuples(index=False):
				f.write(f'<div><a target=details href="../subd_render/{getSubDFilename(dcode,subcode,subname)}" target="details">{subname.strip().title()}</a></div>')
			f.write('</body>')
	print(len(sdfiles),found)		

#rm old files
try:
	subprocess.run(r'rm dept_index.html dept_summaries/*',shell=True)
except Exception as e:
	pass
		
makeIndex()
makeSummaries()