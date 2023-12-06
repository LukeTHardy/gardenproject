from django.db import models


class CompanionPairing(models.Model):
    plant1 = models.ForeignKey("Plant", on_delete=models.CASCADE, related_name='companion_plants_1')
    plant2 = models.ForeignKey("Plant", on_delete=models.CASCADE, related_name='companion_plants_2')