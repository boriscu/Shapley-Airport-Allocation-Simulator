from src.models.enums.algorithm_type import AlgorithmType
from src.models.entities.game_configuration import GameConfiguration
from src.models.entities.calculation_result import CalculationResult

from src.domain.airport_game import AirportGame
from src.domain.airport_game_coalition import AirportGameWithCoalitionConfiguration

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

        self.logger.info(
            f"Starting simulation with {len(config.players)} players using {config.algorithm} algorithm."
        )

        if config.algorithm == AlgorithmType.CONFIGURATION_VALUE:
            self._validate_configuration_value_inputs(config)

            game = AirportGameWithCoalitionConfiguration(
                players=config.players,
                runway_cost_steps=config.runway_cost_steps,
            )
        else:
            self._validate_classic_airport_inputs(config)
            game = AirportGame(config.players)

        calculator = CalculatorFactory.create_calculator(
            config.algorithm, config.num_samples
        )

        result = calculator.calculate(game)

        self.logger.info(
            f"Simulation completed in {result.execution_time:.4f} seconds."
        )
        return result

    def _validate_classic_airport_inputs(self, config: GameConfiguration) -> None:
        """
        Validates the inputs for the classic airport game.
        """

        missing = [p.id for p in config.players if getattr(p, "cost", None) is None]
        if missing:
            raise ValueError(
                f"Classic AirportGame requires Player.cost. Missing cost for player ids: {missing}"
            )

    def _validate_configuration_value_inputs(self, config: GameConfiguration) -> None:
        """
        Validates the inputs for the configuration value algorithm.
        Paper algorithm requires runway_cost_steps + Player.type + Player.airlines
        """

        if not getattr(config, "runway_cost_steps", None):
            raise ValueError(
                "CONFIGURATION_VALUE requires config.runway_cost_steps = [c1..cT]."
            )

        missing_type = [
            p.id for p in config.players if getattr(p, "type", None) is None
        ]
        if missing_type:
            raise ValueError(
                f"CONFIGURATION_VALUE requires Player.type (τ(i)). Missing for player ids: {missing_type}"
            )

        missing_airlines = [
            p.id
            for p in config.players
            if not getattr(p, "airlines", None) or len(getattr(p, "airlines", [])) == 0
        ]
        if missing_airlines:
            raise ValueError(
                f"CONFIGURATION_VALUE requires Player.airlines (code-sharing sets). Missing for player ids: {missing_airlines}"
            )

        max_type = max(getattr(p, "type") for p in config.players)
        if len(config.runway_cost_steps) < max_type:
            raise ValueError(
                f"runway_cost_steps has length {len(config.runway_cost_steps)} "
                f"but max Player.type is {max_type}. Need at least {max_type} entries."
            )
