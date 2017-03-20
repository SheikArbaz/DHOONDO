from bs4 import BeautifulSoup
import requests,urllib3,os, string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


f = open('/home/chandu/Desktop/sepro/hub_sample.html', 'r')
webpage = f.read()
soup = BeautifulSoup(webpage,"html.parser")

# soup = BeautifulSoup(webpage,"html.parser")

noticehead = soup.find_all("a", {"class": "accordion-toggle"})
noticebody = soup.find_all("div",{"class": "panel-body"})
finalbody = ""

tokenwords = list()

for _ in range(20):
	noticebody[_] = noticebody[_].get_text().strip().lower().encode('ascii', 'ignore')
	tokenwordstemp = word_tokenize(noticebody[_])
	tokenwords += tokenwordstemp

	noticehead[_] = noticehead[_].get_text().strip().lower().encode('ascii', 'ignore')
	tokenwordstemp = word_tokenize(noticehead[_])
	tokenwords += tokenwordstemp

stop_words = set(stopwords.words("english"))

print("Token words: "+ str(len(tokenwords)))
tokenwords = filter(lambda x: x not in string.punctuation, tokenwords)
print("Token words after pun: "+ str(len(tokenwords)))
tokenwords = filter(lambda x: x not in stop_words, tokenwords)
tokenwords = [x for x in tokenwords if len(x) > 2]
print("Token words after stop: "+ str(len(tokenwords)))

tokenwords = list(set(tokenwords))
print(tokenwords)
# tokenwords.encode('ascii', 'ignore')
