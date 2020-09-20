import json
import logging
import random
import requests
from locust import HttpUser, task, between, events, SequentialTaskSet


class UserBehavior(SequentialTaskSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.doc_id = None
        self.map_id = None

    @task
    def create_document_task(self):
        self.doc_id = random.randint(100, 999)
        new_stub = f"/document/{self.doc_id}"
        stub_payload = json.dumps({"request": {"url": new_stub, "method": "GET"}, "response": {"status": 200}})
        headers = {"content-type": "application/json"}
        r = self.client.post("/__admin/mappings", data=stub_payload, headers=headers)
        self.map_id = json.loads(r.text)["id"]
        assert r.status_code == 201

    @task
    def get_document(self):
        r = self.client.get(f"/document/{self.doc_id}", name="/document/id")
        assert r.status_code == 200

    @task
    def delete_document(self):
        r = self.client.delete(f"/__admin/mappings/{self.map_id}", name="/__admin/mappings/id")
        assert r.status_code == 200


class WebsiteUser(HttpUser):

    @staticmethod
    @events.test_start.add_listener
    def setup(environment, **kwargs):
        logging.info("Setup called")
        r = requests.delete("http://localhost:8080/__admin/mappings")
        assert r.status_code == 200
        r = requests.delete("http://localhost:8080/__admin/requests")
        assert r.status_code == 200

    @staticmethod
    @events.test_stop.add_listener
    def teardown(environment, **kwargs):
        logging.info("Teardown  called")
        r = requests.delete("http://localhost:8080/__admin/mappings")
        assert r.status_code == 200
        r = requests.delete("http://localhost:8080/__admin/requests")
        assert r.status_code == 200

    host = "http://localhost:8080"
    tasks = [UserBehavior]
    wait_time = between(1, 1)
