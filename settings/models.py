from django.db import models
from django.core.exceptions import ValidationError

class Setting(models.Model):
    logo_path = models.ImageField(upload_to='logos/')

    class Meta:
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'

    def __str__(self):
        return self.logo_path.name

    def clean(self):
        if Setting.objects.exists() and not self.pk:
            raise ValidationError('Only one instance of Setting is allowed.')

    def save(self, *args, **kwargs):
        self.full_clean()  
        super(Setting, self).save(*args, **kwargs)
