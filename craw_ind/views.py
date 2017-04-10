from django.shortcuts import render
from django.http import HttpResponse
from craw_ind.models import keywordsdata,bodyheads
import time
from bs4 import BeautifulSoup
import requests,urllib3,os, string,re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from django.db import transaction
from collections import defaultdict
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import searchForm

import requests,urllib3,os
from django.template import Context, Template,loader

from django.db import connection #for truncating
# Create your views here.
# bodynums = defaultdict(list)

def getBodynum(tempdbstring,bodynums):
	# print(tempdbstring)
	wordpages = list()
	for y in tempdbstring:
		bodynums[int(y.rsplit('_', 1)[0])] = map(int, (y.rsplit('_', 1)[1]).split(','))
		# print(str(y.split('_',1)[1]))
	return(bodynums)

def matching(formlist):
	linkfreq = [0]*50
	qlen = len(formlist)
	todel = ""
	bodynums = defaultdict(list)
	for _ in range(0,qlen):
		try:
			tempdbstring = keywordsdata.objects.filter(keyword=formlist[_].lower())
			todel = str(tempdbstring[0].location)
			tempdbstring = str(tempdbstring[0].location)
			tempdbstring = tempdbstring.split("$")                                  #$ removal
			bodynums = getBodynum(tempdbstring,bodynums)
			# print(bodynums)
			newdbint = list()

			for i in tempdbstring:
				newdbint.append(int(i.rsplit('_', 1)[0]))

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

	# print(pagesindx)

	temphtml = list()
	# print("hje")
	headersum = defaultdict(list)
	for j in range(len(pagesindx)):
		# print(bodynums[j])
		ckompu = bodynums[pagesindx[j]]
		for n in ckompu:
			ttodel = str(pagesindx[j])+"_"+str(n)
			print(ttodel)
			headersum[pagesindx[j]].append(bodyheads.objects.get(bid=ttodel).bodyum)
			# temphtml.append(tedmf.bodyum)

	# print(headersum)
	return headersum

def search(request):
	noticepages = ""
	if request.GET:
		# stopwords = [ 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn', 'download', 'attachment', 'refer', 'please', 'sd/-', 'i.e', 'ay', 'dear', 's.no']
		stop_words = set(stopwords.words("english"))

		form = (request.GET).get('q')
		formlist = re.sub("[^\w]", " ", form).split()                           #spliting words
		formlist = filter(lambda x: x not in stop_words, formlist)               #removing stopwords
		# formlist = formlist.lower
		headers = matching(formlist)

		# temp = keywordsdata.objects.filter(keyword="student")
		context = { 'header' : headers.items(), "searchq" : (request.GET).get('q')}
	# template = loader.get_template('search.html')
	# htmls = template.render(Context({'searchresults' : html}))
	# html += "<h1>Indevelopment</h1>"
	# temp = keywordsdata.objects.filter(keyword="student")
	# temp = temp[0].location
	return render(request, 'search.html', context)

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
	stop_words = set(stopwords.words("english"))
	wbodyloc = defaultdict(list)


	with transaction.atomic():
		for _ in range(20):
			noticebody[_] = noticebody[_].get_text().strip().lower()
			tokenwordstemp = word_tokenize(noticebody[_])
			tokenwordstemp = filter(lambda x: x not in string.punctuation, tokenwordstemp)
			tokenwordstemp = filter(lambda x: x not in stop_words, tokenwordstemp)
			tokenwords += tokenwordstemp
			presentnotice = tokenwordstemp
			bodyheadum = bodyheads(
				bid = str(pagenumber)+"_"+str(_),
				bodyum = noticehead[_].get_text().strip(),
			)
			# print("Saving Body: "+str(_))
			bodyheadum.save()
			noticehead[_] = noticehead[_].get_text().strip().lower()
			tokenwordstemp = word_tokenize(noticehead[_])
			tokenwordstemp = filter(lambda x: x not in string.punctuation, tokenwordstemp)
			tokenwordstemp = filter(lambda x: x not in stop_words, tokenwordstemp)
			tokenwords += tokenwordstemp
			presentnotice += tokenwordstemp
			presentnotice = list(set(presentnotice))
			for j in range(len(presentnotice)):
				wbodyloc[presentnotice[j]].append(_)

	# print(wbodyloc)
	tokenwords = [x for x in tokenwords if len(x) > 1 ]#and RepresentsInt(x)==False]                      #integers ...still to modify
	tokenwords = list(set(tokenwords))                                                                  #removing duplicates

	# print("Token words: "+str(len(tokenwords)) + " found in page :"+ str(pagenumber))
	savecount = 0
	updatecount = 0

	with transaction.atomic():
		for _ in range(len(tokenwords)):
			toappend = wbodyloc[tokenwords[_]]
			toappend = ','.join(str(num) for num in toappend)
			toappend = '_'+toappend
			# print(toappend)
			try:
				temp = keywordsdata.objects.filter(keyword=tokenwords[_])
				strtoapp = str(temp[0].location)
				strtoapp += "$"+str(pagenumber)+toappend
				updatecount += 1
				keywordsdata.objects.filter(keyword=tokenwords[_]).update(location=strtoapp)
				print("Updating "+tokenwords[_]+" with "+strtoapp)
			except:
				indkeywords = keywordsdata(
					keyword = tokenwords[_],
					location = (str(pagenumber)+toappend),
				)
				savecount += 1
				# print("Saving new keyword: "+ tokenwords[_] + " " + str(pagenumber))
				indkeywords.save()
	# transaction.commit()


	# print("Save count: "+str(savecount))
	# print("Update count: "+str(updatecount))

@login_required(login_url='/login')
def crawlnow(request):
	keywordsdata.objects.all().delete()
	bodyheads.objects.all().delete()
	hubsite = "https://hub.rgukt.ac.in/hub/notice/index/"
	start = time.time()
	for i in range(0,50):
		print("Crawling Page: "+str(i))
		tempsite = hubsite+str(i)
		crawlpage(tempsite,i)
	print("Time take in seconds: "+str(int(time.time()-start)))
	template = loader.get_template('crawling.html')
	html = template.render(Context({'finished' : 'Crawled Successfully'}))

	return HttpResponse(html)
