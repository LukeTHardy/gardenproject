import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from gardenapi.models import Water
from django.contrib.auth.models import User

class WaterTests(APITestCase):

    fixtures = ['users', 'tokens', 'waters']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        
    def test_create_water(self):

        url = "/waters"
        data = {
            "frequency": "Test Water"
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["frequency"], "Test Water")

    def test_get_water(self):

        water = Water()
        water.frequency = "Test Water"
        water.save()

        # Initiate request and store response
        response = self.client.get(f"/waters/{water.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the water was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["frequency"], "Test Water")
        
    def test_list_waters(self):

        response = self.client.get('/waters')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for obj in json_response:
            self.assertIn("frequency", obj)

    def test_delete_water(self):
        """
        Ensure we can delete an existing water.
        """
        water = Water()
        water.frequency = "Test Water"
        water.save()

        # DELETE the water you just created
        response = self.client.delete(f"/waters/{water.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the water again to verify you get a 404 response
        response = self.client.get(f"/waters/{water.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_change_water(self):
        """
        Ensure we can change an existing water.
        """
        water = Water()
        water.frequency = "Test Water"
        water.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "frequency": "New Test Water"
        }

        response = self.client.put(f"/waters/{water.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # GET water again to verify changes were made
        response = self.client.get(f"/waters/{water.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
       
        self.assertEqual(json_response["frequency"], "New Test Water")