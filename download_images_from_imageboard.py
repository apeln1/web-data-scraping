import re
import requests
from bs4 import BeautifulSoup

def update_progress(progress):
    print('\r[{0}{1}] {2}%'.format('#'*(progress),'-'*(100-progress), progress),end = '\r')



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

progress = 0
for url in urls:
	progress = progress + 1
	update_progress(int(100.0 * (progress / len(urls))))
	filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
	if not filename:
		#print("Regex didn't match with the url: {}".format(url))
		continue
	with open(filename.group(1), 'wb') as f:
		if 'http' not in url:
            	# sometimes an image source can be relative 
            	# if it is provide the base url which also happens 
            	# to be the site variable atm. 
			url = '{}{}'.format(site, url)
		#print('Downloading '  + url)
		response = requests.get(url)
		f.write(response.content)
print()
print("Finished")
