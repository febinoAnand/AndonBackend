import django
import os
import re
import json
from datetime import datetime
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'andondjango.settings')
django.setup()

from emailtracking.models import *

from django.contrib.auth.models import User


def extract_numbers(text):
    # Define a regex pattern to extract numbers
    pattern = r'\d+'
    # Find all numbers in the text
    numbers = re.findall(pattern, text)
    # Convert the numbers to integers
    numbers = [int(num) for num in numbers]
    return numbers

def extract_dates(text):
    # Define a regex pattern to extract dates
    date_formats = ['%d/%m/%Y', '%d-%m-%Y']  # Add more formats if needed
    dates = []
    for format in date_formats:
        try:
            date_obj = datetime.strptime(text, format)
            dates.append(date_obj.strftime('%Y-%m-%d'))
        except ValueError:
            pass
    return dates

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

# Sample text
text = """Hello moneo-user,

a new ticket "Static threshold - 24-03-15-062104-xLLo" has been created. Please see the following information:

Ticket type: upper alarm
Occurred (UTC+0:00): 15/03/2024 06:21:03
Threshold violation: 21 cm
Defined threshold value: 20 cm
Topology: ip rings / O5D100 / Distance
Urgency: High"""

message_payload = """Hello moneo-user,

a new ticket "Static threshold - 24-03-15-062104-xLLo" has been created. Please see the following information:

Ticket type: upper alarm
Occurred (UTC+0:00): 15/03/2024 06:21:03
Threshold violation: 21 cm
Defined threshold value: 20 cm
Topology: ip rings / O5D100 / Distance
Urgency: High"""

# Extract ticket information
# ticket_info = extract_ticket_info(text)

# Generate JSON
# json_data = generate_json(ticket_info)

# json_data = json.loads(json_data)

# Print the JSON data
# print(json_data)


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
        # extractedTicket = Ticket.objects.create(
        #     ticketname = json_data["Ticket Name"],
        #     date = datetime.now().strftime("%Y-%m-%d"),
        #     time = datetime.now().strftime("%H:%M:%S"),
        #     inboxMessage = inwardMail,
        #     actual_json = json_data["fields"],
        #     required_json = selected_field
        # )
        print("Fields were saved in models.....")

        sms_to_send = []
        notification_to_send = []

        print ("Now Finding Active Triggers with reference selected fields.....")
        print ()

        #finding active trigger
        for key,value in selected_field.items():
            triggerList = Trigger.objects.filter(trigger_field__field__iexact = key).filter(trigger_switch=True)
            print(key,"-",value)
            print("No.of Triggers","-",len(triggerList))

            # if is_number(value) :
            #     print ("field datatype is number")
            # else:
            #     print ("field datatype is character")


            if len(triggerList) > 0:
                print("Getting Trigger Filters...")

            for trigger in triggerList:
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

                #Add it in the ticket report
                # if isTriggerSatisfy:
                    # triggerReport = Report.objects.create(
                    #     date = datetime.now().strftime("%Y-%m-%d"),
                    #     time = datetime.now().strftime("%H:%M:%S"),
                    #     active_trigger = trigger,
                    #     ticket = extractedTicket
                    # )

                triggerReportData = {}
                triggerReportData["date"]=datetime.now().strftime("%Y-%m-%d")
                triggerReportData["time"]=datetime.now().strftime("%H:%M:%S")
                triggerReportData["field"] = trigger.trigger_field.field
                triggerReportData["ticket"] = "Static threshold - 24-03-15-062104-xLLo" #TODO:get is from trigger report
                triggerReportData["triggerfilter"] = "and ".join(filterString)   #TODO:get is from trigger report
                triggerReportData["message"] = trigger.notification_message
                triggerReportData["value"] = "20"                                       #TODO:get is from trigger report

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
                    # if trigger.send_notification:
                    #     userList = User.objects.filter(groups = trigger.group_to_send)
                    #     print (userList)
                print ()

                #get all users and add it to list



            print()
        print("smstosend->",sms_to_send)

        print("notification->",notification_to_send)
        print("----------------------------")
        print ()
    print()
except Exception as e:
    # print ("error->",e)
    traceback.print_exc()
