import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from gardenapi.models import PlantCritterPairing, Plant, Critter
from django.contrib.auth.models import User

class PlantCritterPairingTests(APITestCase):

    fixtures = ['users', 'tokens', 'plantcritterpairings', 'plants', 'zones', 'soils', 'waters', 'lights', 'veggiecats', 'planttypes', 'critters', 'crittertypes']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_plantcritterpairing(self):

        url = "/plantcritterpairings"
        data = {
            "plant": 1,
            "critter": 1
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["plant"], 1)
        self.assertEqual(json_response["critter"], 1)

    def test_get_plantcritterpairing(self):

        plantcritterpairing = PlantCritterPairing()
        plantcritterpairing.plant = Plant.objects.get(id=1)
        plantcritterpairing.critter = Critter.objects.get(id=1)
        plantcritterpairing.save()

        # Initiate request and store response
        response = self.client.get(f"/plantcritterpairings/{plantcritterpairing.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the plantcritterpairing was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["plant"], 1)
        self.assertEqual(json_response["critter"], 1)
        
    def test_list_plantcritterpairings(self):

        response = self.client.get('/plantcritterpairings')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for obj in json_response:
            self.assertIn("plant", obj)
            self.assertIn("critter", obj)

    def test_delete_plantcritterpairing(self):
        """
        Ensure we can delete an existing plantcritterpairing.
        """
        plantcritterpairing = PlantCritterPairing()
        plantcritterpairing.plant = Plant.objects.get(id=1)
        plantcritterpairing.critter = Critter.objects.get(id=1)
        plantcritterpairing.save()

        # DELETE the plantcritterpairing you just created
        response = self.client.delete(f"/plantcritterpairings/{plantcritterpairing.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the plantcritterpairing again to verify you get a 404 response
        response = self.client.get(f"/plantcritterpairings/{plantcritterpairing.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    