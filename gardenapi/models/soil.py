from django.db import models

class Soil(models.Model):
    type = models.CharField(max_length=500, null=True, blank=True)