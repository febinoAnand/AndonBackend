from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from devices.models import Machine


class ProblemCode(models.Model):
    problemCode = models.CharField(max_length=20,blank=False,unique=True)
    problemName = models.CharField(max_length=30)
    problemDescription = models.TextField(max_length=100)

    typeChoice = (
        ("ISSUE", "issue"),
        ("ACKNOWLEDGE", "acknowledge"),
        ("FINE", "fine"),
    )
    problemType = models.CharField(max_length=15,choices=typeChoice,null=False,blank=True)

    def __str__(self):
        return self.problemName

class Indicator(models.Model):
    indicatorID = models.CharField(max_length=15,blank=False,unique=True)
    indicatorpin = models.IntegerField(blank=False,unique=True)
    indicatorColor = models.CharField(max_length=7)
    indicatorColorName = models.CharField(max_length=20)
    def __str__(self):
        return str(self.indicatorID + " - " + self.indicatorColorName)

class Button(models.Model):
    buttonID = models.CharField(max_length=15,blank=False,unique=True)
    buttonName = models.CharField(blank=False,max_length=20)
    buttonColorName = models.CharField(blank=False,max_length=20)
    buttonColor = models.CharField(max_length=7,blank=False)
    def __str__(self):
        return self.buttonName


class Event(models.Model):
    eventID = models.CharField(max_length=15,blank=False,unique=True)
    button = models.ForeignKey(Button,blank=False,on_delete=models.CASCADE,related_name='buttons')
    problem = models.ForeignKey(ProblemCode,blank=False,on_delete=models.CASCADE,related_name='problems')
    indicator = models.ForeignKey(Indicator,blank=False,on_delete=models.CASCADE,related_name='indicators')
    acknowledgeUser = models.ManyToManyField(User,blank=True,related_name='ackuser')
    notifyUser = models.ManyToManyField(User,blank=True,related_name='notiuser')
    def __str__(self):
        return str(self.eventID)

    def Button(self):
        return self.button.buttonID +" - "+ self.button.buttonName

    def Problem(self):
        return self.problem.problemCode +" - "+ self.problem.problemName +" - "+ self.problem.problemType

    def Indicator(self):
        return self.indicator.indicatorID +" - "+ self.indicator.indicatorColorName


class EventGroup(models.Model):
    groupID = models.CharField(max_length=15,blank=False,unique=True)
    groupName = models.CharField(max_length=50,blank=False,null=True)
    events = models.ManyToManyField(Event, related_name='eventGroup')
    machines = models.ManyToManyField(Machine,related_name='machinesList')

    def selectedEvents(self):
        return ", \n".join([str(p)+"--->["+str(p.button.buttonName)+", "+p.problem.problemName+", "+p.indicator.indicatorColorName+"]" for p in self.events.all()])

    def __str__(self):
        return str(self.groupID)






