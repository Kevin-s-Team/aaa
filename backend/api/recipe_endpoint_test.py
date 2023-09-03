import unittest

from .endpoint_test import ApiEndpointTest


class RecipeEndpointTest(ApiEndpointTest):

    def test_malformed_request(self):
        json_request = {
            "ingredients": [{"quantity": {"unit": "kg", "value": 4}}]
        }
        response = self.client.post('/api/recipe', json=json_request)
        self.assertEqual(response.status_code, 400, 'Should return 400')
        self.assertEqual(
            response.json,
            {"error": "malformed request"},
            'Should return malformed request error'
        )

    def test_empty_ingredients_list(self):
        json_request = {
            "ingredients": []
        }
        response = self.client.post('/api/recipe', json=json_request)
        self.assertEqual(response.status_code, 400, 'Should return 400')
        self.assertEqual(
            response.json,
            {"error": "malformed request"},
            'Should return malformed request error'
        )

    def test_too_many_ingredients(self):
        json_request = {
            "ingredients": [{"name": f"ingredient {i}"} for i in range(101)]
        }
        response = self.client.post('/api/recipe', json=json_request)
        self.assertEqual(response.status_code, 400, 'Should return 400')
        self.assertEqual(
            response.json,
            {"error": "too many ingredients"},
            'Should return too many ingredients error'
        )

    def test_ingredient_in_list_wrong_unit(self):
        json_request = {
            "ingredients": [{"name": "carotte", "quantity": {"unit": "kg", "value": 4}}]
        }
        response = self.client.post('/api/recipe', json=json_request)
        self.assertEqual(response.status_code, 400, 'Should return 400')
        self.assertEqual(
            response.json,
            {
                "error": "wrong ingredient unit",
                "ingredient": {"name": "carotte", "quantity": {"unit": "kg", "value": 4}}
            },
            'Should return wrong ingredient error with ingredient'
        )

    def test_too_long_custom_ingredient(self):
        json_request = {
            "ingredients": [
                {"name": "carotte", "quantity": {"unit": "pièce", "value": 4}},
                {"name": "a" * 51, "quantity": {"unit": "kg", "value": 4}}
            ]
        }
        response = self.client.post('/api/recipe', json=json_request)
        self.assertEqual(response.status_code, 400, 'Should return 400')
        self.assertEqual(
            response.json,
            {
                "error": "invalid custom ingredient",
                "ingredient": {"name": "a" * 51, "quantity": {"unit": "kg", "value": 4}}
            },
            'Should return wrong ingredient error with ingredient'
        )

    def test_custom_ingredient_unsuitable_unit(self):
        json_request = {
            "ingredients": [
                {"name": "carotte", "quantity": {"unit": "pièce", "value": 4}},
                {"name": "ananas", "quantity": {"unit": "l", "value": 4}}
            ]
        }
        response = self.client.post('/api/recipe', json=json_request)
        self.assertEqual(response.status_code, 400, 'Should return 400')
        self.assertEqual(
            response.json,
            {
                "error": "invalid custom ingredient unit",
                "ingredient": {"name": "ananas", "quantity": {"unit": "l", "value": 4}}
            },
            'Should return wrong ingredient error with ingredient'
        )

    def test_inappropriate_custom_ingredient(self):
        json_request = {
            "ingredients": [
                {"name": "carotte", "quantity": {"unit": "pièce", "value": 4}},
                {"name": "brique", "quantity": {"unit": "kg", "value": 4}}
            ]
        }
        response = self.client.post('/api/recipe', json=json_request)
        self.assertEqual(response.status_code, 400, 'Should return 400')
        self.assertEqual(
            response.json,
            {
                "error": "invalid custom ingredient",
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

    @unittest.skip('not implemented')
    def test_correct_request(self):
        json_request = {
            "ingredients": [
                {"name": "carotte", "quantity": {"unit": "pièce", "value": 4}},
                {"name": "pommes de terre", "quantity": {"unit": "kg", "value": 2.5}},
                {"name": "poireau", "quantity": {"unit": "pièce", "value": 2}},
                {"name": "oignon", "quantity": {"unit": "pièce", "value": 2}},
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

        self.assertIsInstance(response.json['recipes'], list, 'Should return recipes list')
        self.assertTrue(1 <= len(response.json['recipes']) <= 10, 'Should return recipes list of correct length')

        for recipe in response.json['recipes']:
            self.assertIsInstance(recipe['dishName'], str, 'Should return a dish name')
            self.assertTrue(3 <= len(recipe['dishName']) <= 50, 'Should return a dish name of correct length')

            self.assertIsInstance(recipe['dishDescription'], str, 'Should return a dish description')
            self.assertTrue(3 <= len(recipe['dishDescription']) <= 100,
                            'Should return a dish description of correct length')

            self.assertIsInstance(recipe['ingredients'], str, 'Should return ingredients list')
            self.assertTrue(3 <= len(recipe['ingredients']) <= 500,
                            'Should return ingredients list of correct length')

            self.assertIsInstance(recipe['steps'], list, 'Should return steps list')
            self.assertTrue(1 <= len(recipe['steps']) <= 20, 'Should return steps list of correct length')
            for step in recipe['steps']:
                self.assertIsInstance(step, str, 'Should return steps content')
                self.assertTrue(3 <= len(step) <= 500, 'Steps should have correct length')

            self.assertIsInstance(recipe['coach']['name'], str, 'Should return a coach name')
            self.assertTrue(3 <= len(recipe['coach']['name']) <= 50, 'Should return a coach name of correct length')

            self.assertIsInstance(recipe['coach']['description'], str, 'Should return a coach description')
            self.assertTrue(3 <= len(recipe['coach']['description']) <= 1000,
                            'Should return a coach description of correct length')

            self.assertIsInstance(recipe['coach']['image_url'], str, 'Should return a coach image url')