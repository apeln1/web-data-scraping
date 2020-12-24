import re
import requests
from bs4 import BeautifulSoup

site = 'https://2ch.hk'
board = '/sf/'

response = requests.get(site + board)

soup = BeautifulSoup(response.text, 'html.parser')
elements = soup.findAll('img')
urls = list()
for element in elements:
	url = element.get('data-src')  # the actual img link is just a thumbnail
	if url is not None:
		urls.append(url)

print(urls)

for url in urls:
	filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
	if not filename:
		print("Regex didn't match with the url: {}".format(url))
		continue
	with open(filename.group(1), 'wb') as f:
		if 'http' not in url:
            	# sometimes an image source can be relative 
            	# if it is provide the base url which also happens 
            	# to be the site variable atm. 
			url = '{}{}'.format(site, url)
		response = requests.get(url)
		f.write(response.content)
