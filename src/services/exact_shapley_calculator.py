import time
import itertools
from typing import List

from src.services.shapley_calculator_interface import ShapleyCalculator

from src.domain.cooperative_game import CooperativeGame

from src.models.entities.player import Player
from src.models.enums.algorithm_type import AlgorithmType
from src.models.entities.calculation_result import CalculationResult


class ExactShapleyCalculator(ShapleyCalculator):
    """
    Calculates exact Shapley values by iterating over all permutations of players.
    Complexity is O(N!).
    """

    def calculate(self, game: CooperativeGame) -> CalculationResult:
        """
        Calculates exact Shapley values by iterating over all permutations of players.

        The Shapley value for a player is the average marginal contribution of that player
        across all possible permutations of the coalition formation.

        Formula:
        phi_i(v) = (1/N!) * sum_{R} [v(P_i^R U {i}) - v(P_i^R)]

        Where:
        - N is the number of players.
        - R is a permutation of players.
        - P_i^R is the set of players preceding i in permutation R.
        - v is the characteristic function (cost function).

        Complexity: O(N * N!)

        Use this calculator when the number of players is small (e.g., N <= 10), as the
        factorial complexity makes it infeasible for larger groups.
        """
        start_time = time.time()
        players = game.players
        shapley_values = {player.id: 0.0 for player in players}

        permutations = list(itertools.permutations(players))
        num_permutations = len(permutations)

        for perm in permutations:
            current_coalition: List[Player] = []
            current_cost = 0.0

            for player in perm:
                # Calculate marginal contribution
                # cost(S U {i}) - cost(S)
                # Here S is current_coalition
                # We need to construct the new coalition to calculate its cost

                new_coalition = current_coalition + [player]
                new_cost = game.calculate_characteristic_function(new_coalition)
                marginal_contribution = new_cost - current_cost

                shapley_values[player.id] += marginal_contribution

                current_coalition = new_coalition
                current_cost = new_cost

        # Average the marginal contributions
        for player_id in shapley_values:
            shapley_values[player_id] /= num_permutations

        end_time = time.time()
        total_cost = game.calculate_characteristic_function(players)

        return CalculationResult(
            shapley_values=shapley_values,
            total_cost=total_cost,
            execution_time=end_time - start_time,
            algorithm_used=AlgorithmType.EXACT,
        )
