import camelot, locale, sys
from locale import atof
locale.setlocale(locale.LC_NUMERIC, '')
from os import listdir
import pandas as p

state=sys.argv[1]
pg=sys.argv[2]
startrow=int(sys.argv[3]) 
outfile=r'data/cag/csv/'+state+sys.argv[4]
endrow=-1 if len(sys.argv) <=5 else int(sys.argv[5])
col=3 if len(sys.argv) <=6 else int(sys.argv[6])

states=p.read_csv('States')
dirname=r'data/cag/'+states.cagdir.iloc[states[states['prefix']==state].index[0]]
fnames=["201904.pdf","201905.pdf","201906.pdf","201907.pdf","201908.pdf","201909.pdf","201910.pdf","201911.pdf","201912.pdf","20201.pdf","20202.pdf","20203.pdf"]
m=['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar-P', 'Mar-S']

allfiles=listdir(dirname)
master=[]

for fname in fnames:
	if fname in allfiles:
		print(startrow,endrow,col, dirname+'/'+fname)
		tables=camelot.read_pdf(dirname+'/'+fname, pages=pg)
		result=tables[0].df.iloc[startrow:endrow][col]
		#p.DataFrame(result.str.replace('\n',',')).T.to_csv(outfile,mode='a',header=False,index=False)
		#result=tables[0].df.iloc[startrow:endrow][col].apply(lambda x:atof(x) if x else None)
		print(result.values)
		p.DataFrame(result).T.to_csv(outfile,mode='a',header=False,index=False)

# merge=[]
# for i in range(0,len(tables)):
# 	merge.append(tables[i].df[[2,4]][startrow:].applymap(lambda x:atof(x) if x else None))

# merged=p.concat(merge,axis=1)
# merged.to_csv(r'data/cag/csv/'+sys.argv[4]+'.csv',index=False,header=False)

#tables=camelot.read_pdf(r'/home/s/idb/tn/fin/20201.pdf',pages="1-2,17,18")
#summary=tables[0].df
#rec=tables[1].df
#exp=tables[2].df
# def cumulativeIncoming():
#   rec[4][2:11].apply(atof).plot(color='green',label='18-19',legend=True)
#   rec[2][2:11].apply(atof).plot(color='green',label='19-20',legend=True)
#   plt.show()

# def cumulativeOutgoing():
#   exp[4][2:11].apply(atof).plot(color='green',label='18-19',legend=True)
#   exp[2][2:11].apply(atof).plot(color='green',label='19-20',legend=True)
#   plt.show()
