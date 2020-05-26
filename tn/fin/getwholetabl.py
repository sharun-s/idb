import camelot, locale, sys
from locale import atof
locale.setlocale(locale.LC_NUMERIC, '')
import pandas as p

fname=sys.argv[1]
pg=sys.argv[2]
startrow=int(sys.argv[3]) 
outfile=sys.argv[4]
endrow=-1 if len(sys.argv) <=5 else int(sys.argv[5])
cols=[2,4] if len(sys.argv) <=6 else [int(i) for i in sys.argv[6].split(',')]

print(startrow,endrow,cols)

tables=camelot.read_pdf(fname,pages=pg)
result=tables[0].df[cols][startrow:endrow].applymap(lambda x:atof(x) if x else None)
print(result)
p.DataFrame(result).to_csv(outfile,mode='a',header=False,index=False)

# merge=[]
# for i in range(0,len(tables)):
# 	merge.append(tables[i].df[[2,4]][startrow:].applymap(lambda x:atof(x) if x else None))

# merged=p.concat(merge,axis=1)
# merged.to_csv(r'data/cag/csv/'+sys.argv[4]+'.csv',index=False,header=False)

