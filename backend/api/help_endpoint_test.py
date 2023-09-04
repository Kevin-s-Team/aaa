import unittest

from api.endpoint_test import ApiEndpointTest


@unittest.skip("Not implemented")
class HelpEndpointTest(ApiEndpointTest):

    def test_correct_request(self):
        json_request = {
            "steps": [
                "Préchauffez votre four à 180°C.",
                "Coupez le boeuf en fines tranches et assaisonnez-le avec du sel et du poivre.",
                "Dans une grande poêle, faites chauffer de l'huile d'olive et faites dorer les tranches de boeuf de chaque côté.",
                "Pendant ce temps, épluchez et coupez les courgettes et les carottes en rondelles.",
                "Dans un plat allant au four, disposez les légumes coupés.",
                "Ajoutez les tranches de boeuf dorées sur les légumes.",
                "Dans un bol, mélangez 2 cuillères à soupe d'huile d'olive, 1 cuillère à soupe de vinaigre, 1 cuillère à soupe de sucre et assaisonnez avec du sel et du poivre.",
                "Versez la préparation sur les légumes et le boeuf.",
                "Enfournez le plat pendant 30 minutes.",
                "Servez chaud avec une cuillère à soupe de crème fraîche.",
            ],
            "stepNumber": 2
        }

        response = self.client.post('api/help', json=json_request)

        self.assertEqual(response.status_code, 200, 'Should return 200')
        
        self.assertIsInstance(response.json['helpText'], str, 'Should return a help text')
        self.assertTrue(10 < len(response.json['helpText']) < 100, 'Should return a help text with a correct length')
