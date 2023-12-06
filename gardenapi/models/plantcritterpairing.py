from django.db import models


class PlantCritterPairing(models.Model):
    plant = models.ForeignKey("Plant", on_delete=models.CASCADE, related_name='critters_you_find_on_this_plant')
    critter = models.ForeignKey("Critter", on_delete=models.CASCADE, related_name='plants_where_you_find_this_critter')
