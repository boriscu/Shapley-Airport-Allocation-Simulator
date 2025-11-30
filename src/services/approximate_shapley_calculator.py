import time
import random
from typing import Dict, List, Optional
from src.services.shapley_calculator_interface import ShapleyCalculator
from src.domain.cooperative_game import CooperativeGame
from src.models.entities.calculation_result import CalculationResult
from src.models.entities.player import Player
from src.models.enums.algorithm_type import AlgorithmType

class ApproximateShapleyCalculator(ShapleyCalculator):
    """
    Calculates approximate Shapley values using Monte Carlo sampling.
    """

    def __init__(self, num_samples: int = 1000):
        self.num_samples = num_samples

    def calculate(self, game: CooperativeGame) -> CalculationResult:
        """
        Calculates Shapley values using Monte Carlo sampling.
        
        The algorithm works by:
        1. Sampling random permutations of players.
        2. For each permutation, calculating the marginal contribution of each player
           (cost of coalition with player - cost of coalition without player).
        3. Averaging these marginal contributions over all samples to approximate the Shapley value.
        
        This converges to the true Shapley value as the number of samples increases.
        
        Use this calculator when the number of players is large (e.g., N > 10), where
        calculating the exact value is computationally prohibitive due to N! complexity.
        """
        start_time = time.time()
        players = game.players
        n = len(players)
        shapley_values = {player.id: 0.0 for player in players}
        
        for _ in range(self.num_samples):
            # Generate a random permutation
            perm = list(players)
            random.shuffle(perm)
            
            current_coalition: List[Player] = []
            current_cost = 0.0
            
            for player in perm:
                new_coalition = current_coalition + [player]
                new_cost = game.calculate_characteristic_function(new_coalition)
                marginal_contribution = new_cost - current_cost
                
                shapley_values[player.id] += marginal_contribution
                
                current_coalition = new_coalition
                current_cost = new_cost
                
        # Average over samples
        for player_id in shapley_values:
            shapley_values[player_id] /= self.num_samples
            
        end_time = time.time()
        total_cost = game.calculate_characteristic_function(players) # Note: Sum of approx SVs might not exactly equal total cost, but we return the true total cost
        
        return CalculationResult(
            shapley_values=shapley_values,
            total_cost=total_cost,
            execution_time=end_time - start_time,
            algorithm_used=AlgorithmType.APPROXIMATE
        )
