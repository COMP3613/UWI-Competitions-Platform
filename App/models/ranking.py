from App.database import db
from sqlalchemy.sql import func

class Ranking(db.Model):
    __tablename__ = 'ranking'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.DateTime, default=func.now())
    ranking_score = db.Column(db.Integer, nullable=False)
    
    def __init__(self, student_id, date, ranking_score):
      self.student_id = student_id
      self.data = date
      self.ranking_score = ranking_score

    def get_json(self):
      return {
            "id" : self.id,
            "student_id" : self.student_id,
            "date" : self.date,
            "ranking_score": self.ranking_score
      }

    def __repr__(self):
        return f'<Ranking {self.student_id} : {self.ranking_score}>'