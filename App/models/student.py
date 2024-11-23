from App.database import db
from App.models import User
from App.models.observer import Observer
from App.models.student_memento import StudentMemento


class Student(User, Observer):
    __tablename__ = 'student'

    rating_score = db.Column(db.Float, nullable=False, default=0)
    comp_count = db.Column(db.Integer, nullable=False, default=0)
    curr_rank = db.Column(db.Integer, nullable=False, default=0)
    prev_rank = db.Column(db.Integer, nullable=False, default=0)
    teams = db.relationship('Team', secondary='student_team', overlaps='students', lazy=True)
    notifications = db.relationship('Notification', backref='student', lazy=True)
    competitions = db.relationship('Competition', secondary='competition_observer', back_populates='observers')

    def __init__(self, username, password):
        super().__init__(username, password)
        self.rating_score = 0
        self.comp_count = 0
        self.curr_rank = 0
        self.prev_rank = 0
        self.teams = []
        self.notifications = []

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

    def create_memento(self):
        memento = StudentMemento(
            student_id=self.id,
            username = self.username,
            rating_score=self.rating_score,
            curr_rank=self.curr_rank,
        )
        db.session.add(memento)
        db.session.commit()
        return memento

    def get_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "rating_score": self.rating_score,
            "comp_count": self.comp_count,
            "curr_rank": self.curr_rank
        }

    def to_Dict(self):
        return {
            "ID": self.id,
            "Username": self.username,
            "Rating Score": self.rating_score,
            "Number of Competitions": self.comp_count,
            "Rank": self.curr_rank
        }

    def __repr__(self):
        return f'<Student {self.id} : {self.username}>'

    # def update_rankings(self):
    #     self.caretaker.save_memento(self.originator.create_memento())
    #     print(f"Updating rankings for {self.username}...")


# Define the association table
competition_observer = db.Table('competition_observer',
                                db.Column('competition_id', db.Integer, db.ForeignKey('competition.id')),
                                db.Column('student_id', db.Integer, db.ForeignKey('student.id'))
                                )
