import pandas as p
from pandas.api.types import CategoricalDtype
#import readline
#readline.write_history_file('/home/s/idb/idb-panda.log')

f=open('dashboard-padmaawards_gov_in_get_data')
l=f.read()
f.close()
l=eval(l)

dash=p.DataFrame(l)
dash=dash.drop('id', axis='columns')

acat=dash['award'].value_counts().index.tolist()
acat.reverse()
dash['award']=dash['award'].astype(CategoricalDtype(categories=acat, ordered=True))

dash.place=dash.place.str.strip()
dash.place=dash.place.astype(CategoricalDtype(categories=dash.place.value_counts().index.tolist()))

dash.area=dash.area.astype(CategoricalDtype(categories=dash.area.value_counts().index.tolist()))

g=dash.groupby(['area','year'])

# 1 cum freq of each area over time
#gd=g.describe()
#gd['award','count'].unstack().transpose().cumsum().ffill().plot()

# 2 - same as 1 without describe
#g.agg({'award':lambda x:len(x)}).unstack().transpose().cumsum().ffill().plot()

# 3 - same as 2 without g
# dash.groupby(['year','area']).agg({'award':lambda x:len(x)}).unstack()['award'].cumsum().ffill().plot()

# 4 cumfreq of each area over time for a particular state - Tamil Nadu
dash.groupby(['year','area']).place.value_counts().unstack()['Tamil Nadu'].unstack().cumsum().ffill().plot()