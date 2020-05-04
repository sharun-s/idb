import requests as r
import sys
from bs4 import BeautifulSoup
import pandas as pd

#url =r'https://easy.nic.in/civilListIAS/YrPrev/QryProcessCL.asp'
#data={'HidQryNum':1,'CboCadre':00,'CboBatch':9999,'txtName':sys.argv[1],'Submit':'Submit'}
#print(data)
#x=r.post(url, data=data)
f=open(sys.argv[1])
x=f.read()
f.close()
page=BeautifulSoup(x,'html.parser')

tables=page.findAll('table')
if len(tables) ==0:
	sys.exit(1)

df=pd.read_html(str(tables[0]),header=0)[0]

k=df['Name Identity No.Dt. of Appointment Source of Recruitment IntraIAS User-Id'].str.split(r"(.*)Id No\.(.*);(.*)")
df['ID']=k.str[2].str.split(r"(\d{2}/\d{2}/\d{4})").str[0]
df['Appointment Date']=k.str[2].str.split(r"(\d{2}/\d{2}/\d{4})").str[1]
df['Name']=k.str[1]
df['Path']=k.str[3].str.split(r"([A-Z]+)", expand=True)[0]
df['Date of Birth']=df['Date of BirthAllotment YearCadre & Domicile'].str.split(r'(\d{2}/\d{2}/\d{4})').str[1]

k=df['Date of BirthAllotment YearCadre & Domicile'].str.split(r'(\d{2}/\d{2}/\d{4})').str[2].str.split('(.*);([A-Z]{2})(.*)')
df['Allotment Year']=k.str[1]
df['Cadre']=k.str[2]
df['Domicile']=k.str[3]

k=df['Present PostWith Effect From'].str.split(r'(\d{2}/\d{2}/\d{4})')
df['Present Post']=k.str[0]
df['With Effect From']=k.str[1]

df=df.drop(['Name Identity No.Dt. of Appointment Source of Recruitment IntraIAS User-Id','Date of BirthAllotment YearCadre & Domicile','Present PostWith Effect From','Sl.No.','Photo'],axis=1)

l=tables[0].findAll('a')
li=[(i['href'],i.text.replace('Id No. ','')) for i in l]
df2=pd.DataFrame(li)
df2.columns=['url','ID']
df2['ID']=df2['ID'].str.strip()
df['ID']=df['ID'].str.strip()
df=pd.merge(df, df2, on='ID')

df.to_csv(sys.argv[1].replace('.html','.csv'),index=False)
#rows=tables[0].findAll('tr')

# header=[]
# for i in rows[0]:
# 	header.append(i.text)

# data={}
# rowcnt=0
# for row in rows[1:]:
# 	data[rowcnt]=[]
# 	for col in row:
# 		data[rowcnt].append(col)
# 	rowcnt=rowcnt+1

