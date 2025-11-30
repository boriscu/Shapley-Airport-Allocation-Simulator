from typing import Optional
from src.services.shapley_calculator_interface import ShapleyCalculator
from src.services.exact_shapley_calculator import ExactShapleyCalculator
from src.services.approximate_shapley_calculator import ApproximateShapleyCalculator
from src.models.enums.algorithm_type import AlgorithmType

class CalculatorFactory:
    """
    Factory to create ShapleyCalculator instances.
    """
    
    @staticmethod
    def create_calculator(algorithm: AlgorithmType, num_samples: Optional[int] = None) -> ShapleyCalculator:
        if algorithm == AlgorithmType.EXACT:
            return ExactShapleyCalculator()
        elif algorithm == AlgorithmType.APPROXIMATE:
            samples = num_samples if num_samples is not None else 1000
            return ApproximateShapleyCalculator(num_samples=samples)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
