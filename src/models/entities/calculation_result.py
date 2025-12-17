from typing import Dict
from pydantic import BaseModel, Field

from src.models.enums.algorithm_type import AlgorithmType

class CalculationResult(BaseModel):
    """
    Stores the result of a Shapley value calculation.
    """
    shapley_values: Dict[str, float] = Field(..., description="Mapping of player IDs to their calculated Shapley values")
    total_cost: float = Field(..., description="The total cost that was distributed")
    execution_time: float = Field(..., description="Time taken to perform the calculation in seconds")
    algorithm_used: AlgorithmType = Field(..., description="The algorithm used")

    class Config:
        frozen = True
