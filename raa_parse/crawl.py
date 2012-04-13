from bs4 import BeautifulSoup

import urllib
import urllib2
import string

url = "http://www.fmis.raa.se/cocoon/fornsok/ajax/searchresults"

user_agent = 'Mozilla/5 (Solaris 10) Gecko'
headers = {'User-Agent' : user_agent}
ids = []
start_page=1
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
