import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from gardenapi.models import VeggieCat
from django.contrib.auth.models import User

class VeggieCatTests(APITestCase):

    fixtures = ['users', 'tokens', 'veggiecats']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        
    def test_create_veggiecat(self):

        url = "/veggiecats"
        data = {
            "label": "Test VeggieCat"
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["label"], "Test VeggieCat")

    def test_get_veggiecat(self):

        veggiecat = VeggieCat()
        veggiecat.label = "Test VeggieCat"
        veggiecat.save()

        # Initiate request and store response
        response = self.client.get(f"/veggiecats/{veggiecat.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the veggiecat was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["label"], "Test VeggieCat")
        
    def test_list_veggiecats(self):

        response = self.client.get('/veggiecats')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for obj in json_response:
            self.assertIn("label", obj)

    def test_delete_veggiecat(self):
        """
        Ensure we can delete an existing veggiecat.
        """
        veggiecat = VeggieCat()
        veggiecat.label = "Test VeggieCat"
        veggiecat.save()

        # DELETE the veggiecat you just created
        response = self.client.delete(f"/veggiecats/{veggiecat.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the veggiecat again to verify you get a 404 response
        response = self.client.get(f"/veggiecats/{veggiecat.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_change_veggiecat(self):
        """
        Ensure we can change an existing veggiecat.
        """
        veggiecat = VeggieCat()
        veggiecat.label = "Test VeggieCat"
        veggiecat.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "label": "New Test VeggieCat"
        }

        response = self.client.put(f"/veggiecats/{veggiecat.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # GET veggiecat again to verify changes were made
        response = self.client.get(f"/veggiecats/{veggiecat.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
       
        self.assertEqual(json_response["label"], "New Test VeggieCat")