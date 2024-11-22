from App.models.ranking_memento import RankingMemento

class RankingCaretaker:
    def __init__(self):
        self.mementos = []  # List to hold mementos of rankings

    def save_memento(self, memento: RankingMemento):
        """Save a new memento."""
        self.mementos.append(memento)

    def get_memento(self, index: int) -> RankingMemento:
        """Retrieve a memento by index."""
        return self.mementos[index]