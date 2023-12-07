from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gardenapi.models import Plant, PlantType, VeggieCat, Soil, Water, Light, PlantZonePairing, PlantCritterPairing, CompanionPairing
from django.contrib.auth.models import User

class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class PostRareUserSerializer(serializers.ModelSerializer):
    user = PostUserSerializer(many=False)  # Include the UserSerializer here

    class Meta:
        model = User
        fields = ['id', 'user']  # Include the 'user' field from UserSerializer


class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'label']


class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['label']


class PostSerializer(serializers.ModelSerializer):
    user = PostRareUserSerializer(many=False)
    category = PostCategorySerializer(many=False)
    reactions = ReactionSerializer(many=True)
    reactions_count = serializers.SerializerMethodField()

    def get_reactions_count(self, obj):
        # Count the occurrences of each reaction for the post
        reaction_counts = Counter(reaction['id']
                                  for reaction in obj.reactions.values())

        # Get the IDs of all reactions
        all_reaction_ids = Reaction.objects.values_list('id', flat=True)

        # Create a list of dictionaries for each reaction with or 0 if not present
        reactions_list = [{'id': reaction_id, 'count': reaction_counts[reaction_id]}
                          for reaction_id in all_reaction_ids]
        return reactions_list

    class Meta:
        model = Plant
        fields = ['id', 'user', 'name', 'description',
                  'image', 'icon', 'type', 'veggie_cat', 'soil', 'light', 'water', 'annual', 'spacing', 'height', 'days_to_mature', 'zones', 'critters', 'companions']

class PlantView(ViewSet):

    def retrieve(self, request, pk):
        try:
            plant = Plant.objects.get(pk=pk)
            serializer = PlantSerializer(plant, context={'request': request})
            return Response(serializer.data)
        except Plant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        # Get the query parameter 'user' from the request
        user_param = request.query_params.get('user')

        if user_param == 'current':
            # If user_param is 'current', filter plants by the current user ID
            try:
                user_id = request.user.id
                plants = Plant.objects.filter(user__user__id=user_id)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            # If no 'user' parameter or 'user' is not 'current', return all plants
            plants = Plant.objects.all()

        serializer = PlantSerializer(plants, many=True)
        return Response(serializer.data)

    def create(self, request):

        plant = Plant()
        plant.user = User.objects.get(pk=request.data["user"])
        plant.name = request.data.get('name')
        plant.description = request.data.get('description')
        plant.type = PlantType.objects.get(pk=request.data["type"])
        plant.veggie_cat = VeggieCat.objects.get(pk=request.data["veggie_cat"])
        plant.soil = Soil.objects.get(pk=request.data["soil"])
        plant.water = Water.objects.get(pk=request.data["water"])
        plant.light = Light.objects.get(pk=request.data["light"])
        plant.annual = request.data.get('annual')
        plant.spacing = request.data.get('spacing')
        plant.height = request.data.get('height')
        plant.days_to_mature = request.data.get('days_to_mature')
        plant.content = request.data.get('content')
        plant.image
        plant.icon

        plant.save()

        try:
            serializer = PlantSerializer(plant, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            plant = Plant.objects.get(pk=pk)
            plant.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Plant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)