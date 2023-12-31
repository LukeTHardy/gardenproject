# Generated by Django 5.0 on 2023-12-06 17:14

import django.core.validators
import gardenapi.models.plant
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gardenapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='block_size',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='plant',
            name='icon_url',
            field=models.ImageField(null=True, upload_to='icons/'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='image_url',
            field=models.ImageField(null=True, upload_to='images/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]),
        ),
    ]
