import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from gardenapi.models import Light
from django.contrib.auth.models import User

class LightTests(APITestCase):

    fixtures = ['users', 'tokens', 'lights']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        
    def test_create_light(self):

        url = "/lights"
        data = {
            "label": "Test Light"
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["label"], "Test Light")

    def test_get_light(self):

        light = Light()
        light.label = "Test Light"
        light.save()

        # Initiate request and store response
        response = self.client.get(f"/lights/{light.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the light was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["label"], "Test Light")
        
    def test_list_lights(self):

        response = self.client.get('/lights')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for obj in json_response:
            self.assertIn("label", obj)

    def test_delete_light(self):
        """
        Ensure we can delete an existing light.
        """
        light = Light()
        light.label = "Test Light"
        light.save()

        # DELETE the light you just created
        response = self.client.delete(f"/lights/{light.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the light again to verify you get a 404 response
        response = self.client.get(f"/lights/{light.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_change_light(self):
        """
        Ensure we can change an existing light.
        """
        light = Light()
        light.label = "Test Light"
        light.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "label": "New Test Light"
        }

        response = self.client.put(f"/lights/{light.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # GET light again to verify changes were made
        response = self.client.get(f"/lights/{light.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
       
        self.assertEqual(json_response["label"], "New Test Light")