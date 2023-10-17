from django.db import models

# Create your models here.
class Port(models.Model):
    portname = models.CharField(max_length=20,unique=True,blank=False)
    def __str__(self):
        return self.portname


class UART(models.Model):
    comport = models.OneToOneField(Port, blank=False, on_delete=models.CASCADE)
    baudrate = models.IntegerField(choices=((9600,"9600"), (115200,"115200")), blank=False)
    parity = models.CharField(max_length=10,choices=(("none","None"),("odd","Odd"),("even","Even")),blank=False)
    databit = models.IntegerField(choices=((5,'5'),(6,'6'),(7,'7'),(8,'8')),blank=False)
    stopbit = models.DecimalField(choices=((1.0,'1'),(1.5,'1.5'),(2.0,'2')),max_digits=4,decimal_places=1,blank=False)
    CTS = models.BooleanField()
    DTR = models.BooleanField()
    XON = models.BooleanField()
    def __str__(self):
        return self.comport.portname

class MQTT(models.Model):
    host = models.CharField(max_length=50,blank=False)
    port = models.IntegerField(blank=False)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    def __str__(self):
        return self.host
