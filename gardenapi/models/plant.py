from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
    
class Plant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plants_added_by_this_user')
    name = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='images/plants',
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'avif'])]
    )
    icon = models.ImageField(
    upload_to='images/icons',
    height_field=None,
    width_field=None,
    max_length=None,
    null=True,
    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'avif'])])
    type = models.ForeignKey("PlantType", on_delete=models.CASCADE, related_name='plants_of_this_type')
    veggie_cat = models.ForeignKey("VeggieCat", on_delete=models.CASCADE, related_name='veggies_in_this_category', null=True)
    soil = models.ForeignKey("Soil", on_delete=models.CASCADE, related_name='plants_with_this_soil_type')
    water = models.ForeignKey("Water", on_delete=models.CASCADE, related_name='plants_needing_this_much_water')
    light = models.ForeignKey("Light", on_delete=models.CASCADE, related_name='plants_needing_this_much_light')
    annual = models.BooleanField(default=True)
    spacing = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    maturity = models.CharField(max_length=500, null=True, blank=True)
    zones = models.ManyToManyField(
        "Zone",
        through='PlantZonePairing',
        related_name="plants_for_this_zone"
    )
    critters = models.ManyToManyField(
        "Critter",
        through='PlantCritterPairing',
        related_name="plants_with_these_critters"
    )
    companions = models.ManyToManyField(
        "Plant",
        through='CompanionPairing',
        related_name="companion_plants"
    )