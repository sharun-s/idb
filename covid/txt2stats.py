import sys

for i in range(1,len(sys.argv)):
	f=open(sys.argv[i])
	lines=f.readlines()
	f.close()
	tot=0
	uniq={}
	records=[]
	print(','.join(["d", "caseno", "tot", "ctot"]))
	for j in range(0,len(lines)):
		n=lines[j].split(',')
		date=n[0]
		cases=n[1]
		if not cases in uniq:
			if cases.find('-') > 0:
				g=cases.split('-')
				g=int(g[1])-int(g[0])+1
				uniq[cases]=g
				tot=tot+g
			else:
				tot=tot+1
				uniq[cases]=1
			print(','.join([date, cases, str(uniq[cases]), str(tot)]))