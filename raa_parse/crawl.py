from bs4 import BeautifulSoup

import urllib
import urllib2
import string

url = "http://www.fmis.raa.se/cocoon/fornsok/ajax/searchresults"

user_agent = 'Mozilla/5 (Solaris 10) Gecko'
headers = {'User-Agent' : user_agent}

values = {'county': '05', 'page': 1}
data = urllib.urlencode(values)

req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
soup = BeautifulSoup(response.read())
all_a = soup.table.find_all("a")
ids = []
for tag in all_a:
    ids.append(tag['id'])
print ids
