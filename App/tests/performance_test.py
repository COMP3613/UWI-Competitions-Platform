'''
import time
import random
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def leaderboard_page(self):
        self.client.get(url="/leaderboard")
    
    @task
    def student_profile_page(self):
        student_id = random.randint(1, 30)
        self.client.get(url=f"/student_profile/{student_id}")
    
    @task
    def moderator_profile_page(self):
        moderator_id = random.randint(1, 5)
        self.client.get(url=f"/moderator_profile/{moderator_id}")
    
    @task
    def competitions_page(self):
        self.client.get(url="/competitions")
    
    @task
    def competition_details_page(self):
        competition_id = random.randint(1, 6)
        self.client.get(url=f"/competitions/{competition_id}")

'''