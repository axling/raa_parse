from bs4 import BeautifulSoup

import urllib
import urllib2
import string
import json
import re
import httplib
import requests

url = "http://www.fmis.raa.se/cocoon/fornsok/ajax/searchresults"

user_agent = 'Mozilla/5 (Solaris 10) Gecko'
headers = {'User-Agent' : user_agent}
ids = []
start_page=1

def put_in_database(doc):
    url = "https://remains.iriscouch.com"
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    r = requests.get(url + "/_uuids")

    uuid_dict = json.loads(r.text)
    uuid = uuid_dict["uuids"][0]

    header = {'content-type': 'application/json'}
    r = requests.put(url + "/remains/" + uuid, data=doc, headers=header)
            
    response_dict = json.loads(r.text)
    response_dict['ok'] = "true"
    

def get_remain_page(remain_id):
    url = "http://www.fmis.raa.se/cocoon/fornsok/ajax/showobject"
    values = {'objektid': remain_id}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)
    
    response = urllib2.urlopen(req)
    soup = BeautifulSoup(response.read())
    raa_num = soup.table['summary']
    trs = soup.find_all("tr")
    doc = {}
    for tr in trs:
        if not tr.th:
            continue
        if 'class' in tr.attrs:
            if tr['class'] == "rowheader" or tr['class'] == "rowsub" or tr['class'] == "rowsubheader":
                continue
        elif 'id' in tr.th.attrs:
            if tr.th['id'] == "remnpopanchor":
                link = tr.td.a['href']
                name = tr.th.string
                value = tr.td.a.string
                doc[name] = {"http_link": link, "text": value}
                
            elif tr.th['id'] == "Antikvarisk bed&ouml;mning_anchor":
                link = tr.td.a['href']
                name = tr.th.string
                value = tr.td.a.string
                doc[name] = {"http_link": link, "text": value}
            else:
                name = tr.th.string
                value = tr.td.string
                doc[name] = value        
        else:
            if tr.th.find(text=re.compile("Google Earth")) != None:
                pass
            elif tr.th.find(text=re.compile("eniro.se")) != None:
                pass
            elif tr.th.find(text=re.compile("hitta.se")) != None:
                pass
            else:
                name = tr.th.string
                value = tr.td.string
                doc[name] = value
    return json.dumps(doc)
            

return_doc = get_remain_page("18000000050627")
put_in_database(return_doc)

while True:
    values = {'county': '05', 'page': start_page}
    data = urllib.urlencode(values)

    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    soup = BeautifulSoup(response.read())
    if soup.p != None:
        break
    all_a = soup.table.find_all("a")
    
    for tag in all_a:
        ids.append(tag['id'])
    
    print "page " + str(start_page) + " completed"
    print "ids: " + str(len(ids)) 
    start_page = start_page + 1
        
print len(ids)


