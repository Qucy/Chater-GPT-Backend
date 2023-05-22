import time
from locust import HttpUser, task, between


class ChatAPITest(HttpUser):

    wait_time = between(1, 2)

    @task
    def get(self):
        self.client.post("/chat")

    # @task
    # def post(self):
    #     self.client.post("/api/v1/chat/", {
    #         "message": "Hello World!"
    #     })