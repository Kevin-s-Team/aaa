import unittest

import requests

import json

import main


class ApiEndpointTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = main.create_app()
        self.client = self.app.test_client()


class RecipeEndpointTest(ApiEndpointTest):
    JSON_RECIPE_REQUEST = {
        "ingredients": [
            "carottes",
            "pommes de terre",
            "poireaux",
            "oignons",
            "beurre",
            "lardons"
        ]
    }

    JSON_RECIPE_REQUEST_EMPTY = {
        "ingredients": []
    }

    def test_should_return_400_for_empty_ingredients_list(self):
        response = self.client.post('/api/recipe', json=self.JSON_RECIPE_REQUEST_EMPTY)
        self.assertEqual(response.status_code, 400)

    def test_should_return_200_for_correct_request(self):
        response = self.client.post('/api/recipe', json=self.JSON_RECIPE_REQUEST)
        self.assertEqual(response.status_code, 200)

    def test_should_return_dish_description(self):
        response = self.client.post('/api/recipe', json=self.JSON_RECIPE_REQUEST)
        self.assertIsInstance(response.json['dishDescription'], str)

    def test_should_return_instructions(self):
        response = self.client.post('/api/recipe', json=self.JSON_RECIPE_REQUEST)
        self.assertIsInstance(response.json['instructions'], str)


@unittest.skip("Image endpoint is expensive and thus we don't want to run its tests automatically."
               "To run the image endpoint tests, comment this decorator.")
class ImageEndpointTest(ApiEndpointTest):
    JSON_IMAGE_REQUEST = {
        "dishDescription": "lasagnes aux légumes"
    }

    JSON_IMAGE_REQUEST_EMPTY = {
        "dishDescription": ""
    }

    def test_should_return_400_for_empty_dish_description(self):
        response = self.client.post('/api/image', json=self.JSON_IMAGE_REQUEST_EMPTY)
        self.assertEqual(response.status_code, 400)

    def test_should_return_200_for_correct_request(self):
        response = self.client.post('/api/image', json=self.JSON_IMAGE_REQUEST)
        self.assertEqual(response.status_code, 200)

    def test_should_return_valid_image_url(self):
        response = self.client.post('/api/image', json=self.JSON_IMAGE_REQUEST)
        image_url = response.json['url']
        self.assertTrue(requests.head(image_url).headers['content-type'].startswith('image/'))


class IngredientsEndpointTest(ApiEndpointTest):
    def test_should_return_200(self):
        response = self.client.get('/api/ingredients')
        self.assertEqual(response.status_code, 200)
    
    def test_should_return_correct_json_file(self):
        with open('./data/ingredients_fr.json', 'r', encoding='utf-8') as file:
            ingredients = json.load(file)
        response = self.client.get('/api/ingredients')
        self.assertEqual(response.json, ingredients)