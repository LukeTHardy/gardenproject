import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from gardenapi.models import PlantZonePairing, Plant, Zone
from django.contrib.auth.models import User

class PlantZonePairingTests(APITestCase):

    fixtures = ['users', 'tokens', 'plantzonepairings', 'plants', 'zones', 'soils', 'waters', 'lights', 'veggiecats', 'planttypes']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_plantzonepairing(self):

        url = "/plantzonepairings"
        data = {
            "plant": 1,
            "zone": 1
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["plant"]["id"], 1)
        self.assertEqual(json_response["zone"]["id"], 1)

    def test_get_plantzonepairing(self):

        plantzonepairing = PlantZonePairing()
        plantzonepairing.plant = Plant.objects.get(id=1)
        plantzonepairing.zone = Zone.objects.get(id=1)
        plantzonepairing.save()

        # Initiate request and store response
        response = self.client.get(f"/plantzonepairings/{plantzonepairing.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the plantzonepairing was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["plant"]["id"], 1)
        self.assertEqual(json_response["zone"]["id"], 1)
        
    def test_list_plantzonepairings(self):

        response = self.client.get('/plantzonepairings')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for obj in json_response:
            self.assertIn("plant", obj)
            self.assertIn("zone", obj)

    def test_delete_plantzonepairing(self):
        """
        Ensure we can delete an existing plantzonepairing.
        """
        plantzonepairing = PlantZonePairing()
        plantzonepairing.plant = Plant.objects.get(id=1)
        plantzonepairing.zone = Zone.objects.get(id=1)
        plantzonepairing.save()

        # DELETE the plantzonepairing you just created
        response = self.client.delete(f"/plantzonepairings/{plantzonepairing.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the plantzonepairing again to verify you get a 404 response
        response = self.client.get(f"/plantzonepairings/{plantzonepairing.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    