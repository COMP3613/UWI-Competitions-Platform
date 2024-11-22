from App.models.ranking_memento import RankingMemento


class RankingOriginator:
    def __init__(self):
        self.rankings = []

    def set_rankings(self, rankings):
        self.rankings = rankings

    def create_memento(self):
        return RankingMemento(self.rankings.copy())

    def restore_memento(self, memento):
        self.rankings = memento.rankings