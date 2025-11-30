from abc import ABC, abstractmethod
from typing import List
from src.models.entities.player import Player

class CooperativeGame(ABC):
    """
    Abstract base class representing a generic cooperative game.
    """

    def __init__(self, players: List[Player]):
        self.players = players

    @abstractmethod
    def calculate_characteristic_function(self, coalition: List[Player]) -> float:
        """
        Calculates the worth (cost or value) of a given coalition of players.
        
        Args:
            coalition: A subset of players forming the coalition.
            
        Returns:
            The characteristic value of the coalition.
        """
        pass
