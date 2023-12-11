from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gardenapi.models import PlantCritterPairing, Critter, Plant

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ['id', 'name']

class CritterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Critter
        fields = ['id', 'name']

class PlantCritterPairingSerializer(serializers.ModelSerializer):
    class Meta:
        plant = PlantSerializer(many=False)
        critter = CritterSerializer(many=False)

        model = PlantCritterPairing
        fields = ['id', 'plant', 'critter']

class PlantCritterPairingViewSet(ViewSet):
    def list(self, request):
        plantcritterpairings = PlantCritterPairing.objects.all()
        serializer = PlantCritterPairingSerializer(plantcritterpairings, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            plantcritterpairing = PlantCritterPairing.objects.get(pk=pk)
            serializer = PlantCritterPairingSerializer(plantcritterpairing)
            return Response(serializer.data)
        except PlantCritterPairing.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:    
            plant = Plant.objects.get(pk=request.data['plant'])
            critter = Critter.objects.get(pk=request.data['critter'])

            plantcritterpairing = PlantCritterPairing.objects.create(
                plant = plant,
                critter = critter 
            )
        
            serializer = PlantCritterPairingSerializer(plantcritterpairing, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Plant.DoesNotExist:
            return Response({'error': 'Plant not found'}, status=status.HTTP_404_NOT_FOUND)
        except Critter.DoesNotExist:
            return Response({'error': 'Critter not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def destroy(self, request, pk=None):
        try:
            plantcritterpairing = PlantCritterPairing.objects.get(pk=pk)
            self.check_object_permissions(request, plantcritterpairing)
            plantcritterpairing.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except PlantCritterPairing.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)