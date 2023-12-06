from django.db import models
from django.contrib.auth.models import User

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='this_users_favorites')
    plant = models.ForeignKey("Plant", on_delete=models.CASCADE, related_name='favorites_with_this_plant')