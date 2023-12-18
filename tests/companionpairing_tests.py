import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from gardenapi.models import CompanionPairing, Plant
from django.contrib.auth.models import User

class CompanionPairingTests(APITestCase):

    fixtures = ['users', 'tokens', 'plants', 'zones', 'soils', 'waters', 'lights', 'veggiecats', 'planttypes', 'critters', 'crittertypes', 'companionpairings']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_companionpairing(self):

        url = "/companionpairings"
        data = {
            "plant1": 1,
            "plant2": 2
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["plant1"]["id"], 1)
        self.assertEqual(json_response["plant2"]["id"], 2)

    def test_get_companionpairing(self):

        companionpairing = CompanionPairing()
        companionpairing.plant1 = Plant.objects.get(id=1)
        companionpairing.plant2 = Plant.objects.get(id=2)
        companionpairing.save()

        # Initiate request and store response
        response = self.client.get(f"/companionpairings/{companionpairing.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the companionpairing was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["plant1"]["id"], 1)
        self.assertEqual(json_response["plant2"]["id"], 2)
        
    def test_list_companionpairings(self):

        response = self.client.get('/companionpairings')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for obj in json_response:
            self.assertIn("plant1", obj)
            self.assertIn("plant2", obj)

    def test_delete_companionpairing(self):
        """
        Ensure we can delete an existing companionpairing.
        """
        companionpairing = CompanionPairing()
        companionpairing.plant1 = Plant.objects.get(id=1)
        companionpairing.plant2 = Plant.objects.get(id=2)
        companionpairing.save()

        # DELETE the companionpairing you just created
        response = self.client.delete(f"/companionpairings/{companionpairing.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the companionpairing again to verify you get a 404 response
        response = self.client.get(f"/companionpairings/{companionpairing.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    