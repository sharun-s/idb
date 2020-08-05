import os,re
import pandas as p 
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