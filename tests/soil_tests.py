import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from gardenapi.models import Soil
from django.contrib.auth.models import User

class SoilTests(APITestCase):

    fixtures = ['users', 'tokens', 'soils']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        
    def test_create_soil(self):

        url = "/soils"
        data = {
            "soil_type": "Test Soil"
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["soil_type"], "Test Soil")

    def test_get_soil(self):

        soil = Soil()
        soil.soil_type = "Test Soil"
        soil.save()

        # Initiate request and store response
        response = self.client.get(f"/soils/{soil.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the soil was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["soil_type"], "Test Soil")
        
    def test_list_soils(self):

        response = self.client.get('/soils')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for obj in json_response:
            self.assertIn("soil_type", obj)

    def test_delete_soil(self):
        """
        Ensure we can delete an existing soil.
        """
        soil = Soil()
        soil.soil_type = "Test Soil"
        soil.save()

        # DELETE the soil you just created
        response = self.client.delete(f"/soils/{soil.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the soil again to verify you get a 404 response
        response = self.client.get(f"/soils/{soil.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_change_soil(self):
        """
        Ensure we can change an existing soil.
        """
        soil = Soil()
        soil.soil_type = "Test Soil"
        soil.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "soil_type": "New Test Soil"
        }

        response = self.client.put(f"/soils/{soil.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # GET soil again to verify changes were made
        response = self.client.get(f"/soils/{soil.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
       
        self.assertEqual(json_response["soil_type"], "New Test Soil")