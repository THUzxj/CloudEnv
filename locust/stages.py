from locust import HttpUser, TaskSet, task, constant
from locust import LoadTestShape
import base64
from random import choice


class UserTasks(TaskSet):
    @task(5)
    def get_root(self):
        self.client.get("/")

    @task(10)
    def buy(self):
        base64string = base64.encodebytes(
            ('%s:%s' % ('user', 'password')).encode()).decode().strip()
        catalogue = self.client.get("/catalogue").json()
        category_item = choice(catalogue)
        item_id = category_item["id"]

        self.client.get("/")
        self.client.get(
            "/login", headers={"Authorization": "Basic %s" % base64string})
        self.client.get("/category.html")
        self.client.get("/detail.html?id={}".format(item_id))
        self.client.delete("/cart")
        self.client.post("/cart", json={"id": item_id, "quantity": 1})
        self.client.get("/basket.html")
        self.client.post("/orders")


class WebsiteUser(HttpUser):
    wait_time = constant(0.5)
    tasks = [UserTasks]


class StagesShape(LoadTestShape):
    """
    A simply load test shape class that has different user and spawn_rate at
    different stages.

    Keyword arguments:

        stages -- A list of dicts, each representing a stage with the following keys:
            duration -- When this many seconds pass the test is advanced to the next stage
            users -- Total user count
            spawn_rate -- Number of users to start/stop per second
            stop -- A boolean that can stop that test at a specific stage

        stop_at_end -- Can be set to stop once all stages have run.
    """

    def __init__(self):
        super(StagesShape, self).__init__()
        self.basic_users = 10

        self.stages = [
            {"duration": 600, "users": 10 * self.basic_users, "spawn_rate": 10},
            {"duration": 1000, "users": 50 * self.basic_users, "spawn_rate": 10},
            {"duration": 1800, "users": 100 * self.basic_users, "spawn_rate": 10},
            {"duration": 2200, "users": 30 * self.basic_users, "spawn_rate": 10},
            {"duration": 2300, "users": 10 * self.basic_users, "spawn_rate": 10},
            {"duration": 2400, "users": 1 * self.basic_users, "spawn_rate": 1},
        ]
        self.whole_time = sum([stage["duration"] for stage in self.stages])

    def tick(self):
        run_time = self.get_run_time()
        run_time = run_time % self.whole_time

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
