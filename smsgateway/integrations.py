from .models import SendReport,SMSNumber

def sendSMSWithMobile(fromNumber,tonumber,msg):
    print ("SMS sent from Number = " + fromNumber + ", to Number ="+ tonumber+", msg = "+msg)
    fromNum = SMSNumber.objects.get(smsnumber = fromNumber)
    SendReport.objects.create(
        to_number = tonumber,
        from_number = fromNum,
        message = msg
    )
    print ("Message Sent")


def sendSMS(toNumber,msg):
    fromNumber = SMSNumber.objects.first().smsnumber
    sendSMSWithMobile(fromNumber,tonumber=toNumber,msg=msg)
