from django.contrib import admin

from .models import Question, URLtoScrape


# Register your models here.
admin.site.register(Question)
admin.site.register(URLtoScrape)

