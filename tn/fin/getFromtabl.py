import camelot, locale, sys
from locale import atof
locale.setlocale(locale.LC_NUMERIC, '')
import pandas as p

fname=sys.argv[1]
pg=sys.argv[2]
startrow=int(sys.argv[3]) 
tables=camelot.read_pdf(fname,pages=pg)

result=tables[0].df.iloc[startrow:][3].apply(lambda x:atof(x) if x else None)
print(result)
p.DataFrame(result).T.to_csv(sys.argv[4],mode='a',header=False,index=False)

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
