from django.shortcuts import render
from django.http import HttpResponse
from craw_ind.models import keywordsdata

from bs4 import BeautifulSoup
import requests,urllib3,os, string,re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from .forms import searchForm

import requests,urllib3,os
from django.template import Context, Template,loader

from django.db import connection #for truncating
# Create your views here.

def matching(formlist):
    linkfreq = [0]*100
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
    # linkfreq.sort(reverse=True)
    # newlsit.sort(reverse=True)
    return newlsit

def search(request):
    html = ""
    if request.GET:
        stopwords = [ 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn', 'download', 'attachment', 'refer', 'please', 'sd/-', 'i.e', 'ay', 'dear', 's.no']
        form = (request.GET).get('q')
        formlist = re.sub("[^\w]", " ", form).split()                           #spliting words
        formlist = filter(lambda x: x not in stopwords, formlist)               #removing stopwords
        # formlist = formlist.lower
        html = matching(formlist)

        # temp = keywordsdata.objects.filter(keyword="student")
    html += "<h1>Indevelopment</h1>"
    # temp = keywordsdata.objects.filter(keyword="student")
    # temp = temp[0].location
    return HttpResponse(html)
    
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

    tokenwords = filter(lambda x: x not in string.punctuation, tokenwords)  #punctuation
    tokenwords = filter(lambda x: x not in stop_words, tokenwords)          #stopwords
    tokenwords = [x for x in tokenwords if len(x) > 1]                      #integers ...still to modify
    tokenwords = list(set(tokenwords))                                      #removing duplicates

    for _ in range(len(tokenwords)):
        try:
            temp = keywordsdata.objects.filter(keyword=tokenwords[_])
            strtoapp = str(temp[0].location)
            strtoapp += "$"+str(pagenumber)

            keywordsdata.objects.filter(keyword=tokenwords[_]).update(location=strtoapp)
        except:
            indkeywords = keywordsdata(
                keyword = tokenwords[_],
                location = pagenumber,
            )
            indkeywords.save()

def crawlnow(request):
    keywordsdata.objects.all().delete()
    hubsite = "https://hub.rgukt.ac.in/hub/notice/index/"

    for i in range(5):
        tempsite = hubsite+str(i)
        crawlpage(tempsite,i)

    template = loader.get_template('crawling.html')
    html = template.render(Context({'finished' : 'done mama'}))

    return HttpResponse(html)
