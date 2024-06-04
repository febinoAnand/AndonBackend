from django.db import models



class Setting(models.Model):
    
    logo_path = models.ImageField(upload_to='logos/')

    class Meta:
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'

    def __str__(self):
        return self.logo_path.name  

