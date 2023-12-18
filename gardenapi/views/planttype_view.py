from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gardenapi.models import PlantType

class PlantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantType
        fields = ['id', 'label']


class PlantTypeViewSet(ViewSet):

    def list(self, request):
        planttypes = PlantType.objects.all()
        serializer = PlantTypeSerializer(planttypes, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            planttype = PlantType.objects.get(pk=pk)
            serializer = PlantTypeSerializer(planttype)
            return Response(serializer.data)
        except PlantType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:
            label = request.data.get('label')
            planttype = PlantType.objects.create(
                label=label
            )
            
            serializer = PlantTypeSerializer(planttype, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            planttype = PlantType.objects.get(pk=pk)
            self.check_object_permissions(request, planttype)
            planttype.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except PlantType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            planttype = PlantType.objects.get(pk=pk)
            serializer = PlantTypeSerializer(data=request.data)
            if serializer.is_valid():
                planttype.label = serializer.validated_data['label']
                planttype.save()
                
                serializer = PlantTypeSerializer(planttype, context={'request': request})
                return Response(None, status.HTTP_200_OK)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except PlantType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)