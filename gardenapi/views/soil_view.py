from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gardenapi.models import Soil

class SoilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soil
        fields = ['id', 'soil_type']


class SoilViewSet(ViewSet):

    def list(self, request):
        soils = Soil.objects.all()
        serializer = SoilSerializer(soils, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            soil = Soil.objects.get(pk=pk)
            serializer = SoilSerializer(soil)
            return Response(serializer.data)
        except Soil.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:
            soil_type = request.data.get('soil_type')
            soil = Soil.objects.create(soil_type=soil_type)
            serializer = SoilSerializer(soil, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            soil = Soil.objects.get(pk=pk)
            self.check_object_permissions(request, soil)
            soil.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Soil.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            soil = Soil.objects.get(pk=pk)
            serializer = SoilSerializer(data=request.data)
            if serializer.is_valid():
                soil.soil_type = serializer.validated_data['soil_type']
                soil.save()
                
                serializer = SoilSerializer(soil, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Soil.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)