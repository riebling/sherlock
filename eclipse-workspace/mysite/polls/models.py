from __future__ import unicode_literals

import datetime
from django.db import models
from django.utils import timezone # so


# Create your models here.
class Question(models.Model):
    #
    def __str__(self):
        return self.question_text
    #
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    #
    def __str__(self):
        return self.choice_text
    #
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class URLtoScrape(models.Model):
    def __str__(self):
        return self.url_text
    url_text = models.CharField(max_length=200)
    actual_url = models.CharField(max_length=200)
