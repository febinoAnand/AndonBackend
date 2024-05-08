import traceback

from celery import shared_task
import imaplib, email
from email import policy
from .models import *
import json
import re
from datetime import datetime
from email.utils import parsedate_to_datetime
from django.contrib.auth.models import User


# inwardMail = Inbox.objects.get(message_id = 70)
def smsFormat(info):
    message = """TicketName: {ticket},
    Raised: {date} {time},
    Field: {field},
    value: {value},
    trigger: [{triggerfilter}],
    message: {message}""".format(
        ticket = info["ticket"],
        date = info["date"],
        time = info["time"],
        field = info["field"],
        value = info["value"],
        triggerfilter = info["triggerfilter"],
        message = info["message"]
    )
    # print ("message->",message)
    return message

def notificationFormat(info):
    message = """TicketName: {ticket},
    Raised: {date} {time},
    Field: {field},
    value: {value},
    trigger: [{triggerfilter}],
    message: {message}""".format(
        ticket = info["ticket"],
        date = info["date"],
        time = info["time"],
        field = info["field"],
        value = info["value"],
        triggerfilter = info["triggerfilter"],
        message = info["message"]
    )
    # print ("message->",message)
    return message

def checkTriggerPassString(filter,value):
    print ("checkfilterstring",filter.operator,filter.value)
    if filter.operator == "equals":
        return value == filter.value
    return False

def checkTriggerPassNumber(filter,value):

    print ("checkfilternumber",filter.operator,filter.value)
    if filter.operator == "greater than":
        return value > filter.value

    elif filter.operator == "greater than or equal":
        return value >= filter.value

    elif filter.operator == "less than":
        return value < filter.value

    elif filter.operator == "less than or equal":
        return value <= filter.value

    elif filter.operator == "equals":
        return value == filter.value

    elif filter.operator == "not equals":
        return value != filter.value

    # elif filter.operator == "is exist":
    #     if value != None or value == 0:
    #     return value

    return False

def is_number(num):
    types = [int, float, complex]
    for t in types:
        if isinstance(num, t):
            return True
    return False

def extract_numbers(text):
    # Define a regex pattern to extract numbers
    pattern = r'\d+'
    # Find all numbers in the text
    numbers = re.findall(pattern, text)
    # Convert the numbers to integers
    numbers = [int(num) for num in numbers]
    return numbers


def extract_ticket_info(text):
    # Define the pattern to extract key-value pairs and ticket name
    pattern = r"a new ticket \"(?P<ticket_name>.*?)\" has been created.*?(?P<info>Ticket type:.*?)(?=(a new ticket|$))"

    # Match the pattern in the text
    match = re.search(pattern, text, re.DOTALL)

    if match:
        ticket_name = match.group('ticket_name')
        info = match.group('info')

        # Define the pattern to extract key-value pairs
        info_pattern = r"(?P<key>.*?): (?P<value>[^\n]+)"

        # Match the pattern in the ticket info
        matches = re.findall(info_pattern, info)

        # Convert matches into a dictionary with key type mentioned
        ticket_info = {f"{key.strip()}": value.strip() for key, value in matches}

        # Extract numbers and dates from the values
        for key, value in ticket_info.items():
            ticket_info[key] = value
            # numbers = extract_numbers(value)
            # dates = extract_dates(value)
            # if numbers:
            #     ticket_info[key] = numbers[0] if len(numbers) == 1 else numbers
            # if dates:
            #     ticket_info[key] = dates[0] if len(dates) == 1 else dates

        ticket_info['Ticket Name'] = ticket_name

        return ticket_info

    else:
        return None

def generate_json(ticket_info):
    if ticket_info:
        json_data = {
            "Ticket Name": ticket_info['Ticket Name'],
            "fields": ticket_info
        }
        del json_data['fields']['Ticket Name']
        return json.dumps(json_data)
    else:
        return None



def checkTriggerPassString(filter,value):
    print ("checkfilterstring",filter.operator,filter.value)
    if filter.operator == "equals":
        return value == filter.value
    return False

def checkTriggerPassNumber(filter,value):

    print ("checkfilternumber",filter.operator,filter.value)
    if filter.operator == "greater than":
        return value > filter.value

    elif filter.operator == "greater than or equal":
        return value >= filter.value

    elif filter.operator == "less than":
        return value < filter.value

    elif filter.operator == "less than or equal":
        return value <= filter.value

    elif filter.operator == "equals":
        return value == filter.value

    elif filter.operator == "not equals":
        return value != filter.value

    # elif filter.operator == "is exist":
    #     if value != None or value == 0:
    #     return value

    return False

def is_number(num):
    types = [int, float, complex]
    for t in types:
        if isinstance(num, t):
            return True
    return False

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


    # for each e-mail messages, print text content
    for num in data[0].split():
        # get a single message and parse it by policy.SMTP (RFC compliant)
        status, data = mail.fetch(num, '(RFC822)')
        email_msg = data[0][1]
        email_msg = email.message_from_bytes(email_msg, policy=policy.SMTP)

        # print("\n----- MESSAGE START -----\n")

        print("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\n" % ( \
            str(email_msg['From']), \
            str(email_msg['To']), \
            str(email_msg['Date']), \
            str(email_msg['Subject'] )))

        message_payload = ""
        for part in email_msg.walk():
            if part.get_content_type() == "text/plain":
                for line in part.get_content():
                    message_payload += line


        print("email->"+message_payload)

        # print("\n----- MESSAGE END -----\n")

        email_date = parsedate_to_datetime(email_msg['Date'])
        if email_date:
            email_date = email_date.date()

        email_time = parsedate_to_datetime(email_msg['Date'])
        if email_time:
            email_time = email_time.time()

        #save mail in the inbox
        inwardMail = Inbox.objects.create(
            date = email_date,
            time = email_time,
            from_email = email_msg['From'],
            to_email = email_msg['To'],
            subject = email_msg['Subject'],
            message = message_payload,
            message_id = num
        )

        print("inbox create...")

        #parse the fields with Ticket name
        try:
            print()
            print("Extracting all fields with ticket name from the message.....")

            ticket_info = extract_ticket_info(message_payload)
            json_data = json.loads(generate_json(ticket_info))

            # print("Json->"+json_data["Ticket Name"])
            print("All Fields were Extracted.....")

            print("Now Extracting Selected fields.....")

            if "Ticket Name" in json_data.keys():

                selected_field = {}

                for key,value in json_data["fields"].items():
                    # print ("'"+key+"'='"+value+"'")
                    fieldExist = Parameter.objects.filter(field=key)
                    count = len(fieldExist)
                    # print(key,"-",count)

                    if count > 0:
                        selected_field[key] = value
                        numbers = extract_numbers(value)
                        if fieldExist[0].datatype == "number":
                            selected_field[key] = numbers[0] if len(numbers) == 1 else numbers
                            if not numbers:
                                selected_field[key] = "Not valid"

                # print(selected_field)

                print("saving all extracted fields and selected fields in the ticket models.....")

                #create ticket model data here
                extractedTicket = Ticket.objects.create(
                    ticketname = json_data["Ticket Name"],
                    date = email_date,
                    time = email_time,
                    inboxMessage = inwardMail,
                    actual_json = json_data["fields"],
                    required_json = selected_field
                )
                print("Fields were saved in models.....")
                print ("Now Finding Active Triggers with reference selected fields.....")
                print ()

                sms_to_send = []
                notification_to_send = []

                #finding active trigger
                for key,value in selected_field.items():
                    triggerList = Trigger.objects.filter(trigger_field__field = key).filter(trigger_switch=True)
                    print(key,"-",value)
                    print("No.of Triggers","-",len(triggerList))

                    # if is_number(value) :
                    #     print ("field datatype is number")
                    # else:
                    #     print ("field datatype is character")


                    if len(triggerList) > 0:
                        print("Getting Trigger Filters...")

                    for trigger in triggerList:
                        print()
                        parameterFilterList = trigger.parameter_filter_list.all()
                        print (parameterFilterList)

                        isTriggerSatisfy = True
                        filterString = []
                        for filter in parameterFilterList:
                            filterString.append(filter.operator+" - "+filter.value)
                            # check the trigger->trigger_field->datatype is string or character
                            if trigger.trigger_field.datatype == "number" and is_number(value) == True:
                                filter.value = int(filter.value)
                                if is_number(filter.value):
                                    isTriggerPass = checkTriggerPassNumber(filter,value)
                                print("filter-",isTriggerPass)

                            elif trigger.trigger_field.datatype == "character" and is_number(value) != True:
                                isTriggerPass = checkTriggerPassString(filter,value)
                                print("filter-",isTriggerPass)
                            else:
                                isTriggerPass = False
                                # print ("given input wrong")

                            isTriggerSatisfy = isTriggerSatisfy and isTriggerPass

                        print ("trigger",isTriggerSatisfy)

                        if isTriggerSatisfy:
                            triggerReport = Report.objects.create(
                                date = datetime.now().strftime("%Y-%m-%d"),
                                time = datetime.now().strftime("%H:%M:%S"),
                                active_trigger = trigger,
                                actual_value = value,
                                ticket = extractedTicket
                            )

                        triggerReportData = {}
                        triggerReportData["date"]=datetime.now().strftime("%Y-%m-%d")
                        triggerReportData["time"]=datetime.now().strftime("%H:%M:%S")
                        triggerReportData["field"] = trigger.trigger_field.field
                        triggerReportData["ticket"] = extractedTicket.ticketname
                        triggerReportData["triggerfilter"] = "and ".join(filterString)
                        triggerReportData["message"] = trigger.notification_message
                        triggerReportData["value"] = value

                        print ("triggerReportData->",triggerReportData)

                        #check trigger satisfies if yes check sms to send and notication to send
                        if isTriggerSatisfy:
                            if trigger.send_sms:
                                userList = User.objects.filter(groups = trigger.group_to_send)
                                for user in userList:
                                    sms_detail_dic = {}
                                    sms_detail_dic["mobileNo"] = user.last_name #TODO: change this to mobile no in  user auth model
                                    sms_detail_dic["message"] = smsFormat(triggerReportData)
                                    sms_to_send.append(sms_detail_dic)
                                    # print(sms_detail_dic)
                            if trigger.send_notification:
                                userList = User.objects.filter(groups = trigger.group_to_send)
                                for user in userList:
                                    notification_detail_dic = {}
                                    notification_detail_dic["noti-token"] = user.last_name       #TODO: change this to noti-token in notification app
                                    notification_detail_dic["title"] = triggerReportData["ticket"]
                                    notification_detail_dic["message"] = notificationFormat(triggerReportData)
                                    notification_to_send.append(notification_detail_dic)


                        print ()
                    print("smstosend->",sms_to_send)
                    print("notification->",notification_to_send)
                    print()
        except Exception as e:
            traceback.print_exc()

    return "Successfully done"