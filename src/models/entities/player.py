from pydantic import BaseModel, Field

class Player(BaseModel):
    """
    Represents an agent (airplane) in the airport cost-sharing game.
    """
    id: str = Field(..., description="Unique identifier for the player")
    name: str = Field(..., description="Human-readable name of the player")
    cost: float = Field(..., gt=0, description="The cost or requirement associated with this player (e.g., runway length)")

    class Config:
        frozen = True # Make instances immutable
