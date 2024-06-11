from smsgateway.models import SendReport, SMSNumber, Setting


def sendSMSWithMobile(fromNumber, toNumber, msg):
    # Check if the Setting instance is active
    setting = Setting.objects.first()
    if setting and setting.is_active:
        print(f"SMS sent from Number = {fromNumber}, to Number = {toNumber}, msg = {msg}")
        fromNum = SMSNumber.objects.get(smsnumber=fromNumber)
        SendReport.objects.create(
            to_number=toNumber,
            from_number=fromNum,
            message=msg
        )
        print("Message Sent")
    else:
        print("SMS not sent. The Setting instance is inactive.")

def sendSMS(toNumber, msg):
    # Check if the Setting instance is active
    setting = Setting.objects.first()
    if setting and setting.is_active:
        fromNumber = SMSNumber.objects.first().smsnumber
        sendSMSWithMobile(fromNumber, toNumber=toNumber, msg=msg)
    else:
        print("SMS not sent. The Setting instance is inactive.")

