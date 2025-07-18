from locust import HttpUser, task, between

class CloudUser(HttpUser):
    host = "https://flask-api-<REGION>-<YOUR_PROJECT>.run.app"
    wait_time = between(1,3)

    def on_start(self):
        with self.client.post("/api/login",
                              json={"username":"user","password":"pass"},
                              catch_response=True, name="Login") as resp:
            if resp.status_code!=200:
                resp.failure(f"Login failed: {resp.status_code}")

    @task(3)
    def get_resources(self):
        self.client.get("/api/resources", name="Get Resources")

    @task(2)
    def create_resource(self):
        self.client.post("/api/resources",
                         json={"name":"test_resource","type":"compute"},
                         name="Create Resource")

    @task(1)
    def scale_resource(self):
        self.client.post("/api/resources/1/scale",
                         json={"size":"large"},
                         name="Scale Resource")
