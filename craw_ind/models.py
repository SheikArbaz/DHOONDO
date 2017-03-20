from __future__ import unicode_literals

from django.db import models

# Create your models here.

class keywordsdata(models.Model):
    keyword = models.CharField(max_length=255,)
    location = models.CharField(max_length=255,)
    # hits = models.IntegerField()

    class Meta:
        db_table = "indkeywords" #my own table name
