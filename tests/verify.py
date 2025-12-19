import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.entities.player import Player
from src.models.entities.game_configuration import GameConfiguration
from src.models.enums.algorithm_type import AlgorithmType
from src.simulation.simulation_engine import SimulationEngine


def verify_airport_game():
    print("Verifying Airport Game Logic...")

    # Example: 3 Players with costs 10, 20, 30
    # Expected Shapley Values:
    # P1 (10): 10/3 = 3.33
    # P2 (20): 10/3 + 10/2 = 3.33 + 5 = 8.33
    # P3 (30): 10/3 + 10/2 + 10/1 = 3.33 + 5 + 10 = 18.33
    # Total: 30

    p1 = Player(id="P1", name="A", cost=10.0)
    p2 = Player(id="P2", name="B", cost=20.0)
    p3 = Player(id="P3", name="C", cost=30.0)

    players = [p1, p2, p3]
    config = GameConfiguration(players=players, algorithm=AlgorithmType.EXACT)

    engine = SimulationEngine()
    result = engine.run_simulation(config)

    print("\nResults:")
    print(f"Total Cost: {result.total_cost}")
    print("Shapley Values:")
    for pid, val in result.shapley_values.items():
        print(f"{pid}: {val:.4f}")

    # Check Efficiency
    sum_vals = sum(result.shapley_values.values())
    print(f"\nSum of Shapley Values: {sum_vals:.4f}")
    assert abs(sum_vals - result.total_cost) < 1e-6, "Efficiency property violated!"

    # Check specific values (approximate check)
    assert abs(result.shapley_values["P1"] - 3.3333) < 0.01
    assert abs(result.shapley_values["P2"] - 8.3333) < 0.01
    assert abs(result.shapley_values["P3"] - 18.3333) < 0.01

    print("\nVerification Successful!")


if __name__ == "__main__":
    verify_airport_game()
