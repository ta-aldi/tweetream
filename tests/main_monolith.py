from locust import HttpUser, TaskSet, LoadTestShape, task

import socketio, math, random, time


def poissonDistSample():
    mean = 5
    L = math.exp(-mean)
    k = 0
    p = 1.0
    
    # do while
    p *= random.random()
    k += 1

    while (p > L):
        p *= random.random()
        k += 1

    return k-1


class TweetreamMonolithTaskSet(TaskSet):

    @task(1)
    def landing_page(self):
        self.client.get('/')

    @task(3)
    def subscribe_topic(self):
        sio = socketio.Client()
        host = self.user.host.split('://')[1]
        ws_url = 'http://%s/socket.io/?topic=%s' % (host, 'jakarta')
        sio.connect(ws_url, transports="polling", namespaces=['/topic'])
    #     self.ws = sio

    # def on_quit(self):
    #     self.ws.disconnect()


class WebsiteUser(HttpUser):
    tasks = [TweetreamMonolithTaskSet]
    
    def wait_time(self):
        return poissonDistSample()


class TweetreamShape(LoadTestShape):
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

    stages = [
        {"duration": 60, "users": 10, "spawn_rate": 10},
        {"duration": 120, "users": 50, "spawn_rate": 10},
        {"duration": 240, "users": 100, "spawn_rate": 10},
        {"duration": 480, "users": 250, "spawn_rate": 10},
        {"duration": 720, "users": 500, "spawn_rate": 10},
        {"duration": 840, "users": 1000, "spawn_rate": 10},
        # {"duration": 960, "users": 100, "spawn_rate": 10},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None