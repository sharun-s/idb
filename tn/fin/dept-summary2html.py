#!/usr/bin/env python3
#Generates a dept summary file for all depts
#Should contain list of subdepts with link to expenditure and income details
#

from common import *

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

# def highlight(x):
#     return ['font-weight: bold' for v in x]

# def pp(d,v,ftitle,titleStr):
# 	with open(f'func_explorer/{ftitle}-depts.html','w') as f:
# 		f.write('<body style="font-family:verdana,sans-serif;">')
# 		f.write(f'<br>--{titleStr}<br>')
# 		dk=p.DataFrame(v,index=[i.title() for i in d])
# 		f.write(dk.to_html(header=False,border=0,bold_rows=False))
# 		f.write('</body>')

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

#pfft junk it after standardizing subd file naming in data/revenue dir
def getSubDIncomeFilename(dcode,subcode,subname):
	fn=''
	dcode=str(dcode)
	subcode=str(int(subcode))
	if len(dcode)==1:
		fn='0'+dcode+'-'
	else:
		fn=dcode+'-'
	if len(subcode)==1:
		fn=fn+'0'+subcode+'_'
	else:
		fn=fn+subcode+'_'
	fn=fn+subname.replace(' ','_')
	return fn.rstrip('_')

def makeIndex():
	with open('dept_index.html','a') as f:
		f.write('<body style="font-family:sans-serif;"><div>Dept Index</div>')
		for code,name in dept_map[dept_map[1].isna()][[0,2]].itertuples(index=False):
			f.write(f'<div><a href="dept_summaries/{code}.html" target="details">{name.strip().title()}</a></div>')
		f.write('</body>')

def makeSummaries():
	for code,name in dept_map[dept_map[1].isna()][[0,2]].itertuples(index=False):
		with open(f'dept_summaries/{code}.html','a') as f:
			f.write(f'<body style="font-family:sans-serif;"><div><a href=../startpage.html target=details>Home</a>&nbsp;<b>{name.strip().title()}</b></div>Sub-Departments:<br>')
			#get subdepts and link to them
			for dcode,subcode,subname in dept_map[dept_map[0]==code].iloc[1:].itertuples(index=False):
				ofile=getSubDFilename(dcode,subcode,subname)
				ifile=getSubDIncomeFilename(dcode,subcode,subname)
				fstr=f'<div>--{subname.strip().title()}<br>&nbsp;&nbsp;<a target=details href="../subd_render/{ofile}" target="details" title="Expenditure/Investments/Loans">Outflow</a>&nbsp;&nbsp;&nbsp;&nbsp;'
				if os.path.exists('subd_income/'+ifile+'.html'):
					fstr=fstr+f'<a target=details href="../subd_income/{ifile}.html" target="details" title="Income">Inflow</a></div>'
				else:
					print(ifile,'not found')
					fstr=fstr+'</div>'
				f.write(fstr)
			f.write('</body>')
	print(len(sdfiles),found)		

#rm old files
try:
	subprocess.run(r'rm dept_index.html dept_summaries/*',shell=True)
except Exception as e:
	pass
		
makeIndex()
makeSummaries()