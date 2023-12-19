# Generated by Django 5.0 on 2023-12-18 18:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gardenapi', '0008_critter_insect_alter_plant_annual'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='icon',
            field=models.ImageField(null=True, upload_to='images/icons', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'avif'])]),
        ),
    ]
