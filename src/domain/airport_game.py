from typing import List

from src.models.entities.player import Player
from src.domain.cooperative_game import CooperativeGame


class AirportGame(CooperativeGame):
    """
    Concrete implementation of the Airport Cost-Sharing Game.
    In this game, the cost of a coalition is determined by the player with the largest requirement (cost).
    """

    def calculate_characteristic_function(self, coalition: List[Player]) -> float:
        """
        Calculates the cost for a coalition of airplanes (players).
        The cost is equal to the maximum runway length required by any player in the coalition.
        If the coalition is empty, the cost is 0.
        """
        if not coalition:
            return 0.0

        # The cost of the coalition is the maximum individual cost among its members
        return max(player.cost for player in coalition)
