from django.db import models

class VeggieCat(models.Model):
    label = models.CharField(max_length=500, null=True, blank=True)