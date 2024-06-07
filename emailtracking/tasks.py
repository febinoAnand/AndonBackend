import traceback
from celery import shared_task
import imaplib
import email
from email import policy
from .models import *
import json
import re
from datetime import datetime
from email.utils import parsedate_to_datetime
from django.contrib.auth.models import User

# Format the message for SMS
def smsFormat(info):
    print("Formatting SMS message with info:", info)
    message = """TicketName: {ticket},
    Raised: {date} {time},
    Field: {field},
    value: {value},
    trigger: [{triggerfilter}],
    message: {message}""".format(
        ticket=info["ticket"],
        date=info["date"],
        time=info["time"],
        field=info["field"],
        value=info["value"],
        triggerfilter=info["triggerfilter"],
        message=info["message"]
    )
    return message

# Format the message for notifications
def notificationFormat(info):
    print("Formatting notification message with info:", info)
    message = """TicketName: {ticket},
    Raised: {date} {time},
    Field: {field},
    value: {value},
    trigger: [{triggerfilter}],
    message: {message}""".format(
        ticket=info["ticket"],
        date=info["date"],
        time=info["time"],
        field=info["field"],
        value=info["value"],
        triggerfilter=info["triggerfilter"],
        message=info["message"]
    )
    return message

# Check if a string value passes the filter criteria
def checkTriggerPassString(filter, value):
    print("Checking string filter:", filter.operator, filter.value, "against value:", value)
    if filter.operator == "equals":
        return value == filter.value
    return False

# Check if a numerical value passes the filter criteria
def checkTriggerPassNumber(filter, value):
    print("Checking number filter:", filter.operator, filter.value, "against value:", value)
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
    return False

# Check if a value is a number
def is_number(num):
    types = [int, float, complex]
    for t in types:
        if isinstance(num, t):
            return True
    return False

# Extract numbers from a string
def extract_numbers(text):
    print("Extracting numbers from text:", text)
    pattern = r'\d+'
    numbers = re.findall(pattern, text)
    return [int(num) for num in numbers]

# Extract ticket information from the email message
def extract_ticket_info(text):
    print("Extracting ticket info from text")
    pattern = r"a new ticket \"(?P<ticket_name>.*?)\" has been created.*?(?P<info>Ticket type:.*?)(?=(a new ticket|$))"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        ticket_name = match.group('ticket_name')
        info = match.group('info')
        info_pattern = r"(?P<key>.*?): (?P<value>[^\n]+)"
        matches = re.findall(info_pattern, info)
        ticket_info = {f"{key.strip()}": value.strip() for key, value in matches}
        ticket_info['Ticket Name'] = ticket_name
        print("Extracted ticket info:", ticket_info)
        return ticket_info
    print("No match found for ticket info extraction")
    return None

# Generate JSON data from the ticket information
def generate_json(ticket_info):
    print("Generating JSON from ticket info:", ticket_info)
    if ticket_info:
        json_data = {
            "Ticket Name": ticket_info['Ticket Name'],
            "fields": ticket_info
        }
        del json_data['fields']['Ticket Name']
        return json.dumps(json_data)
    return None

# Connect to the email server and retrieve unread emails
def connect_to_mail_server(imap_host, imap_user, password, port):
    print(f"Connecting to mail server: {imap_host} with user: {imap_user}")
    mail = imaplib.IMAP4_SSL(imap_host, port)
    mail.login(imap_user, password)
    mail.select('Inbox')
    status, data = mail.search(None, '(UNSEEN)')
    print("Connected to mail server, status:", status)
    return mail, data

# Process each unread email
def process_email(mail, email_id):
    print(f"Processing email ID: {email_id}")
    status, data = mail.fetch(email_id, '(RFC822)')
    email_msg = data[0][1]
    email_msg = email.message_from_bytes(email_msg, policy=policy.SMTP)
    message_payload = ""
    for part in email_msg.walk():
        if part.get_content_type() == "text/plain":
            message_payload += part.get_payload(decode=True).decode()
    email_date = parsedate_to_datetime(email_msg['Date']).date() if parsedate_to_datetime(email_msg['Date']) else None
    email_time = parsedate_to_datetime(email_msg['Date']).time() if parsedate_to_datetime(email_msg['Date']) else None
    print(f"Processed email: From - {email_msg['From']}, Date - {email_date}, Time - {email_time}, Subject - {email_msg['Subject']}")
    return email_msg, message_payload, email_date, email_time

# Save the email to the inbox model
def save_inbox(email_msg, message_payload, email_date, email_time, email_id):
    print("Saving email to Inbox model")
    return Inbox.objects.create(
        date=email_date,
        time=email_time,
        from_email=email_msg['From'],
        to_email=email_msg['To'],
        subject=email_msg['Subject'],
        message=message_payload,
        message_id=email_id
    )

# Extract fields and save to the ticket model
def extract_and_save_fields(message_payload, email_date, email_time, inwardMail):
    print("Extracting and saving fields from email payload")
    ticket_info = extract_ticket_info(message_payload)
    json_data = json.loads(generate_json(ticket_info))
    selected_field = {}
    if "Ticket Name" in json_data.keys():
        for key, value in json_data["fields"].items():
            field_exist = Parameter.objects.filter(field=key)
            if field_exist:
                numbers = extract_numbers(value)
                if field_exist[0].datatype == "number":
                    value = numbers[0] if numbers else "Not valid"
                selected_field[key] = value
        extractedTicket = Ticket.objects.create(
            ticketname=json_data["Ticket Name"],
            date=email_date,
            time=email_time,
            inboxMessage=inwardMail,
            actual_json=json_data["fields"],
            required_json=selected_field
        )
        print("Fields extracted and saved to Ticket model:", extractedTicket)
        return extractedTicket, selected_field
    return None, None

# Check if triggers are satisfied and generate reports
def check_triggers(selected_field, extractedTicket):
    print("Checking triggers for selected fields")
    sms_to_send = []
    notification_to_send = []
    for key, value in selected_field.items():
        triggerList = Trigger.objects.filter(trigger_field__field=key).filter(trigger_switch=True)
        print(f"Field: {key}, Value: {value}, Number of triggers: {len(triggerList)}")
        for trigger in triggerList:
            parameterFilterList = trigger.parameter_filter_list.all()
            isTriggerSatisfy = True
            filterString = []
            for filter in parameterFilterList:
                filterString.append(filter.operator + " - " + filter.value)
                if trigger.trigger_field.datatype == "number" and is_number(value):
                    filter.value = int(filter.value)
                    isTriggerPass = checkTriggerPassNumber(filter, value)
                elif trigger.trigger_field.datatype == "character" and not is_number(value):
                    isTriggerPass = checkTriggerPassString(filter, value)
                else:
                    isTriggerPass = False
                isTriggerSatisfy = isTriggerSatisfy and isTriggerPass
            print(f"Trigger: {trigger}, Is satisfied: {isTriggerSatisfy}")
            if isTriggerSatisfy:
                Report.objects.create(
                    date=datetime.now().strftime("%Y-%m-%d"),
                    time=datetime.now().strftime("%H:%M:%S"),
                    active_trigger=trigger,
                    actual_value=value,
                    ticket=extractedTicket
                )
                triggerReportData = {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "field": trigger.trigger_field.field,
                    "ticket": extractedTicket.ticketname,
                    "triggerfilter": "and ".join(filterString),
                    "message": trigger.notification_message,
                    "value": value
                }
                print("Trigger report data:", triggerReportData)
                if trigger.send_sms:
                    for user in User.objects.filter(groups=trigger.group_to_send):
                        sms_to_send.append({
                            "mobileNo": user.last_name,  # TODO: change this to mobile no in user auth model
                            "message": smsFormat(triggerReportData)
                        })
                if trigger.send_notification:
                    for user in User.objects.filter(groups=trigger.group_to_send):
                        notification_to_send.append({
                            "noti-token": user.last_name,  # TODO: change this to noti-token in notification app
                            "title": triggerReportData["ticket"],
                            "message": notificationFormat(triggerReportData)
                        })
    return sms_to_send, notification_to_send

# Main task function
@shared_task
def inboxReadTask(args):
    currentSetting = Setting.objects.all()[0]
    if not currentSetting.checkstatus:
        print("Check status is False. Exiting task.")
        return

    print("Reading Mail Box")

    imap_host = currentSetting.host
    imap_user = currentSetting.username
    password = currentSetting.password
    port = currentSetting.port

    mail, data = connect_to_mail_server(imap_host, imap_user, password, port)

    # Retrieve and sort email ids by received time
    email_data = []
    for num in data[0].split():
        try:
            status, fetched_data = mail.fetch(num, '(RFC822)')
            email_msg = fetched_data[0][1]
            email_msg = email.message_from_bytes(email_msg, policy=policy.SMTP)
            email_date = parsedate_to_datetime(email_msg['Date']) if parsedate_to_datetime(email_msg['Date']) else None
            email_data.append((num, email_date))
        except Exception as e:
            print("Exception occurred while fetching email:", e)
            traceback.print_exc()

    # Sort emails by date (oldest first)
    email_data.sort(key=lambda x: x[1])

    # Process each email in the sorted order
    for email_id, email_date in email_data:
        try:
            email_msg, message_payload, email_date, email_time = process_email(mail, email_id)
            inwardMail = save_inbox(email_msg, message_payload, email_date, email_time, email_id)
            extractedTicket, selected_field = extract_and_save_fields(message_payload, email_date, email_time, inwardMail)
            if extractedTicket:
                sms_to_send, notification_to_send = check_triggers(selected_field, extractedTicket)
                print("smstosend->", sms_to_send)
                print("notification->", notification_to_send)
        except Exception as e:
            print("Exception occurred while processing email:", e)
            traceback.print_exc()

    return "Successfully done"

