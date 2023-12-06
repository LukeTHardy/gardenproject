from django.db import models

class Light(models.Model):
    hours = models.IntegerField(null=True)