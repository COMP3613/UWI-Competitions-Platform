from App.models import Command
from App.controllers import *
from App.models import Competition, Team , CompetitionTeam
from App.database import db


class UpdateRank(Command):

    def execute(self):
        print("Updating Ranks")
        students = get_all_students()
        students.sort(key=lambda x: (x.rating_score, x.comp_count), reverse=True)
        count = 1
        for student in students:
            curr_rank = count
            if student.comp_count != 0:
                student.create_memento()
                count += 1
                student.update_ranking(curr_rank)
                if student.prev_rank == 0:
                    message = f'RANK : {student.curr_rank}. Congratulations on your first rank!'
                elif student.curr_rank == student.prev_rank:
                    message = f'RANK : {student.curr_rank}. Well done! You retained your rank.'
                elif student.curr_rank < student.prev_rank:
                    message = f'RANK : {student.curr_rank}. Congratulations! Your rank has went up.'
                else:
                    message = f'RANK : {student.curr_rank}. Oh no! Your rank has went down.'
                notification = Notification(student.id, message)
                student.update_notifications(notification)


class UpdateRating(Command):
    def __init__(self, competition):
        self.competition = competition

    def execute(self):
        print("Updating Ratings")
        competition = Competition.query.filter_by(name=self.competition).first()
        comp_teams = CompetitionTeam.query.filter_by(comp_id=competition.id).all()
        for comp_team in comp_teams:
            team = Team.query.get(comp_team.team_id)
            for student in team.students:
                student.rating_score = (student.rating_score * student.comp_count + comp_team.rating_score) / (
                            student.comp_count + 1)
                student.comp_count += 1
                db.session.add(student)

        competition.confirm = True
        db.session.add(competition)
        db.session.commit()

