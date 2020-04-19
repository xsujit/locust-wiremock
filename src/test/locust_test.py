from locust import HttpLocust, TaskSet, task, between
import urllib3
import random
import json
import requests


class UserBehavior(TaskSet):
    id_dict = {}  # create a pool of ids from which to GET
    counter = 0

    def on_start(self):
        pass

    @staticmethod
    def on_stop():
        pass

    @task(3)
    def get_document(self):
        max_len = len(self.id_dict) if len(self.id_dict) <= 5 else 5
        random_value = random.randint(1, max_len)
        print("Len: {} | Random: {}".format(len(self.id_dict), random_value))
        doc_id = str(self.id_dict[random_value]["id"])
        url_path = "/document/" + doc_id
        print("Url: " + url_path)
        r = self.client.get(url_path, verify=False)
        assert r.status_code == 200

    @task(1)
    def create_document_task(self):
        doc_id = self.get_random()
        self.counter += 1
        new_stub = "/document/" + str(doc_id)
        stub_payload = json.dumps({"request": {"url": new_stub, "method": "GET"}, "response": {"status": 200}})
        wire_mock_url = "http://localhost:8080/__admin/mappings/new"
        r = self.client.post(wire_mock_url, data=stub_payload, headers={"content-type": "application/json"},
                             verify=False)
        assert r.status_code == 201

    def get_random(self):
        while True:
            print("Inside while")
            found = False
            doc_id = random.randint(1, 999999999)
            for x in self.id_dict.values():
                if doc_id == x["id"]:
                    found = True
                    break
            if not found:
                break
        return doc_id


class WebsiteUser(HttpLocust):
    counter = 0

    def setup(self):
        print("Setup called")
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        r = requests.delete("http://localhost:8080/__admin/mappings")
        assert r.status_code == 200
        r = requests.delete("http://localhost:8080/__admin/requests")
        assert r.status_code == 200
        for i in range(0, 500):
            doc_id = i
            sample_data = {"id": doc_id}
            self.counter += 1
            nest_data = {self.counter: sample_data}
            new_stub = "/document/" + str(doc_id)
            stub_payload = json.dumps({"request": {"url": new_stub, "method": "GET"}, "response": {"status": 200}})
            wire_mock_url = "http://localhost:8080/__admin/mappings/new"
            r = requests.post(wire_mock_url, data=stub_payload, headers={"content-type": "application/json"})
            assert r.status_code == 201
            UserBehavior.id_dict.update(nest_data)

    @staticmethod
    def teardown():
        print("Teardown  called")
        r = requests.delete("http://localhost:8080/__admin/mappings")
        assert r.status_code == 200
        r = requests.delete("http://localhost:8080/__admin/requests")
        assert r.status_code == 200

    host = "https://localhost:8443"
    task_set = UserBehavior
    wait_time = between(10.0, 10.0)
