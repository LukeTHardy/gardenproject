from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gardenapi.models import Plant, PlantType, VeggieCat, Soil, Water, Light
from django.contrib.auth.models import User
from gardenapi.views.planttype_view import PlantTypeSerializer
from gardenapi.views.veggiecat_view import VeggieCatSerializer
from gardenapi.views.soil_view import SoilSerializer
from gardenapi.views.water_view import WaterSerializer
from gardenapi.views.light_view import LightSerializer
from gardenapi.views.plantzonepairing_view import PlantZonePairingSerializer
from gardenapi.views.plantcritterpairing_view import PlantCritterPairingSerializer
from gardenapi.views.companionpairing_view import CompanionPairingSerializer
# import uuid
import base64
from django.core.files.base import ContentFile

        
class PlantSerializer(serializers.ModelSerializer):
    type = PlantTypeSerializer(many=False)
    veggie_cat = VeggieCatSerializer(many=False)
    soil = SoilSerializer(many=False)
    water = WaterSerializer(many=False)
    light = LightSerializer(many=False)
    zones = PlantZonePairingSerializer(many=True)
    critters = PlantCritterPairingSerializer(many=True)
    companions = CompanionPairingSerializer(many=True)

    class Meta:
        model = Plant
        fields = ['user', 'name', 'description', 'image', 'icon', 'type', 'veggie_cat', 'soil', 'water', 'light', 'annual', 'spacing', 'height', 'days_to_mature', 'zones', 'critters', 'companions']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request and instance.id:
            representation["zones"] = PlantZonePairingSerializer(
                instance.zones.filter(plant=instance),
                many=True,
                context={"request": request}
            ).data

            representation["critters"] = PlantCritterPairingSerializer(
                instance.critters.filter(plant=instance),
                many=True,
                context={"request": request}
            ).data

            representation["companions"] = CompanionPairingSerializer(
                instance.companions.filter(plant1=instance) | instance.companions.filter(plant2=instance),
                many=True,
                context={"request": request}
            ).data

        return representation

class PlantViewSet(ViewSet):

    def retrieve(self, request, pk):
        try:
            plant = Plant.objects.get(pk=pk)
            plant_serializer = PlantSerializer(plant, context={"request": request})
            return Response(plant_serializer.data)
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

            plant = Plant()
            plant.user = User.objects.get(pk=request.data["user"])
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
            plant.days_to_mature = request.data.get('days_to_mature')
            

            image_format, image_str = request.data["image"].split(';base64,')
            image_ext = image_format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(image_str), name=f'{request.data["name"]}.{image_ext}')

            icon_format, icon_str = request.data["icon"].split(';base64,')
            icon_ext = icon_format.split('/')[-1]
            icon_data = ContentFile(base64.b64decode(icon_str), name=f'{request.data["name"]}-icon.{icon_ext}')

            plant.image = image_data
            plant.icon = icon_data

            plant.save()
            serializer = PlantSerializer(plant, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    def update(self, request, pk=None):
        try:
            plant = Plant.objects.get(pk=pk)
            image_data = request.data.get('image', None)
            icon_data = request.data.get('icon', None)

            serializer = PlantSerializer(data=request.data)
            if serializer.is_valid():
                plant.user = User.objects.get(pk=serializer.validated_data["user"])
                plant.name = serializer.validated_data['name']
                plant.description = serializer.validated_data['description']
                plant.type = PlantType.objects.get(pk=serializer.validated_data["type"])
                plant.veggie_cat = VeggieCat.objects.get(pk=serializer.validated_data["veggie_cat"])
                plant.soil = Soil.objects.get(pk=serializer.validated_data["soil"])
                plant.water = Water.objects.get(pk=serializer.validated_data["water"])
                plant.light = Light.objects.get(pk=serializer.validated_data["light"])
                plant.annual = serializer.validated_data['annual']
                plant.spacing = serializer.validated_data['spacing']
                plant.height = serializer.validated_data['height']
                plant.days_to_mature = serializer.validated_data['days_to_mature']

                if image_data:
                    # Process and save image data
                    image_format, image_str = image_data.split(';base64,')
                    image_ext = image_format.split('/')[-1]
                    image_data = ContentFile(base64.b64decode(image_str), name=f'{serializer.validated_data["name"]}.{image_ext}')
                    plant.image = image_data

                if icon_data:
                    # Process and save icon data
                    icon_format, icon_str = icon_data.split(';base64,')
                    icon_ext = icon_format.split('/')[-1]
                    icon_data = ContentFile(base64.b64decode(icon_str), name=f'{serializer.validated_data["name"]}-icon.{icon_ext}')
                    plant.icon = icon_data

                plant.save()
                
                serializer = PlantSerializer(plant, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Plant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, pk=None):
        try:
            plant = Plant.objects.get(pk=pk)
            plant.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Plant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)