from unittest import TestCase
from unittest.mock import patch, mock_open

from algorithm import PlaceHomeBuyersInNeighborhoods
from entities import HomeBuyer, Neighborhood


class PlaceHomeBuyersInNeighborhoodsTest(TestCase):
    def setUp(self):
        self.neighborhoods = {
            0: Neighborhood.create_from_string('N N0 E:7 W:7 R:10'),
            1: Neighborhood.create_from_string('N N1 E:2 W:1 R:1')
        }
        self.homebuyers = {
            0: HomeBuyer.create_from_string('H H0 E:3 W:9 R:2 N0>N1'),
            1: HomeBuyer.create_from_string('H H1 E:4 W:3 R:7 N0>N1'),
            2: HomeBuyer.create_from_string('H H2 E:4 W:0 R:10 N0>N1'),
            3: HomeBuyer.create_from_string('H H3 E:10 W:3 R:8 N1>N0'),
        }

        file_path = 'fake_path/input.txt'
        self.allocator_algorithm = PlaceHomeBuyersInNeighborhoods(file_path)
    
    def test_read_input_file(self):
        """
        Test the `read_input_file` method
        """
        file_content = (
            'N N0 E:7 W:7 R:10\n'
            'N N1 E:2 W:1 R:1\n'
            '\n'
            '\n'
            'H H0 E:3 W:9 R:2 N0>N1\n'
            'H H1 E:4 W:3 R:7 N0>N1\n'
            'H H2 E:4 W:0 R:10 N0>N1\n'
            'H H3 E:10 W:3 R:8 N1>N0\n'
        )
        
        m = mock_open(read_data=''.join(file_content))
        m.return_value.__iter__ = lambda self: self
        m.return_value.__next__ = lambda self: next(iter(self.readline, ''))

        with patch('builtins.open', m):
            self.allocator_algorithm.read_input_file()


        # Check the internal state after reading the file
        self.assertEqual(len(self.allocator_algorithm.neighborhoods), 2)
        self.assertEqual(len(self.allocator_algorithm.homebuyers), 4)

    def test_initialize_algorithm(self):
        """
        Test the `initialize_algorithm` method
        """
        self.allocator_algorithm.homebuyers = self.homebuyers
        self.allocator_algorithm.neighborhoods = self.neighborhoods
        
        self.allocator_algorithm.initialize_algorithm()
        
        self.assertEqual(self.allocator_algorithm.priority_buyers, {0: [], 1: []})
        self.assertEqual(self.allocator_algorithm.neighb_limit, 2)
    
    def test_assign_homebuyers(self):
        """
        Test the `assign_homebuyers` method
        """
        self.allocator_algorithm.priority_buyers = {0: [], 1: []}
        self.allocator_algorithm.neighb_limit = 2
        self.allocator_algorithm.homebuyers = self.homebuyers
        self.allocator_algorithm.neighborhoods = self.neighborhoods

        self.allocator_algorithm.assign_homebuyers()

        self.assertEqual(
            self.allocator_algorithm.priority_buyers, 
            {
                0: [(128, self.homebuyers[2]), (119, self.homebuyers[1])], 
                1: [(31, self.homebuyers[3]), (17, self.homebuyers[0])]
            }
        )
    
    @patch('builtins.open', new_callable=mock_open)
    def test_write_output_data(self, mock_file):
        """
        Test the `write_output_data` method
        """
        self.allocator_algorithm.priority_buyers = {
            0: [(128, self.homebuyers[2]), (119, self.homebuyers[1])], 
            1: [(31, self.homebuyers[3]), (17, self.homebuyers[0])]
        }

        self.allocator_algorithm.write_output_file()
        
        expected_data = (
            'N0: H2(128) H1(119)\n'
            'N1: H3(31) H0(17)\n'
        )
        
        mock_file().write.assert_called_once_with(expected_data)
