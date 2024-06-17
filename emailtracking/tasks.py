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
from Userauth.models import UserDetail
from pushnotification.integrations import sendNotification, sendNotificationWithUser
import operator
from smsgateway.integrations import *
from emailtracking.models import Setting


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
def check_conditions(conditions, input_number):
    ops = {
        '>=': operator.ge,
        '<': operator.lt,
        '==': operator.eq,
        '!=': operator.ne,
        '<=': operator.le,
        '>': operator.gt,
        '<': operator.lt,
        'exists': lambda x, y: x == y
    }

    final_result = None

    for i, cond in enumerate(conditions):
        op = ops[cond['operator']]
        value = float(cond['fixed_value'])

        current_result = op(input_number, value)

        if i == 0:
            final_result = current_result
        else:
            logical_op = cond.get('logical_operator', 'and') 
            if logical_op == 'and':
                final_result = final_result and current_result
            elif logical_op == 'or':
                final_result = final_result or current_result

        if not final_result:
            break

    return final_result

def map_operator(operator_text):
    operator_mapping = {
        'greater than': '>',
        'less than': '<',
        'greater than or equal to': '>=',
        'less than or equal to': '<=',
        'equal to': '==',
        'not equal to': '!='
    }
    return operator_mapping.get(operator_text, operator_text)


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
            print("parameterFilterList------>", parameterFilterList)
            isTriggerSatisfy = True
            filterString = []
            conditions = []
            for filter in parameterFilterList:
                filterString.append(filter.operator + " - " + str(filter.value))
                condition = {
                    'operator': map_operator(filter.operator),
                    'fixed_value': filter.value,
                    'logical_operator': filter.logical_operator
                }
                conditions.append(condition)

            if trigger.trigger_field.datatype == "number" and is_number(value):
                isTriggerSatisfy = check_conditions(conditions, float(value))

            elif trigger.trigger_field.datatype == "character" and not is_number(value):
                for filter in parameterFilterList:
                    isTriggerPass = checkTriggerPassString(filter, value)
                    isTriggerSatisfy = isTriggerSatisfy and isTriggerPass
            else:
                isTriggerSatisfy = False

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
                    for user in trigger.users_to_send.all():
                        try:
                            user_detail = UserDetail.objects.get(extUser=user)
                            sms_to_send.append({
                                "mobileNo": user_detail.mobile_no,
                                "message": smsFormat(triggerReportData)
                            })
                        except UserDetail.DoesNotExist:
                            print(f"UserDetail does not exist for user: {user}")

                if trigger.send_notification:
                    for user in trigger.users_to_send.all():
                        try:
                            user_detail = UserDetail.objects.get(extUser=user)
                            notification_to_send.append({
                                "noti-token": user_detail.device_id,
                                "title": triggerReportData["ticket"],
                                "message": notificationFormat(triggerReportData)
                            })
                        except UserDetail.DoesNotExist:
                            print(f"UserDetail does not exist for user: {user}")

    return sms_to_send, notification_to_send

# Main task function
@shared_task
def inboxReadTask(args):
    try:
        currentSetting = Setting.objects.first()
        if not currentSetting:
            print("No current setting found. Exiting task.")
            return

        if not currentSetting.checkstatus:
            print("Check status is False. Exiting task.")
            return

        print("Reading Mail Box")

        imap_host = currentSetting.host
        imap_user = currentSetting.username
        password = currentSetting.password
        port = currentSetting.port

        mail, data = connect_to_mail_server(imap_host, imap_user, password, port)
        if not mail:
            print("Failed to connect to mail server")
            return

        # Get all allowed email IDs from the EmailID table
        allowed_email_ids = EmailID.objects.filter(active=True).values_list('email', flat=True)

        # Retrieve and sort email ids by received time
        email_data = []
        for num in data[0].split():
            try:
                status, fetched_data = mail.fetch(num, '(RFC822)')
                if status != 'OK':
                    continue
                
                email_msg = email.message_from_bytes(fetched_data[0][1])
                email_from = email_msg.get("From")

                if any(allowed_email in email_from for allowed_email in allowed_email_ids):
                    email_date = parsedate_to_datetime(email_msg['Date'])
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
                    for sendto in sms_to_send:
                        # if sendto["user"].is_active:
                        sendSMS(sendto["mobileNo"], sendto["message"])
                        # else:
                        #     print('User is Inactive')
                    print("notification->", notification_to_send)
                    for notification in notification_to_send:
                        # if notification["user"].is_active:
                        msg = sendNotification(notification["noti-token"], notification["title"], notification["message"])
                        print(msg)
                        # else:
                            # print('User is Inactive')
            except Exception as e:
                print("Exception occurred while processing email:", e)
                traceback.print_exc()

        return "Successfully done"
    except Exception as e:
        print("Exception occurred in inboxReadTask:", e)
        traceback.print_exc()
        return "Task failed"

