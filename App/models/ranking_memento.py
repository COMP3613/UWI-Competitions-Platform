from typing import List
from App.models.ranking import Ranking

class RankingMemento:
    def __init__(self, rankings: List[Ranking]):
        self.rankings = rankings  # The state of rankings at a certain point

    def get_rankings(self):
        """Get the stored rankings."""
        return self.rankings