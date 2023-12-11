from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gardenapi.models import PlantZonePairing, Plant, Zone

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ['id', 'name']

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ['id', 'name']

class PlantZonePairingSerializer(serializers.ModelSerializer):
    plant = PlantSerializer(many=False)
    zone = ZoneSerializer(many=False)
    
    class Meta:
        model = PlantZonePairing
        fields = ['id', 'plant', 'zone']

class PlantZonePairingViewSet(ViewSet):
    def list(self, request):
        plantzonepairings = PlantZonePairing.objects.all()
        serializer = PlantZonePairingSerializer(plantzonepairings, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            plantzonepairing = PlantZonePairing.objects.get(pk=pk)
            serializer = PlantZonePairingSerializer(plantzonepairing)
            return Response(serializer.data)
        except PlantZonePairing.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:    
            plant = Plant.objects.get(pk=request.data['plant'])
            zone = Zone.objects.get(pk=request.data['zone'])

            plantzonepairing = PlantZonePairing.objects.create(
                plant = plant,
                zone = zone 
            )
        
            serializer = PlantZonePairingSerializer(plantzonepairing, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Plant.DoesNotExist:
            return Response({'error': 'Plant not found'}, status=status.HTTP_404_NOT_FOUND)
        except Zone.DoesNotExist:
            return Response({'error': 'Zone not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def destroy(self, request, pk=None):
        try:
            plantzonepairing = PlantZonePairing.objects.get(pk=pk)
            self.check_object_permissions(request, plantzonepairing)
            plantzonepairing.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except PlantZonePairing.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)