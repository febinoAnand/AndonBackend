from celery import shared_task

@shared_task
def inboxReadTask():
    return "trackInbox"