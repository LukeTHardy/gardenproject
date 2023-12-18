import json
import os
import base64
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from gardenapi.models import Critter, CritterType
from django.contrib.auth.models import User


class CritterTests(APITestCase):

    fixtures = ['users', 'tokens', 'critters', 'crittertypes']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_critter(self):

        critter = Critter()
        critter.user = User.objects.get(id=1)
        critter.type = CritterType.objects.get(id=1)
        critter.name = "Test Critter"
        critter.description = "Test description"
        critter.image = "images/critters/test_critter.jpg"
        critter.size = 5
        critter.management = "Test management"
        critter.save()

        response = self.client.get(f"/critters/{critter.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the critter was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json_response["user"], 1)
        self.assertEqual(
            json_response["type"]["id"], 1)
        self.assertEqual(
            json_response["name"], "Test Critter")
        self.assertEqual(json_response["description"], "Test description")
        self.assertTrue("images/critters/test_critter.jpg" in json_response["image"])
        self.assertEqual(json_response["size"], 5)
        self.assertEqual(json_response["management"], "Test management")

    def test_get_all_critters(self):

        response = self.client.get('/critters')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for obj in json_response:
            self.assertIn("user", obj)
            self.assertIn("name", obj)
            self.assertIn("image", obj)
            self.assertIn("description", obj)
            self.assertIn("size", obj)
            self.assertIn("type", obj)
            self.assertIn("management", obj)

    def test_create_critter(self):
        url = "/critters"

        image_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')
        with open(image_path, 'rb') as image_file:
            image_content = base64.b64encode(image_file.read()).decode('utf-8')

        data = {
            "user": 1,
            "name": "Test Critter",
            "image": f'data:image/jpeg;base64,{image_content}',
            "description": "Test description",
            "size": 5,
            "type": 1,
            "management": "Test management",
        }

        response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        json_response = json.loads(response.content)
        
        # Assertions
        self.assertEqual(json_response["user"], 1)
        self.assertEqual(json_response["type"]["id"], 1)
        self.assertEqual(json_response["name"], "Test Critter")
        self.assertEqual(json_response["description"], "Test description")
        self.assertEqual(json_response["size"], 5)
        self.assertEqual(json_response["management"], "Test management")
        # Adjust this assertion based on the actual URL generated by your system
        critter = Critter.objects.get(id=json_response["id"])
        self.assertTrue(critter.image.name.startswith('images/critters/'))
        self.assertTrue(os.path.isfile(critter.image.path))
        
        Critter.objects.all().delete()

    def test_delete_critter(self):

        critter = Critter()
        critter.user = User.objects.get(id=1)
        critter.type = CritterType.objects.get(id=1)
        critter.name = "Test Critter"
        critter.description = "Test description"
        critter.image = "images/critters/test_critter.jpg"
        critter.size = 5
        critter.management = "Test management"
        critter.save()

        # DELETE the critter you just created
        response = self.client.delete(f"/critters/{critter.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the critter again to verify you get a 404 response
        response = self.client.get(f"/critters/{critter.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_change_critter(self):
    #     """
    #     Ensure we can change an existing critter.
    #     """
    #     critter = Critter()
    #     critter.user = User.objects.get(id=1)
    #     critter.type = CritterType.objects.get(id=1)
    #     critter.name = "Test Critter"
    #     critter.description = "Test description"
    #     critter.image = "images/critters/test_critter.jpg"
    #     critter.size = 5
    #     critter.management = "Test management"
    #     critter.save()

    #     # DEFINE NEW PROPERTIES FOR Critter
    #     image2_path = os.path.join(os.path.dirname(__file__), 'test_image2.jpeg')
    #     with open(image2_path, 'rb') as image_file:
    #         image2_content = base64.b64encode(image_file.read()).decode('utf-8')

    #     data = {
    #         "user": 1,
    #         "name": "Test Critter 2",
    #         "image": f'data:image/jpeg;base64,{image2_content}',
    #         "description": "Test description 2",
    #         "size": 4,
    #         "type": 2,
    #         "management": "Test management 2",
    #     }

    #     response = self.client.put(f"/critters/{critter.id}", data, format='multipart')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # GET critter again to verify changes were made
    #     response = self.client.get(f"/critters/{critter.id}")
    #     json_response = json.loads(response.content)
    #     print(response.content)

    #     # Assert that the properties are correct
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # self.assertEqual(json_response["user"], 1)
    #     self.assertEqual(json_response["name"], "Test Critter 2")
    #     self.assertEqual(json_response["image"], "images/critters/test_critter2.jpg")
    #     self.assertEqual(json_response["description"], "Test description 2")
    #     self.assertEqual(json_response["size"], 4)
    #     self.assertEqual(json_response["type"]["id"], 2)
    #     self.assertEqual(json_response["management"], "Test management 2")
    #     critter = Critter.objects.get(id=json_response["id"])
    #     self.assertTrue(critter.image.name.startswith('images/critters/'))
    #     self.assertTrue(os.path.isfile(critter.image.path))

    #     Critter.objects.all().delete()