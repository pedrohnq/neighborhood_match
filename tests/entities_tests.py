from unittest import TestCase

from entities import HomeBuyer, Neighborhood


class HomeBuyerTest(TestCase):
    def setUp(self):
        self.input_string = 'H H0 E:3 W:9 R:2 N0>N1'
    
    def test_create_from_string(self):
        """
        Test `create_from_string` method
        """
        homebuyer = HomeBuyer.create_from_string(self.input_string)
        self.assertEqual(homebuyer.entity_id, 0)
        self.assertEqual(homebuyer.prefix, 'H')
        self.assertEqual(homebuyer.energy, 3)
        self.assertEqual(homebuyer.water, 9)
        self.assertEqual(homebuyer.resilience, 2)
        self.assertEqual(homebuyer.neighborhood_priority, ['N0', 'N1'])
    
    def test_calculate_neighborhood_score(self):
        """
        Test `calculate_neighborhood_score` method 
        """
        neighborhoods = {
            0: Neighborhood(entity_id=0, energy=5, water=9, resilience=8)
        }
        homebuyer = HomeBuyer(
            entity_id=0, energy=4, water=2, resilience=9, neighborhood_priority=['N0', 'N1']
        )
        
        result = homebuyer.calculate_neighborhood_score(neighborhoods[0])

        self.assertEqual(result, 110)

    def test_is_preferred_neighborhood(self):
        """
        Test `is_preferred_neighborhood` method
        """
        homebuyer = HomeBuyer(
            entity_id=0, energy=4, water=2, resilience=9, neighborhood_priority=['N0', 'N1']
        )
        
        self.assertTrue(homebuyer.is_preferred_neighborhood(0))
        self.assertFalse(homebuyer.is_preferred_neighborhood(1))
        self.assertFalse(homebuyer.is_preferred_neighborhood(0, priority=1))
        self.assertTrue(homebuyer.is_preferred_neighborhood(1, priority=1))
        

class NeighborhoodTest(TestCase):
    def setUp(self):
        self.input_string = 'N N0 E:7 W:7 R:10'

    def test_create_from_string(self):
        """
        Test `create_from_string` method
        """
        neighborhood = Neighborhood.create_from_string(self.input_string)
        self.assertEqual(neighborhood.entity_id, 0)
        self.assertEqual(neighborhood.prefix, 'N')
        self.assertEqual(neighborhood.energy, 7)
        self.assertEqual(neighborhood.water, 7)
        self.assertEqual(neighborhood.resilience, 10)