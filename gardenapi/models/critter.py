from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Critter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='critters_added_by_this_user')
    name = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='images/critters',
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'avif'])]
    )
    description = models.CharField(max_length=500, null=True, blank=True)
    size = models.FloatField(null=True)
    type = models.ForeignKey("CritterType", on_delete=models.CASCADE, related_name='critters_of_this_type')
    management = models.CharField(max_length=500, null=True, blank=True)
    insect = models.BooleanField(default=True)
    plants = models.ManyToManyField(
        "Plant",
        through='PlantCritterPairing',
        related_name="critters_on_this_plant"
    )