import time
from typing import Dict
from src.services.shapley_calculator_interface import ShapleyCalculator
from src.models.entities.calculation_result import CalculationResult
from src.models.enums.algorithm_type import AlgorithmType
from src.domain.airport_game_coalition import AirportGameWithCoalitionConfiguration


class ConfigurationValueAirportCalculator(ShapleyCalculator):
    """
    Computes the configuration value for airport games with coalition configuration (N,c,B)
    using Theorem 4.1 (polynomial expression).
    """

    def calculate(self, game: AirportGameWithCoalitionConfiguration) -> CalculationResult:
        start = time.time()

        players = game.players
        if not players:
            raise ValueError("Game has no players")
        if any(getattr(p, "type", None) is None for p in players):
            raise ValueError("CONFIGURATION_VALUE requires Player.type for all players.")

        T = max(p.type for p in players)  # |T|
        c = game.c  # c[0..T]
        if len(c) <= T:  # c includes c0, so length should be T+1
            raise ValueError(f"game.c must include costs up to type {T}. Got length {len(c)}.")

        # Index players by id
        by_id = {p.id: p for p in players}

        # Precompute N^a_{>=t} sizes and A_{>=t} sizes from Theorem 4.1 
        # Na_ge[a][t] = |N^a_{>=t}|
        Na_ge: Dict[str, Dict[int, int]] = {a: {} for a in game.B_a.keys()}
        A_ge_count: Dict[int, int] = {}

        # For each threshold t, compute which airlines have any movement with type >= t
        for t in range(1, T + 1):
            airlines_ge_t = 0
            for a, movement_ids in game.B_a.items():
                count = 0
                for mid in movement_ids:
                    if by_id[mid].type >= t:
                        count += 1
                Na_ge[a][t] = count
                if count > 0:
                    airlines_ge_t += 1
            A_ge_count[t] = airlines_ge_t

        # Compute CV_i by Theorem 4.1
        cv: Dict[str, float] = {p.id: 0.0 for p in players}

        for p in players:
            i = p.id
            tau_i = p.type
            for a in game.B_i[i]:  # airlines operating movement i
                for t in range(1, tau_i + 1):
                    denom = A_ge_count[t] * Na_ge[a][t]
                    if denom == 0:
                        continue
                    cv[i] += (c[t] - c[t - 1]) / denom

        total_cost = game.calculate_characteristic_function(players)
        end = time.time()

        return CalculationResult(
            shapley_values=cv,
            total_cost=total_cost,
            execution_time=end - start,
            algorithm_used=AlgorithmType.CONFIGURATION_VALUE,  # add this enum value
        )
