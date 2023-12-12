from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gardenapi.models import Zone

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'

class ZoneViewSet(ViewSet):

    def list(self, request):
        zones = Zone.objects.all()
        serializer = ZoneSerializer(zones, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            zone = Zone.objects.get(pk=pk)
            serializer = ZoneSerializer(zone)
            return Response(serializer.data)
        except Zone.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:    
            name = request.data.get('name')
            zone = Zone.objects.create(
                name = name
            )
        
            serializer = ZoneSerializer(zone, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            zone = Zone.objects.get(pk=pk)
            self.check_object_permissions(request, zone)
            zone.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Zone.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            zone = Zone.objects.get(pk=pk)
            serializer = ZoneSerializer(data=request.data)
            if serializer.is_valid():
                zone.name = serializer.validated_data['name']
                zone.save()
                
                serializer = ZoneSerializer(zone, context={'request': request})
                return Response(None, status.HTTP_200_OK)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Zone.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)