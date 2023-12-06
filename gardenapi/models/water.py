from django.db import models

class Water(models.Model):
    frequency = models.CharField(max_length=500, null=True, blank=True)