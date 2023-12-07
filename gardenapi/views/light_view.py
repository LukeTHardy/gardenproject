from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gardenapi.models import Light

class LightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Light
        fields = ['id', 'label']


class LightViewSet(ViewSet):

    def list(self, request):
        lights = Light.objects.all()
        serializer = LightSerializer(lights, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            light = Light.objects.get(pk=pk)
            serializer = LightSerializer(light)
            return Response(serializer.data)
        except Light.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        #get data from JSON payload
        label = request.data.get('label')
        light = Light.objects.create(
            label=label
        )
        
        serializer = LightSerializer(light, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        try:
            light = Light.objects.get(pk=pk)
            self.check_object_permissions(request, light)
            light.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Light.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            light = Light.objects.get(pk=pk)
            serializer = LightSerializer(data=request.data)
            if serializer.is_valid():
                light.label = serializer.validated_data['label']
                light.save()
                
                serializer = LightSerializer(light, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Light.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)