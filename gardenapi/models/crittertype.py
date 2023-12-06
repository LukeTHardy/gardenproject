from django.db import models

class CritterType(models.Model):
    label = models.CharField(max_length=500, null=True, blank=True)