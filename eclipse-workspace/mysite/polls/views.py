from django.http import HttpResponse
from django.shortcuts import render

from .models import Question, URLtoScrape


#from django.template import loader
# Create your views here.
# basic index.html type view
def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    
    # query the db for URLtoScrape objects
    urls_list = URLtoScrape.objects.all()#.order_by('url_text')

    # dictionary mapping template variable names to Python objects
    # this formats the urls_list we pulled from the URLtoScrape object
    # such that it can be referenced by index.html for 'rendering'
    context = {'urls_list': urls_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
