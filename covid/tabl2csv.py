import camelot
import sys

fname=sys.argv[1]
pageno=sys.argv[2]
tables=camelot.read_pdf(r'/home/s/Downloads/covid/pdfs/'+fname,pages=pageno)

#tables[0].df['d']=fname.replace(".pdf",'')
tables[0].df.insert(0, 'd', fname.replace(".pdf",''))
tables[0].df.to_csv(r'/home/s/Downloads/covid/'+pageno+'_'+fname+'.csv',index=False,header=False)