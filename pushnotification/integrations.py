from django.contrib.auth.models import User
# from userauth.models import UserDetail  
from .models import SendReport  
import datetime

def sendNotificationWithUser(user, title, message):
    print(f"Notification sent to User = {user.username}, Title = {title}, Message = {message}")
    SendReport.objects.create(
        date=datetime.date.today(),
        time=datetime.datetime.now().time(),
        title=title,
        message=message,
        send_to_user=user
    )
    print("Notification Sent")

def sendNotification(noti_token, title, message):
    try:
        user_detail = UserDetail.objects.get(device_id=noti_token)
        user = user_detail.extUser
        sendNotificationWithUser(user, title, message)
        print(f"Notification sent to {user.username} with Device ID: {user_detail.device_id}")
    except UserDetail.DoesNotExist:
        print(f"UserDetail with noti-token {noti_token} does not exist. Notification not sent.")


