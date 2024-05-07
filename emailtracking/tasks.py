from celery import shared_task
import imaplib, email
from email import policy
from .models import Setting


@shared_task
def inboxReadTask(args):

    currentSetting = Setting.objects.all()[0]
    if currentSetting.checkstatus != True:
        return

    print ("reading Mail Box")

    imap_host = currentSetting.host
    imap_user = currentSetting.username
    password = currentSetting.password
    port = currentSetting.port

    # init imap connection
    mail = imaplib.IMAP4_SSL(imap_host, port)
    rc, resp = mail.login(imap_user, password)

    # select only unread messages from inbox
    mail.select('Inbox')
    status, data = mail.search(None, '(UNSEEN)')

    # print ("Status--->",status)
    # print ("Data--->",data[0])

    # for each e-mail messages, print text content
    for num in data[0].split():
        # get a single message and parse it by policy.SMTP (RFC compliant)
        status, data = mail.fetch(num, '(RFC822)')
        email_msg = data[0][1]
        email_msg = email.message_from_bytes(email_msg, policy=policy.SMTP)

        print("\n----- MESSAGE START -----\n")

        print("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\n" % ( \
            str(email_msg['From']), \
            str(email_msg['To']), \
            str(email_msg['Date']), \
            str(email_msg['Subject'] )))

        # print only message parts that contain text data
        for part in email_msg.walk():
            if part.get_content_type() == "text/plain":
                for line in part.get_content().splitlines():
                    print(line)

        print("\n----- MESSAGE END -----\n")
        # inboxReadTask.delay()
    return "Successfully done"