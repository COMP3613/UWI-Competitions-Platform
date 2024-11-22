from datetime import datetime


class Ranking:
    def __init__(self, student_id: int, rank: int, date: datetime):
        self.student_id = student_id  # The student's name
        self.rank = rank         # The student's rank
        self.date = date.now()

    def to_dict(self):
        """Convert the ranking to a dictionary format."""
        return {
            "student": self.student_id,
            "rank": self.rank,
            "date": self.date
        }

    def __repr__(self):
        return f'<Ranking {self.rank} : {self.student_id} : {self.date}>'