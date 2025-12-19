import time
import numpy as np
import matplotlib.pyplot as plt
from typing import List
import os
import sys

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.entities.player import Player
from src.models.enums.algorithm_type import AlgorithmType
from src.models.entities.game_configuration import GameConfiguration
from src.simulation.simulation_engine import SimulationEngine

def generate_random_players(n: int) -> List[Player]:
    return [
        Player(id=f"P{i}", name=f"Airline {i}", cost=float(np.random.randint(1000, 4000)))
        for i in range(n)
    ]

def benchmark_scaling():
    engine = SimulationEngine()
    player_counts = [3, 5, 7, 9, 10, 11]
    
    exact_times = []
    approx_times_2k = []
    
    print("| N | Exact Time (s) | Approx Time (2000 samples) (s) |")
    print("|---|----------------|--------------------------------|")
    
    for n in player_counts:
        players = generate_random_players(n)
        
        # Benchmark Exact
        try:
            config_exact = GameConfiguration(players=players, algorithm=AlgorithmType.EXACT)
            result_exact = engine.run_simulation(config_exact)
            t_exact = result_exact.execution_time
        except Exception as e:
            t_exact = float('inf')
            
        # Benchmark Approx (2000 samples)
        config_approx = GameConfiguration(players=players, algorithm=AlgorithmType.APPROXIMATE, num_samples=2000)
        result_approx = engine.run_simulation(config_approx)
        t_approx = result_approx.execution_time
        
        exact_times.append(t_exact)
        approx_times_2k.append(t_approx)
        
        print(f"| {n} | {t_exact:.4f} | {t_approx:.4f} |")

def benchmark_convergence():
    engine = SimulationEngine()
    n = 10
    players = [
        Player(id="P1", name="A1", cost=3238.0),
        Player(id="P2", name="A2", cost=3901.0),
        Player(id="P3", name="A3", cost=3486.0),
        Player(id="P4", name="A4", cost=1162.0),
        Player(id="P5", name="A5", cost=2806.0),
        Player(id="P6", name="A6", cost=3790.0),
        Player(id="P7", name="A7", cost=1579.0),
        Player(id="P8", name="A8", cost=2681.0),
        Player(id="P9", name="A9", cost=2921.0),
        Player(id="P10", name="A10", cost=1119.0),
    ]
    
    print("\nBenchmark: Convergence of Approximate vs Exact (N=10)")
    config_exact = GameConfiguration(players=players, algorithm=AlgorithmType.EXACT)
    result_exact = engine.run_simulation(config_exact)
    exact_values = np.array(list(result_exact.shapley_values.values()))
    
    sample_sizes = [500, 1000, 2000, 4000, 6000, 10000]
    print("| Samples | Time (s) | RMSE Error |")
    print("|---------|----------|------------|")
    
    for s in sample_sizes:
        config_approx = GameConfiguration(players=players, algorithm=AlgorithmType.APPROXIMATE, num_samples=s)
        result_approx = engine.run_simulation(config_approx)
        approx_values = np.array([result_approx.shapley_values[pid] for pid in result_exact.shapley_values.keys()])
        
        rmse = np.sqrt(np.mean((exact_values - approx_values)**2))
        print(f"| {s} | {result_approx.execution_time:.4f} | {rmse:.2f} |")

if __name__ == "__main__":
    benchmark_scaling()
    benchmark_convergence()
