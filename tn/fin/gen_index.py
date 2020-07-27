f=open('index')
lines=f.readlines()
f.close()
s=sorted([line.split(':') for line in lines],key=lambda x:x[1])
f=open('index.html','w')
for t in s:
	f.write(f'<div><a href="{t[0]}" target="details">{t[1].title().strip()}</a></div>')
f.close()