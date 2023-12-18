import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from gardenapi.models import Zone
from django.contrib.auth.models import User

class ZoneTests(APITestCase):

    fixtures = ['users', 'tokens', 'zones']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        
    def test_create_zone(self):

        url = "/zones"
        data = {
            "name": "Test Zone"
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["name"], "Test Zone")

    def test_get_zone(self):

        zone = Zone()
        zone.name = "Test Zone"
        zone.save()

        # Initiate request and store response
        response = self.client.get(f"/zones/{zone.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the zone was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["name"], "Test Zone")
        
    def test_list_zones(self):

        response = self.client.get('/zones')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for obj in json_response:
            self.assertIn("name", obj)

    def test_delete_zone(self):
        """
        Ensure we can delete an existing zone.
        """
        zone = Zone()
        zone.name = "Test Zone"
        zone.save()

        # DELETE the zone you just created
        response = self.client.delete(f"/zones/{zone.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the zone again to verify you get a 404 response
        response = self.client.get(f"/zones/{zone.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_change_zone(self):
        """
        Ensure we can change an existing zone.
        """
        zone = Zone()
        zone.name = "Test Zone"
        zone.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "name": "New Test Zone"
        }

        response = self.client.put(f"/zones/{zone.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # GET zone again to verify changes were made
        response = self.client.get(f"/zones/{zone.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
       
        self.assertEqual(json_response["name"], "New Test Zone")