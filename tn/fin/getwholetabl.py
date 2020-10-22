#!/usr/bin/env python3
import camelot, locale, sys
from locale import atof
locale.setlocale(locale.LC_NUMERIC, '')
import pandas as p
import numpy as np
import argparse
parser = argparse.ArgumentParser(description='Basic Table extract from pdf')
parser.add_argument('infile', help='input pdf filename')
parser.add_argument('pages', help='page number eg:2 3-19 (camelot format)')
parser.add_argument('startrow', type=int, help='int usually passed to skip header rows')
parser.add_argument('-endrow', default=-1,type=int, help='int passed to skip footerrows. Default is -1 ie last row')
parser.add_argument('--cols',default="1,2", help='columns comma seperated')
parser.add_argument('-tableno', type=int, default=0, help='table number if more than 1 table in page. Default 0')
parser.add_argument('outfile', help='output filename specify extn')

args = parser.parse_args()
print(args)
cols=[int(i) for i in args.cols.split(',')]

tables=camelot.read_pdf(args.infile,pages=args.pages)
# multipage requires merge
if args.pages:#pg.find('-') > 0:
	merge=[]
	for i in range(0,len(tables)):
		#merge.append(tables[i].df[[2,4]][startrow:].applymap(lambda x:atof(x) if x else None))
		for j in cols:
			tmp=tables[i].df
			#print(tmp.dtypes)
			if tmp[j].dtypes == np.object:
				try:
					tmp[j]=tmp[j].apply(lambda x:atof(x) if x else None)
				except ValueError as e:
					print(e)
					continue
				
		merge.append(tables[i].df[cols][args.startrow:])#.applymap(lambda x:atof(x) if x else None))
	merged=p.concat(merge,axis=1)
	merged.to_csv(args.outfile,index=False,header=False)
else:
	#tno=int(args.tno) # 0 - top table 1 bottom tabl
	result=tables[args.tno].df[cols][args.startrow:args.endrow].applymap(lambda x:atof(x) if x else None)
	print(result)
	p.DataFrame(result).to_csv(args.outfile,mode='a',header=False,index=False)
