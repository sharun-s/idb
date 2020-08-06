import sys,re
import pandas as p
import subprocess
import csv

p.set_option('display.max_colwidth', -1)
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
	d.append([i[1],subdeptname.replace('_',' '),dept,functional_head])
df=p.DataFrame(d,columns=['Project','SubDept','Dept','Functional Head'])

with open('sif_index.html','a') as f:
	f.write('<body style="font-family:verdana,sans-serif;">')

for i in df.SubDept.unique():
	tmp=df[df['SubDept'] == i]
	sd=i.replace(' ','_')
	with open(f'sif_explorer/{sd}.html','w') as f:
		f.write('<body style="font-family:verdana,sans-serif;">')
		f.write('<div><a href=startpage.html target=details>Go Back</a></div>')
		f.write(tmp.to_html(index=False))
		f.write('</body>')
	with open('sif_index.html','a') as f:
		#f.write('<body style="font-family:verdana,sans-serif;">')
		f.write(f'<div><a href=sif_explorer/{sd}.html target=details>{i}</a></div>')

with open('sif_index.html','a') as f:
	f.write('</body>')

# with open('sif_all_details.html','w') as f:
# 	f.write('<body style="font-family:verdana,sans-serif;">')
# 	f.write('<div><a href=startpage.html target=details>Go Back</a></div>')
# 	f.write(df.to_html())
# 	f.write('</body>')
	
