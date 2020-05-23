import matplotlib.pyplot as plt
import sys
import pandas as p
from itertools import cycle

states=p.read_csv('States')
m=['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar-P', 'Mar-S']
master=[]
for s in range(0,len(states)):
	df=p.read_csv(r'data/cag/csv/'+states.prefix.iloc[s]+sys.argv[1],header=None,comment='#')
	if len(df) == 0:
		print(states.prefix.iloc[s] + 'no data found')
		sys.exit()
	df['month']=m[:len(df)]
	df['State']=states.name.iloc[s]
	master.append(df)

master=p.concat(master, ignore_index=True, sort=False)
master=master.rename(columns={0:'GST',1:'Stamp',2:'Land',3:'Sales',4:'Excise',5:'ShareOfUnion',6:'Other'})
cats=['GST','Stamp','Sales','Excise','ShareOfUnion','Other']
colors=["#ffc107","#33ccff",'#F95733','#00ff88','#F9e792',"#ff1122",'#A6E22E']

#ignore kerala
tmp=states.drop(2)
for s in range(0,len(tmp)):
	df=p.read_csv(r'data/cag/csv/'+tmp.prefix.iloc[s]+'-ntr.csv',header=None,comment='#')
	idx=master[master['State']==tmp.name.iloc[s]][7].index
	master.loc[idx,7]=df[0].values

for s in range(0,len(tmp)):
	df=p.read_csv(r'data/cag/csv/'+tmp.prefix.iloc[s]+'-grants.csv',header=None,comment='#')
	idx=master[master['State']==tmp.name.iloc[s]][8].index
	master.loc[idx,8]=df[0].values

master=master.rename(columns={7:'NTR',8:'Grants'})