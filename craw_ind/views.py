from django.shortcuts import render
from django.http import HttpResponse
from craw_ind.models import keywordsdata
import time
from bs4 import BeautifulSoup
import requests,urllib3,os, string,re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from django.db import transaction

from .forms import searchForm

import requests,urllib3,os
from django.template import Context, Template,loader

from django.db import connection #for truncating
# Create your views here.

def matching(formlist):
	linkfreq = [0]*50
	qlen = len(formlist)
	todel = ""
	for _ in range(0,qlen):
		try:
			tempdbstring = keywordsdata.objects.filter(keyword=formlist[_].lower())
			todel = str(tempdbstring[0].location)
			tempdbstring = str(tempdbstring[0].location)
			tempdbstring = tempdbstring.split("$")                                  #$ removal

			newdbint = list()

			for i in range(len(tempdbstring)):
				newdbint.append(int(tempdbstring[i]))

			for i in range(len(newdbint)):
				linkfreq[int(newdbint[i])] += 1
		except:
			pass

	newlsit = sorted(range(len(linkfreq)), key=lambda x:linkfreq[x])
	newlsit.reverse()

	pagesprio = list()
	pagesindx = list()

	# print(linkfreq)

	for i in range(len(linkfreq)):
		if linkfreq[i] > 0:
			pagesindx.append(i)
			pagesprio.append(linkfreq[i])

	for x in range(len(pagesindx)):
		for y in range(len(pagesindx)-x-1):
			if pagesprio[x] > pagesprio[y]:
				pagesprio[x],pagesprio[y] = pagesprio[y],pagesprio[x]
				pagesindx[x],pagesindx[y] = pagesindx[y],pagesindx[x]

	print(pagesindx)

	temphtml = ""

	for i in range(len(pagesindx)):
		temphtml += "<a href='http://hub.rgukt.ac.in/hub/notice/index/"+ str(pagesindx[i]) + "'>Link Index : " + str(pagesindx[i]) + "</a><br>"

	return pagesindx

def search(request):
	html = ""
	if request.GET:
		# stopwords = [ 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn', 'download', 'attachment', 'refer', 'please', 'sd/-', 'i.e', 'ay', 'dear', 's.no']
		stop_words = set(stopwords.words("english"))

		form = (request.GET).get('q')
		formlist = re.sub("[^\w]", " ", form).split()                           #spliting words
		formlist = filter(lambda x: x not in stop_words, formlist)               #removing stopwords
		# formlist = formlist.lower
		html = matching(formlist)

		# temp = keywordsdata.objects.filter(keyword="student")

	template = loader.get_template('search.html')
	htmls = template.render(Context({'searchresults' : html}))
	# html += "<h1>Indevelopment</h1>"
	# temp = keywordsdata.objects.filter(keyword="student")
	# temp = temp[0].location
	return HttpResponse(htmls)

def RepresentsInt(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

def crawlpage(newsite,pagenumber):
	webpage = requests.get(newsite,verify=False).text
	soup = BeautifulSoup(webpage,"html.parser")

	noticehead = soup.find_all("a", {"class": "accordion-toggle"})
	noticebody = soup.find_all("div",{"class": "panel-body"})
	finalbody = ""

	tokenwords = list()

	for _ in range(20):
		noticebody[_] = noticebody[_].get_text().strip().lower()
		tokenwordstemp = word_tokenize(noticebody[_])
		tokenwords += tokenwordstemp

		noticehead[_] = noticehead[_].get_text().strip().lower()
		tokenwordstemp = word_tokenize(noticehead[_])
		tokenwords += tokenwordstemp

	stop_words = set(stopwords.words("english"))

	tokenwords = filter(lambda x: x not in string.punctuation and stop_words, tokenwords)                              #punctuation
	# tokenwords = filter(lambda x: x not in stop_words, tokenwords)                                      #stopwords
	tokenwords = [x for x in tokenwords if len(x) > 1 ]#and RepresentsInt(x)==False]                      #integers ...still to modify
	tokenwords = list(set(tokenwords))                                                                  #removing duplicates

	print("Token words: "+str(len(tokenwords)) + " found in page :"+ str(pagenumber))
	savecount = 0
	updatecount = 0

	with transaction.atomic():
		for _ in range(len(tokenwords)):
			try:
				temp = keywordsdata.objects.filter(keyword=tokenwords[_])
				strtoapp = str(temp[0].location)
				strtoapp += "$"+str(pagenumber)
				updatecount += 1
				keywordsdata.objects.filter(keyword=tokenwords[_]).update(location=strtoapp)
				print("Updating "+tokenwords[_]+" with "+strtoapp)
			except:
				indkeywords = keywordsdata(
					keyword = tokenwords[_],
					location = pagenumber,
				)
				savecount += 1
				print("Saving new keyword: "+ tokenwords[_] + " " + str(pagenumber))
				indkeywords.save()
	# transaction.commit()


	print("Save count: "+str(savecount))
	print("Update count: "+str(updatecount))

def crawlnow(request):
	keywordsdata.objects.all().delete()
	hubsite = "https://hub.rgukt.ac.in/hub/notice/index/"
	start = time.time()
	for i in range(0,50):
		tempsite = hubsite+str(i)
		crawlpage(tempsite,i)
	print("Time take in seconds: "+str(int(time.time()-start)))
	template = loader.get_template('crawling.html')
	html = template.render(Context({'finished' : 'done mama'}))

	return HttpResponse(html)
