#find and replace overflowing descriptions
findoflow = r",([\"\w '\-/\.\(\)]+),{5,6}\n([\"a-z '\-/\.\(\)]+,{5,6}.*)"
replaceoflow = r",\g<1> \g<2>"

common_overflow={
'"Clothing, Tentage and"':['Stores'],
'Clothing, Tentage and':['Stores'],
'"Expenses on Conducted"':['Tours'],
'Expenses on Conducted':['Tours'],
'"Payments for"':['Professional and Special','Services'],
'Payments for':['Professional and Special','Services'],
'"Petroleum, Oil and"':['Lubricant'],
'Petroleum, Oil and':['Lubricant'],
'"Purchase  of  Books &"':['Periodicals to Libraries', '"etc.,"'],
#'"Purchase  of  Books &"':'Periodicals to Libraries',
'"Scholarships and"':['Stipends'],
'"Service Postage & Postal"':['Expenditure'],
'Service Postage & Postal':['Expenditure'],
'"Tour Travelling"':['Allowances'],
'Tour Travelling':['Allowances'],
'"Transfer Travelling"':['Allowances'],
'Transfer Travelling':['Allowances'],
'Advertising and':['Publicity'],
'City Compensatory':['Allowance'],
'Expenses on Conducted':['Tours'],
'Grants for Creation of':['Capital Assets'],
'Grants for Current':['Expenditure'],
'Grants for Specific':['Schemes'],
'Maintenance of':['Functional Vehicles'],
'Other Compensations  -':['Voted'],
'Purchase  of  Books &':['Periodicals to Libraries','etc.,'],
'Recoveries of':['Overpayments /','Remittance of excess','drawals'],
'Scholarships and':['Stipends'],
'Service or Commitment':['Charges'],
'T.A./D.A.to Non-Official':['Members'],
'Cost of Books/Note':['Books/Slates, etc.'],
'Procurement of':['Agricultural Inputs'],
'Fixed Travelling':['Allowances'],
'Hospitality /':['Entertainment','Expenditure'],
'Claims under no fault':['liability -  principal'],
'Purchase and Upkeep of':['Animals'],
'Contribution to Specific':['Fund']
}

import pandas as p
import json,csv,pprint,sys
import locale
locale.setlocale(locale.LC_NUMERIC, '')
#f=open('meta_Heads_simple.json')  
#h=json.load(f)
#f.close()

#ValueError: csv:/home/s/idb/tn/fin/data/expenditure/d4-004-02-v1.csv Error tokenizing data. C error: Expected 7 fields in line 248, saw 8

try:
	df=p.read_csv(sys.argv[1])#,comment='#')
except p.errors.ParserError as e:
	#print()
	raise ValueError("csv:"+sys.argv[1]+' '+e.args[0])
#print("csv:",sys.argv[1])
parent_tree={}
dropindexes=[]
i=0
se=0
#print(df.head())
while True:
	try:
		head=df.iloc[i]['head'].split('-')[0]
		desc=df.iloc[i]['desc'] if not p.isnull(df.iloc[i]['desc']) else head+' MISSING Desc' 
	except AttributeError as e:
		#print('head was prob nan chk desc',i,df.iloc[i])
		raise ValueError("csv:"+sys.argv[1]+" in line "+str(i))
	#if head=="State's Expenditure,,,,,":
	#	df.iloc[i]['head']="#State's Expenditure"
	#	df.iloc[i]['desc']=""

	data=df.iloc[i][['2018', '2019Est', '2019Rev', '2020Est']]
	if 'dpcode' in df.columns:
		dpcode=df.iloc[i]['dpcode']
	else:
		dpcode=None

	if desc in common_overflow:
		print('found ',desc,i)
		#check next lines
		cnt=1
		todel=common_overflow[desc]
		for j in common_overflow[desc]:
			if df.iloc[i+cnt]['head'] == j:  
				print('    appending', j, ' to ', desc)
				desc=desc+' ' + j
			else:
				raise ValueError("csv:"+sys.argv[1]+' in line '+str(i+2))
			cnt=cnt+1
		cnt=1
		for j in todel:
			dropindexes.append(i+cnt)
			cnt=cnt+1
		df.iloc[i]['desc']=desc
	# elif desc.replace(' Charged','') in common_overflow:
	# 	tmpdesc=desc.replace(' Charged','')
	# 	print('found ',desc,i)
	# 	cnt=1
	# 	todel=common_overflow[tmpdesc]
	# 	for j in common_overflow[tmpdesc]:
	# 		if df.iloc[i+cnt]['head'] == j:  
	# 			print('    appending', j, ' to ', tmpdesc)
	# 			tmpdesc=tmpdesc+' ' + j
	# 		else:
	# 			raise ValueError("csv:"+sys.argv[1]+' in line '+str(i+2))
	# 		cnt=cnt+1
	# 	cnt=1
	# 	for j in todel:
	# 		dropindexes.append(i+cnt)
	# 		cnt=cnt+1
	# 	df.iloc[i]['desc']=tmpdesc+' Charged'
	# 	print('updating df')
	i=i+1
	if i>=len(df):
		break

df=df.drop(dropindexes)
df.to_csv(sys.argv[1],index=False)	