import nltk 
import re
import urlparse
import urllib
from bs4 import BeautifulSoup
def show_words(url):
	html = urllib.urlopen(url).read()
	soup = BeautifulSoup(html, 'html.parser')
	for script in soup(["script", "style"]):
		script.extract()
	text = soup.get_text()

	lines = (line.strip() for line in text.splitlines())
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	text = '\n'.join(chunk for chunk in chunks if chunk)
	
	print(str(url)+" Words:-")
	print(type(text.encode('utf-8')))
	print(text.encode('utf-8').split())

url="http://nptel.rgukt.ac.in"
urls=[url]
visited=[url]
while(len(urls)>0):
	try:
		htmltext=urllib.urlopen(urls[0]).read()
	except:
		print(urls[0])
	soup=BeautifulSoup(htmltext,"html.parser")
	url=urls.pop(0)
	show_words(url)
	for tag in soup.findAll('a',href=True):
		tag['href']=urlparse.urljoin(url,tag['href'])
		x=tag['href']
		if url in tag['href'] and tag['href'] not in visited:
			urls.append(x)
			visited.append(x)
print("1.Visited: ")
print(visited)
