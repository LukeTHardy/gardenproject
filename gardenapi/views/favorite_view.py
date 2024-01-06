from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gardenapi.models import Favorite, Plant, Zone
from gardenapi.views.planttype_view import PlantTypeSerializer
from gardenapi.views.veggiecat_view import VeggieCatSerializer
from django.contrib.auth.models import User

class PlantZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ['id', 'name']

class FavoritePlantSerializer(serializers.ModelSerializer):
    type = PlantTypeSerializer(many=False)
    veggie_cat = VeggieCatSerializer(many=False)
    zones = PlantZoneSerializer(many=True)
    class Meta:
        model = Plant
        fields = ['id', 'name', 'description', 'type', 'veggie_cat', 'annual', 'image', 'zones']

class FavoriteSerializer(serializers.ModelSerializer):
    plant = FavoritePlantSerializer(many=False)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'plant']

class FavoriteViewSet(ViewSet):
    
    def list(self, request):
        # Get the query parameter 'user' from the request
        user_param = request.query_params.get('user')

        if user_param == 'current':
            # If user_param is 'current', filter posts by the current user ID
            try:
                user_id = request.user.id
                favorites = Favorite.objects.filter(user__id=user_id)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            # If no 'user' parameter or 'user' is not 'current', return all posts
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