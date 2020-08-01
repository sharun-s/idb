f=open('tn_function_dept_map')
lines=f.readlines()
f.close()
f=open('sub-depts.html','w')
f.write('<body style="font-family:sans-serif;">')
for t in lines:
	token=t.split(',')
	subd=" ".join(token[2:])
	subd=subd.replace('"','').strip()
	details=token[0]+'_'+token[1]
	if token[1]=='':
		f.write(f'<div>{subd.title().strip()}</div>')
	else:
		f.write(f'<div>--<a href="{details}.html" target="details">{subd}</a></div>')
f.write('</body>')
f.close()