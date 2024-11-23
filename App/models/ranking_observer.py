from App.database import db
from App.models.student import Student
from App.models.ranking import Ranking

class RankingObserver(db.Model):
    __tablename__ = 'ranking_observer'
    
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id', use_alter=True, name='fk_competition'), nullable=False)
    observers = db.relationship('Student', secondary='observer_student', lazy='dynamic', backref=db.backref('ranking_observers', lazy=True))
    
    def __init__(self):
        self.observers = []
    
    def attach(self, student):
        """Attach a student to observe"""
        if student not in self.observers:
            try:
                self.observers.append(student)
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                return False
        return False
    
    def detach(self, student):
        """Detach a student from observers"""
        if student in self.observers:
            try:
                self.observers.remove(student)
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                return False
        return False
    
    def notify(self):
        """Notify all observers of ranking changes"""
        try:
            self.recalculate_rankings()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False
    
    def recalculate_rankings(self):
        """Recalculate rankings for all observers"""
        # Get all students ordered by rating score
        sorted_students = self.observers.order_by(Student.rating_score.desc()).all()
        
        # Update ranks
        for i, student in enumerate(sorted_students, 1):
            student.prev_rank = student.curr_rank
            student.curr_rank = i
    
    def update_ranking(self, competition):
        """Update rankings based on competition results"""
        try:
            # Get all participating students from competition teams
            participating_students = set()
            for team in competition.teams:
                participating_students.update(team.students)
            
            # Update competition count for participating students
            for student in participating_students:
                student.comp_count += 1
                
                # Create new ranking entry
                new_ranking = Ranking(
                    student_id=student.id,
                    ranking_score=student.rating_score
                )
                db.session.add(new_ranking)
            
            # Recalculate rankings
            self.recalculate_rankings()
            
            # Commit all changes
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            return False
    
    def get_json(self):
        return {
            "id": self.id,
            "competition_id": self.competition_id,
            "observer_count": self.observers.count()
        }
    
    def __repr__(self):
        return f'<RankingObserver {self.id}>'

# Association table for observer-student relationship
observer_student = db.Table('observer_student',
    db.Column('observer_id', db.Integer, db.ForeignKey('ranking_observer.id'), primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True)
)
