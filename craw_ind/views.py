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

def search(request):
    # hello

    html = ""
    if request.GET:
        stopwords = [ 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn', 'download', 'attachment', 'refer', 'please', 'sd/-', 'i.e', 'ay', 'dear', 's.no']
        form = (request.GET).get('q')
        formlist = re.sub("[^\w]", " ", form).split()                           #spliting words
        formlist = filter(lambda x: x not in stopwords, formlist)               #removing stopwords

        html = (formlist)
        # temp = keywordsdata.objects.filter(keyword="student")
    html += "<h1>Indevelopment</h1>"
    temp = keywordsdata.objects.filter(keyword="student")
    temp = temp[0].location
    return HttpResponse(html)

def crawlnow(request):
    keywordsdata.objects.all().delete()
    f = open('/home/chandu/Desktop/sepro/hub_sample.html', 'r')

def crawlnow(request):
    keywordsdata.objects.all().delete()
    f = open('/root/Desktop/sepro/hub_sample.html', 'r')
    webpage = f.read()
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
    tokenwords = [x for x in tokenwords if len(x) > 2]                      #intergers or other
    tokenwords = list(set(tokenwords))                                      #removing duplicates

    for _ in range(len(tokenwords)):
        indkeywords = keywordsdata(
            keyword = tokenwords[_],
            location = "1",
        )
        indkeywords.save()

    template = loader.get_template('crawling.html')
    html = template.render(Context({'finished' : 'done mama'}))

    return HttpResponse(html)
