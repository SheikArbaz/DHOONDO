from django.shortcuts import render
from django.http import HttpResponse
from craw_ind.models import keywordsdata

from bs4 import BeautifulSoup
import requests,urllib3,os, string
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
        form = (request.GET).get('searchquery')
        html = form
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
