#! /usr/bin/env python3
from qwikidata.linked_data_interface import get_entity_dict_from_api
from qwikidata.entity import WikidataItem, WikidataProperty
import sys

q=get_entity_dict_from_api(sys.argv[1])
w=WikidataItem(q)

c=w.get_claim_groups()

for i in c:
	prop = WikidataProperty(get_entity_dict_from_api(i))
	#print(i, prop.get_label(), len(c[i]))
	print(prop.get_label())
	for j in range(0,len(c[i])):
		dv=c[i][j].mainsnak.datavalue
		if isinstance(dv.value, dict) and 'id' in dv.value:  
			qid = dv.value["id"]
			entity = WikidataItem(get_entity_dict_from_api(qid))
			print(entity.get_label())
		else:
			print(dv.value) 
	

# for pid, quals in claim.qualifiers.items():
#     prop = WikidataProperty(get_entity_dict_from_api(pid))
#     for qual in quals:
#         if qual.snak.snaktype != "value":
#             continue
#         else:
#             print(f"{prop.get_label()}: {qual.snak.datavalue}")
