import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from gardenapi.models import PlantType
from django.contrib.auth.models import User

class PlantTypeTests(APITestCase):

    fixtures = ['users', 'tokens', 'planttypes']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        
    def test_create_planttype(self):

        url = "/planttypes"
        data = {
            "label": "Test PlantType"
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["label"], "Test PlantType")

    def test_get_planttype(self):

        planttype = PlantType()
        planttype.label = "Test PlantType"
        planttype.save()

        # Initiate request and store response
        response = self.client.get(f"/planttypes/{planttype.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the planttype was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["label"], "Test PlantType")
        
    def test_list_planttypes(self):

        response = self.client.get('/planttypes')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for obj in json_response:
            self.assertIn("label", obj)

    def test_delete_planttype(self):
        """
        Ensure we can delete an existing planttype.
        """
        planttype = PlantType()
        planttype.label = "Test PlantType"
        planttype.save()

        # DELETE the planttype you just created
        response = self.client.delete(f"/planttypes/{planttype.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the planttype again to verify you get a 404 response
        response = self.client.get(f"/planttypes/{planttype.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_change_planttype(self):
        """
        Ensure we can change an existing planttype.
        """
        planttype = PlantType()
        planttype.label = "Test PlantType"
        planttype.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "label": "New Test PlantType"
        }

        response = self.client.put(f"/planttypes/{planttype.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # GET planttype again to verify changes were made
        response = self.client.get(f"/planttypes/{planttype.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
       
        self.assertEqual(json_response["label"], "New Test PlantType")