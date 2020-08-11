#!/usr/bin/env python3
# generates files in loan_explorer, investment_explorer, expense_explorer, income_explorer
# for income json breakup details file is parsed for sub head [A-Z][A-Z]
# for revex,capex,loan simple grep of the functional head across all demand files TODO get amts pull code from gen_Innovation
# generates indexes - loan_index capex_index revex_index income_index

from common import *

def dumpIncomeDetails(detailsfile,head):
	#Find all sub depts generating income
	#TODO the grep 2018 at end of command above should be setable to any year
	o=subprocess.run(r"cat "+ shlex.quote(detailsfile.strip()) + ' | jq -r \'paths as $p|getpath($p) | select(scalars)| ($p | map(select(type=="string"))) + [.]|@csv\'' + r"| grep '\[.*\]\",\"Total'  | grep 2018 " ,shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	rows=[]
	#get relevant fields from jq parsing details json file
	for i in csv.reader(o.stdout.splitlines()):
		descidx=2
		for idx,val in enumerate(i):
			if val.find('[') >-1:
				descidx=idx
				break
		rows.append([i[descidx],i[descidx+3]]) 
	df=p.DataFrame(rows)
	#get the dept subdept code generating the revenue which is in desc as [\d\d\d\d]
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
	# weird hack - print below fails without doing a setlocale
	locale.setlocale(locale.LC_NUMERIC, '')
	#print(locale.atof("60,20"))
	df.columns=['Head','Amt','Code']
	df['Amt']=df['Amt'].apply(lambda x:str(x).replace('- ','-'))#
	df['Amt']=df['Amt'].apply(Amt2Str) 
	df['SubDept']=df['Code'].apply(lambda x:m[x])
	df=df.sort_values(by=['Code','Amt'],ascending=False)
	df['Amt']=df['Amt'].apply(format_indian)
	with open(f'income_explorer/{head}.html','w') as f:
		f.write('<style>td { min-width: 100px;}</style>')
		f.write('<body style="font-family:verdana,sans-serif;">')
		f.write(f'<a href=../startpage.html target=details>Home</a>&nbsp;<br>--Income Sources (Revenue)<br>')
		f.write(df.to_html(index=False,border=0,justify='center',columns=['Head','Amt','Code','SubDept']))
		f.write('</body>')	
	try:
		r=func_map[func_map[0]==head].iloc[0]
		return (r[0],r[1],'') # TODO: get the total the way dept-summary2html does
	except Exception as e:
		print(head)
		raise e

def parseResults(o):
	details=[]
	highlevel=[]
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
			highlevel.append(v)
		elif demand.find('-depts') > -1:
			continue
		else:
			head=i[0].split(':')[1]
			filename=i[0].split('.')[0].split('/')[-1]
			subdeptname=re.sub(r'([0-9]{1,2}[\-_])+','',filename).replace('_',' ')
			subdeptname="".join([' '+i if i.isupper() else i for i in subdeptname])
			dept=filename.split("-")[0]
			if len(head)==2 and head.isupper():
				try:
					row=[i[1],subdeptname.strip(),dept]
					row.extend(get_amounts(i[0].rsplit('.',maxsplit=1)[0]+'.csv', i[-1]))
					details.append(row)
				except Exception as e:
					print('SKIPPING', i)
					print(head,subdeptname,dept,i[0].rsplit('.',maxsplit=1)[0]+'.csv',i[-1])
					sys.exit()
					#raise e
	return (highlevel, details,totamt)

def highlight(x):
    return ['font-weight: bold' for v in x]

def dumpDetails(highlevel,details,ftitle,titleStr,detailsdir):		
	h=p.DataFrame(highlevel)
	dk=p.DataFrame(details)
	if(len(dk)==0):
		return False
	if(len(h)>0):
		h.columns=["Dept","Total"]
	dk.columns=["Description",'SubDept','Dept','2018','2019','2020']
	dk['2018']=dk['2018'].apply(lambda x:str(x).replace('- ','-'))
	dk['2019']=dk['2019'].apply(lambda x:str(x).replace('- ','-'))
	dk['2020']=dk['2020'].apply(lambda x:str(x).replace('- ','-'))
	#print(ftitle,titleStr,dk['2020'])
	dk['2018']=dk['2018'].apply(Amt2Str) 
	dk['2019']=dk['2019'].apply(Amt2Str) 
	dk['2020']=dk['2020'].apply(Amt2Str) 
	dk=dk.sort_values(by=['Dept','SubDept','2018'],ascending=False)
	dk['2018']=dk['2018'].apply(format_indian)
	dk['2019']=dk['2019'].apply(format_indian)
	dk['2020']=dk['2020'].apply(format_indian)

	with open(f'{detailsdir}/{ftitle}.html','w') as f:
		f.write('<style>td { min-width: 100px;}</style>')
		f.write('<body style="font-family:verdana,sans-serif;">')
		f.write(f'<a href=../startpage.html target=details>Home</a>&nbsp;<b>--{titleStr}</b><br>')
		f.write(h.to_html(justify='center',index=False,border=0,bold_rows=False,na_rep='-'))
		f.write(dk.to_html(columns=["Description",'2018','2019','2020','SubDept','Dept'], justify='center',index=False,border=0,bold_rows=False,na_rep='-'))
		f.write('<br><a href="history_explorer/dummy.html">[Historic Data 2002-2018]</a>')
		f.write('</body>')
		f.write('\n')
	return True
		
def writeIndex(index, indexfile, detailsdir, sortcol=1):
	#remove None if any exist in index
	index=[i for i in index if i]
	fname=indexfile
	reverseorder=False
	if sortcol==2:
		fname=indexfile+'-by-amount'
		reverseorder=True
	if sortcol==0:
		fname=indexfile+'-by-head'
		reverseorder=False

	with open(fname+'.html','w') as f:
		f.write('<body style="font-family:sans-serif;">')
		f.write(f'<div>Sort by: <a target=ind href={indexfile+".html"}>A-Z</a>&nbsp;&nbsp;<a target=ind href={indexfile+"-by-head.html"}>Code</a>&nbsp;&nbsp;<a target=ind href={indexfile+"-by-amount.html"}>Amount</a></div>')
		for head,funcname,totamt in sorted(index,key=lambda x:x[sortcol],reverse=reverseorder):
			# format total if its a float
			if isinstance(totamt,float):
				f.write(f'<div style="font-family:sans-serif;"><a href="{detailsdir}/{head}.html" target=details>{funcname.title()}</a>&nbsp;{head}&nbsp;<b>{format_indian(1000*totamt)}</b></div>')
			else:
				f.write(f'<div style="font-family:sans-serif;"><a href="{detailsdir}/{head}.html" target=details>{funcname.title()}</a>&nbsp;{head}&nbsp;{totamt}</div>')
		f.write('</body>')

def SubDeptsBreakup(titleStr, head,detailsdir):
	#note this catches head at start of line only
	#o=subprocess.run(r"grep -Ir '^"+head+"' data/expenditure --exclude-dir=tmp",shell=True, stdout=subprocess.PIPE, universal_newlines=True)	
	#this catches head anywhere - esp all occurrences within dpcode
	o=subprocess.run(r"grep -Ir '"+head+"' data/expenditure --exclude-dir=tmp",shell=True, stdout=subprocess.PIPE, universal_newlines=True)	
	h,d,ta=parseResults(o)
	if dumpDetails(h,d,head,titleStr,detailsdir):
		try:
			r=func_map[func_map[0]==head].iloc[0]
			return (r[0],r[1],ta)
		except Exception as e:
			print(head)
			raise e
		#print('done',head)
	#NOTE no else so None gets returned in some cases and is removed from index in writeIndex
	#print(f'<b>{format_indian(ta*1000)}</b>')

try:
	subprocess.run(r'rm income_index.html loan_index.html revex_index.html capex_index.html income_explorer/* investment_explorer/* expense_explorer/* loan_explorer/*',shell=True)
except Exception as e:
	pass

revex_index=[]
capex_index=[]
loan_index=[]
rev_index=[]
#collect index data
for head in func_map[0]:
	if head[0]=='2' or head[0]=='3':
		revex_index.append(SubDeptsBreakup("Expenditure day to day (revex)", head, 'expense_explorer'))
	elif head[0]=='4' or head[0]=='5':
		capex_index.append(SubDeptsBreakup('Investments (capex)',head,'investment_explorer'))
	elif head[0]=='6' or head[0]=='7':
		loan_index.append(SubDeptsBreakup('Loans',head,'loan_explorer'))
	else:
		pass#print('Unrecognized head',head)

revfiles=listdir('data/revenue/breakup/')
for f in revfiles:
	rev_index.append(dumpIncomeDetails(f'data/revenue/breakup/{f}', f[:4]))

for i in range(0,3):
	writeIndex(revex_index,'revex_index','expense_explorer',i)
	writeIndex(capex_index,'capex_index','investment_explorer',i)
	writeIndex(loan_index,'loan_index','loan_explorer',i)
	writeIndex(rev_index,'income_index','income_explorer',i)
#print('done',f)