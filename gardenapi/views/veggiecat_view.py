from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gardenapi.models import VeggieCat

class VeggieCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = VeggieCat
        fields = ['id', 'label']


class VeggieCatViewSet(ViewSet):

    def list(self, request):
        veggiecats = VeggieCat.objects.all()
        serializer = VeggieCatSerializer(veggiecats, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            veggiecat = VeggieCat.objects.get(pk=pk)
            serializer = VeggieCatSerializer(veggiecat)
            return Response(serializer.data)
        except VeggieCat.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:    #get data from JSON payload
            label = request.data.get('label')
            veggiecat = VeggieCat.objects.create(
                label=label
            )
            
            serializer = VeggieCatSerializer(veggiecat, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            veggiecat = VeggieCat.objects.get(pk=pk)
            self.check_object_permissions(request, veggiecat)
            veggiecat.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except VeggieCat.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            veggiecat = VeggieCat.objects.get(pk=pk)
            serializer = VeggieCatSerializer(data=request.data)
            if serializer.is_valid():
                veggiecat.label = serializer.validated_data['label']
                veggiecat.save()
                
                serializer = VeggieCatSerializer(veggiecat, context={'request': request})
                return Response(None, status.HTTP_200_OK)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except VeggieCat.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)