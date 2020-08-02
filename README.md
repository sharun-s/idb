TN budget - https://sharun-s.github.io/idb/tn/fin/basic_explorer.html

Given N updating data sources - dashboard - pdfs - wikidata - zimfile etc., create unified indexes of entities and props from all sources. Philosophy here is to automate as many steps and pull in operator only to disambiguate. 

**Goal**
1. Add Record/Update mechanism as new data from Source(s) becomes available to Target db  
2. Entity Mapper between Source(s) and Target (Reconciliation/Disambiguation) based on single or multiple props 
  eg: 
    name in dashboard > wikidata, 
    name in wikidata > dashboard etc
    name variation generator -> suggestion api -> false positive check -> false neg check
3. Property Mapper between Source(s) and Target 
  exists in one missing in another
  exitsts in both but types differ - str <> list, str <> sub str, date <> str etc   
4. Index creation based on all prop values  
5. Enable command line autocomplete of source.prop.value for quick querying/exploration/debug
6. Relationship graph of props+values - Hierarchical/Networks 
7. Time series handling/graphing 

v1 - spagetti code to work out patterns required  
v2 - identify and replace sections where possible with pandas functionality  
v3 - optimize for minimal operator involvement

Gates -   
Mapper issues - spelling, title, prefix, suffix, abbr, initials, space issues  
Entities missing and overlaps requiring special merge  
Props missing and overlaps requiring special merge. 
  Example props from 2 datasets: prop:prize, type:str <> prop:awards type:list

See wiki for case wise history
