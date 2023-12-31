# Generated by Django 5.0 on 2023-12-05 21:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanionPairing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CritterType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Light',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlantType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Soil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VeggieCat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Water',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Critter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('image_url', models.CharField(blank=True, max_length=500, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('size', models.FloatField(null=True)),
                ('management', models.CharField(blank=True, max_length=500, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='critters_added_by_this_user', to=settings.AUTH_USER_MODEL)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='critters_of_this_type', to='gardenapi.crittertype')),
            ],
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('image_url', models.CharField(blank=True, max_length=500, null=True)),
                ('icon_url', models.CharField(blank=True, max_length=500, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('annual', models.BooleanField(null=True)),
                ('spacing', models.IntegerField(null=True)),
                ('height', models.IntegerField(null=True)),
                ('days_to_mature', models.IntegerField(null=True)),
                ('companions', models.ManyToManyField(related_name='companion_plants', through='gardenapi.CompanionPairing', to='gardenapi.plant')),
                ('light', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plants_needing_this_much_light', to='gardenapi.light')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plants_added_by_this_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='this_users_favorites', to=settings.AUTH_USER_MODEL)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites_with_this_plant', to='gardenapi.plant')),
            ],
        ),
        migrations.AddField(
            model_name='companionpairing',
            name='plant1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companion_plants_1', to='gardenapi.plant'),
        ),
        migrations.AddField(
            model_name='companionpairing',
            name='plant2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companion_plants_2', to='gardenapi.plant'),
        ),
        migrations.CreateModel(
            name='PlantCritterPairing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('critter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plants_where_you_find_this_critter', to='gardenapi.critter')),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='critters_you_find_on_this_plant', to='gardenapi.plant')),
            ],
        ),
        migrations.AddField(
            model_name='plant',
            name='critters',
            field=models.ManyToManyField(related_name='plants_with_these_critters', through='gardenapi.PlantCritterPairing', to='gardenapi.critter'),
        ),
        migrations.AddField(
            model_name='critter',
            name='plants',
            field=models.ManyToManyField(related_name='critters_on_this_plant', through='gardenapi.PlantCritterPairing', to='gardenapi.plant'),
        ),
        migrations.AddField(
            model_name='plant',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plants_of_this_type', to='gardenapi.planttype'),
        ),
        migrations.CreateModel(
            name='PlantZonePairing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zones_this_plant_grows_in', to='gardenapi.plant')),
            ],
        ),
        migrations.AddField(
            model_name='plant',
            name='soil',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plants_with_this_soil_type', to='gardenapi.soil'),
        ),
        migrations.AddField(
            model_name='plant',
            name='veggie_cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='veggies_in_this_category', to='gardenapi.veggiecat'),
        ),
        migrations.AddField(
            model_name='plant',
            name='water',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plants_needing_this_much_water', to='gardenapi.water'),
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('plants', models.ManyToManyField(related_name='zones_for_this_plant', through='gardenapi.PlantZonePairing', to='gardenapi.plant')),
            ],
        ),
        migrations.AddField(
            model_name='plantzonepairing',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plants_that_grow_in_this_zone', to='gardenapi.zone'),
        ),
        migrations.AddField(
            model_name='plant',
            name='zones',
            field=models.ManyToManyField(related_name='plants_for_this_zone', through='gardenapi.PlantZonePairing', to='gardenapi.zone'),
        ),
    ]
