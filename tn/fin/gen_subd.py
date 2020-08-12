#Generates html of Expenditure details of all subdepartments in subd_render directory
#i.e. all subd expenditure files found in data/expenditure dir conforming to dept-subept...csv naming format are converted to html
#The expenditure details are split by Function

#Generates an index to all html files produced 
import os
from common import *

try:
	subprocess.run(r'rm sub-dept.html sub-depts-Income.html subd_render/* subd_income/*',shell=True)
except Exception as e:
	pass

expfiles = os.listdir('data/expenditure')
expfiles = [i for i in expfiles if re.match('[0-9]{1,2}-[0-9]{1,2}',i) != None]

for i in expfiles:
	try:
		df=p.read_csv('data/expenditure/'+i)
		f=open('subd_render/'+i.replace('.csv','.html'),'w')
		f.write('<a href=../startpage.html target=details>Home</a>&nbsp; [All amounts in Thousands]')
		f.write(df.to_html(border=0,index=False,columns=['desc','2018','2019Rev','2020Est'],na_rep=''))
		f.close()
	except Exception as e:
		print(i,e)

f=open('tn_dept2subdept_map')
lines=f.readlines()
f.close()
# Note: detail files are generated based on files found in data/expenditure. Index is generated on subdepts mentioned in TN Budget cor statement
# If the 2 lists dont match means subdept details file is missing (maybe a filename spelling error) in data/expenditure or that subdept has no expenditure reported
f=open('sub-depts.html','w')
f.write('<body style="font-family:sans-serif;">')
for t in lines:
	token=t.split(',')
	subd=" ".join(token[2:])
	subd=subd.replace('"','').strip()
	details=token[0]+'-'+token[1]
	for i in expfiles:
		if i.startswith(details) or i.startswith(token[0]+'-0'+token[1]):
			details=i
			break

	if token[1]=='':
		f.write(f'<div>{subd.title().strip()}</div>')
	else:
		f.write(f'<div>--<a href="subd_render/{details.replace(".csv",".html")}" target="details">{subd}</a></div>')
f.write('</body>')
f.close()

#code 4digit code - 2 dept 2 subd - from income json files
def code2filename(code):
	result=dept_map[dept_map[0]==str(code)[:2] and dept_map[1]==str(code)[2:]]
	if len(result) >0:
		return result[0]+'-'+result[1]+'_'+result[2]+'.html'
	else:
		print('name for ',code,' not found')
		return code

def dumpSubdIncomeDetails(detailsfile,head):
	income_idx=[]
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
	df.columns=['Desc','2018','Code']
	df['2018']=df['2018'].apply(lambda x:str(x).replace('- ','-'))
	df['SubDept']=df['Code'].apply(lambda x:m[x])
	df=df.sort_values(by=['Code'])
	#the same Code can be found in multiple functional heads
	for c, grp in df.groupby('Code'):
		subdname=grp['SubDept'].unique()[0] # no need for uniq just take 1st val
		subdfile=subdname.strip().replace(' ','_')
		subdfile=grp.iloc[0]['Code'][:2]+'-'+grp.iloc[0]['Code'][2:]+'_'+subdfile
		headname=" ".join(detailsfile.split('_')[1:]).replace('.json','')
		firstwrite=os.path.exists(f'subd_income/{subdfile}.html')
		grp['2018']=grp['2018'].apply(amt2flt)
		grp.sort_values(by=['2018'],inplace=True,ascending=False)
		ftot=format_indian(grp['2018'].sum())
		grp['2018']=grp['2018'].apply(format_indian)
		with open(f'subd_income/{subdfile}.html','a') as f:
			if not firstwrite:
				f.write('<style>td { min-width: 100px;max-width:360px}</style>')
				f.write('<style>body {font-family:verdana,sans-serif;}</style>')
				f.write(f'<a href=../startpage.html target=details>Home</a>&nbsp; <b>{subdname}</b> [{c}] <br>--  Income Sources By Function  --<br>--<b>{headname}</b>&nbsp;{ftot} &nbsp;<a title="See Income of ALL SubDepts related to this Function" href=../income_explorer/{head[:4]}.html>#</a> &nbsp;&nbsp; <br>')
			else:
				f.write(f'<a name={head[:4]}></a><br><b>{headname}</b>&nbsp;{ftot} &nbsp;<a title="See Income of ALL SubDepts related to this Function" href=../income_explorer/{head[:4]}.html>#</a>&nbsp;&nbsp; <br>')
			
			f.write(grp.to_html(index=False,border=0,justify='center',columns=['Desc','2018']))
			#f.write('</body>')
		income_idx.append([c,subdname,subdfile,head,headname,len(grp)])
	return income_idx

subd_income_index=[]
with open("sub-depts-Income.html","w") as f:
	f.write('<body style="font-family:verdana,sans-serif;">')
	for func_incomefile in os.listdir('data/revenue/breakup/'):
		i=dumpSubdIncomeDetails(f'data/revenue/breakup/{func_incomefile}', func_incomefile[:4])
		for j in i:
			subd_income_index.append(j)
	df=p.DataFrame(subd_income_index)
	df.columns=['DCode','SubD','SubDIncomeDetails','Func','Funcname','inFunc']
	df=df.sort_values(['DCode','inFunc'])
	for i,grp in df.groupby(['DCode','SubD','SubDIncomeDetails']):
		f.write(f'<div><a target=details title={i[0]} href="subd_income/{i[2]}.html">{i[1]}</a></div>')
		for fh,fname,fhcnt in grp[['Func','Funcname','inFunc']].itertuples(index=False):
			f.write(f'<div style="font-size:8px">&nbsp;&nbsp;{fname}  <a target=details href="subd_income/{i[2]}.html#{fh}">{fhcnt}</a></div>')
	f.write('</body>')