from django.shortcuts import render
from django.http import JsonResponse
from threading import Thread
import time

# Create your views here.

thread_running = False

def startThreadView(request):
    global thread_running
    if not thread_running:
        thread_running = True
        thread = Thread(target=thread_process)
        thread.start()
        return JsonResponse({'message': 'Thread started'})
    else:
        return JsonResponse({'message': 'Thread already running'})


def stopThreadView(request):
    global thread_running
    if thread_running:
        thread_running = False
        return JsonResponse({'message': 'Thread stopped'})
    else:
        return JsonResponse({'message': 'Thread already stopped'})


def thread_process():
    global thread_running
    while thread_running:
        print("Thread running")
        time.sleep(2)