import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from gardenapi.models import Favorite, Plant
from django.contrib.auth.models import User

class FavoriteTests(APITestCase):

    fixtures = ['users', 'tokens', 'plantcritterpairings', 'favorites', 'plants', 'zones', 'soils', 'waters', 'lights', 'veggiecats', 'planttypes', 'critters', 'crittertypes']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_favorite(self):

        url = "/favorites"
        data = {
            "user": 1,
            "plant": 1
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["user"], 1)
        self.assertEqual(json_response["plant"]["id"], 1)

    def test_get_favorite(self):

        favorite = Favorite()
        favorite.user = User.objects.get(id=1)
        favorite.plant = Plant.objects.get(id=1)
        favorite.save()

        # Initiate request and store response
        response = self.client.get(f"/favorites/{favorite.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the favorite was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["user"], 1)
        self.assertEqual(json_response["plant"]["id"], 1)
        
    def test_list_favorites(self):

        response = self.client.get('/favorites')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for obj in json_response:
            self.assertIn("user", obj)
            self.assertIn("plant", obj)

    def test_delete_favorite(self):
        """
        Ensure we can delete an existing favorite.
        """
        favorite = Favorite()
        favorite.user = User.objects.get(id=1)
        favorite.plant = Plant.objects.get(id=1)
        favorite.save()

        # DELETE the favorite you just created
        response = self.client.delete(f"/favorites/{favorite.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the favorite again to verify you get a 404 response
        response = self.client.get(f"/favorites/{favorite.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    