import pandas as p
from pandas.api.types import CategoricalDtype
from titles import *
#import readline
#readline.write_history_file('/home/s/idb/idb-panda.log')

def loadfile(name, evaluate=False):
    with open(name) as f:
        if evaluate:
            data=eval(f.read())
        else:
            data=f.read()
    return data

def createDataFrame(data):
	dash=p.DataFrame(data)
	dash=dash.drop('id', axis='columns')
	dash['name']=dash['name'].str.strip()
	dash['place']=dash['place'].str.strip()
	acat=dash['award'].value_counts().index.tolist()
	acat.reverse()
	dash['award']=dash['award'].astype(CategoricalDtype(categories=acat, ordered=True))
	dash.place=dash.place.str.strip()
	#locs=CategoricalDtype(categories=dash.place.value_counts().index.tolist())
	#dash.place=dash.place.astype(locs)
	dash.area=dash.area.astype(CategoricalDtype(categories=dash.area.value_counts().index.tolist()))
	return dash

#def cf():
#g=dash.groupby(['area','year'])

# 1 cum freq of each area over time
#gd=g.describe()
#gd['award','count'].unstack().transpose().cumsum().ffill().plot()

# 2 - same as 1 without describe
#g.agg({'award':lambda x:len(x)}).unstack().transpose().cumsum().ffill().plot()

# 3 - same as 2 without g
#dash.groupby(['year','area']).agg({'award':lambda x:len(x)}).unstack()['award'].cumsum().ffill().plot()
	#return g.award.value_counts().unstack().cumsum().ffill().plot()
	# 4 using pivot_table - SLOW!!
	# dash.pivot_table(index=['year'],columns=['place'],aggfunc=len)
# 5 - groupby year - no need for area, year
	# dash.groupby(['year']).place.value_counts().unstack().cumsum()[['Delhi','Maharashtra']].plot()
	# dash.groupby(['year']).place.value_counts().unstack().cumsum()[lambda x:x.columns.difference(['Delhi','Maharashtra','Tamil Nadu','West Bengal','Karnatake'])].ffill()

# freq distribution
def fd(prop='place',top=10):
	return dash[prop].value_counts()[:top]

# cumulative freq
def cf(df=dash, x='year', y='place', include_only=['Delhi','Maharashtra','Tamil Nadu'], exclude=['Delhi','Maharashtra','Tamil Nadu','West Bengal','Karnatake']):
	# 1 using groupby area year - unnecessary
	#g.place.value_counts().unstack()[state].unstack().cumsum().ffill().plot()
	if include_only:
		return df.groupby(x)[y].value_counts().unstack().cumsum()[include_only]		
	if exclude:
		return df.groupby(x)[y].value_counts().unstack().cumsum()[lambda x:x.columns.difference(exclude)].ffill()

def facet(df, prop='place',val="Tamil Nadu"):
	return df[df[prop].str.contains(val)]

def stripTitles(df):
	return df['name'].str.replace(titles,'')

def getTitles(df):
	# str[1] is a bit of a hack cuz where no recognizable title exists array will contain the whole name eg [Prabhu Deva] doing a str[1] makes it Nan
	return df['name'].str.split('('+gtitles+')').str[1]

def getNamesWithUnrecognized_NO_Titles(df):
	return df['name'].str.split('('+titles+')').str[0].value_counts()  

l=loadfile('dashboard-padmaawards_gov_in_get_data', evaluate=True)
dash=createDataFrame(l)

alltitles=getTitles()
alltitles.value_counts(normalize=True)
alltitles.value_counts(dropna=False) # check NA found
# find specific title
filter('name','Gen.').sort_values('place')
# women - 861
women=filter('name', )

# dash.place.value_counts()[:6]
# Delhi            810
# Maharashtra      786
# Tamil Nadu       413
# Uttar Pradesh    314
# West Bengal      274
# Karnataka        255
# Name: place, dtype: int64
# >>> dash.place.value_counts()[:6].sum()
# 2852
# >>> dash.place.value_counts().sum()
# 4615
# >>> 2852/4615
# 0.6179848320693391
# >>> dash.place.value_counts()[:10].sum()
# 3421
# >>> 2421/4615
# 0.5245937161430119
# >>> 3421/4615
# 0.7412784398699892