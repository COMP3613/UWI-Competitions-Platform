from App.database import db
from datetime import datetime
from App.models.ranking_observer import RankingObserver
from .competition_moderator import *
from .competition_team import *

class Competition(db.Model):
    __tablename__='competition'

    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String, nullable=False, unique=True)
    date = db.Column(db.DateTime, default= datetime.utcnow)
    location = db.Column(db.String(120), nullable=False)
    level = db.Column(db.Float, default=1)
    max_score = db.Column(db.Integer, default=25)
    confirm = db.Column(db.Boolean, default=False)
    moderators = db.relationship('Moderator', secondary="competition_moderator", overlaps='competitions', lazy=True)
    teams = db.relationship('Team', secondary="competition_team", overlaps='competitions', lazy=True)

    observer_id = db.Column(db.Integer, db.ForeignKey('ranking_observer.id'))
    observers = db.relationship('RankingObserver',
                              foreign_keys='RankingObserver.competition_id',
                              backref=db.backref('competition', lazy=True))

    def __init__(self, name, date, location, level, max_score):
        self.name = name
        self.date = date
        self.location = location
        self.level = level
        self.max_score = max_score
        self.moderators = []
        self.teams = []
        self.observers = []
    
    def add_mod(self, mod):
        for m in self.moderators:
            if m.id == mod.id:
                print(f'{mod.username} already added to {self.name}!')
                return None
        
        comp_mod = CompetitionModerator(comp_id=self.id, mod_id=mod.id)
        try:
            self.moderators.append(mod)
            mod.competitions.append(self)
            db.session.commit()
            print(f'{mod.username} was added to {self.name}!')
            return comp_mod
        except Exception as e:
            db.session.rollback()
            print("Something went wrong!")
            return None

    def add_team(self, team):
        for t in self.teams:
            if t.id == team.id:
                print(f'Team already registered for {self.name}!')
                return None
        
        comp_team = CompetitionTeam(comp_id=self.id, team_id=team.id)
        try:
            self.teams.append(team)
            team.competitions.append(self)
            db.session.commit()
            print(f'{team.name} was added to {self.name}!')
            return comp_team
        except Exception as e:
            db.session.rollback()
            print("Something went wrong!")
            return None
        
    def update_student_rankings(self, team_id, student_performances):
        try:
            # Verify team is in this competition
            comp_team = CompetitionTeam.query.filter_by(
                comp_id=self.id,
                team_id=team_id
            ).first()
            
            if not comp_team:
                return False
            
            team = comp_team.team
            if not team:
                return False
                
            # Update each student's rating individually
            for student_id, score in student_performances.items():
                # Verify student is in the team
                student = next((s for s in team.students if s.id == student_id), None)
                if not student:
                    continue
                    
                # Calculate individual rating score based on performance and competition level
                rating_score = (score / self.max_score) * self.level * 100
                
                # Attach student to observer if not already attached
                self.observers.attach(student)
                
                # Update student's rating
                student.update_aggregate_ranking(rating_score)
                
                # Increment student's competition count
                student.comp_count += 1

                #notify observer
                self.notify_observer()
            
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            return False

    def finalize_competition(self):
        try:
            if self.confirm:  # Already finalized
                return False
            
            # Get all participating students
            participating_students = set()
            for team in self.teams:
                participating_students.update(team.students)
            
            # Make sure all participating students are attached to observer
            for student in participating_students:
                self.observers.attach(student)
            
            # Update rankings through observer
            self.observers.update_ranking(self)
            
            # Mark competition as confirmed
            self.confirm = True
            db.session.commit()
            
            # Notify observers to recalculate rankings
            self.notify_observer()
            
            return True
            
        except Exception as e:
            db.session.rollback()
            return False
    
    def notify_observer(self):
        try:
            if self.observers:
                self.observers.notify()
                return True
            return False
            
        except Exception as e:
            return False
 

    def get_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date.strftime("%d-%m-%Y"),
            "location": self.location,
            "level" : self.level,
            "max_score" : self.max_score,
            "moderators": [mod.username for mod in self.moderators],
            "teams": [team.name for team in self.teams]
        }

    def toDict(self):
        return {
            "ID": self.id,
            "Name": self.name,
            "Date": self.date,
            "Location": self.location,
            "Level" : self.level,
            "Max Score" : self.max_score,
            "Moderators": [mod.username for mod in self.moderators],
            "Teams": [team.name for team in self.teams]
        }

    def __repr__(self):
        return f'<Competition {self.id} : {self.name}>'