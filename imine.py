#! /usr/bin/env python3
import sys
from datetime import datetime

class Entity(object):
    def __init__(self,**kargs):
        for i in kargs.keys():
            setattr(self, i, kargs[i])

def flatten(l):
    aaa=[]
    for i in l:
        aaa.extend(i)
    return aaa

# dProps is output from a mine*(lobj) 
# minePropValCounts returns for each prop val combo a count of objs found
def minePropValCounts(dProps):
    dd={} #allcounts
    for prop in dProps:
        for val in dProps[prop]:
            if prop in dd:
                dd[prop].append((val,len(dProps[prop][val])))
            else:
                dd[prop]=[(val,len(dProps[prop][val]))]
    return dd

#Takes a list of objects - lobjs - and builds a dict of all prop val combos found.
#and dict[prop][val] = [index of objects in lobjs]
def mineObj(lobjs):
    results={}
    idx=0
    for obj in lobjs:
        print(idx, " ")
        for prop in obj.__dict__:                             
            if results.has_key(prop):

                if type(obj.__dict__[prop]) is list:
                    for i in obj.__dict__[prop]:
                        #print i
                        if results[prop].has_key(i):
                            results[prop][i].append(idx)
                        else:
                            results[prop].update({i:[idx]})
                else:
                    if results[prop].has_key(obj.__dict__[prop]):
                        results[prop][obj.__dict__[prop]].append(idx)
                    else:
                        results[prop].update({obj.__dict__[prop]:[idx]})
            else:
                #adding neew prop eg: results['location']= {'adyar':[3]} where 3 is a index into listof ads
                if type(obj.__dict__[prop]) is list:
                    l=obj.__dict__[prop]
                    results[prop]=dict([(item,[idx]) for item in l])
                else:
                    results[prop]={obj.__dict__[prop]:[idx]}
        #pprint.pprint(results)                    
        idx=idx+1
    return results

#Takes a list of dicts - lobjs - and builds a dict of all prop val combos found.
#and dProps[prop][val] = [index of objects in lobjs]
def mineDict(lobjs, ignore=[]):
    global idx
    for obj in lobjs:
        #print idx,
        for prop in obj:
            if prop not in ignore:
                if type(obj[prop]) is list:
                    # here list of dicts with time will be skipped
                    handlePropValueList(obj, prop)
                elif type(obj[prop]) is dict:
                    handlePropValueDict(obj, prop)
                else:
                    # here dicts without time will be skipped
                    handlePropValue(obj, prop)
        #pprint.pprint(dProps)                    
        idx=idx+1
    return dProps

def handlePropValueList(obj, prop):
    lval=obj[prop]
    if len(lval) == 0:
        print('skipped ',prop, ' - EMPTY LIST?')
        return
    elif type(lval[0]) is dict:
        print('skipped ',prop, ' - not handling list of dict values')
        return
    if prop not in dProps:
        dProps[prop]=dict([(item,[idx]) for item in lval])
    else:
        for val in lval:
            try:
                if val in dProps[prop]:
                    dProps[prop][val].append(idx)
                else:
                    dProps[prop].update({val:[idx]})
            except TypeError as e:
                print(e, prop)
                #raise e

def handlePropValueDict(obj, prop):
    try:
        if "time" in obj[prop]:
            val=datetime.strptime(obj[prop]['time'], "+%Y-%m-%dT%H:%M:%SZ").year
        elif "amount" in obj[prop]:
            val=obj[prop]["amount"]
        elif "text" in obj[prop]:
            val=obj[prop]["text"]
        else:
            print("UNKNOWN dict",obj[prop])
    except ValueError as e:
        print('valerror',prop)
    else:
        if prop not in dProps:
            dProps[prop]={val:[idx]}
        else:
            if val in dProps[prop]:
                dProps[prop][val].append(idx)
            else:
                dProps[prop].update({val:[idx]})

def handlePropValue(obj, prop):
    val = obj[prop]
    if type(val) is dict:
        print('skipping ',prop, val)
        return
    if prop not in dProps:
        try:
            dProps[prop]={val:[idx]}
        except TypeError as e:
            print(e, prop, obj[prop])
    else:
        if val in dProps[prop]:
            dProps[prop][val].append(idx)
        else:
            dProps[prop].update({val:[idx]})


#open file with list of objs or list of dicts
f=open(sys.argv[1])
text=f.read()
db=eval(text)
# db is a dict - entityID to wikidata entity dict of props
# convert db to ldicts or lobjs - basically indexing it - ie lobjs[n] = someobj
lobjs=[]
dProps={} # output of mineDict stored here
idx=0 # init index of lobjs
for i in db:
    db[i]['MyWikiDataID']=i
    lobjs.append(db[i])
mineDict(lobjs)
counts=minePropValCounts(dProps)

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

