from typing import List
from src.models.entities.game_configuration import GameConfiguration
from src.models.entities.calculation_result import CalculationResult
from src.domain.airport_game import AirportGame
from src.services.calculator_factory import CalculatorFactory
from src.infrastructure.logger_service import LoggerService

class SimulationEngine:
    """
    Orchestrates the execution of game simulations.
    """

    def __init__(self):
        self.logger = LoggerService().get_logger()

    def run_simulation(self, config: GameConfiguration) -> CalculationResult:
        """
        Runs a single simulation based on the provided configuration.
        """
        self.logger.info(f"Starting simulation with {len(config.players)} players using {config.algorithm} algorithm.")
        
        # 1. Create the game instance
        game = AirportGame(config.players)
        
        # 2. Create the calculator
        calculator = CalculatorFactory.create_calculator(config.algorithm, config.num_samples)
        
        # 3. Perform calculation
        result = calculator.calculate(game)
        
        self.logger.info(f"Simulation completed in {result.execution_time:.4f} seconds.")
        return result
