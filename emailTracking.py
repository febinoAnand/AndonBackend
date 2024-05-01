import json
import os
import django
import imaplib
import email
import time
from email.header import decode_header
from email.utils import parsedate_to_datetime
from twilio.rest import Client
import requests

from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)
from requests.exceptions import ConnectionError, HTTPError

session = requests.Session()
session.headers.update(
    {
        "Authorization": f"Bearer {os.getenv('EXPO_TOKEN')}",
        "accept": "application/json",
        "accept-encoding": "gzip, deflate",
        "content-type": "application/json",
    }
)



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'andondjango.settings')
django.setup()
from EmailTracking.models import Inbox
from EmailTracking.models import Settings
from EmailTracking.models import SearchParameter, UserEmailTracking

import sys

try:
    settings_instance = Settings.objects.first()
    imap_host = settings_instance.host
    imap_port = settings_instance.port
    imap_user = settings_instance.username
    imap_password = settings_instance.password
except:
    print("no username found")
    sys.exit()

try:
    settings_instance = Settings.objects.first()
    sms_sid = settings_instance.sid
    sms_auth_token = settings_instance.auth_token
    sms_from_phone = settings_instance.phone

except:
    print("No Data found")
    sys.exit()



def process_email(msg,num):
    sender = msg['From']
    to_email = msg['To']
    subject = decode_header(msg['Subject'])[0][0]
    # message_id = msg['Message-ID']

    if isinstance(subject, bytes):
        subject = subject.decode()
    body = ""

    for part in msg.walk():
        content_type = part.get_content_type()
        content_disposition = str(part.get("Content-Disposition"))

        if content_type == "text/plain" and "attachment" not in content_disposition:
            body += part.get_payload(decode=True).decode(part.get_content_charset(), 'ignore')

    scanBody = body.strip()
    print("Sender:", sender)
    print("To:", to_email)
    print("Subject:", subject)
    print("Body:", scanBody)
    print("Message-ID:", num)

    SMSmsg = "Email Received!!!\n"
    SMSmsg += "From:" + sender + "\n"
    SMSmsg += "TO:" + to_email + "\n"
    SMSmsg += "Subject:" + subject + "\n"
    SMSmsg += "Email Body:" +scanBody + "\n"


    # sendSMS("+919790928992","Hi testing")
    params = SearchParameter.objects.all()

    for para in params:
        # print (para.hunt_word)
        if para.hunt_word in scanBody:
            print ("Hunted --->",para)
            usersToSend = UserEmailTracking.objects.filter(user__groups__name=para.user_group.name)
            userNotificationToken = ["ExponentPushToken[M6xd9NK-fpsc3t-MNNtQer]","ExponentPushToken[skDDHvLUgvrH7j-VB3gHFP]"]

            for userSend in usersToSend:
                sendSMS("+91"+userSend.mobile,SMSmsg)
                print("Message send to " + userSend.user.username + " to " + userSend.mobile)
                print()
            sendNotificaiton(userNotificationToken,"Test Title", scanBody)



    email_date = parsedate_to_datetime(msg['Date'])
    if email_date:
        email_date = email_date.date()

    email_time = parsedate_to_datetime(msg['Date'])
    if email_time:
        email_time = email_time.time()

    inbox_instance = Inbox.objects.create(
        from_email=sender,
        to_email=to_email,
        subject=subject,
        message=body,
        message_id=num,
        date=email_date,
        time=email_time
    )

    # print("Stored in Inbox:", inbox_instance)

def read_emails():
    mail = imaplib.IMAP4_SSL(imap_host,imap_port)
    mail.login(imap_user, imap_password)
    mail.select('inbox')

    result, data = mail.search(None, 'UNSEEN')  

    if not data[0]:
        # print("No new messages.")
        mail.logout()
        return

    for num in data[0].split():
        # print(num)
        result, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        # print(msg)
        process_email(msg,num)
        mail.store(num, '+FLAGS', '\\Seen')

    mail.logout()

# def sendNotificaiton(UserPushTokenlist, title, message):
#     URL = "https://exp.host/--/api/v2/push/send"
#     headers = {
#         "host": "exp.host",
#         "accept": "application/json",
#         "accept-encoding": "gzip, deflate",
#         "content-type": "application/json"
#     }
#     data = {
#         # "to": "ExponentPushToken[skDDHvLUgvrH7j-VB3gHFP]",
#         "to": UserPushTokenlist,
#         "sound" : "default",
#         "title":title,
#         "body": message
#     }
#     res = requests.post(URL,data=json.dumps(data),headers=headers)
#     print("response",res.text)


def sendNotificaiton(UserPushToken, title, message):
    URL = "https://exp.host/--/api/v2/push/send"
    headers = {
        "host": "exp.host",
        "accept": "application/json",
        "accept-encoding": "gzip, deflate",
        "content-type": "application/json"
    }
    data = {
        # "to": "ExponentPushToken[skDDHvLUgvrH7j-VB3gHFP]",
        "to": UserPushToken,
        "sound" : "default",
        "title":title,
        "body": message
    }
    res = requests.post(URL,data=json.dumps(data),headers=headers)
    print("Notifcation response",res.text)

def sendSMS(toMobile,msg):
    client = Client(sms_sid, sms_auth_token)

    message = client.messages.create(
        from_=sms_from_phone,
        body=msg,
        to=toMobile
    )

    print(message.sid)



# sendSMS("+919790928992","Hi testing")


while True:
    read_emails()
    time.sleep(3)
