from django.db import models

class PlantType(models.Model):
    label = models.CharField(max_length=500, null=True, blank=True)
    