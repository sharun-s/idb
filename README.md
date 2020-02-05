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
6. Relationship graph of props+values 
7. Time graph 

v1 - spagetti code to work out patterns required  
v2 - identify and replace sections where possible with pandas functionality
v3 - optimize for minimal operator involvement

Gates -   
Mapper issues - spelling, title, prefix, suffix, abbr, initials, space issues  
Entities missing and overlaps requiring special merge  
Props missing and overlaps requiring special merge. 
  Example props from 2 datasets: prop:prize, type:str <> prop:awards type:list

**History**
1. Datasource - Initially awards list was pulled from a pdf 
2. Imported into openrefine for cleanup
3. Some cleanup happened - title stripping - filtering > tn only - manual spell correction to get wikidata ids 
4. reflect.py - round about method to pull the wikidata ids into refine, when refine had the IDs in recon object and column could have been produced based on that
5. Then question became how to get _all available props_ for each entity available in wikidata/wikipedia infobox/wikipedia article content
6. Different scripts where produced to create prop list from local zimfile article content OR just infobox - awards2info, ib, dumpib.sh, inspecttabs, check.sh 
7. getWikidata.py - sample code using qwikidata to get a single entity from wikidata
8. qwikidata was modified to use media wiki api, rather than the linked data api, cause it allows 50 entities at a time to be retrieved as opposed to one at a time
7. dumpprops.py - Getting all the props available in wikidata required maintaining meta info on each prop - ie if the prop pointed at string no prob - if it pointed at a dict or another wikidata entity or list of wikidata entities - a second query to get that value was required - dumpprops.py handles this retrieval
9. Index of prop values were built using imine.py
10. Mistake here was all available prop values should have been merged into cleaned data in refine - it would have shown lot of missing entities
11. Merge of data produced in 3 and 7 required a satisficing automated mapper/reconcile/disambiguation mechanism - and manual checks of results
12. Mistake at this stage another datasource was found - json from dashboard - step 1/2/3 was forgotten about and merge was attempted with data from 7 - redoing lot of work that was done in step 3/4 to map govt data-wikidata via name of person - spelling - title stripping - abbr/space/prefix/suffix/spelling variations 
13. New Design requires 
  - [ ] handle N sources - update can happen constantly - 
  - [ ] each source has entitites - each entity has props - 
  - [ ] create unified data - overlaps and new content in all sources are handled using mapper interface 
  - [ ] mapper interface reconciles not just IDs across sources but same prop expressed differently across sources 
    - eg awards recevied in one is a list of str and another is a list of dicts 
  - [ ] produce a indexes/counts for all known prop+value combos from all sources.
