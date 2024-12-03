import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import *
from App.controllers import *
from App.controllers.commands import *



LOGGER = logging.getLogger(__name__)
invoker = CommandInvoker()

'''
   Unit Tests
'''
class UnitTests(unittest.TestCase):
    #User Unit Tests
    def test_new_user(self):
        user = User("ryan", "ryanpass")
        assert user.username == "ryan"

    def test_hashed_password(self):
        password = "ryanpass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("ryan", password)
        assert user.password != password

    def test_check_password(self):
        password = "ryanpass"
        user = User("ryan", password)
        assert user.check_password(password)

    #Student Unit Tests
    def test_new_student(self):
      db.drop_all()
      db.create_all()
      student = Student("james", "jamespass")
      assert student.username == "james"

    def test_student_get_json(self):
      db.drop_all()
      db.create_all()
      student = Student("james", "jamespass")
      self.assertDictEqual(student.get_json(), {"id": None, "username": "james", "rating_score": 0, "comp_count": 0, "curr_rank": 0})

    #Moderator Unit Tests
    def test_new_moderator(self):
      db.drop_all()
      db.create_all()
      mod = Moderator("robert", "robertpass")
      assert mod.username == "robert"

    def test_moderator_get_json(self):
      db.drop_all()
      db.create_all()
      mod = Moderator("robert", "robertpass")
      self.assertDictEqual(mod.get_json(), {"id":None, "username": "robert", "competitions": []})
    
    #Team Unit Tests
    def test_new_team(self):
      db.drop_all()
      db.create_all()
      team = Team("Scrum Lords")
      assert team.name == "Scrum Lords"
    
    def test_team_get_json(self):
      db.drop_all()
      db.create_all()
      team = Team("Scrum Lords")
      self.assertDictEqual(team.get_json(), {"id":None, "name":"Scrum Lords", "students": []})
    
    #Competition Unit Tests
    def test_new_competition(self):
      db.drop_all()
      db.create_all()
      competition = Competition("RunTime", datetime.strptime("09-02-2024", "%d-%m-%Y"), "St. Augustine", 1, 25)
      assert competition.name == "RunTime" and competition.date.strftime("%d-%m-%Y") == "09-02-2024" and competition.location == "St. Augustine" and competition.level == 1 and competition.max_score == 25

    def test_competition_get_json(self):
      db.drop_all()
      db.create_all()
      competition = Competition("RunTime", datetime.strptime("09-02-2024", "%d-%m-%Y"), "St. Augustine", 1, 25)
      self.assertDictEqual(competition.get_json(), {"id": None, "name": "RunTime", "date": "09-02-2024", "location": "St. Augustine", "level": 1, "max_score": 25, "moderators": [], "teams": []})
    
    #Notification Unit Tests
    def test_new_notification(self):
      db.drop_all()
      db.create_all()
      notification = Notification(1, "Ranking changed!")
      assert notification.student_id == 1 and notification.message == "Ranking changed!"

    def test_notification_get_json(self):
      db.drop_all()
      db.create_all()
      notification = Notification(1, "Ranking changed!")
      self.assertDictEqual(notification.get_json(), {"id": None, "student_id": 1, "notification": "Ranking changed!"})
    """
    #Ranking Unit Tests
    def test_new_ranking(self):
      db.drop_all()
      db.create_all()
      ranking = Ranking(1)
      assert ranking.student_id == 1
  
    def test_set_points(self):
      db.drop_all()
      db.create_all()
      ranking = Ranking(1)
      ranking.set_points(15)
      assert ranking.total_points == 15

    def test_set_ranking(self):
      db.drop_all()
      db.create_all()
      ranking = Ranking(1)
      ranking.set_ranking(1)
      assert ranking.curr_ranking == 1

    def test_previous_ranking(self):
      db.drop_all()
      db.create_all()
      ranking = Ranking(1)
      ranking.set_previous_ranking(1)
      assert ranking.prev_ranking == 1

    def test_ranking_get_json(self):
      db.drop_all()
      db.create_all()
      ranking = Ranking(1)
      ranking.set_points(15)
      ranking.set_ranking(1)
      self.assertDictEqual(ranking.get_json(), {"rank":1, "total points": 15})
    """
    #CompetitionTeam Unit Tests
    def test_new_competition_team(self):
      db.drop_all()
      db.create_all()
      competition_team = CompetitionTeam(1, 1)
      assert competition_team.comp_id == 1 and competition_team.team_id == 1

    def test_competition_team_update_points(self):
      db.drop_all()
      db.create_all()
      competition_team = CompetitionTeam(1, 1)
      competition_team.update_points(15)
      assert competition_team.points_earned == 15

    def test_competition_team_update_rating(self):
      db.drop_all()
      db.create_all()
      competition_team = CompetitionTeam(1, 1)
      competition_team.update_rating(12)
      assert competition_team.rating_score == 12

    def test_competition_team_get_json(self):
      db.drop_all()
      db.create_all()
      competition_team = CompetitionTeam(1, 1)
      competition_team.update_points(15)
      competition_team.update_rating(12)
      self.assertDictEqual(competition_team.get_json(), {"id": None, "team_id": 1, "competition_id": 1, "points_earned": 15, "rating_score": 12})

    #CompetitionModerator Unit Tests
    def test_new_competition_moderator(self):
      db.drop_all()
      db.create_all()
      competition_moderator = CompetitionModerator(1, 1)
      assert competition_moderator.comp_id == 1 and competition_moderator.mod_id == 1

    def test_competition_moderator_get_json(self):
      db.drop_all()
      db.create_all()
      competition_moderator = CompetitionModerator(1, 1)
      self.assertDictEqual(competition_moderator.get_json(), {"id": None, "competition_id": 1, "moderator_id": 1})

    #StudentTeam Unit Tests
    def test_new_student_team(self):
      db.drop_all()
      db.create_all()
      student_team = StudentTeam(1, 1)
      assert student_team.student_id == 1 and student_team.team_id == 1
    
    def test_student_team_get_json(self):
      db.drop_all()
      db.create_all()
      student_team = StudentTeam(1, 1)
      self.assertDictEqual(student_team.get_json(), {"id": None, "student_id": 1, "team_id": 1})

'''
    Integration Tests
'''
class IntegrationTests(unittest.TestCase):
    
    #Feature 1 Integration Tests
    def test1_create_competition(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      invoker.set_on_start(AddCompetition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25))
      invoker.execute_command()
      comp = db.session.query(Competition).filter_by(name="RunTime").first()
      assert comp is not None
      assert comp.name == "RunTime" and comp.date.strftime("%d-%m-%Y") == "29-03-2024" and comp.location == "St. Augustine" and comp.level == 2 and comp.max_score == 25

    def test2_create_competition(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      invoker.set_on_start(AddCompetition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25))
      invoker.execute_command()
      comp = db.session.query(Competition).filter_by(name="RunTime").first()
      assert comp is not None
      self.assertDictEqual(comp.get_json(), {"id": 1, "name": "RunTime", "date": "29-03-2024", "location": "St. Augustine", "level": 2, "max_score": 25, "moderators": ["debra"], "teams": []})
      
    #Feature 2 Integration Tests
    def test1_add_results(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")

      invoker.set_on_start(AddCompetition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25))
      invoker.execute_command()
      comp = db.session.query(Competition).filter_by(name="RunTime").first()

      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      students = [student1.username, student2.username, student3.username]
      
      invoker.set_on_start(AddResults(mod.username, comp.name, "Runtime Terrors", students, 15))
      invoker.execute_command()
      comp_team = db.session.query(Team).filter_by(name="Runtime Terrors").first()
      comp_team = db.session.query(CompetitionTeam).filter_by(id=comp_team.id).first()
      assert comp_team is not None
      assert comp_team.points_earned == 15
    
    def test2_add_results(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      student4 = create_student("mark", "markpass")
      student5 = create_student("eric", "ericpass")
      students = [student1.username, student2.username, student3.username, student4.username, student5.username]

      invoker.set_on_start(AddCompetition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25))
      invoker.execute_command()
#     print(get_all_competitions())
      comp = db.session.query(Competition).filter_by(name="RunTime").first()
      invoker.set_on_start(AddResults(mod.username, comp.name, "Runtime Terrors", students, 15))
      invoker.execute_command()
      assert team is not None
    
    def test3_add_results(self):
      db.drop_all()
      db.create_all()
      mod1 = create_moderator("debra", "debrapass")
      mod2 = create_moderator("robert", "robertpass")

      invoker.set_on_start(AddCompetition(mod1.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25))
      invoker.execute_command()
      comp = db.session.query(Competition).filter_by(name='RunTime').first()

      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      students = [student1.username, student2.username, student3.username]

      invoker.set_on_start(AddResults(mod2.username, comp.name, "Runtime Terrors", students, 15))
      invoker.execute_command()
      team = db.session.query(Team).filter_by(name="Runtime Terrors").first()
      assert team == None

    #Feature 3 Integration Tests
    def test_display_student_info(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      invoker.set_on_start(AddCompetition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25))
      invoker.execute_command()
      comp = db.session.query(Competition).filter_by(name="RunTime").first()
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      students = [student1.username, student2.username, student3.username]
      invoker.set_on_start(AddResults(mod.username, comp.name, "Runtime Terrors", students, 15))
      invoker.execute_command()
      team = db.session.query(Team).filter_by(name="Runtime Terrors").first()
      invoker.set_on_start(UpdateRating(comp.name))
      invoker.set_on_finish(UpdateRank())
      invoker.execute_command()
#     update_ratings(mod.username, comp.name)
#     update_rankings()
      data = display_student_info('james')
      assert data['profile']['id'] == 1
      assert data['profile']['username'] == 'james'
 
    #Feature 4 Integration Tests
    def test_display_competition(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      invoker.set_on_start(AddCompetition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25))
      invoker.execute_command()
      comp = db.session.query(Competition).filter_by(name="RunTime").first()
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      student4 = create_student("mark", "markpass")
      student5 = create_student("eric", "ericpass")
      student6 = create_student("ryan", "ryanpass")
      student7 = create_student("isabella", "isabellapass")
      student8 = create_student("richard", "richardpass")
      student9 = create_student("jessica", "jessicapass")
      students1 = [student1.username, student2.username, student3.username]
      students2 = [student4.username, student5.username, student6.username]
      students3 = [student7.username, student8.username, student9.username]

      invoker.set_on_start(AddResults(mod.username, comp.name, "Runtime Terrors", students1, 15))
      invoker.execute_command()

      invoker.set_on_start(AddResults(mod.username, comp.name, "Scrum Lords", students2, 12))
      invoker.execute_command()

      invoker.set_on_start(AddResults(mod.username, comp.name, "Beyond Infinity", students3, 10))
      invoker.execute_command()

      invoker.set_on_start(UpdateRating(comp.name))
      invoker.set_on_finish(UpdateRank())
      invoker.execute_command()
      self.assertDictEqual(comp.get_json(), {'id': 1, 'name': 'RunTime', 'date': '29-03-2024', 'location': 'St. Augustine', 'level': 2, 'max_score': 25, 'moderators': ['debra'], 'teams': ['Runtime Terrors', 'Scrum Lords', 'Beyond Infinity']})

    #Feature 5 Integration Tests
    def test_display_rankings(self):
      self.maxDiff = None
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      invoker.set_on_start(AddCompetition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25))
      invoker.execute_command()
      comp = db.session.query(Competition).filter_by(name="RunTime").first()
      comp = Competition.query.filter_by(name="RunTime").first()
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      student4 = create_student("mark", "markpass")
      student5 = create_student("eric", "ericpass")
      student6 = create_student("ryan", "ryanpass")

      invoker.set_on_start(AddResults(mod.username, comp.name, "Runtime Terror", [student1.username], 30))
      invoker.execute_command()
      
      invoker.set_on_start(AddResults(mod.username, comp.name, "Scrum Lords", [student2.username], 25))
      invoker.execute_command()

      invoker.set_on_start(AddResults(mod.username, comp.name, "Node Ninja", [student3.username], 20))
      invoker.execute_command()

      invoker.set_on_start(AddResults(mod.username, comp.name, "Python Police", [student4.username], 15))
      invoker.execute_command()

      invoker.set_on_start(AddResults(mod.username, comp.name, "C Samurai", [student5.username], 10))
      invoker.execute_command()

      invoker.set_on_start(AddResults(mod.username, comp.name, "Java Jumby", [student6.username], 5))
      invoker.execute_command()

      invoker.set_on_start(UpdateRating(comp.name))
      invoker.set_on_finish(UpdateRank())
      invoker.execute_command()

      data = display_rankings()

      assert data[0]['placement'] == 1
      assert data[0]['student'] == 'james'
      assert data[1]['placement'] == 2
      assert data[1]['student'] == 'steven'
      assert data[2]['placement'] == 3
      assert data[2]['student'] == 'emily'
      assert data[3]['placement'] == 4
      assert data[3]['student'] == 'mark'
      assert data[4]['placement'] == 5
      assert data[4]['student'] == 'eric'
      assert data[5]['placement'] == 6
      assert data[5]['student'] == 'ryan'

    #Feature 6 Integration Tests
    def test1_display_notification(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")
      invoker.set_on_start(AddCompetition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25))
      invoker.execute_command()
      comp = Competition.query.filter_by(name="RunTime").first()
      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      student4 = create_student("mark", "markpass")
      student5 = create_student("eric", "ericpass")
      student6 = create_student("ryan", "ryanpass")

      target_student = [student1.username]
      students1 = [student2.username, student3.username]
      students2 = [student4.username, student5.username, student6.username]

      invoker.set_on_start(AddResults(mod.username, comp.name, "Target Student", target_student, 30))
      invoker.execute_command()

      invoker.set_on_start(AddResults(mod.username, comp.name, "Runtime Terrors", students1, 15))
      invoker.execute_command()

      invoker.set_on_start(AddResults(mod.username, comp.name, "Scrum Lords", students2, 10))
      invoker.execute_command()

      invoker.set_on_start(UpdateRating(comp.name))
      invoker.set_on_finish(UpdateRank())
      invoker.execute_command()
      self.assertDictEqual(display_notifications("james"), {"notifications": [{"ID": 1, "Notification": "RANK : 1. Congratulations on your first rank!"}]})

    def test2_display_notification(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")

      invoker.set_on_start(AddCompetition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25))
      invoker.set_on_finish(AddCompetition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 30))
      invoker.execute_command()

      comp1 = db.session.query(Competition).filter_by(name="RunTime").first()
      comp2 = db.session.query(Competition).filter_by(name="Hacker Cup").first()

      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      student4 = create_student("mark", "markpass")
      student5 = create_student("eric", "ericpass")
      student6 = create_student("ryan", "ryanpass")

      students1 = [student1.username, student2.username, student3.username]
      students2 = [student4.username, student5.username, student6.username]

      invoker.set_on_start(AddResults(mod.username, comp1.name, "Runtime Terrors", students1, 15))
      invoker.execute_command()

      invoker.set_on_start(AddResults(mod.username, comp1.name, "Scrum Lords", students2, 10))
      invoker.execute_command()

      invoker.set_on_start(UpdateRating(comp1.name))
      invoker.set_on_finish(UpdateRank())
      invoker.execute_command()

      students3 = [student1.username, student4.username, student5.username]
      students4 = [student2.username, student3.username, student6.username]

      invoker.set_on_start(AddResults(mod.username, comp2.name, "Runtime Terrors", students3, 15))
      invoker.execute_command()

      invoker.set_on_start(AddResults(mod.username, comp2.name, "Scrum Lords", students4, 10))
      invoker.execute_command()

      invoker.set_on_start(UpdateRating(comp2.name))
      invoker.set_on_finish(UpdateRank())
      invoker.execute_command()

      data=display_notifications("james")
      assert data['notifications'][0]['Notification'] == 'RANK : 1. Congratulations on your first rank!'
      assert data['notifications'][1]['Notification'] == 'RANK : 1. Well done! You retained your rank.'


    def test3_display_notification(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")

      invoker.set_on_start(AddCompetition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25))
      invoker.set_on_finish(AddCompetition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 20))
      invoker.execute_command()

      comp1 = db.session.query(Competition).filter_by(name="RunTime").first()
      comp2 = db.session.query(Competition).filter_by(name="Hacker Cup").first()

      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      student4 = create_student("mark", "markpass")
      student5 = create_student("eric", "ericpass")
      student6 = create_student("ryan", "ryanpass")
      students1 = [student1.username, student2.username, student3.username]
      students2 = [student4.username, student5.username, student6.username]
      students3 = [student1.username, student4.username, student5.username]
      students4 = [student2.username, student3.username, student6.username]

      invoker.set_on_start(AddResults(mod.username, comp1.name, "Runtime Terrors", students1, 15))
      invoker.execute_command()

      invoker.set_on_start(AddResults(mod.username, comp1.name, "Scrum Lords", students2, 10))
      invoker.execute_command()

      invoker.set_on_start(UpdateRating(comp1.name))
      invoker.set_on_finish(UpdateRank())
      invoker.execute_command()

      invoker.set_on_start(AddResults(mod.username, comp2.name, "Runtime Terrors", students3, 20))
      invoker.execute_command()

      invoker.set_on_start(AddResults(mod.username, comp2.name, "Scrum Lords", students4, 10))
      invoker.execute_command()

      invoker.set_on_start(UpdateRating(comp2.name))
      invoker.set_on_finish(UpdateRank())
      invoker.execute_command()
      data=display_notifications("steven")
      assert len(data) == 1
      assert data['notifications'][0]['Notification'] == 'RANK : 2. Congratulations on your first rank!'



    def test4_display_notification(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")

      invoker.set_on_start(AddCompetition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25))
      invoker.set_on_finish(AddCompetition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 20))
      invoker.execute_command()

      comp1 = db.session.query(Competition).filter_by(name="RunTime").first()
      comp2 = db.session.query(Competition).filter_by(name="Hacker Cup").first()

      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      student4 = create_student("mark", "markpass")
      student5 = create_student("eric", "ericpass")
      student6 = create_student("ryan", "ryanpass")

      students1 = [student1.username, student2.username, student3.username]
      students2 = [student4.username, student5.username, student6.username]
      students3 = [student1.username, student4.username, student5.username]
      students4 = [student2.username, student3.username, student6.username]

      invoker.set_on_start(AddResults(mod.username, comp1.name, "Runtime Terrors", students1, 15))
      invoker.execute_command()

      invoker.set_on_start(AddResults(mod.username, comp1.name, "Scrum Lords", students2, 10))
      invoker.execute_command()

      invoker.set_on_start(UpdateRating(comp1.name))
      invoker.set_on_finish(UpdateRank())
      invoker.execute_command()

      invoker.set_on_start(AddResults(mod.username, comp2.name, "Runtime Terrors", students3, 20))
      invoker.execute_command()

      invoker.set_on_start(AddResults(mod.username, comp2.name, "Scrum Lords", students4, 10))
      invoker.execute_command()
      
      invoker.set_on_start(UpdateRating(comp2.name))
      invoker.set_on_finish(UpdateRank())
      invoker.execute_command()

      data=display_notifications("mark")
      assert len(data) is 1
      assert data['notifications'][0]['Notification'] == 'RANK : 4. Congratulations on your first rank!'
      assert data['notifications'][1]['Notification'] == 'RANK : 2. Congratulations! Your rank has went up.'


    #Additional Integration Tests
    def test1_add_mod(self):
      db.drop_all()
      db.create_all()
      mod1 = create_moderator("debra", "debrapass")
      mod2 = create_moderator("robert", "robertpass")

      invoker.set_on_start(AddCompetition(mod1.username,"RunTime", "29-03-2024", "St. Augustine", 2, 25))
      invoker.execute_command()

      comp = db.session.query(Competition).filter_by(name="RunTime").first()
      assert add_mod(mod1.username, comp.name, mod2.username) != None
       
    def test2_add_mod(self):
      db.drop_all()
      db.create_all()
      mod1 = create_moderator("debra", "debrapass")
      mod2 = create_moderator("robert", "robertpass")
      mod3 = create_moderator("raymond", "raymondpass")

      invoker.set_on_start(AddCompetition(mod1.username,"RunTime", "29-03-2024", "St. Augustine", 2, 25))
      invoker.execute_command()

      comp = db.session.query(Competition).filter_by(name="RunTime").first()

      assert add_mod(mod2.username, comp.name, mod3.username) == None
    
    def test_student_list(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")

      invoker.set_on_start(AddCompetition(mod.username,"RunTime", "29-03-2024", "St. Augustine", 2, 25))
      invoker.execute_command()

      comp1 = db.session.query(Competition).filter_by(name="RunTime").first()

      invoker.set_on_start(AddCompetition(mod.username,"Hacker Cup", "23-02-2024", "Macoya", 1, 20))
      invoker.execute_command()

      comp2 = db.session.query(Competition).filter_by(name="Hacker Cup").first()

      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      student4 = create_student("mark", "markpass")
      student5 = create_student("eric", "ericpass")
      student6 = create_student("ryan", "ryanpass")
      students1 = [student1.username, student2.username, student3.username]
      students2 = [student4.username, student5.username, student6.username]
      students3 = [student1.username, student4.username, student5.username]
      students4 = [student2.username, student3.username, student6.username]

      invoker.set_on_start(AddResults(mod.username, comp1.name, "Runtime Terrors", students1, 15))
      invoker.execute_command()

      invoker.set_on_start(AddResults(mod.username, comp1.name, "Scrum Lords", students2, 10))
      invoker.execute_command()
      
      invoker.set_on_start(UpdateRating(comp1.name))
      invoker.set_on_finish(UpdateRank())
      invoker.execute_command()

      invoker.set_on_start(AddResults(mod.username, comp2.name, "Runtime Terrors", students3, 20))
      invoker.execute_command()

      invoker.set_on_start(AddResults(mod.username, comp2.name, "Scrum Lords", students4, 10))
      invoker.execute_command()
      
      invoker.set_on_start(UpdateRating(comp2.name))
      invoker.set_on_finish(UpdateRank())
      invoker.execute_command()

      data = get_all_students_json()
      assert data[0]['id'] == 1
      assert data[0]['username'] == 'james'
      assert data[0]['rating_score'] == 22.0
      assert data[1]['id'] == 2
      assert data[1]['username'] == 'steven'
      assert data[1]['rating_score'] == 17.0
      assert data[2]['id'] == 3
      assert data[2]['username'] == 'emily'
      assert data[2]['rating_score'] == 17.0
      assert data[3]['id'] == 4
      assert data[3]['username'] == 'mark'
      assert data[3]['rating_score'] == 18.0
      assert data[4]['id'] == 5
      assert data[4]['username'] == 'eric'
      assert data[4]['rating_score'] == 18.0
      assert data[5]['id'] == 6
      assert data[5]['username'] == 'ryan'
      assert data[5]['rating_score'] == 13.0

    def test_comp_list(self):
      db.drop_all()
      db.create_all()
      mod = create_moderator("debra", "debrapass")

      invoker.set_on_start(AddCompetition(mod.username,"RunTime", "29-03-2024", "St. Augustine", 2, 25))
      invoker.execute_command()

      comp1 = db.session.query(Competition).filter_by(name="RunTime").first()

      invoker.set_on_start(AddCompetition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 20))
      invoker.execute_command()

      comp2 = db.session.query(Competition).filter_by(name="Hacker Cup").first()

      student1 = create_student("james", "jamespass")
      student2 = create_student("steven", "stevenpass")
      student3 = create_student("emily", "emilypass")
      student4 = create_student("mark", "markpass")
      student5 = create_student("eric", "ericpass")
      student6 = create_student("ryan", "ryanpass")

      students1 = [student1.username, student2.username, student3.username]
      students2 = [student4.username, student5.username, student6.username]
      students3 = [student1.username, student4.username, student5.username]
      students4 = [student2.username, student3.username, student6.username]

      invoker.set_on_start(AddResults(mod.username, comp1.name, "Runtime Terrors", students1, 15))
      invoker.execute_command()

      invoker.set_on_start(AddResults(mod.username, comp1.name, "Scrum Lords", students2, 10))
      invoker.execute_command()

      invoker.set_on_start(UpdateRating(comp1.name))
      invoker.set_on_finish(UpdateRank())
      invoker.execute_command()

      invoker.set_on_start(AddResults(mod.username, comp2.name, "Runtime Terrors", students3, 20))
      invoker.execute_command()     

      invoker.set_on_start(AddResults(mod.username, comp2.name, "Scrum Lords", students4, 10))
      invoker.execute_command()

      invoker.set_on_start(UpdateRating(comp2.name))
      invoker.set_on_finish(UpdateRank())
      invoker.execute_command()

      self.assertListEqual(get_all_competitions_json(), [{"id": 1, "name": "RunTime", "date": "29-03-2024", "location": "St. Augustine", "level": 2, "max_score": 25, "moderators": ["debra"], "teams": ["Runtime Terrors", "Scrum Lords"]}, {"id": 2, "name": "Hacker Cup", "date": "23-02-2024", "location": "Macoya", "level": 1, "max_score": 20, "moderators": ["debra"], "teams": ["Runtime Terrors", "Scrum Lords"]}])