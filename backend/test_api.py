import unittest

import requests

import json

import main


class ApiEndpointTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = main.create_app()
        self.client = self.app.test_client()


@unittest.skip("Not implemented")
class RecipeEndpointTest(ApiEndpointTest):

    def test_empty_ingredients_list(self):
        json_request = {
            "ingredients": []
        }
        response = self.client.post('/api/recipe', json=json_request)
        self.assertEqual(response.status_code, 400, 'Should return 400')
        self.assertEqual(
            response.json,
            {"error": "no ingredients"},
            'Should return no ingredients error'
        )

    def test_too_many_ingredients(self):
        json_request = [
            {f"name": f"ingredient{i}"} for i in range(101)
        ]
        response = self.client.post('/api/recipe', json=json_request)
        self.assertEqual(response.status_code, 400, 'Should return 400')
        self.assertEqual(
            response.json,
            {"error": "too many ingredients"},
            'Should return too many ingredients error'
        )

    def test_ingredient_in_list_wrong_unit(self):
        json_request = {
            "ingredients": [{"name": "carottes", "quantity": {"unit": "kg", "value": 4}}]
        }
        response = self.client.post('/api/recipe', json=json_request)
        self.assertEqual(response.status_code, 400, 'Should return 400')
        self.assertEqual(
            response.json,
            {
                "error": "wrong ingredient",
                "ingredient": {"name": "carottes", "quantity": {"unit": "kg", "value": 4}}
            },
            'Should return wrong ingredient error with ingredient'
        )

    def test_too_long_custom_ingredient(self):
        json_request = {
            "ingredients": [
                {"name": "carottes", "quantity": {"unit": "kg", "value": 4}},
                {"name": "a" * 51, "quantity": {"unit": "kg", "value": 4}}
            ]
        }
        response = self.client.post('/api/recipe', json=json_request)
        self.assertEqual(response.status_code, 400, 'Should return 400')
        self.assertEqual(
            response.json,
            {
                "error": "wrong ingredient",
                "ingredient": {"name": "a" * 51, "quantity": {"unit": "kg", "value": 4}}
            },
            'Should return wrong ingredient error with ingredient'
        )

    def test_custom_ingredient_unsuitable_unit(self):
        json_request = {
            "ingredients": [
                {"name": "carottes", "quantity": {"unit": "kg", "value": 4}},
                {"name": "ananas", "quantity": {"unit": "l", "value": 4}}
            ]
        }
        response = self.client.post('/api/recipe', json=json_request)
        self.assertEqual(response.status_code, 400, 'Should return 400')
        self.assertEqual(
            response.json,
            {
                "error": "wrong ingredient",
                "ingredient": {"name": "ananas", "quantity": {"unit": "l", "value": 4}}
            },
            'Should return wrong ingredient error with ingredient'
        )

    def test_inappropriate_custom_ingredient(self):
        json_request = {
            "ingredients": [
                {"name": "carottes", "quantity": {"unit": "kg", "value": 4}},
                {"name": "brique", "quantity": {"unit": "kg", "value": 4}}
            ]
        }
        response = self.client.post('/api/recipe', json=json_request)
        self.assertEqual(response.status_code, 400, 'Should return 400')
        self.assertEqual(
            response.json,
            {
                "error": "wrong ingredient",
                "ingredient": {"name": "brique", "quantity": {"unit": "kg", "value": 4}}
            },
            'Should return wrong ingredient error with ingredient'
        )

    def test_insufficient_ingredients(self):
        json_request = {
            "ingredients": [
                {"name": "sel"},
                {"name": "poivre"}
            ]
        }
        response = self.client.post('/api/recipe', json=json_request)
        self.assertEqual(response.status_code, 400, 'Should return 400')
        self.assertEqual(
            response.json,
            {"error": "insufficient ingredients"},
            'Should return insufficient ingredients error'
        )

    def test_correct_request(self):
        json_request = {
            "ingredients": [
                {"name": "carottes", "quantity": {"unit": "pièces", "value": 4}},
                {"name": "pommes de terre", "quantity": {"unit": "kg", "value": 2.5}},
                {"name": "poireaux", "quantity": {"unit": "pièce", "value": 2}},
                {"name": "oignons", "quantity": {"unit": "pièce", "value": 2}},
                {"name": "beurre"},
                {"name": "lardons"},
                {"name": "lait", "quantity": {"unit": "l", "value": 0.5}},
                {"name": "farine", "quantity": {"unit": "g", "value": 50}},
                {"name": "gruyère râpé", "quantity": {"unit": "g", "value": 50}},
                {"name": "sel"},
                {"name": "poivre"},
            ]
        }
        response = self.client.post('/api/recipe', json=json_request)

        self.assertEqual(response.status_code, 200, 'Should return 200')

        self.assertIsInstance(response.json['dishName'], str, 'Should return a dish name')
        self.assertTrue(3 <= len(response.json['dishName']) <= 50, 'Should return a dish name of correct length')

        self.assertIsInstance(response.json['dishDescription'], str, 'Should return a dish description')
        self.assertTrue(3 <= len(response.json['dishDescription']) <= 100,
                        'Should return a dish description of correct length')

        self.assertIsInstance(response.json['ingredients'], str, 'Should return ingredients list')
        self.assertTrue(3 <= len(response.json['ingredients']) <= 500,
                        'Should return ingredients list of correct length')

        self.assertIsInstance(response.json['steps'], list, 'Should return steps list')
        self.assertTrue(1 <= len(response.json['steps']) <= 20, 'Should return steps list of correct length')
        for step in response.json['steps']:
            self.assertIsInstance(step, str, 'Should return steps content')
            self.assertTrue(3 <= len(step) <= 500, 'Steps should have correct length')

        self.assertIsInstance(response.json['coach']['name'], str, 'Should return a coach name')
        self.assertTrue(3 <= len(response.json['coach']['name']) <= 50, 'Should return a coach name of correct length')

        self.assertIsInstance(response.json['coach']['description'], str, 'Should return a coach description')
        self.assertTrue(3 <= len(response.json['coach']['description']) <= 500,
                        'Should return a coach description of correct length')


@unittest.skip("Image endpoint is expensive and thus we don't want to run its tests automatically.")
class ImageEndpointTest(ApiEndpointTest):

    def test_empty_image_request(self):
        json_request = {
            "dishDescription": ""
        }
        response = self.client.post('/api/image', json=json_request)
        self.assertEqual(response.status_code, 400, 'Should return 400')

    def test_correct_request(self):
        json_request = {
            "dishDescription": "lasagnes aux légumes"
        }
        response = self.client.post('/api/image', json=json_request)

        self.assertEqual(response.status_code, 200, 'Should return 200')

        image_url = response.json['url']
        self.assertTrue(requests.head(image_url).headers['content-type'].startswith('image/'),
                        'Should return an image url')


class IngredientsEndpointTest(ApiEndpointTest):

    def test_a(self):
        response = self.client.get('/api/ingredients')

        self.assertEqual(response.status_code, 200, 'Should return 200')

        with open(main.PROJECT_ROOT_PATH / 'data' / 'ingredients_fr.json', 'r', encoding='utf-8') as file:
            ingredients = json.load(file)
        response = self.client.get('/api/ingredients')
        self.assertEqual(response.json, ingredients, 'Should return ingredients list')
