import json
import sys

# Convert JSON tree to a Python dict
with open(sys.argv[1]) as fp:
	data = json.load(fp)

# Extract tree edges from the dict
edges = []
rmbrkt=lambda x:x.replace('(','').replace(')','').replace('.','').replace('-','')
nodes={}
cnt=0
def get_edges(treedict, parent=None):
	for child in treedict.keys():
		if isinstance(treedict[child], dict):
			get_edges(treedict[child], parent=child)
		if parent!=None:
			if parent not in nodes:
				nodes[parent]='n'+str(len(nodes))
			if child not in nodes:
				nodes[child]='n'+str(len(nodes))
			edges.append((nodes[parent],nodes[child]))

get_edges(data)#["CONSOLIDATED FUND – REVENUE"])
print('graph g {');
#print('graph [rankdir = "LR", nodesep=0.1, ranksep=0.3];');
#print('graph [ nodesep=0.1, ranksep=0.3];');
print('node [fontsize = "16", shape = "record", height=0.1, color=lightblue2];');
print('edge [];');

#print('strict digraph tree {')
for node in nodes:
	print(nodes[node] + '[label="' + node + '"];');
for row in edges:
    print('    {0} -- {1};'.format(*row))
print('}')