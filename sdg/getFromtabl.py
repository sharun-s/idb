import camelot, locale, sys
from locale import atof
locale.setlocale(locale.LC_NUMERIC, '')
import pandas as p

fname=sys.argv[1]
pg=sys.argv[2]
startrow=int(sys.argv[3]) 


#outfile=sys.argv[4]
#endrow=-1 if len(sys.argv) <=4 else int(sys.argv[4])

tablenoInpage=0 if len(sys.argv) <=4 else int(sys.argv[4])


#table_areas=['83,730,420,708']
#t=camelot.read_pdf(fname,pages=pg,flavor='stream',table_areas=table_areas)
#header=t[0].df[0][0].split(":")
#outfile=header[0].replace('.','').replace(' ','')
#print(header[1]) 

for i in range(int(pg),int(pg)+25): 
	tables=camelot.read_pdf(fname,pages=str(i))
	header=tables[tablenoInpage].df[0][0].split(':')
	outfile=header[0].replace('.','').replace(' ','')
	print(header[1]) 
	# Ask user to specify simple file name
	suffix=input('Desc: '+outfile+" Suffix:")
	#not removing last row cause it has source
	result=tables[tablenoInpage].df.iloc[startrow:].copy(deep=True)
	result.iloc[0]=result.iloc[0].str.replace('\n','').str.capitalize()

	print(result.head(3))
	result.to_csv(outfile+'_'+suffix+'.csv',mode='w',header=False,index=False)

