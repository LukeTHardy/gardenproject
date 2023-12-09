from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gardenapi.models import CompanionPairing, Plant

class CompanionPairingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanionPairing
        fields = ['id', 'plant1', 'plant2']

class CompanionPairingViewSet(ViewSet):
    def list(self, request):
        companionpairings = CompanionPairing.objects.all()
        serializer = CompanionPairingSerializer(companionpairings, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            companionpairing = CompanionPairing.objects.get(pk=pk)
            serializer = CompanionPairingSerializer(companionpairing)
            return Response(serializer.data)
        except CompanionPairing.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:    
            plant1 = Plant.objects.get(pk=request.data['plant1'])
            plant2 = Plant.objects.get(pk=request.data['plant2'])

            companionpairing = CompanionPairing.objects.create(
                plant1 = plant1,
                plant2 = plant2 
            )
        
            serializer = CompanionPairingSerializer(companionpairing, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Plant.DoesNotExist:
            return Response({'error': 'Plant not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def destroy(self, request, pk=None):
        try:
            companionpairing = CompanionPairing.objects.get(pk=pk)
            self.check_object_permissions(request, companionpairing)
            companionpairing.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except CompanionPairing.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)