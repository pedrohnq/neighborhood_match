import heapq

from entities import HomeBuyer, Neighborhood


class PlaceHomeBuyersInNeighborhoods:
    """
    Manages the process of assigning homebuyers to neighborhoods based on their preferences and scores 

    Attributes:
        file_path (str): The path to the file containing the data for neighborhoods and homebuyers 
        neighborhoods (dict): A dictionary mapping neighborhood IDs to Neighborhood objects 
        homebuyers (dict): A dictionary mapping homebuyer IDs to HomeBuyer objects 
        priority_buyers (dict): A dictionary mapping neighborhood IDs to lists of prioritized HomeBuyer objects 
        neighb_limit (int): The maximum number of homebuyers that can be allocated to each neighborhood 
    """
    def __init__(self, file_path: str) -> None:
        """
        Initializes the PlaceHomeBuyersInNeighborhoods instance with the given file path 

        Args:
            file_path (str): The path to the file containing the data for neighborhoods and homebuyers 
        """
        self.file_path = file_path
        self.neighborhoods = dict()
        self.homebuyers = dict()
        self.priority_buyers = dict()
        self.neighb_limit = 0
    
    def initialize_algorithm(self) -> None:
        """
        Initializes the allocation algorithm by setting up priority buyers and the neighborhood limit 
        """
        self.priority_buyers = {
            neighb_id: [] for neighb_id in self.neighborhoods.keys()
        }
        self.neighb_limit = len(self.homebuyers) // len(self.neighborhoods)

    def _parse_line(self, line: str) -> None:
        """
        Parses a line from the input file to create and store Neighborhood or HomeBuyer objects 

        Args:
            line (str): A line of text from the file, expected to start with 'N' for Neighborhood 
                        or 'H' for HomeBuyer 
        """
        if line.startswith('N'):
            neighborhood = Neighborhood.create_from_string(line) 
            self.neighborhoods[neighborhood.entity_id] = neighborhood
        elif line.startswith('H'):
            homebuyer = HomeBuyer.create_from_string(line)
            self.homebuyers[homebuyer.entity_id] = homebuyer

    def read_input_file(self) -> None:
        """
        Reads and parses the file specified by `file_path` 
        """
        with open(self.file_path, 'r') as file:
            for line in file:
                self._parse_line(line)

    def assign_homebuyers(self):
        unallocated_homebuyers = list(self.homebuyers.values())
        out_of_priority = []
        index = 0
        while unallocated_homebuyers:
            for hb in unallocated_homebuyers[:]:
                index+=1
                try:
                    neighb_preferred = int(hb.neighborhood_priority.pop(0).replace('N', ''))
                except:
                    out_of_priority.append(hb)
                    unallocated_homebuyers.remove(hb)
                    continue

                neighb_score = hb.calculate_neighborhood_score(self.neighborhoods[neighb_preferred])

                heapq.heappush(self.priority_buyers[neighb_preferred], (neighb_score, -id(hb), hb))
                unallocated_homebuyers.remove(hb)

                if len(self.priority_buyers[neighb_preferred]) > self.neighb_limit:
                    element = heapq.heappop(self.priority_buyers[neighb_preferred])
                    unallocated_homebuyers.append(element[2])

    def write_output_file(self) -> None:
        """
        Writes the final allocation of homebuyers to neighborhoods to the output file
        """
        file_name = 'data/output.txt'
        output_string = ''
        
        with open(file_name, 'w') as file:
            for neighb, homebuyers in dict(sorted(self.priority_buyers.items())).items():
                homebuyers_string = ' '.join(f'H{hb.entity_id}({score})' for score, mid, hb in sorted(homebuyers, key=lambda x: -x[0]))
                output_string += f'N{neighb}: {homebuyers_string}\n'
            
            file.write(output_string)

    def execute(self) -> None:
        """
        Executes the full algorithm to match homebuyers with neighborhoods based on preferences 
        and scores
        """
        self.read_input_file()
        self.initialize_algorithm()
        self.assign_homebuyers()
        self.write_output_file()
