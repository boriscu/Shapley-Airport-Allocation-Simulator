from typing import FrozenSet, Optional
from pydantic import BaseModel, Field

class Player(BaseModel):
    id: str
    name: str

    # Exact and approximate airport game field
    cost: Optional[float] = Field(None, gt=0)

    # only needed for CONFIGURATION_VALUE
    type: Optional[int] = Field(None, ge=1, description="τ(i)")
    airlines: Optional[FrozenSet[str]] = Field(None, min_items=1)

    class Config:
        frozen = True
