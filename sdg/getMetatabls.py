import camelot, locale, sys
from locale import atof
locale.setlocale(locale.LC_NUMERIC, '')
import pandas as p

fname=sys.argv[1]
pgs=sys.argv[2] #eg '86-95'
startrow=int(sys.argv[3])
outfile=sys.argv[4] 
master=[]
tables=camelot.read_pdf(fname,pages=pgs)
for i in range(0,len(tables)): 
	header=tables[i].df[0][0]#.split(':')
	print(header)
	result=tables[i].df.iloc[startrow:].copy(deep=True)
	if len(result)==24:
		master.append(result[2][1:11].values)
		master.append(result[2][14:24].values)
	elif len(result)==37:
		master.append(result[2][1:11].values)
		master.append(result[2][14:24].values)
		master.append(result[2][27:37].values)
	else:
		print(i,'??? ',len(result))
		master.append(result[2][1:11].values)

meta=p.DataFrame(master,columns=['Goal', 'Target', 'Indicator', 'Desc', 'Source', 'Data Reference Period', 'Periodicity', 'Unit of Measurement', 'Latest Data Availability', 'url'])
meta.to_csv(outfile,index=False)