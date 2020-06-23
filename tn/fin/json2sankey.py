import json, sys, re
import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey

# fig = plt.figure(figsize=(15,10))
# ax = fig.add_subplot(1, 1, 1, xticks=[], yticks=[],
#                     title="")

# sankey = Sankey(ax=ax, 
#                 scale=0.0000001, 
#                 offset= 0.1,
#                 format = '%d')


with open(sys.argv[1]) as fp:
	data = json.load(fp)

edges = []
rmbrkt=lambda x:x.replace('(','').replace(')','').replace('.','').replace('-',' ')
stripbullets=lambda x:re.sub("^[A-Za-z][ \.]+","",x)
nodes={}
cnt=0
uptolevel=int(sys.argv[2])  
def get_edges(treedict, parent=None,level=0):
	if level > uptolevel:
		return
	for child in treedict.keys():
		if parent!=None:
			if str(level)+'_'+parent not in nodes:
				nodes[str(level)+'_'+parent]=parent
			if child not in nodes:
				nodes[str(level+1)+'_'+child]=child
			edges.append((nodes[str(level)+'_'+parent],nodes[str(level+1)+'_'+child]))
		if isinstance(treedict[child], dict):
			get_edges(treedict[child], parent=child,level=level+1)

#get_edges(data,'Funds')
get_edges(data["CONSOLIDATED FUND – REVENUE"])

#nodes1={}
#for node in nodes:
#	if int(nodes[node].split('_')[0]) < uptolevel: 
#		nodes1[nodes[node]]= node.capitalize()

for row in edges:
	if int(row[1].split('_')[0]) < uptolevel:
		print('{0} [5] {1}'.format(rmbrkt(stripbullets(nodes1[row[0]])).strip().capitalize(), 
			stripbullets(rmbrkt(nodes1[row[1]])).strip().capitalize()))
		#sankey.add(labels=[rmbrkt(nodes1[row[0]].capitalize()), rmbrkt(nodes1[row[1]].capitalize())],flows=['1', '-1'])

#sankey.finish()		