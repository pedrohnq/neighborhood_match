from abc import ABC, abstractmethod


class BaseEntity(ABC):
    """
    Abstract base class that defines the common structure shared between different entities 

    This class serves as a blueprint for entities like Neighborhood and Homebuyers, focusing on 
    common attributes such as energy, water, and resilience. Subclasses are expected to implement 
    additional behaviors specific to each type of entity 

    Attributes:
        entity_id (int): A identifier for the entity 
        energy (int): The entity's energy score 
        water (int): The entity's water score 
        resilience (int): The entity's resilience score 
        prefix (str): A prefix used to identify the type of entity

    Note:
        This class cannot be instantiated directly. It must be inherited by other classes that 
        implement additional behaviors 
    """
    prefix = ''

    def __init__(self, entity_id: int, energy: int, water: int, resilience: int) -> None:
        """
        Initialize the class setting default attributes
        """
        self.entity_id = entity_id
        self.energy = energy
        self.water = water
        self.resilience = resilience

    @abstractmethod
    def __str__(self) -> str:
        """
        Abstract method that should return a string representation of the entity 

        Subclasses must override this method to provide a meaningful string representation
        that includes key details of the entity

        Returns:
            str: A string that represents the object
        """
        pass
    
    @classmethod
    def _parse_base_attributes(cls, string: str) -> dict:
        """
        Parses a string to extract entity attributes such as energy, water, and resilience 

        This method expects a string formatted with specific entity information and processes it to 
        retrieve the entity's ID and its associated attributes 
        
        Args:
            string (str): A string containing entity data in the format 
                          '{prefix} {prefix}{id} E:{energy} W:{water} R:{resilience}' 

        Returns:
            dict: A dictionary containing the parsed entity attributes:
                - entity_id (int): The entity's ID 
                - energy (int): The extracted energy score 
                - water (int): The extracted water score 
                - resilience (int): The extracted resilience score 
                - splitted_string (list): The components of the string after splitting 
        """
        string = string.replace('\n', '')
        splitted_string = string.split(' ')
        entity_id = splitted_string[1].split(cls.prefix)[-1]
        attributes = {attr.split(':')[0]: attr.split(':')[1] for attr in splitted_string[2:5]}
        energy = attributes.get('E', 0)
        water = attributes.get('W', 0)
        resilience = attributes.get('R', 0)
        return {
            'entity_id': int(entity_id), 
            'energy': int(energy), 
            'water': int(water), 
            'resilience': int(resilience), 
            'splitted_string': splitted_string
        }
        
    @classmethod
    def create_from_string(cls, string: str) -> 'BaseEntity':
        """
        Creates an entity instance from a formatted string 

        This method calls `_parse_base_attributes` to extract entity information from the string and
        uses those attributes to instantiate the class 

        Args:
            string (str): A string containing entity data 

        Returns:
            BaseEntity: An instance of the class with the parsed attributes 
        """
        base_attrs = cls._parse_base_attributes(string)
        base_attrs.pop('splitted_string', None)
        return cls(**base_attrs)