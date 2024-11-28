from App.models import StudentMemento, Student, Notification, Moderator, Competition, CompetitionTeam, Team
from App.controllers import get_all_students, get_historical_ranking
from App.database import db


def update_rankings():
    students = get_all_students()

    students.sort(key=lambda x: (x.rating_score, x.comp_count), reverse=True)
    new_rankings = []
    count = 1

    for student in students:
        history = get_historical_ranking(student)
        student.create_memento()
        curr_rank = count
        if student.comp_count != 0:

            count += 1
            new_rankings.append(
                {"placement": count, "student": student.username, "rating": student.rating_score, "history": history})
            student.curr_rank = curr_rank
            if student.prev_rank == 0:
                message = f'RANK : {student.curr_rank}. Congratulations on your first rank!'
            elif student.curr_rank == student.prev_rank:
                message = f'RANK : {student.curr_rank}. Well done! You retained your rank.'
            elif student.curr_rank < student.prev_rank:
                message = f'RANK : {student.curr_rank}. Congratulations! Your rank has went up.'
            else:
                message = f'RANK : {student.curr_rank}. Oh no! Your rank has went down.'
            student.prev_rank = student.curr_rank
            notification = Notification(student.id, message)
            student.notifications.append(notification)

            try:
                db.session.add(student)
                db.session.commit()
            except Exception as e:
                db.session.rollback()

    return new_rankings


def update_ratings(comp_name):
    comp = Competition.query.filter_by(name=comp_name).first()
    comp_teams = CompetitionTeam.query.filter_by(comp_id=comp.id).all()
    for comp_team in comp_teams:
        team = Team.query.filter_by(id=comp_team.team_id).first()

        for stud in team.students:
            stud.rating_score = (stud.rating_score * stud.comp_count + comp_team.rating_score) / (stud.comp_count + 1)
            stud.comp_count += 1
            try:
                db.session.add(stud)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
    return True
