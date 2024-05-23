import datetime as datetime
from django.utils import timezone,dateformat
import datetime
from django.db import models
from events.models import Event,EventGroup
from devices.models import Machine,RFID, Device

# Create your models here.

class RawData(models.Model):
    # {"date": "2023-08-26", "time": "08:26:17", "eventID": "EV123-001", "deviceID": "DEV123","eventGroupID":"GEV123"} Data format
    # datetime = models.DateTimeField(editable=False,default=dateformat.format(timezone.now(), 'Y-m-d H:i:s'))
    datetime = models.DateTimeField(editable=False,default=datetime.datetime.now)
    data = models.TextField(blank=False)
    date = models.DateField(blank=True,null=True)
    time = models.TimeField(blank=True,null=True)
    eventID = models.ForeignKey(Event,on_delete=models.CASCADE,blank=True,null=True)
    deviceID = models.ForeignKey(Device,on_delete=models.CASCADE,blank=True,null=True)
    machineID = models.ForeignKey(Machine,on_delete=models.CASCADE,blank=False,null=True)
    eventGroupID = models.ForeignKey(EventGroup,on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return str(self.id)

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.datetime = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    #
    #     return super(RawData, self).save(*args, **kwargs)

class ProblemData(models.Model):
    date = models.DateField()
    time = models.TimeField()
    eventID = models.ForeignKey(Event,blank=False,on_delete=models.CASCADE)
    eventGroupID = models.ForeignKey(EventGroup,blank=False,on_delete=models.CASCADE)
    machineID = models.ForeignKey(Machine, blank=False, on_delete=models.CASCADE)
    deviceID = models.ForeignKey(Device, blank=False, on_delete=models.CASCADE, null=True)
    issueTime = models.DateTimeField()
    acknowledgeTime = models.DateTimeField(blank=True,null=True)
    rfidTime = models.ForeignKey(RFID,on_delete=models.CASCADE,blank=True,null=True)
    endTime = models.DateTimeField(blank=True,null=True)
    dateTimeNow = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.eventGroupID)


class LastProblemData(models.Model):
    # UUID = models.UUIDField()
    date = models.DateField()
    time = models.TimeField()
    eventID = models.ForeignKey(Event,blank=False,on_delete=models.CASCADE)
    eventGroupID = models.ForeignKey(EventGroup,blank=False,on_delete=models.CASCADE)
    deviceID = models.ForeignKey(Device, blank=False, on_delete=models.CASCADE, null=True)
    machineID = models.ForeignKey(Machine, blank=False, on_delete=models.CASCADE)
    issueTime = models.DateTimeField(blank=True,null=True)
    acknowledgeTime = models.DateTimeField(blank=True,null=True)
    rfidTime = models.ForeignKey(RFID,on_delete=models.CASCADE,blank=True,null=True)
    endTime = models.DateTimeField(blank=True,null=True)
    dateTimeNow = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.eventGroupID)








