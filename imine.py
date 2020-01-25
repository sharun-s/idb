#! /usr/bin/env python3
import sys
from datetime import datetime
import requests
from titles import *
import re, difflib

def getWikidataID(name):
    r=requests.get('https://tools.wmflabs.org/openrefine-wikidata/en/suggest/entity?prefix='+name)
    return r.json()['result'][0]

def loadfile(name, evaluate=False):
    with open(name) as f:
        if evaluate:
            data=eval(f.read())
        else:
            data=f.read()
    return data

def tofile(name, data):
    f=open(name,'w')
    f.write(str(data)) 
    f.close()

ids=[]
#run variantset before running this if untitledname isn't what is in wikidata label
def collectForDumpProps(obj):
    global ids
    result=getWikidataID(obj['untitledname'])
    obj.update( {'MyWikiDataID':result['id'], 'desc':result['description'] })
    ids.append(obj)

def variantset(i, v):
    i['variant']=i['untitledname']
    i['untitledname']=v

labelRegex=r"[ ,',.]"
#this is for lobjs
class Entity(object):
    def __init__(self,**kargs):
        for i in kargs.keys():
            setattr(self, re.sub(labelRegex,'',i), kargs[i])

class dictEntity(dict):
    def __init__(self, d):
        dict.__init__(self, d)
        for i in d:
            setattr(self, re.sub(labelRegex,'',i), d[i])

#this is for qwikidata data
class dEntity(object):
    def __init__(self, d):
        if 'en' in d['labels']:        
            setattr(self, 'labels', d['labels']['en']['value'])
        if d['descriptions'] and 'en' in d['descriptions']:
            setattr(self, 'descriptions', d['descriptions']['en']['value'])
        if d['aliases'] and 'en' in d['aliases']:
            setattr(self, 'aliases', d['aliases'])
        if d['claims']:
            setattr(self, 'claims', d['claims'])

class L(object):
    def __init__(seld, lobjs):
        for i in lobjs:
            setattr(self, re.sub(labelRegex,'',i['label']), dictEntity(i))

def flatten(l):
    aaa=[]
    for i in l:
        aaa.extend(i)
    return aaa

#given a name-wikidataid list dumpprop queries wikidata and dumps all available props into db
dumped_props=source(file='db', evaluate=True)
#both have to then be merged into a list of dicts, based on label,alias <-> name map
dumped_props.merge(file='wikidataIDs', mergefn)

def mergefn(a, b):
lines=l.split('\n')
for i in lines:
    if i.split(',')[0] not in idx['label'].keys():
        lobjs.append({'label':i.split(',')[0]})


# Map govt data names to wikidata names and merge into single dataset
statedata=source(file='dashboard-padmaawards_gov_in_get_data', dbfilter=lambda x:x['place']=='Tamil Nadu')

# file contains list of dicts - entityID to wikidata entity dict of props
# convert db to ldicts or lobjs - basically indexing it - ie lobjs[n] = someobj
s.convert_to_list_of_dicts()

allowedProps=['label', 'desc', 'wikiurl', 'occupation', 'country of citizenship', 'date of birth', 'date of death', 'member of political party', 'educated at', 'instance of', 'position held', 'place of death', 'award received', 'place of birth', 'religion', 'Commons category', 'name in native language', 'family name',  'languages spoken, written or signed', 'sex or gender', 'native language', 'writing language', 'described by source', 'MyWikiDataID', 'member of', 'given name', 'nominated for', 'field of work', 'employer', 'Google Doodle', 'notable work', 'exact match', 'doctoral student', 'military rank', 'candidacy in election', "topic's main category", 'spouse', 'sibling', 'ethnic group', 'cause of death', 'manner of death', 'official website', 'patronym or matronym for this person', 'ancestral home', 'quotation or excerpt', 'genre', 'work period (start)', 'instrument', 'number of children', 'sport', 'member of sports team', 'country for sport', 'father', 'residence', 'academic degree', 'doctoral advisor',  'child', 'handedness', 'playing hand', 'work period (end)', 'participant of', 'influenced by', 'mother', 'related category', 'chairperson', 'height',  'mass', 'prize money', 'different from', 'birth name', 'partner', 'relative', 'discography', 'filmography','owner of',  'conferred by', 'pseudonym', 'part of', 'significant event']
ignore=['Encyclopædia Universalis ID', 'Amazon author ID', 'CANTIC ID', 'SUDOC authorities ID', 'Freebase ID', 'FAST ID', 'SELIBR ID', 'Plarr ID', 'ATP player ID', 'Persée author ID', 'Treccani ID', 'signature', 'CiNii author ID (books)', 'National Library of Israel identifier', 'Chess Games ID', "Photographers' Identities Catalog ID", 'Open Library ID', 'TWAS Fellow ID', 'Scopus Author ID', 'Libris-URI', 'TV.com ID', 'record label', 'SNAC Ark ID', 'NTA ID', 'NLA Trove ID', 'Danish National Filmography person ID', 'NE.se ID', 'FIDE ID', 'SHARE Catalogue author ID', 'Publons author ID', 'Commons gallery', 'BNB person ID', 'Dharma Drum Buddhist College person ID', 'ITTF table tennis player ID', 'NKCR AUT ID', 'Nobel prize ID', 'DC Books author ID', 'iTunes artist ID', 'Commonwealth Games Federation athlete ID', 'TED speaker ID', 'DUC ID', 'LNB ID', 'Physics History Network ID', 'IPNI author ID', 'PORT person ID', 'Fellow of the Royal Society ID', 'AlloCiné person ID', 'Munzinger Sport number', 'Gaana.com artist ID', 'ULAN ID', 'GTAA ID', 'VIAF ID', 'Biblioteca Nacional de España ID', 'CTHS person ID', 'CineMagia person ID', '365chess player ID', 'Genius artist ID', 'Store norske leksikon ID', 'BIU Santé person ID', 'Regensburg Classification', 'Scope.dk person ID', 'CricketArchive player ID', 'Mathematics Genealogy Project ID', 'ČSFD person ID', 'Bibliothèque nationale de France ID', 'WBPLN author ID', 'Leopoldina member ID', 'Twitter username', 'Oxford Dictionary of National Biography ID', 'NORAF ID', 'Box Office Mojo person ID', "Munk's Roll ID", 'Great Russian Encyclopedia Online ID', 'Davis Cup player ID', 'AllMovie person ID', 'Internet Broadway Database person ID', 'Tennis Temple player ID', 'Rupa Publications author ID', 'Quora topic ID', 'Elo rating', 'audio', 'NNDB people ID', 'Last.fm ID', 'National Diet Library Auth ID', 'HDS ID', 'YouTube channel ID', 'GND ID', 'Nederlandse Top 40 artist ID', 'IMDb ID', 'singles record', 'Indian gallantry awardee ID', 'elFilm person ID', 'OlimpBase Chess Olympiad player ID', 'title of chess person', 'PRS Legislative Research MP ID', 'CONOR ID', 'Encyclopædia Britannica Online ID', 'AllMusic artist ID', 'Elonet person ID', 'Filmportal ID', 'Facebook ID', 'Les Archives du Spectacle Person ID', 'University of Barcelona authority ID', 'Artnet artist ID', 'International Olympic Committee athlete ID', 'Academic Tree ID', 'MusicBrainz artist ID', 'Library of Congress authority ID', 'Discogs artist ID', 'National Library of Korea Identifier', 'ISNI', 'World Athletics athlete ID', 'image', 'Swedish Film Database person ID', 'doubles record', 'Brockhaus Enzyklopädie online ID', 'Nobel Prize People Nomination ID', 'Kinopoisk person ID', 'PM20 folder ID', 'Erdős number', 'Genius artist numeric ID', 'National Library of Greece ID', 'ESPNcricinfo.com player ID', 'Libraries Australia ID', 'Carnegie Hall agent ID', 'ITF player ID', 'TCM Movie Database person ID', 'botanist author abbreviation', 'NUKAT ID', 'Loop ID', 'chesstempo ID', 'Acharts.co artist ID', 'ResearcherID', 'Open Media Database person ID', 'Theatricalia person ID', 'National Academy of Sciences member ID', 'BDEL ID', 'Instagram username', 'Spotify artist ID', 'MovieMeter director ID', 'Gran Enciclopèdia Catalana ID', 'zbMATH author ID', 'Billboard artist ID', 'ORCID iD', 'Goodreads author ID', 'Sports-Reference.com Olympic athlete ID', 'Tennis Archives player ID', 'BHL creator ID', 'ranking', 'NSK ID', 'Muziekweb performer ID', "audio recording of the subject's spoken voice", 'Songkick artist ID', 'racing-reference.info driver ID', 'Squash Info player ID', 'Europeana Entity', 'pronunciation audio', 'PSA World Tour player ID', 'WikiTree person ID', 'Find A Grave memorial ID', 'Munzinger person ID']
famrel=['father','mother','parent','child','sibling','sister','brother','relative','spouse']
        
idx = index(lobjs, ignore)

####################################################
s.addWikiDataIDs()
i.reindex(lobjs) #s.createPropIndex(lobjs,ignore)

#import pandas as pd
#n=loadfile('wikidataIDs')
#n=n.split('\n') # 389 rows
#n=[{'label':i.split(',')[0], 'MyWikiDataID':i.split(',')[1]} for i in n]
#db=loadfile('db', True) # 297 rows
#m=pd.merge(pd.DataFrame(db.values()), pd.DataFrame(n),on='label') => 331 rows x 240col

def getclosematch(award, awardlist):
    return [i for i in awardlist if i.startswith(award)]

# NOTE: lobj not lobjs eg lobjs[44]
def createOrUpdatePropList(lobj, propstr, val):
    if propstr in lobj:
        if type(lobj[propstr]) is list:
            lobj[propstr].append(val)
        else: # its a string turn it into a list
            lobj[propstr]=[lobj[propstr], val]
    else: 
        lobj[propstr]=[val]

il=initlabels(dProps['label'])
tl=tinitlabels(dProps['label'])
cleanAwardStr=lambda x:' '.join(x.split()[:2]) 
updated=0
def mergeProp(index, data):
    global updated
    updated=updated+1
    a=cleanAwardStr(data['award'])
    if 'award received' in lobjs[index]:
        if type(lobjs[index]['award received']) is list:
            gg=getclosematch(a, lobjs[index]['award received'])
            if gg:
                #print("removing "+gg[0])
                lobjs[index]['award received'].remove(gg[0])
        else:
            gg=getclosematch(a, [lobjs[index]['award received']])
            if gg:
                #print("removing "+gg[0])
                lobjs[index]['award received']=[]
            else:
                lobjs[index]['award received']=[lobjs[index]['award received']]
        lobjs[index]['award received'].append(a)
        lobjs[index][a+' '+data['area']]=data['year']
        #print('added '+a+' '+data['area']+' '+str(data['year']))
    else:
        lobjs[index]['award received']=[a]
        lobjs[index][a+' '+data['area']]=data['year']
    if 'untitledname' in data:
        createOrUpdatePropList(lobjs[index], 'variant', data['untitledname'])        
    else:
        n=re.sub(titles,'',data['name'])
        if lobjs[index]['label'] != n:
            createOrUpdatePropList(lobjs[index],'variant', n)

# strip title from name and check if name exists in dProp labels
# if not check if initials and tight initials exist in dProp labels
# if not check against dProp lables initialed and tight initialed
# if not mop up with difflib.getclosesmatch
# one mapping between statedata and dProps is found update statedata into dProps
# basically if 'award received' in lobjs[foundindex] convert its entities to {award:,area, year:} form
# award received will be a list of dicts  
notfound=[];dilabel=[];dtlabel=[];ilabel=[];tlabel=[];label=0
for i in statedata:
    # remove title in name eg shri dr prof etc
    i['name']=i['name'].strip()
    n=re.sub(titles,'',i['name'])
    #find index if name exists in dProps['label']
    #abbreviated and expanded form might exist either in dprops[label] or statedata so check both
    index=-1 
    if n in dProps['label']:
        index=dProps['label'][n][0]; label=label+1 
        #area, name, place, award, year
        mergeProp(index, i)
    elif initial(n) in dProps['label']:
        ilabel.append((n, initial(n)))
        index=dProps['label'][initial(n)][0]; 
        mergeProp(index, i)
    elif tightinitial(n) in dProps['label']:
        tlabel.append((n,tightinitial(n)))
        index=dProps['label'][tightinitial(n)][0]; 
        mergeProp(index, i)
    elif n in il:
        dilabel.append((n, il[n])) 
        index=dProps['label'][il[n]][0];
        mergeProp(index, i)
    elif n in tl:
        dtlabel.append((n, tl[n])) 
        index=dProps['label'][tl[n]][0];
        mergeProp(index, i)
    else:
        i['untitledname']=n
        notfound.append(i)
    #if index > -1:
    #    lobjs[index]['label'],
gcmlabels=[]
notfound1=[]
for i in notfound:
    gg=difflib.get_close_matches(i['untitledname'], dProps['label'].keys(), cutoff=0.9)
    if gg:
        gcmlabels.append((i['untitledname'],gg[0])) 
        index=dProps['label'][gg[0]][0]
        mergeProp(index, i)
    else:
        notfound1.append(i)
notfound=notfound1
del(notfound1)

print(label, len(ilabel), len(tlabel), len(dilabel), len(dtlabel), len(gcmlabels))
#m=[dict(ilabel), dict(tlabel), dict(dilabel), dict(dtlabel), dict(gcmlabels)]
#i=notfound.pop(0);i;checkNotFound(i)
#[j[i['untitledname']] for j in m if i['untitledname'] in j]
# if index found in lobjs -> mergeProp(index, i)
#   NB spelling mismatches between untitledname and label in lobjs are preserved by pushing untitledname into 'variant'
#   spelling maybe so diff that checknotfound may not catch it -> use contains and distinct part of phrase to dig it out like otty for mamootty)
# if not in lobjs
#   -> check if it is in wikidata [and collect its ID for future processing with dumprops]
#        if it is in wikidata name might be exact match with untitledname
#           preserve that spelling diff with 
#               variantset(i, wikidatalabelspelling)
#        then call collectForDumpProps(i)
#        if name matches dont no need to call variantset 
# it is in lobjs but not in wikidata - 
#   justmerge [process later get list of all not in wikidata > lobjs without MyWikiDataID key]
###############
# 
# process ids -> run dumpprops on them and pull into lobjs
# time values have to be handled
#  
################### phase 2 of merge
# between the 2 or 3 sources - dash/tn_pdf_csv <(wikidataid() wikidata
#     - overlaps have been handled by finding a rosetta such as wikidataid
#     - mapping processes have been uncovered and mostly are complete between the sources 
# there are are still gaps - 
#     wikidataids have been found for some but props have to be retreived
#     wikidataids have not been found for others and need to be done manually

# len([i for i in lobjs if 'MyWikiDataID' not in i])
# 58
# restore data context from console session
lobjs=loadfile("lobjs")
ids=loadfile("ids")
notfound=loadfile('notfound')

def addNotFoundEntities():
    for i in notfound:
        lobjs.append({'label':i['untitledname']})
        mergeProp(len(lobjs)-1,i)

from pprint import pprint
from qwikidata.mediawiki_api import get_entities_from_mwapi
from qwikidata.entity import WikidataItem, WikidataProperty
from qwikidata.linked_data_interface import get_entity_dict_from_api
import collections
# 4 so 58+4 dont have wikidataids
entities={}
#WARN : if len(ids) > 50 look for sample code in dumpprops to get 50 at a time [api constraint]
entities.update(get_entities_from_mwapi("|".join([i["MyWikiDataID"] for i in ids]))['entities'])

idcache={}

def completeObj(e):
  global idcache
  tmp={}
  w=WikidataItem(e)
  tmp['MyWikiDataID']=e['title']
  tmp['label']=w.get_label()
  tmp['desc']=w.get_description()
  tmp['wikiurl']=w.get_enwiki_title()
  claims=w.get_claim_groups()
  for claim in claims:
    prop=WikidataProperty(props[claim])
    tmp[prop.get_label()]=[]
    #each claim/prop can point at someother entity eg: an Organization/Country etc
    for i in range(0, len(claims[claim])):
      dv=claims[claim][i].mainsnak.datavalue
      if isinstance(dv.value, dict) and 'id' in dv.value:  
        qid = dv.value["id"]
        if qid in idcache:
            entity = WikidataItem(idcache[qid])
        else:
            queryresponse=get_entity_dict_from_api(qid)
            entity=WikidataItem(queryresponse)
            idcache[qid]=queryresponse
        tmp[prop.get_label()].append(entity.get_label())
      else:
        tmp[prop.get_label()].append(dv.value) 
    if len(tmp[prop.get_label()]) == 1:
      tmp[prop.get_label()]=tmp[prop.get_label()][0]
    #handle props with time
    for k in tmp:
      if 'time' in tmp[k]:
        tmp[k]=tmp[k]['time'][1:].split('-')[0]
        continue
      if type(tmp[k]) is list and len(tmp[k])>0 and 'time' in tmp[k][0]:
        tmp[k]=[tmp[k][t]['time'][1:].split('-')[0] for t in range(0,len(lobjs[i][k]))]  
  return tmp

allprops=set(flatten([entities[i]['claims'].keys() for i in entities]))
c=collections.Counter(flatten([entities[i]['claims'].keys() for i in entities]))
props={}
for i in range(0,len(c), 50):
  print(i)
  ids="|".join(list(c.keys())[i:i+50])
  props.update(get_entities_from_mwapi(ids)['entities'])

props.update(get_entities_from_mwapi("|".join(list(c.keys())[i:len(c)]))['entities'])

for e in entities:
    lobjs.append(completeObj(entities[e]))

###############################################
idx.reindex(lobjs,ignore)
#usage idx[prop] -> 
#idx[prop][value]

##### End Hack #####
#counts=idx.counts()

getProps=lambda index:{i:lobjs[index][i] for i in lobjs[index] if i not in ignore}
dashcontains=lambda phrase:[i for i in statedata if i['name'].find(phrase) >= 0]
contains=lambda phrase:[(i, dProps['label'][i][0]) for i in dProps['label'].keys() if i.find(phrase) >= 0]
def checkNotFound(i):
    pprint([(i['untitledname'],contains(n)) for n in i['untitledname'].split() if len(contains(n))>0])
def p(index):
    pprint(getProps(index))
def pall(index):
    pprint({i:lobjs[index][i] for i in lobjs[index]})
#find(somename)
#find=lambda name:pprint([*filter(lambda i:i['label']==name,lobjs)][0])
find=lambda name:pprint([*filter(lambda i:i['label']==name,lobjs)][0])
pfind=lambda name:pprint({i:getProps(i) for i in range(0,len(lobjs)) if lobjs[i]['label']==name})
#r('child'), r('spouse') will print parent and chlid who have won awards
r=lambda relationship:[ (lobjs[dProps[relationship][relative][0]]['label'],relative) for relative in dProps[relationship] if relative in dProps['label'] ]
# rall prints related 
rall=lambda relationship:[ (lobjs[dProps[relationship][relative][0]]['label'],relative) for relative in dProps[relationship] ]
#group('educated at','Kalakshetra')
group=lambda p,v:[lobjs[i]['label'] for i in dProps[p][v]]
#pgroup('educated at','Kalakshetra',['label','occupation'])
pgroup=lambda p,v,l:[(i,[lobjs[i][j] for j in l]) for i in dProps[p][v] ]
def pg(p,v,l=['label','occupation']):
    pprint(pgroup(p,v,l))

pprint(sorted([i for i in counts['award received'] if i[0].startswith('Padma')],key=lambda x:(x[1],x[0]),reverse=True))
print('ids found',str(len(counts['MyWikiDataID'])))

#[*filter(lambda x:x['area']=='Sports',notfound)]
#pprint(sorted([*filter(lambda x:x[0].startswith('P'),counts['award received'])], key=lambda x:(x[0],x[1])))
#########################################################

class source():
    def __init__(self, url, file, dbfilter, dumpfile=False):
        self.lobjs=[]
        if file:
            self.db=loadfile(file)

        elif url:
            self.db=loadurl(url)
        else:
            print('Either url or filename must be specified')
            return
        if dbfilter:
            self.db=[*filter(dbfilter, self.db)]

    def convert_to_list_of_dicts(self):
        for i in self.db:
            self.db[i]['MyWikiDataID']=i
            self.lobjs.append(self.db[i])

        # for entities with time based props such as data of birth,death etc just use Year
        for i in range(0,len(self.lobjs)):
            for k in self.lobjs[i]:
                if 'time' in self.lobjs[i][k]:
                    self.lobjs[i][k]=self.lobjs[i][k]['time'][1:].split('-')[0]
                    continue
                if type(self.lobjs[i][k]) is list and len(self.lobjs[i][k])>0 and 'time' in self.lobjs[i][k][0]:
                    self.lobjs[i][k]=[self.lobjs[i][k][t]['time'][1:].split('-')[0] for t in range(0,len(self.lobjs[i][k]))]
            
    def convert_to_list of_objs():
        pass

# class mapper():
#     source1, source2, binderProp

#     def mapEntities():
#         # refineOut, dumpProps, wikidataID
#         # dash, dumpProps, Name

#     def mapProps():
#         #handle list, dict, val
#     def mapValue():
#         #value in one might be different from value in another 
#         #Padma Shri, Padma Shti in arts
#         #Subbalakshmi Subbulakshmi

# #index is created from unified list of all sources
class index():
    self.idx;
    self.dProps;
    self.cnt;
    #Takes a list of dicts - lobjs - and builds a dict of all prop val combos found.
    #and dProps[prop][val] = [index of objects in lobjs]
    def __init__(lobjs, ignore=[]):
        self.reindex(lobjs, ignore)

    def reindex(self, lobjs, ignore):
        self.idx=0
        self.dProps={}
        self.createPropIndex(lobjs, ignore)

    # minePropValCounts returns for each prop val combo a count of objs found
    def counts(self):
        dd={} #allcounts
        for prop in self.dProps:
            for val in self.dProps[prop]:
                if prop in dd:
                    dd[prop].append((val,len(self.dProps[prop][val])))
                else:
                    dd[prop]=[(val,len(self.dProps[prop][val]))]
        for i in dd:
            dd[i]=sorted(dd[i],key=lambda x:x[1])
        return dd

    def createPropIndex(self, lobjs, ignore):
        for obj in lobjs:
            #print idx,
            for prop in obj:
                if prop not in ignore:
                    if type(obj[prop]) is list:
                        # here list of dicts with time will be skipped
                        handlePropValueList(obj, prop)
                    elif type(obj[prop]) is dict:
                        handlePropValueDict(prop, obj[prop])
                    else:
                        # here dicts without time will be skipped
                        handlePropValue(prop, obj[prop])
            #pprint.pprint(dProps)                    
            self.idx=self.idx+1

    def handlePropValueList(obj, prop):
        lval=obj[prop]
        if len(lval) == 0:
            print('skipped ',prop, ' - EMPTY LIST?')
            return
        elif type(lval[0]) is dict:
            #print('skipped ',prop, ' - not handling list of dict values')
            val=getMainValFromDict(lval[0])
            handlePropValue(prop, val)
            return
        if prop not in dProps:
            self.dProps[prop]=dict([(item,[idx]) for item in lval])
        else:
            for val in lval:
                try:
                    if val in self.dProps[prop]:
                        self.dProps[prop][val].append(self.idx)
                    else:
                        self.dProps[prop].update({val:[self.idx]})
                except TypeError as e:
                    print('L', e, prop)
                    #raise e

    def getMainValFromDict(val):
        if "time" in val:
            #print(val['time'])
            #val=datetime.strptime(val['time'], "+%Y-%m-%dT%H:%M:%SZ").year
            val=val['time'][1:].split('-')[0]
        elif "amount" in val:
            val=val["amount"]
        elif "text" in val:
            val=val["text"]
        else:
            print("UNKNOWN dict",val)
        return val

    def handlePropValueDict(prop, val):
        try:
            val=getMainValFromDict(val)
        except ValueError as e:
            print('hpvd', e, prop)
        else:
            handlePropValue(prop, val)
            
    def handlePropValue(prop, val):
        if type(val) is dict:
            print('skipping ',prop, val)
            return
        if prop not in self.dProps:
            try:
                self.dProps[prop]={val:[self.idx]}
            except TypeError as e:
                print('hpv', e, prop, obj[prop])
        else:
            if val in dProps[prop]:
                self.dProps[prop][val].append(self.idx)
            else:
                self.dProps[prop].update({val:[self.idx]})

#     dProps_update(prop):

#getmainvalue from imine
#how is time dict handled 

# example of unifying prop 
# for i in range(0,len(lobjs)):
#     if 'award received' in lobjs[i]:
#         if type(obj[prop]) is list:
#             # maybe list of dicts careful
#             pass
#         elif type(obj[prop]) is dict:
#             pass #handlePropValueDict(prop, obj[prop])
#         else:
#             # here dicts without time will be skipped
#             pass #handlePropValue(prop, obj[prop])

# After finding common indexes in tn_dict AND dash via name mapping 
#     tn_dict is dumpprop output  
#         is missing field and awardyear, 
#         has fewer entities because its based on wikidataIDs found and is missing entities with no wikiids 
#         is missing padma vib winners
# 1. entities found in both - prop merge - in this case merge awardname - field - year - awardforstate
# 2. entites not found in one but found in other
#     if dumpprop has not been run on entity run dumpProp
#         and handle overlap props when merging
# 3. reflect can be used to do the merge into refine 
#     why do we need imine dprops if refine works
#     because in refine there wasnt a way to get all available props given a wikiid

# Is it easier to push props into larger entity list
#     in dash for eg ms sub appears twice, but in db and lobj entity might appear multiple times with prop value 'award received' different 
# create a new lobjs and discard the older intermediates - 3 way merge - dash - wikiids/dumprop - 

#########################################################
#import simplejson
#import urllib2
#from urllib import urlencode

#Assumes refine is running and project exists

# class Refine(object):
#     addr = 'http://127.0.0.1:3333/'
#     def __init__(self, name=''):
#         self.projects = None
#         self.current = None
#         if not name:
#             self.showProjects()
#         else:
#             self.getProjects()
#             self.loadProject(name)

#     def getProjects(self):
#         u = urllib2.urlopen('http://127.0.0.1:3333/command/core/get-all-project-metadata')
#         self.projects = simplejson.load(u)['projects']

#     def showProjects(self):
#         if not self.projects:
#             self.getProjects()
#         for i in self.projects:
#             print('%s\t%s\t%s' % tuple(reversed(self.projects[i].values())))

#     def loadProject(self, name):
#         for i in self.projects:
#             if self.projects[i]['name'] == name:
#                 self.current = i
#                 modelurl = "http://127.0.0.1:3333/command/core/get-models?project=" + self.current
#                 u = urllib2.urlopen(modelurl)
#                 self.model = simplejson.load(u)
#                 metaurl = "http://127.0.0.1:3333/command/core/get-project-metadata?project=" + self.current
#                 self.meta = simplejson.load(urllib2.urlopen(metaurl))
#                 print('loaded ' + self.current)

#     #text filtering 
#     def find(self, columnName, term, start=0, limit=10, caseSensitive='false', mode='record-based'):
#         param = '{"facets":[{"type":"text","name":"x","columnName":"'+columnName+'","mode":"text","caseSensitive":'+caseSensitive+',"query":"'+term+'"}],"mode":"'+mode+'"}'
#         if self.current:
#             url = 'http://127.0.0.1:3333/command/core/get-rows?project='+self.current+'&start='+str(start)+'&limit='+str(limit)
#             u = urllib2.urlopen(url, 'engine='+urllib2.quote(param))
#             self.rows = simplejson.load(u)
#         else:
#             print('Project has not been loaded yet')

#     def textFacet(self, columnName, omitBlank='false', omitError='false', selectBlank='false', selectError='false', invert='false', mode='record-based'):
#         param = '{"facets":[{"type":"list","name":"'+columnName+'","columnName":"'+columnName+'","expression":"value","omitBlank":'+omitBlank+',"omitError":'+omitError+',"selection":[],"selectBlank":'+selectBlank+',"selectError":'+selectError+',"invert":'+invert+'}],"mode":"'+mode+'"}'
#         #print urllib2.quote(param)
#         #param2 = r"engine%3A%7B%22facets%22%3A%5B%7B%22type%22%3A%22list%22%2C%22name%22%3A%22location%22%2C%22columnName%22%3A%22location%22%2C%22expression%22%3A%22value%22%2C%22omitBlank%22%3Afalse%2C%22omitError%22%3Afalse%2C%22selection%22%3A%5B%5D%2C%22selectBlank%22%3Afalse%2C%22selectError%22%3Afalse%2C%22invert%22%3Afalse%7D%5D%2C%22mode%22%3A%22record-based%22%7D"
#         if self.current:
#             url = 'http://127.0.0.1:3333/command/core/compute-facets?project='+self.current
#             u = urllib2.urlopen(url, 'engine='+urllib2.quote(param))
#             self.facets = simplejson.load(u)["facets"]
#         else:
#             print('Project has not been loaded yet')

#     #"function":"ngram-fingerprint","params":{"ngram-size":2}
#     #                "double-metaphone"
#     #                "levenshtein","params":{"radius":1,"blocking-ngram-size":6}  AND "type":"knn"
#     #                "PPM",           "params":{"radius":1,"blocking-ngram-size":6}
#     # two things to note
#     # 1. if cluster + merge is done once ie cells have been edited, calling this will return 0 clusters - need to undo mass edit 
#     # 2. select all merge and recluster has not been implemented
#     # a /command/core/mass-edit needs to be implemented to support it
#     ##    columnName:location
#     ##    expression:value
#     ##    edits:[{"from":["Besant Nagar","besant nagar","BESANT NAGAR","Besant nagar"],"to":"Besant Nagar"},{"from":["Adyar","adyar","ADYAR"],"to":"Adyar"},{"from":["ROYAPETTAH","Royapettah"],"to":"ROYAPETTAH"},{"from":["Velachery","VELACHERY"],"to":"Velachery"},{"from":["Anna Nagar","Anna nagar"],"to":"Anna Nagar"}]
#     ##    engine:{"facets":[],"mode":"record-based"}
#     def cluster(self, columnname, ctype="binning", function="fingerprint", mode="record-based"):
#         engine='{"facets":[],"mode":"'+mode+'"}'
#         if ctype== "binning":
#             clusterer='{"type":"'+ctype+'","function":"'+function+'","column":"'+columnname+'","params":{}}'
#         else:
#             clusterer='{"type":"'+ctype+'","function":"'+function+'","column":"'+columnname+'","params":{"radius":1,"blocking-ngram-size":6}}'
#         if self.current:
#             url = 'http://127.0.0.1:3333/command/core/compute-clusters?project='+self.current
#             #print urlencode({'engine':engine,'clusterer':clusterer})
#             u = urllib2.urlopen(url, urlencode({'engine':engine,'clusterer':clusterer})) #'engine='+urllib2.quote(engine)+'%0A%26clusterer='+urllib2.quote(clusterer))
#             self.clusters = simplejson.load(u)
#         else:
#             print('Project has not been loaded yet')

#     # used to get the cluster mass edits
#     def getOps(self):
#         if self.current:
#             url = 'http://127.0.0.1:3333/command/core/get-operations?project=' + self.current
#             u = urllib2.urlopen(url)
#             self.ops =simplejson.load(u)["entries"]
#         else:
#             print('Project has not been loaded yet')

# # from pprint import pprint
# # r=Refine('galerts')
# # r.find('domain','tech-bug')
# # print len(r.rows['rows'])
# # r.rows=None
# # r.textFacet('location')
# # pprint(r.facets[0]["choices"])
# # ##r.cluster("location")
# # ##pprint(r.clusters)
# # ##r.cluster("location",ctype="knn",function="levenshtein")
# # ##pprint(r.clusters)
# # ##r.getOps()
# # ##pprint(r.ops)

# # ##r=Refine('chennaitweetsuser')
# # ##r.find('name','ravi')
# # ##print len(r.rows['rows'])
# # ##r.textFacet('name')
# # ##print len(r.facets)
# # #pprint(r.rows)
# # #r.model
# # #pprint(r.meta)

