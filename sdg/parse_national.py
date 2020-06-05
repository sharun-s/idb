import csv,re,json,sys
from pprint import pprint
with open(sys.argv[1]) as csvfile:
	spamreader = csv.reader(csvfile)
	lastg=''
	lastt=''
	master={}
	for row in spamreader:
		#print(', '.join(row))
		if row[0].startswith('SL') or row[0].startswith('0'):
			continue
		if row[0].startswith("Goal"):
			g,gdesc= row[0].split(':')
			lastg=g.replace('Goal ','')
			master[lastg]={'desc':gdesc.strip(),'targets':{}}
		elif row[0].startswith("Target"):
			t,tdesc= row[0].split(':')
			lastt=t.replace('Target ','')
			master[lastg]['targets'][lastt]={'desc':tdesc.strip(),'indicators':{}}			
		elif row[0].isdigit():
			print(lastg,lastt,row[0])
			if row[1].startswith(lastt):
				i=row[1].split(':')
				indi,indi_desc=i[0],' '.join(i[1:])
				indi_desc=' '.join(indi_desc.strip().split()) #remove \n
				master[lastg]['targets'][lastt]['indicators'][indi]={'desc':indi_desc,'val':[]}
				lastindi=indi
		else:
			#pass
			if row[0].lower()=='National Indicator is under development'.lower():
				master[lastg]['targets'][lastt]['indev']=True
			else:	
				master[lastg]['targets'][lastt]['indicators'][lastindi]['val'].extend(row[2:])
		
with open(sys.argv[1].replace('.csv','.json'), "w") as write_file:
	json.dump(master, write_file)			
		
