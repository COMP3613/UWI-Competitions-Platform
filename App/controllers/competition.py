from App.controllers.ranking import update_ratings
from App.database import db
from App.models import Competition, Moderator, CompetitionTeam, Team, Student#, Student, Admin, competition_student
from datetime import datetime

def get_competition_by_name(name):
    return Competition.query.filter_by(name=name).first()

def get_competition(id):
    return Competition.query.get(id)

def get_all_competitions():
    return Competition.query.all()

def get_all_competitions_json():
    competitions = Competition.query.all()

    if not competitions:
        return []
    else:
        return [comp.get_json() for comp in competitions]
def display_competition_results(name):
    comp = get_competition_by_name(name)

    if not comp:
        print(f'{name} was not found!')
        return None
    elif len(comp.teams) == 0:
        print(f'No teams found for {name}!')
        return []
    else:
        comp_teams = CompetitionTeam.query.filter_by(comp_id=comp.id).all()
        comp_teams.sort(key=lambda x: x.points_earned, reverse=True)

        leaderboard = []
        count = 1
        curr_high = comp_teams[0].points_earned
        curr_rank = 1
        
        for comp_team in comp_teams:
            if curr_high != comp_team.points_earned:
                curr_rank = count
                curr_high = comp_team.points_earned

            team = Team.query.filter_by(id=comp_team.team_id).first()
            leaderboard.append({"placement": curr_rank, "team": team.name, "members" : [student.username for student in team.students], "score":comp_team.points_earned})
            count += 1
        
        return leaderboard

def add_results(mod_name, comp_name, team_name, score):
    mod = Moderator.query.filter_by(username=mod_name).first()
    comp = Competition.query.filter_by(name=comp_name).first()
    teams = Team.query.filter_by(name=team_name).all()

    if not mod:
        print(f'{mod_name} was not found!')
        return None
    else:
        if not comp:
            print(f'{comp_name} was not found!')
            return None
        elif comp.confirm:
            print(f'Results for {comp_name} have already been finalized!')
            return None
        elif mod not in comp.moderators:
            print(f'{mod_name} is not authorized to add results for {comp_name}!')
            return None
        else:
            results = {}
            for team in teams:
                comp_team = CompetitionTeam.query.filter_by(comp_id=comp.id, team_id=team.id).first()

                if comp_team:
                    comp_team.points_earned = score
                    comp_team.rating_score = (score / comp.max_score) * 20 * comp.level
                    results[team.name] = score
                    try:
                        db.session.add(comp_team)
                        db.session.commit()
                        print(f'Score successfully added for {team_name}!')

                    except Exception as e:
                        db.session.rollback()
                        print("Something went wrong!")
                        return None
            comp.add_results(results)
            return results
    return None
