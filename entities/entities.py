from typing import List, Dict

from entities.base import BaseEntity


class Neighborhood(BaseEntity):
    """
    Represents a neighborhood with key attributes like energy, water, and resilience scores, and 
    maintains a list of associated homebuyers 

    Attributes:
        entity_id (int): A identifier for the entity 
        energy (int): The entity's energy score 
        water (int): The entity's water score 
        resilience (int): The entity's resilience score 
        prefix (str): A prefix used to identify the type of entity ('N' for Neighborhood) 
        homebuyers (list): A list of homebuyers associated with the neighborhood 
    """
    prefix = 'N'

    def __init__(self, entity_id: int, energy: int, water: int, resilience: int) -> None:
        """
        Initialize the class setting default attributes
        """
        super().__init__(entity_id, energy, water, resilience)
        self.homebuyers = []
    
    def __str__(self) -> str:
        """
        Returns a string representation of the neighborhood 

        The string includes the prefix, ID, and key attributes of the neighborhood. The format is 
        as follows: 'N N{entity_id} E:{energy} W:{water} R:{resilience}'

        Returns:
            str: A formatted string representing the neighborhood 
        """
        return f'N N{self.entity_id} E:{self.energy} W:{self.water} R:{self.resilience}'
    

class HomeBuyer(BaseEntity):
    """
    Represents a homebuyer with attributes and neighborhood preferences 

    Attributes:
        entity_id (int): A identifier for the homebuyer 
        energy (int): The homebuyer's energy score 
        water (int): The homebuyer's water score 
        resilience (int): The homebuyer's resilience score 
        prefix (str): A prefix used to identify the type of entity ('H' for HomeBuyer) 
        neighborhood_priority (list): A list of neighborhood identifiers in order of preference 
    """
    prefix = 'H'

    def __init__(self, entity_id: int, energy: int, water: int, resilience: int, neighborhood_priority: List[str]) -> None:
        """
        Initialize the class setting default attributes
        """
        super().__init__(entity_id, energy, water, resilience)
        self.neighborhood_priority = neighborhood_priority

    def __str__(self) -> str:
        """
        Returns a string representation of the homebuyer 

        The string includes the prefix, ID, and key attributes of the homebuyer. The format is 
        as follows: 'H H{entity_id} E:{energy} W:{water} R:{resilience} {neighborhood_priority}'

        Where {neighborhood_priority} is a sequence of neighborhood IDs separated by '>', e.g., 'N1>N2>N3' 

        Returns:
            str: A formatted string representing the homebuyer 
        """
        return f'H H{self.entity_id} E:{self.energy} W:{self.water} R:{self.resilience} {">".join(self.neighborhood_priority)}'


    @classmethod
    def _parse_base_attributes(cls, string: str) -> dict:
        """
        Parses a string to extract entity attributes such as energy, water, and resilience and
        neighborhood_priority 

        This method expects a string formatted with specific entity information and processes it to 
        retrieve the entity's ID and its associated attributes 
        
        Args:
            string (str): A string containing entity data in the format 
                          '{prefix} {prefix}{id} E:{energy} W:{water} R:{resilience} {neighborhood_priority}' 
                          
                          Where {neighborhood_priority} is a sequence of neighborhood IDs separated by '>',
                          e.g., 'N1>N2>N3' 

        Returns:
            dict: A dictionary containing the parsed entity attributes:
                - entity_id (int): The entity's ID 
                - energy (int): The extracted energy score
                - water (int): The extracted water score
                - resilience (int): The extracted resilience score 
                - splitted_string (list): The components of the string after splitting 
        """
        base_attributes = super()._parse_base_attributes(string)
        base_attributes['neighborhood_priority'] = base_attributes['splitted_string'][-1].split('>')
        return base_attributes

    def calculate_neighborhood_score(self, neighborhood: Neighborhood) -> int:
        """
        Calculates the scores for th neighborhood based on the dot product of the 
        homebuyer's attributes and the neighborhood's attributes 

        Args:
            neighborhood (Neighborhood): An instance of the Neighborhood class

        Returns:
            int: Returns the result of dot product
        """
        return (
            self.energy * neighborhood.energy
            + self.water * neighborhood.water 
            + self.resilience * neighborhood.resilience
        )

    def is_preferred_neighborhood(self, neighborhood_id: int, priority = 0) -> bool:
        """
        Checks if a given neighborhood ID matches the preferred neighborhood at a specified priority

        Args:
            neighborhood_id (int): The ID of the neighborhood to check 
            priority (int, optional): The priority level to check. Defaults to 0 (highest priority)

        Returns:
            bool: True if the given neighborhood ID matches the preferred neighborhood at the 
                  specified priority
        """
        if f'N{neighborhood_id}' in self.neighborhood_priority and priority < len(self.neighborhood_priority):
            return self.neighborhood_priority[priority] == f'N{neighborhood_id}'
        return False