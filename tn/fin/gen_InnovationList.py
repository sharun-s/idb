import sys,re
import pandas as p
import subprocess
import csv
p.set_option('display.max_colwidth', -1)

def get_amounts(filename,dpcode):
	g=p.read_csv(filename)
	tmp=g[g['dpcode']==dpcode].index[0]
	head=g.ix[tmp]['head']
	idx=tmp
	while True:
		idx=idx+1
		if g.ix[idx]['head']==head:
			if g.ix[idx]['desc']=='Total '+head:
				return g.ix[idx][['2018','2019Rev','2020Est']]
		if idx>tmp+20:
			return ['?','?','?']

try:
	subprocess.run(r'rm sif_index.html',shell=True)
	subprocess.run(r'rm sif_explorer/*',shell=True)
except Exception as e:
	pass

o=subprocess.run(r"grep 'Innovation Fund' data/expenditure/*.csv --exclude-dir=tmp |  grep -P ',,,,,[0-9]{4} [0-9]{2}'| grep -v 'Deduct'",shell=True, stdout=subprocess.PIPE, universal_newlines=True)	 

#df=p.read_csv(o.stdout,header=None)
#print(df.to_html(header=False,index=False,columns=[0,1,6]))

y=o.stdout.splitlines()
d=[]
for i in csv.reader(y):
	filename=i[0].split('.')[0].split('/')[-1]
	dept=filename.split("-")[0]
	subdeptname=re.sub(r'([0-9]{1,2}[\-_])+','',filename)
	functional_head=i[6].split(' ')[0]
	row=[i[1].replace('under State Innovation Fund',''),subdeptname.replace('_',' '),dept,functional_head]
	row.extend(get_amounts(i[0].split('.')[0]+'.csv', i[-1]))
	#assert len(row)==7
	d.append(row)

df=p.DataFrame(d,columns=['Project','SubDept','Dept','Functional Head','2018','2019','2020'])

with open('sif_index.html','a') as f:
	f.write('<body style="font-family:verdana,sans-serif;">')

dept_map=p.read_csv('tn_dept2subdept_map',header=None)

vc=df.Dept.value_counts()
l=[]
#gets all rows for a each dept, sorted by dept with most projects, convert deptcode to name
for i in vc.index:
	tmp=df[df['Dept'] == i]
	d=dept_map[dept_map[0] == int(i)].iloc[0][2]
	txt=d.strip().replace('_DEPARTMENT','').title()
	fd=d.strip().replace(' ','_').replace('_DEPARTMENT','').title()
	cnt=vc.ix[i]
	l.append([fd,tmp,txt,cnt])
# resort dept alphabetically, easier to browse than abv order
for fd,tmp,txt,cnt in sorted(l,key=lambda x:x[2]):
	with open(f'sif_explorer/{fd}.html','w') as f:
		f.write('<body style="font-family:verdana,sans-serif;">')
		f.write('<div><a href=../startpage.html target=details>Go Back</a></div>')
		f.write(tmp.to_html(index=False,justify='center',na_rep='',columns=['Project','2018','2019','2020','SubDept','Functional Head']))
		f.write('</body>')
	with open('sif_index.html','a') as f:
		#f.write('<body style="font-family:verdana,sans-serif;">')
		f.write(f'<div><a href=sif_explorer/{fd}.html target=details>{txt}</a>&nbsp;{cnt}</div>')

#index by subdept
# for i in df.SubDept.unique():
# 	tmp=df[df['SubDept'] == i]
# 	sd=i.replace(' ','_')
# 	with open(f'sif_explorer/{sd}.html','w') as f:
# 		f.write('<body style="font-family:verdana,sans-serif;">')
# 		f.write('<div><a href=startpage.html target=details>Go Back</a></div>')
# 		f.write(tmp.to_html(index=False))
# 		f.write('</body>')
# 	with open('sif_index.html','a') as f:
# 		#f.write('<body style="font-family:verdana,sans-serif;">')
# 		f.write(f'<div><a href=sif_explorer/{sd}.html target=details>{i}</a></div>')

with open('sif_index.html','a') as f:
	f.write('</body>')

# with open('sif_all_details.html','w') as f:
# 	f.write('<body style="font-family:verdana,sans-serif;">')
# 	f.write('<div><a href=startpage.html target=details>Go Back</a></div>')
# 	f.write(df.to_html())
# 	f.write('</body>')
	
