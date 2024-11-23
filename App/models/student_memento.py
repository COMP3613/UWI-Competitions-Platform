from typing import List
from App.database import db
from datetime import datetime, timedelta


class StudentMemento(db.Model):
    __tablename__ = 'student_memento'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    username = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    rating_score = db.Column(db.Float, nullable=False)
    curr_rank = db.Column(db.Integer, nullable=False)


    def get_history_in_range(username, days):
        timeframe = datetime.utcnow() - timedelta(days=days)  # 6 months previous
        return (
            db.session.query(StudentMemento.rating_score, StudentMemento.curr_rank , StudentMemento.timestamp)
            .filter_by(username=username)
            .filter(StudentMemento.timestamp >= timeframe)
            .order_by(StudentMemento.timestamp.desc())
            .all()
        )
