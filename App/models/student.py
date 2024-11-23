from App.database import db
from App.models import User
from App.models.ranking import Ranking
from datetime import datetime

class Student(User):
    __tablename__ = 'student'

    rating_score = db.Column(db.Float, nullable=False, default=0)
    comp_count = db.Column(db.Integer, nullable=False, default=0)
    curr_rank = db.Column(db.Integer, nullable=False, default=0)
    prev_rank = db.Column(db.Integer, nullable=False, default=0)
    teams = db.relationship('Team', secondary='student_team', overlaps='students', lazy=True)
    notifications = db.relationship('Notification', backref='student', lazy=True)
    ranking_history = db.relationship('Ranking', overlaps='students', lazy=True)

    def __init__(self, username, password):
        super().__init__(username, password)
        self.rating_score = 0
        self.comp_count = 0
        self.curr_rank = 0
        self.prev_rank = 0
        self.teams = []
        self.notifications = []
        self.ranking_history = []

    def add_notification(self, notification):
        if notification:
          try:
            self.notifications.append(notification)
            db.session.commit()
            return notification
          except Exception as e:
            db.session.rollback()
            return None
        return None

    def get_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "rating_score": self.rating_score,
            "comp_count" : self.comp_count,
            "curr_rank" : self.curr_rank
        }
    
    def get_aggregate_score(self):
        return self.rating_score

    def store_historical_ranking(self, score: float, date: datetime = None):
        try:
            # Use provided date or current time
            ranking_date = date or datetime.utcnow()
            
            # Create new ranking entry
            new_ranking = Ranking(
                student_id=self.id,
                ranking_score=score
            )
            new_ranking.date = ranking_date
            
            # Add to database
            db.session.add(new_ranking)
            db.session.commit()
            
            return new_ranking
            
        except Exception as e:
            db.session.rollback()
            return None

    def update_aggregate_ranking(self, ranking_score: float):
        try:
            # Update the rating score
            self.rating_score = ranking_score
            
            # Store the historical ranking
            if self.store_historical_ranking(ranking_score):
                db.session.commit()
                return True
            return False
            
        except Exception as e:
            db.session.rollback()
            return False

    def to_Dict(self):
        return {
            "ID": self.id,
            "Username": self.username,
            "Rating Score": self.rating_score,
            "Number of Competitions" : self.comp_count,
            "Rank" : self.curr_rank
        }

    def __repr__(self):
        return f'<Student {self.id} : {self.username}>'