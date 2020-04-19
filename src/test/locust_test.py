from locust import HttpLocust, TaskSet, task, between
import urllib3
import random
import json


class UserBehavior(TaskSet):

    id_dict = {}  # create a pool of ids from which to GET
    counter = 0

    def on_start(self):
        self.create_document()

    @staticmethod
    def on_stop():
        print("on_stop called")

    def create_document(self):  # POST new data which can be fetched later in the GET
        doc_id = self.get_random()
        sample_data = {"id": doc_id}
        self.counter += 1
        nest_data = {self.counter: sample_data}
        if self.counter <= 5:
            self.id_dict.update(nest_data)  # add to the pool
        new_stub = "/document/" + str(doc_id)
        stub_payload = json.dumps({"request": {"url": new_stub, "method": "GET"}, "response": {"status": 200}})
        wire_mock_url = "http://localhost:8080/__admin/mappings/new"
        r = self.client.post(wire_mock_url, data=stub_payload, headers={"content-type": "application/json"},
                             verify=False, name="Create Initial Document")
        assert r.status_code == 201

    @task(3)
    def get_document(self):
        random_value = random.randint(1, len(self.id_dict))
        print("Len: {} | Random: {}".format(len(self.id_dict), random_value))
        doc_id = str(self.id_dict[random_value]["id"])
        url_path = "/document/" + doc_id
        print("Url: " + url_path)
        r = self.client.get(url_path, verify=False, name="Get Document " + doc_id)
        assert r.status_code == 200

    @task(1)
    def create_document_task(self):
        doc_id = self.get_random()
        sample_data = {"id": doc_id}
        self.counter += 1
        nest_data = {self.counter: sample_data}
        if self.counter <= 5:
            self.id_dict.update(nest_data)
        new_stub = "/document/" + str(doc_id)
        stub_payload = json.dumps({"request": {"url": new_stub, "method": "GET"}, "response": {"status": 200}})
        wire_mock_url = "http://localhost:8080/__admin/mappings/new"
        r = self.client.post(wire_mock_url, data=stub_payload, headers={"content-type": "application/json"},
                             verify=False, name="Create Document")
        assert r.status_code == 201

    def get_random(self):
        while True:
            print("Inside while")
            found = False
            doc_id = random.randint(1, 100)
            for x in self.id_dict.values():
                if doc_id == x["id"]:
                    found = True
                    break
            if not found:
                break
        return doc_id


class WebsiteUser(HttpLocust):

    @staticmethod
    def setup():
        print("Setup called")
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    @staticmethod
    def teardown():
        print("Teardown  called")

    host = "https://localhost:8443"
    task_set = UserBehavior
    wait_time = between(10.0, 10.0)
