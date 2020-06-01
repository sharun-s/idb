import camelot
#import matplotlib.pyplot as p
#to determine table areas
#camelot.plot(t[0], kind='text')
#camelot.plot(t[0], kind='grid')

t=camelot.read_pdf('../fin/data/2021budget_detailed_rev_receipts.pdf',pages='54-61',flavor='stream',table_areas=table_areas)

table_areas=['116,732,567,108']

for i in range(0,len(t)):
	t[i].df.to_csv(str(i)+'.csv',index=False)

#cat all csvs into rev_receipts.csv
#replace /^,//
#replace /(0039 \d\d \d\d\d \w\w \d{5})/","\1/
#replace /^,(\d+) (\w)/,\1,\2