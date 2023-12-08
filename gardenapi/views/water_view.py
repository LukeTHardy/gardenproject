from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gardenapi.models import Water

class WaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Water
        fields = ['id', 'frequency']


class WaterViewSet(ViewSet):

    def list(self, request):
        waters = Water.objects.all()
        serializer = WaterSerializer(waters, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            water = Water.objects.get(pk=pk)
            serializer = WaterSerializer(water)
            return Response(serializer.data)
        except Water.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:
            frequency = request.data.get('frequency')
            water = Water.objects.create(frequency=frequency)
            serializer = WaterSerializer(water, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            water = Water.objects.get(pk=pk)
            self.check_object_permissions(request, water)
            water.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Water.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            water = Water.objects.get(pk=pk)
            serializer = WaterSerializer(data=request.data)
            if serializer.is_valid():
                water.frequency = serializer.validated_data['frequency']
                water.save()
                
                serializer = WaterSerializer(water, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Water.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)