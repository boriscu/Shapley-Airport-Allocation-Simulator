from typing import Dict, List, Sequence, Set

from src.models.entities.player import Player
from src.domain.cooperative_game import CooperativeGame

class AirportGameWithCoalitionConfiguration(CooperativeGame):
    """
    Airport game (N,c) enriched with coalition configuration B induced by airlines.
    Paper model is (N, c, B). :contentReference[oaicite:4]{index=4}
    """

    def __init__(self, players: List[Player], runway_cost_steps: Sequence[float]):
        """
        runway_cost_steps: [c1, c2, ..., c_|T|] where c0 is defined as 0 in the paper. :contentReference[oaicite:5]{index=5}
        """
        super().__init__(players)
        if len(runway_cost_steps) == 0:
            raise ValueError("runway_cost_steps must be non-empty")
        self.c = [0.0] + list(runway_cost_steps)  # c[0]=0, c[t]=c_t

        # Build B_a and B_i
        self.B_a: Dict[str, Set[str]] = {}  # airline -> set of movement ids
        self.B_i: Dict[str, Set[str]] = {}  # movement id -> set of airlines

        for p in players:
            self.B_i[p.id] = set(p.airlines)
            for a in p.airlines:
                self.B_a.setdefault(a, set()).add(p.id)

    def calculate_characteristic_function(self, coalition: List[Player]) -> float:
        """
        Standard airport game: coalition cost is max runway requirement among its members.
        Here we map type -> c_type (piecewise runway segments).
        """
        if not coalition:
            return 0.0
        t = max(p.type for p in coalition)
        return self.c[t]
