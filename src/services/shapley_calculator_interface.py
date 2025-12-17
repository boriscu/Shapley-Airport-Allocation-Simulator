from abc import ABC, abstractmethod

from src.domain.cooperative_game import CooperativeGame

from src.models.entities.calculation_result import CalculationResult


class ShapleyCalculator(ABC):
    """
    Interface for Shapley value calculators.
    """

    @abstractmethod
    def calculate(self, game: CooperativeGame) -> CalculationResult:
        """
        Calculates the Shapley values for the given game.

        Args:
            game: The cooperative game instance.

        Returns:
            A CalculationResult object containing the Shapley values and metadata.
        """
        pass
