from django.shortcuts import render
from django.http import HttpResponse
from .tasks import inboxReadTask
# Create your views here.
def readMailView(request):
    inboxReadTask.delay("Read from views")
    return HttpResponse("Task Called..")