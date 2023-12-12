from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gardenapi.models import CritterType

class CritterTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CritterType
        fields = ['id', 'label']


class CritterTypeViewSet(ViewSet):

    def list(self, request):
        crittertypes = CritterType.objects.all()
        serializer = CritterTypeSerializer(crittertypes, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            crittertype = CritterType.objects.get(pk=pk)
            serializer = CritterTypeSerializer(crittertype)
            return Response(serializer.data)
        except CritterType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:
            label = request.data.get('label')
            crittertype = CritterType.objects.create(
                label=label
            )
            
            serializer = CritterTypeSerializer(crittertype, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            crittertype = CritterType.objects.get(pk=pk)
            self.check_object_permissions(request, crittertype)
            crittertype.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except CritterType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            crittertype = CritterType.objects.get(pk=pk)
            serializer = CritterTypeSerializer(data=request.data)
            if serializer.is_valid():
                crittertype.label = serializer.validated_data['label']
                crittertype.save()
                
                serializer = CritterTypeSerializer(crittertype, context={'request': request})
                return Response(None, status.HTTP_200_OK)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except CritterType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)