# Generated by Django 5.0 on 2023-12-06 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gardenapi', '0003_rename_icon_url_plant_icon_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='light',
            name='hours',
        ),
        migrations.AddField(
            model_name='light',
            name='label',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
