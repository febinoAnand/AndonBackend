import os
import django
import imaplib
import email
import time
from email.header import decode_header
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'andondjango.settings')
django.setup()
from EmailTracking.models import Inbox

imap_host = 'imap.gmail.com'
imap_user = 'emailtrackfebinosolutions@gmail.com'
imap_password = 'zugo eiey rzby vdgb'

def process_email(msg,num):
    sender = msg['From']
    subject = decode_header(msg['Subject'])[0][0]
    message_id = msg['Message-ID']

    if isinstance(subject, bytes):
        subject = subject.decode()

    body = ""

    for part in msg.walk():
        content_type = part.get_content_type()
        content_disposition = str(part.get("Content-Disposition"))

        if content_type == "text/plain" and "attachment" not in content_disposition:
            body += part.get_payload(decode=True).decode(part.get_content_charset(), 'ignore')

    print("Sender:", sender)
    print("Subject:", subject)
    print("Body:", body.strip())
    print("Message-ID:", message_id)

    
    current_datetime = datetime.now()
    inbox_instance = Inbox.objects.create(from_email=sender,to_email=imap_user, subject=subject, message=body, message_id=num,date=current_datetime.date(),
    time=current_datetime.time())
    
    print("Stored in Inbox:", inbox_instance)

def read_emails():
    mail = imaplib.IMAP4_SSL(imap_host)
    mail.login(imap_user, imap_password)
    mail.select('inbox')

    result, data = mail.search(None, 'UNSEEN')  

    if not data[0]:
        print("No new messages.")
        mail.logout()
        return

    for num in data[0].split():
        print(num)
        result, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        process_email(msg,num)
        mail.store(num, '+FLAGS', '\\Seen')

    mail.logout()

while True:
    read_emails()
    time.sleep(3)
