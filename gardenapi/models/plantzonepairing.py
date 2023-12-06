from django.db import models


class PlantZonePairing(models.Model):
    plant = models.ForeignKey("Plant", on_delete=models.CASCADE, related_name='zones_this_plant_grows_in')
    zone = models.ForeignKey("Zone", on_delete=models.CASCADE, related_name='plants_that_grow_in_this_zone')
