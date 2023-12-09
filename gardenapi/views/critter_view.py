from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from gardenapi.models import Critter, CritterType
from gardenapi.views.crittertype_view import CritterTypeSerializer
from gardenapi.views.plantcritterpairing_view import PlantCritterPairingSerializer
# import uuid
import base64
from django.core.files.base import ContentFile

class CritterSerializer(serializers.ModelSerializer):
    type = CritterTypeSerializer(many=False)
    plants = PlantCritterPairingSerializer(many=True)

    class Meta:
        model = Critter
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request")
        
        if request and instance.id:

            representation["plants"] = PlantCritterPairingSerializer(
                instance.plants.filter(critter=instance),
                many=True,
                context={"request": request}
            ).data

        return representation
    
class CritterViewSet(ViewSet):

    def retrieve(self, request, pk):
        try:
            critter = Critter.objects.get(pk=pk)
            critter_serializer = CritterSerializer(critter, context={"request": request})
            return Response(critter_serializer.data)
        except Critter.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        critters = Critter.objects.all()
        serializer = CritterSerializer(critters, many=True, context={"request": request})
        return Response(serializer.data)

    def create(self, request):

        try:
            image_data = request.data.get('image', None)
            icon_data = request.data.get('icon', None)

            critter = Critter()
            critter.user = User.objects.get(pk=request.data["user"])
            critter.name = request.data.get('name')
            critter.description = request.data.get('description')
            critter.type = CritterType.objects.get(pk=request.data["type"])
            critter.size = request.data.get('size')
            critter.management = request.data.get('management')

            image_format, image_str = request.data["image"].split(';base64,')
            image_ext = image_format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(image_str), name=f'{request.data["name"]}.{image_ext}')

            critter.image = image_data

            critter.save()
            serializer = CritterSerializer(critter, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    def update(self, request, pk=None):
        try:
            critter = Critter.objects.get(pk=pk)
            image_data = request.data.get('image', None)
            icon_data = request.data.get('icon', None)

            serializer = CritterSerializer(data=request.data)
            if serializer.is_valid():
                critter.user = User.objects.get(pk=serializer.validated_data["user"].id)
                critter.name = serializer.validated_data['name']
                critter.description = serializer.validated_data['description']
                critter.type = CritterType.objects.get(pk=serializer.validated_data["type"])
                critter.size = serializer.validated_data['size']
                critter.management = serializer.validated_data['management']

                if image_data:
                    # Process and save image data
                    image_format, image_str = image_data.split(';base64,')
                    image_ext = image_format.split('/')[-1]
                    image_data = ContentFile(base64.b64decode(image_str), name=f'{serializer.validated_data["name"]}.{image_ext}')
                    critter.image = image_data


                critter.save()
                
                serializer = CritterSerializer(critter, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Critter.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, pk=None):
        try:
            critter = Critter.objects.get(pk=pk)
            critter.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Critter.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)