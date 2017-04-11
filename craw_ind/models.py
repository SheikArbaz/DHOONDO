from __future__ import unicode_literals

from django.db import models

# Create your models here.

class keywordsdata(models.Model):
    keyword = models.CharField(max_length=255,db_index=True)
    location = models.CharField(max_length=255,db_index=True)
    # hits = models.IntegerField()

    class Meta:
        db_table = "indkeywords" #my own table name

class bodyheads(models.Model):
    bid = models.CharField(max_length=10,db_index=True)
    bodyum = models.CharField(max_length=1000)

    class Meta:
        db_table = "bodyheadum"
