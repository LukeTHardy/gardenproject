from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gardenapi.models import Plant, PlantType, VeggieCat, Soil, Water, Light, Critter, CompanionPairing, Zone, PlantZonePairing, PlantCritterPairing
from django.contrib.auth.models import User
from gardenapi.views.planttype_view import PlantTypeSerializer
from gardenapi.views.veggiecat_view import VeggieCatSerializer
from gardenapi.views.crittertype_view import CritterTypeSerializer
from gardenapi.views.soil_view import SoilSerializer
from gardenapi.views.water_view import WaterSerializer
from gardenapi.views.light_view import LightSerializer
import base64
from django.core.files.base import ContentFile

class PlantCompanionSerializer(serializers.ModelSerializer):
    type = PlantTypeSerializer(many=False)
    class Meta:
        model = Plant
        fields = ['id', 'name', 'image', 'type', 'annual']


class PlantCritterSerializer(serializers.ModelSerializer):
    type = CritterTypeSerializer(many=False)
    class Meta:
        model = Critter
        fields = ['id', 'name', 'size', 'type', 'image']

class PlantZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ['id', 'name']
        
class PlantSerializer(serializers.ModelSerializer):
    type = PlantTypeSerializer(many=False)
    veggie_cat = VeggieCatSerializer(many=False)
    soil = SoilSerializer(many=False)
    water = WaterSerializer(many=False)
    light = LightSerializer(many=False)
    zones = PlantZoneSerializer(many=True)
    critters = PlantCritterSerializer(many=True)
    companions = serializers.SerializerMethodField()

    class Meta:
        model = Plant
        fields = '__all__'

    def get_companions(self, obj):
        # Retrieve distinct companions using the CompanionPairing model
        companion_pairings = CompanionPairing.objects.filter(plant1=obj) | CompanionPairing.objects.filter(plant2=obj)
        
        # Use a set to store unique companion plant IDs
        companion_ids_set = set()

        for pairing in companion_pairings:
            if pairing.plant1 != obj:
                companion_ids_set.add(pairing.plant1.id)
            else:
                companion_ids_set.add(pairing.plant2.id)

        # Convert the set to a list and exclude the current plant
        companions_ids = list(companion_ids_set - {obj.id})

        # Fetch companion plants
        companions = Plant.objects.filter(id__in=companions_ids)

        # Serialize the companions
        companion_serializer = PlantCompanionSerializer(companions, many=True)
        return companion_serializer.data


class PlantViewSet(ViewSet):

    def retrieve(self, request, pk):
        try:
            plant = Plant.objects.get(pk=pk)
            serializer = PlantSerializer(plant, context={"request": request})
            return Response(serializer.data)
        except Plant.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        plants = Plant.objects.all()
        serializer = PlantSerializer(plants, many=True, context={"request": request})
        return Response(serializer.data)

    def create(self, request):
        try:
            image_data = request.data.get('image', None)
            icon_data = request.data.get('icon', None)

            image_format, image_str = request.data["image"].split(';base64,')
            image_ext = image_format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(image_str), name=f'{request.data["name"]}.{image_ext}')

            icon_format, icon_str = request.data["icon"].split(';base64,')
            icon_ext = icon_format.split('/')[-1]
            icon_data = ContentFile(base64.b64decode(icon_str), name=f'{request.data["name"]}-icon.{icon_ext}')

            zone_ids = request.data.get('zones', [])
            zones = Zone.objects.filter(pk__in=zone_ids)

            companion_ids = request.data.get('companions', [])
            companions = Plant.objects.filter(pk__in=companion_ids)

            critter_ids = request.data.get('critters', [])
            critters = Critter.objects.filter(pk__in=critter_ids)

            plant = Plant()
            plant.user = User.objects.get(pk=request.user.id)
            plant.name = request.data.get('name')
            plant.description = request.data.get('description')
            plant.type = PlantType.objects.get(pk=request.data["type"])
            plant.veggie_cat = VeggieCat.objects.get(pk=request.data["veggie_cat"])
            plant.soil = Soil.objects.get(pk=request.data["soil"])
            plant.water = Water.objects.get(pk=request.data["water"])
            plant.light = Light.objects.get(pk=request.data["light"])
            plant.annual = request.data.get('annual')
            plant.spacing = request.data.get('spacing')
            plant.height = request.data.get('height')
            plant.maturity = request.data.get('maturity')
            plant.image = image_data
            plant.icon = icon_data

            plant.save()

            for zoneId in zones:
                try:
                    PlantZonePairing.objects.create(plant=plant, zone=zoneId)
                except Exception as zone_exception:
                    print(f"Failed to create PlantZonePairing: {zone_exception}")

            for companionId in companions:
                try:
                    CompanionPairing.objects.create(plant1=plant, plant2=companionId)
                except Exception as companion_exception:
                    print(f"Failed to create CompanionPairing: {companion_exception}")

            for critterId in critters:
                try:
                    PlantCritterPairing.objects.create(plant=plant, critter=critterId)
                except Exception as critter_exception:
                    print(f"Failed to create PlantCritterPairing: {critter_exception}")

            serializer = PlantSerializer(plant, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            plant = Plant.objects.get(pk=pk)
            
            # Check if new image data is provided (including empty string)
            new_image_data = request.data.get('image', None)
            if new_image_data is not None and ';' in new_image_data:  # Check for explicit empty string
                # Update the image
                image_format, image_str = new_image_data.split(';base64,')
                image_ext = image_format.split('/')[-1]
                image_data = ContentFile(base64.b64decode(image_str), name=f'{request.data["name"]}.{image_ext}')
                plant.image = image_data

            # Check if new icon data is provided (including empty string)
            new_icon_data = request.data.get('icon', None)
            if new_icon_data is not None and ';' in new_icon_data:  # Check for explicit empty string
                # Update the icon
                icon_format, icon_str = new_icon_data.split(';base64,')
                icon_ext = icon_format.split('/')[-1]
                icon_data = ContentFile(base64.b64decode(icon_str), name=f'{request.data["name"]}-icon.{icon_ext}')
                plant.icon = icon_data

            # Update plant fields
            plant.user = User.objects.get(pk=request.user.id)
            plant.name = request.data.get('name', plant.name)
            plant.description = request.data.get('description', plant.description)
            plant.type = PlantType.objects.get(pk=request.data.get("type", plant.type.pk))
            plant.veggie_cat = VeggieCat.objects.get(pk=request.data.get("veggie_cat", plant.veggie_cat.pk))
            plant.soil = Soil.objects.get(pk=request.data.get("soil", plant.soil.pk))
            plant.water = Water.objects.get(pk=request.data.get("water", plant.water.pk))
            plant.light = Light.objects.get(pk=request.data.get("light", plant.light.pk))
            plant.annual = request.data.get('annual', plant.annual)
            plant.spacing = request.data.get('spacing', plant.spacing)
            plant.height = request.data.get('height', plant.height)
            plant.maturity = request.data.get('maturity', plant.maturity)
          

            plant.save()

            # Clear existing related objects
            plant.zones.clear()
            plant.companions.clear()
            plant.critters.clear()

            # Add new related objects
            zone_ids = request.data.get('zones', [])
            companion_ids = request.data.get('companions', [])
            critter_ids = request.data.get('critters', [])
            zones = Zone.objects.filter(pk__in=zone_ids)
            companions = Plant.objects.filter(pk__in=companion_ids)
            critters = Critter.objects.filter(pk__in=critter_ids)
            
            for zoneId in zones:
                try:
                    PlantZonePairing.objects.create(plant=plant, zone=zoneId)
                except Exception as zone_exception:
                    print(f"Failed to create PlantZonePairing: {zone_exception}")

            for companionId in companions:
                try:
                    CompanionPairing.objects.create(plant1=plant, plant2=companionId)
                except Exception as companion_exception:
                    print(f"Failed to create CompanionPairing: {companion_exception}")

            for critterId in critters:
                try:
                    PlantCritterPairing.objects.create(plant=plant, critter=critterId)
                except Exception as critter_exception:
                    print(f"Failed to create PlantCritterPairing: {critter_exception}")

            serializer = PlantSerializer(plant, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Plant.DoesNotExist:
            return Response({'error': 'Plant not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, pk=None):
        try:
            plant = Plant.objects.get(pk=pk)
            plant.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Plant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)