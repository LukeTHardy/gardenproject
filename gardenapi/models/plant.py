from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from PIL import Image
from django.core.files.images import ImageFile
    
def validate_square_image(value):
    if isinstance(value, ImageFile):
        img = Image.open(value)
        width, height = img.size
        if width != height:
            raise ValidationError("The image must be square.")
    else:
        raise ValidationError("Invalid image file.")

class Plant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plants_added_by_this_user')
    name = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='images/',
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']), validate_square_image]
    )
    icon = models.ImageField(upload_to='icons/',
        height_field=None,
        width_field=None,
        max_length=None,
        null=True)
    type = models.ForeignKey("PlantType", on_delete=models.CASCADE, related_name='plants_of_this_type')
    veggie_cat = models.ForeignKey("VeggieCat", on_delete=models.CASCADE, related_name='veggies_in_this_category')
    soil = models.ForeignKey("Soil", on_delete=models.CASCADE, related_name='plants_with_this_soil_type')
    water = models.ForeignKey("Water", on_delete=models.CASCADE, related_name='plants_needing_this_much_water')
    light = models.ForeignKey("Light", on_delete=models.CASCADE, related_name='plants_needing_this_much_light')
    annual = models.BooleanField(null=True)
    spacing = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    days_to_mature = models.IntegerField(null=True)
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