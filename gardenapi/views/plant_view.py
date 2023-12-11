from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gardenapi.models import Plant, PlantType, VeggieCat, Soil, Water, Light, Critter, CompanionPairing, Zone
from django.contrib.auth.models import User
from gardenapi.views.planttype_view import PlantTypeSerializer
from gardenapi.views.veggiecat_view import VeggieCatSerializer
from gardenapi.views.soil_view import SoilSerializer
from gardenapi.views.water_view import WaterSerializer
from gardenapi.views.light_view import LightSerializer
import base64
from django.core.files.base import ContentFile

class PlantCompanionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ['id', 'name']


class PlantCritterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Critter
        fields = ['id', 'name']

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