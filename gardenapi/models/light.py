from django.db import models

class Light(models.Model):
    label = models.CharField(max_length=500, null=True, blank=True)