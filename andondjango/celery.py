import os

from celery import Celery
# import celery
import urllib.request
import requests
import json

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'andondjango.settings')

app = Celery('andondjango')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task
def andonDjangoTest(arg):
    print ("testing..."+arg)


@app.task(bind=True, ignore_result=True)
def mainMailReadTask(arg):
    # from celerytaskapp.tasks import readMailInbox
    # readMailInbox(arg)
    # from emailtracking.tasks import inboxReadTask
    # inboxReadTask()
    pass



@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5.0, mainMailReadTask.s())