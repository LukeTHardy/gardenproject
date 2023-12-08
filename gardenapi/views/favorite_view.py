from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gardenapi.models import Favorite, Plant
from django.contrib.auth.models import User


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'plant']

class FavoriteViewSet(ViewSet):
    def list(self, request):
        favorites = Favorite.objects.all()
        serializer = FavoriteSerializer(favorites, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            favorite = Favorite.objects.get(pk=pk)
            serializer = FavoriteSerializer(favorite)
            return Response(serializer.data)
        except Favorite.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:    
            user = User.objects.get(pk=request.user.id)
            plant = Plant.objects.get(pk=request.data['plant'])

            favorite = Favorite.objects.create(
                user = user,
                plant = plant 
            )
        
            serializer = FavoriteSerializer(favorite, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        try:
            favorite = Favorite.objects.get(pk=pk)
            self.check_object_permissions(request, favorite)
            favorite.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Favorite.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)