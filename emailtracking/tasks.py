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
from pushnotification.models import NotificationAuth
from pushnotification.integrations import sendNotification, sendNotificationWithUser
from smsgateway.integrations import sendSMS

def smsFormat(info):
    print("Formatting SMS message with info:", info)
    message = """TicketName: {ticket_name},
    Raised: {occurred},
    Threshold violation: {threshold_violation},
    Defined threshold: {defined_threshold},
    Topology: {topology},
    HR1: {hr1}""".format(
        ticket_name=info["ticket_name"],
        occurred=info["occurred"],
        threshold_violation=info["threshold_violation"],
        defined_threshold=info["defined_threshold"],
        topology=info["topology"],
        hr1=info["hr1"]
    )
    return message

def notificationFormat(info):
    print("Formatting notification message with info:", info)
    message = """TicketName: {ticket_name},
    Raised: {occurred},
    Threshold violation: {threshold_violation},
    Defined threshold: {defined_threshold},
    Topology: {topology},
    HR1: {hr1}""".format(
        ticket_name=info["ticket_name"],
        occurred=info["occurred"],
        threshold_violation=info["threshold_violation"],
        defined_threshold=info["defined_threshold"],
        topology=info["topology"],
        hr1=info["hr1"]
    )
    return message


def extract_numbers(text):
    print("Extracting numbers from text:", text)
    pattern = r'\d+'
    numbers = re.findall(pattern, text)
    return [int(num) for num in numbers]

def extract_ticket_info(text):
    print("Extracting ticket info from text")
    pattern = r"a new ticket \"(?P<ticket_name>.*?)\" has been created\..*?Ticket type: (?P<ticket_type>.*?)\n.*?Occurred \(UTC\+0:00\): (?P<occurred>.*?)\n.*?Threshold violation: (?P<threshold_violation>.*?)\n.*?Defined threshold value: (?P<defined_threshold>.*?)\n.*?Topology: (?P<topology>.*?)\n.*?HR1: (?P<hr1>.*?)\n"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        ticket_info = match.groupdict()
        print("Extracted ticket info:", ticket_info)
        return ticket_info
    print("No match found for ticket info extraction")
    return None


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

def connect_to_mail_server(imap_host, imap_user, password, port):
    print(f"Connecting to mail server: {imap_host} with user: {imap_user}")
    mail = imaplib.IMAP4_SSL(imap_host, port)
    mail.login(imap_user, password)
    mail.select('Inbox')
    status, data = mail.search(None, '(UNSEEN)')
    print("Connected to mail server, status:", status)
    return mail, data

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

def extract_department_from_topology(topology):
    print(f"Extracting department from topology: {topology}")
    topology_parts = topology.split('/')
    for part in topology_parts:
        stripped_part = part.strip()
        if Department.objects.filter(department=stripped_part).exists():
            return stripped_part
    return None


def extract_and_save_fields(message_payload, email_date, email_time, inwardMail):
    print("Extracting and saving fields from email payload")
    ticket_info = extract_ticket_info(message_payload)
    json_data = json.loads(generate_json(ticket_info))
    selected_field = {}
    department_name = None
    if "Ticket Name" in json_data.keys():
        for key, value in json_data["fields"].items():
            selected_field[key] = value
            if key == "Topology":
                topology_parts = extract_department_from_topology(value)
                for part in topology_parts:
                    if Department.objects.filter(department=part.strip()).exists():
                        department_name = part.strip()
                        break
        extractedTicket = Ticket.objects.create(
            ticketname=json_data["Ticket Name"],
            date=email_date,
            time=email_time,
            inboxMessage=inwardMail,
            actual_json=json_data["fields"]
        )
        if department_name:
            extractedTicket.actual_json['department_name'] = department_name
        print("Fields extracted and saved to Ticket model:", extractedTicket)
        return extractedTicket, selected_field
    return None, None

def check_ticket_satisfaction(selected_field, extractedTicket):
    print("Checking if ticket is satisfied")
    department_name = extractedTicket.actual_json.get('department_name')
    if department_name:
        department_exists = Department.objects.filter(department=department_name).exists()
        extractedTicket.is_satisfied = department_exists
    else:
        extractedTicket.is_satisfied = False
    extractedTicket.save()
    return extractedTicket.is_satisfied

def generate_reports(selected_field, extractedTicket):
    print("Generating reports for ticket:", extractedTicket.ticketname)
    department_name = extractedTicket.actual_json.get('department_name')
    
    if department_name:
        try:
            department = Department.objects.get(department=department_name)
            report = Report.objects.create(
                Department=department.dep_alias,
                message=f"""TicketName: {extractedTicket.ticketname},
                          Raised: {extractedTicket.date} {extractedTicket.time},
                          Message: {extractedTicket.inboxMessage.message}"""
            )
            for user in department.users_to_send.all():
                report.send_to_user.add(user)
            
            print(f"Report created for department: {department.department}")
            return report
        except Department.DoesNotExist:
            print(f"Department {department_name} does not exist. Report not created.")
    else:
        print("Department name not found in ticket. Report not created.")
    
    return None

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

        allowed_email_ids = EmailID.objects.filter(active=True).values_list('email', flat=True)

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

        email_data.sort(key=lambda x: x[1])

        for email_id, email_date in email_data:
            try:
                email_msg, message_payload, email_date, email_time = process_email(mail, email_id)
                inwardMail = save_inbox(email_msg, message_payload, email_date, email_time, email_id)
                ticket_info = extract_ticket_info(message_payload)

                if ticket_info:
                    sms_message = smsFormat(ticket_info)
                    notification_message = notificationFormat(ticket_info)
                    department_name = extract_department_from_topology(ticket_info["topology"])

                    if department_name:
                        try:
                            department = Department.objects.get(department=department_name)
                            report = Report.objects.create(
                                Department=department.dep_alias,
                                message=f"""TicketName: {ticket_info["ticket_name"]},
                                          Raised: {ticket_info["occurred"]},
                                          Message: {message_payload}"""
                            )
                            for user in department.users_to_send.all():
                                user_detail = UserDetail.objects.get(extUser=user)
                                sendSMS(user_detail.mobile_no, sms_message)
                                # sendNotification(user, notification_message)

                                try:
                                    noti_auth = NotificationAuth.objects.get(user_to_auth=user)
                                    noti_token = noti_auth.noti_token
                                    sendNotification(noti_token, email_msg['Subject'], notification_message)
                                except NotificationAuth.DoesNotExist:
                                    print(f"NotificationAuth entry not found for user {user.username}. Notification not sent.")
                        except Department.DoesNotExist:
                            print(f"Department {department_name} does not exist. Report not created.")
                    else:
                        print("Department name not found in ticket. Report not created.")
                else:
                    print(f"Ticket info could not be extracted from email ID: {email_id}. Skipping report generation.")
            except Exception as e:
                print("Exception occurred while processing email ID:", email_id, e)
                traceback.print_exc()
    except Exception as e:
        print("Exception occurred in inboxReadTask:", e)
        traceback.print_exc()
