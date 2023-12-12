import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from gardenapi.models import CritterType
from django.contrib.auth.models import User

class CritterTypeTests(APITestCase):

    fixtures = ['users', 'tokens', 'crittertypes']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        
    def test_create_crittertype(self):

        url = "/crittertypes"
        data = {
            "label": "Test CritterType"
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["label"], "Test CritterType")

    def test_get_crittertype(self):

        crittertype = CritterType()
        crittertype.label = "Test CritterType"
        crittertype.save()

        # Initiate request and store response
        response = self.client.get(f"/crittertypes/{crittertype.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the crittertype was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["label"], "Test CritterType")
        
    def test_list_crittertypes(self):

        response = self.client.get('/crittertypes')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for obj in json_response:
            self.assertIn("label", obj)

    def test_delete_crittertype(self):
        """
        Ensure we can delete an existing crittertype.
        """
        crittertype = CritterType()
        crittertype.label = "Test CritterType"
        crittertype.save()

        # DELETE the crittertype you just created
        response = self.client.delete(f"/crittertypes/{crittertype.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the crittertype again to verify you get a 404 response
        response = self.client.get(f"/crittertypes/{crittertype.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_change_crittertype(self):
        """
        Ensure we can change an existing crittertype.
        """
        crittertype = CritterType()
        crittertype.label = "Test CritterType"
        crittertype.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "label": "New Test CritterType"
        }

        response = self.client.put(f"/crittertypes/{crittertype.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # GET crittertype again to verify changes were made
        response = self.client.get(f"/crittertypes/{crittertype.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
       
        self.assertEqual(json_response["label"], "New Test CritterType")