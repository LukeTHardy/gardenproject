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
from django.core.files.base import ContentFile
from base64 import b64decode
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import io

        
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

class PlantView(ViewSet):

    def retrieve(self, request, pk):
        try:
            plant = Plant.objects.get(pk=pk)
            serializer = PlantSerializer(plant)
            return Response(serializer.data)
        except Plant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        plants = Plant.objects.all()
        serializer = PlantSerializer(plants, many=True)
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
            if image_data:
                # Process and save image data
                plant.image.save("image.jpg", ContentFile(b64decode(image_data)), save=True)

            if icon_data:
                # Process and save icon data
                plant.icon.save("icon.jpg", ContentFile(b64decode(icon_data)), save=True)
            plant.save()
            serializer = PlantSerializer(plant, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def handle_uploaded_image(self, image_data):
        # Decode base64 and create an InMemoryUploadedFile
        image_data = b64decode(image_data)
        image = Image.open(io.BytesIO(image_data))

        # Convert image to JPEG format (you can adjust the format based on your needs)
        with io.BytesIO() as output:
            image.save(output, format='JPEG')
            image_data = output.getvalue()

        return InMemoryUploadedFile(
            io.BytesIO(image_data),
            'ImageField',
            'image.jpg',
            'image/jpeg',
            len(image_data),
            None
        )
        
    def update(self, request, pk=None):
        try:
            plant = Plant.objects.get(pk=pk)
            serializer = PlantSerializer(data=request.data)
            if serializer.is_valid():
                plant.label = serializer.validated_data['label']
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
                plant.image
                plant.icon
                plant.save()
                
                serializer = PlantTypeSerializer(plant, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except PlantType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            plant = Plant.objects.get(pk=pk)
            plant.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Plant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)