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
        _allocated_homebuyers (list): A list of homebuyers that have been allocated to neighborhoods 
        _unallocated_homebuyers (set): A set of homebuyers that have not yet been allocated to any neighborhood 
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
        self._allocated_homebuyers = []
        self._unallocated_homebuyers = set()
    
    def initialize_algorithm(self) -> None:
        """
        Initializes the allocation algorithm by setting up priority buyers and the neighborhood limit 
        """
        self.priority_buyers = {
            i: [] for i in range(len(self.neighborhoods))
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
            homebuyer.set_neighborhoods_score(self.neighborhoods)
            self.homebuyers[homebuyer.entity_id] = homebuyer

    def read_file(self) -> None:
        """
        Reads and parses the file specified by `file_path` 
        """
        with open(self.file_path, 'r') as file:
            for line in file:
                self._parse_line(line)

    def _buyer_can_be_allocated(self, homebuyer: HomeBuyer, neighborhood_index: int) -> bool:
        """
        Checks if a homebuyer can be allocated to a given neighborhood based on current allocations 

        Args:
            homebuyer (HomeBuyer): The homebuyer to be checked
            neighborhood_index (int): The index of the neighborhood to check against

        Returns:
            bool: True if the homebuyer can be allocated
        """
        return (homebuyer not in self._allocated_homebuyers) and (homebuyer not in self.priority_buyers[neighborhood_index])

    def _update_allocation(self, neighborhood_index: int) -> None:
        """
        Updates the allocation of homebuyers to the specified neighborhood and manages 
        unallocated homebuyers

        Args:
            neighborhood_index (int): The index of the neighborhood to update

        """
        self.priority_buyers[neighborhood_index] = list(set(self.priority_buyers[neighborhood_index]))
        self.priority_buyers[neighborhood_index].sort(key = lambda obj: obj.neighborhood_scores[neighborhood_index], reverse=True)
        self._unallocated_homebuyers = (
            set(list(self._unallocated_homebuyers) + self.priority_buyers[neighborhood_index][self.neighb_limit:]) 
            - set(self.priority_buyers[neighborhood_index][:self.neighb_limit])
        )

        self.priority_buyers[neighborhood_index] = self.priority_buyers[neighborhood_index][:self.neighb_limit]
        self._allocated_homebuyers.extend(self.priority_buyers[neighborhood_index])

    def assign_homebuyers(self, iteration: int = 0) -> None:
        """
        Assigns homebuyers to neighborhoods based on their preferences and scores

        Args:
            iteration (int, optional): The current iteration level for checking preferences. 
                                       Defaults to 0
        """
        next_priority = iteration
        for neighb in self.neighborhoods.values():
            if len(self.priority_buyers[neighb.entity_id]) != self.neighb_limit:
                for hb in self.homebuyers.values():
                    if (
                        hb.is_preferred_neighborhood(neighb.entity_id) 
                        and self._buyer_can_be_allocated(hb, neighb.entity_id)
                    ):
                        self.priority_buyers[neighb.entity_id].append(hb)

                if self._unallocated_homebuyers:
                    for rm in self._unallocated_homebuyers:
                        if (
                            rm.is_preferred_neighborhood(neighb.entity_id, priority=next_priority) 
                            and self._buyer_can_be_allocated(rm, neighb.entity_id)
                        ):
                            self.priority_buyers[neighb.entity_id].append(rm)
                    next_priority += 1

                self._update_allocation(neighb.entity_id)
                
        if self._unallocated_homebuyers and iteration < len(self.neighborhoods):
            self.assign_homebuyers(iteration + 1)
        
    def write_file(self) -> None:
        """
        Writes the final allocation of homebuyers to neighborhoods to the output file
        """
        file_name = 'data/output.txt'
        output_string = ''
        
        with open(file_name, 'w') as file:
            for neighb, homebuyers in self.priority_buyers.items():
                homebuyers_string = ' '.join(f'H{hb.entity_id}({hb.neighborhood_scores[neighb]})' for hb in homebuyers)
                output_string += f'N{neighb}: {homebuyers_string}\n'
            
            file.write(output_string)

    def execute(self) -> None:
        """
        Executes the full algorithm to match homebuyers with neighborhoods based on preferences 
        and scores
        """
        self.read_file()
        self.initialize_algorithm()
        self.assign_homebuyers()
        self.write_file()
