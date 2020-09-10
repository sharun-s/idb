import camelot, locale, sys
from locale import atof
locale.setlocale(locale.LC_NUMERIC, '')
import pandas as p
from os import listdir
import subprocess

#rm old files
try:
	subprocess.run(r'rm tn-cag-maintable.csv',shell=True)
except Exception as e:
	pass

state=sys.argv[1]
pg='1-2'#sys.argv[2]
startrow=int(sys.argv[2]) 
states=p.read_csv('States')
dirname=r'/home/s/idb-stash/tn-budget-docs/cag/'+states.cagdir.iloc[states[states['prefix']==state].index[0]]
allfiles=listdir(dirname)
#allfiles=[i for i in allfiles if len(i) < 10]
outfile=state+'-cag-maintable.csv'

#endrow=-1 if len(sys.argv) <=5 else int(sys.argv[5])
firsttime=True
for i in allfiles:
	Year=i[:4]
	Month=i[4:i.find('.pdf')]
	print(Year, Month)
	tables=camelot.read_pdf(dirname+'/'+i,pages=pg)
	if firsttime:
		labels=tables[0].df.iloc[startrow:][0].append(tables[1].df.iloc[0:][0]).append(p.Series(['Year','Month']))
		p.DataFrame(labels.str.replace('\n',',')).T.to_csv(outfile,mode='a',header=False,index=False)
		firsttime=False
	if Month.find('4')>-1:
		estimate=tables[0].df.iloc[startrow:][1].append(tables[1].df.iloc[0:][1]).apply(lambda x:x.replace(' ','')).apply(lambda x:atof(x) if x and x!='..' and x!='$' else None).append(p.Series([int(Year),9999]))
		p.DataFrame(estimate).T.to_csv(outfile,mode='a',header=False,index=False)

	actual=tables[0].df.iloc[startrow:][2].append(tables[1].df.iloc[0:][2]).apply(lambda x:x.replace(' ','')).apply(lambda x:atof(x) if x and x!='..' and x!='$' else None).append(p.Series([int(Year),int(Month)]))
	if int(actual.iloc[1])== int(actual.iloc[2:9].sum()) and len(labels) == len(actual):
		#assert len(actual) == len(estimate)
		p.DataFrame(actual).T.to_csv(outfile,mode='a',header=False,index=False)
	

