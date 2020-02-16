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

dash=None 
# cumulative freq - similar to accumulating structure below
def cf(df=dash, x='year', y='place', include_only=['Delhi','Maharashtra','Tamil Nadu'], exclude=['Delhi','Maharashtra','Tamil Nadu','West Bengal','Karnatake']):
	# 1 using groupby area year - unnecessary
	#g.place.value_counts().unstack()[state].unstack().cumsum().ffill().plot()
	if include_only:
		return df.groupby(x)[y].value_counts().unstack().cumsum()[include_only]		
	if exclude:
		return df.groupby(x)[y].value_counts().unstack().cumsum()[lambda x:x.columns.difference(exclude)].ffill()

# find specific title
# eg facet(tn,'name','Gen.').sort_values('place')
def facet(df, prop='place',val="Tamil Nadu"):
	return df[df[prop].str.contains(val)]

def stripTitles(df):
	return df['name'].str.replace(titles,'')

def getTitles(df):
	# str[1] is a bit of a hack cuz where no recognizable title exists array will contain the whole name eg [Prabhu Deva] doing a str[1] makes it Nan
	return df['name'].str.split('('+gtitles+')').str[1]

#TODO if too many uniq vals in prop with low counts show top 10
def structure(df, prop, perc=False):
	if perc:
		return df[prop].value_counts(normalize=True)
	else: 
		return df[prop].value_counts() #.plot(kind='bar')

# include_only has prop values not group values
# eg: s=strc(all_women, 'area', 'place', ['Delhi', 'Maharashtra', 'Tamil Nadu', 'Uttar Pradesh', 'West Bengal'])
# s.plot.pie(subplots=True, legend=False, layout=(5,1), figsize=(8,4))
# s.plot(kind='bar')
def structureOfGroup(df, group, prop, include_only=[]):
	if include_only:
		return df.groupby(x)[y].value_counts().unstack()[include_only]
	else:
		alllabels=df[prop].value_counts().index.tolist()
		return df.groupby(x)[y].value_counts().unstack()[alllabels]
	
def accumulatingStructOfGroup(df, group, prop, include_only):
	return structureOfGroup(df, group, prop, i).cumsum().ffill()

def change(df, prop):
	return structureOfGroup(df, 'year', prop).cumsum().ffill()

facet_name=lambda df,regex:facet(df, 'name', regex)
get_women=lambda df:facet_name(df, re_women)
get_mil=lambda df:facet_name(df, "|".join[brckt(re_mil), brckt(re_af), brckt(re_navy)])
get_af=lambda df:facet_name(df, re_af)
get_navy=lambda df:facet_name(df, re_navy)
get_rel=lambda df:facet_name(df, '|'.join([brckt(re_rel_h), brckt(re_rel_m), brckt(re_rel_c)]))
get_prof=lambda df:facet_name(df, re_prof)
get_dr=lambda df:facet_name(df, re_med)
get_dead=lambda df:facet_name(df, 'Late|Posthu')
get_royal=lambda df:facet_name(df, re_royal)

#def getNamesWithUnrecognized_NO_Titles(df):
#	return df['name'].str.split('('+titles+')').str[0].value_counts()  

l=loadfile('dashboard-padmaawards_gov_in_get_data', evaluate=True)
dash=createDataFrame(l)

dash['titles']=getTitles(dash)

tn=facet(dash, 'place', 'Tamil Nadu')

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
# women - 861
# w=facet(dash, 'name', re_women)
# another way to get unrecognized titles
# dash[dash['titles'].isna()][['name', 'titles']]

# look at percentages
# dash['titles'].value_counts(normalize=True, dropna=False) 
