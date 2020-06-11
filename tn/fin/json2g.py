import json
import sys

with open(sys.argv[1]) as fp:
	data = json.load(fp)

edges = []
rmbrkt=lambda x:x.replace('(','').replace(')','').replace('.','').replace('-','')
nodes={}
cnt=0
uptolevel=int(sys.argv[2])  
def get_edges(treedict, parent=None,level=0):
	for child in treedict.keys():
		if parent!=None:
			if parent not in nodes:
				nodes[parent]=str(level)+'_'+str(len(nodes))
			if child not in nodes:
				nodes[child]=str(level+1)+'_'+str(len(nodes))
			edges.append((nodes[parent],nodes[child]))
		if isinstance(treedict[child], dict):
			get_edges(treedict[child], parent=child,level=level+1)

get_edges(data,'Major Heads')#["CONSOLIDATED FUND – REVENUE"])
print('graph g {');
print('graph [rankdir = "LR", nodesep=0.1, ranksep=0.3];');
#print('graph [ nodesep=0.1, ranksep=0.3];');
print('node [fontsize = "24!",splines="ortho", shape = "record", height=0.1, color=lightblue2];');
print('edge [];');

#print('strict digraph tree {')
for node in nodes:
	if int(nodes[node].split('_')[0]) < uptolevel: 
		print('"'+nodes[node] + '"[label="' + node.capitalize() + '"];');
for row in edges:
	if int(row[1].split('_')[0]) < uptolevel:
		print('    "{0}" -- "{1}";'.format(*row))
print('}')