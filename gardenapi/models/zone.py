from django.db import models

class Zone(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    plants = models.ManyToManyField(
        "Plant",
        through='PlantZonePairing',
        related_name="zones_for_this_plant"
    )
    