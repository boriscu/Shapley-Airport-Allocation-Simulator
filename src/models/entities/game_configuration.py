from typing import List, Optional
from pydantic import BaseModel, Field

from src.models.entities.player import Player
from src.models.enums.algorithm_type import AlgorithmType


class GameConfiguration(BaseModel):
    """
    Holds the configuration for a game session.
    """

    players: List[Player] = Field(
        ..., min_items=1, description="List of players participating in the game"
    )
    algorithm: AlgorithmType = Field(
        AlgorithmType.EXACT,
        description="The algorithm to use for Shapley value calculation",
    )
    num_samples: Optional[int] = Field(
        None,
        description="Number of samples for approximate calculation (if applicable)",
    )

    runway_cost_steps: Optional[List[float]] = Field(
        None, description="c1..c_|T| (c0 assumed 0). Required for CONFIGURATION_VALUE."
    )

    class Config:
        frozen = True
