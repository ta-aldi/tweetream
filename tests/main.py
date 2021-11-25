import gevent, math, random, time

from locust import HttpUser, TaskSet, LoadTestShape, task, events
from locust.runners import STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP, WorkerRunner
from locust_plugins.users import SocketIOUser


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


class TweetreamTaskSet(TaskSet):

    @task(1)
    def landing_page(self):
        self.client.get('/')

    @task(3)
    def subscribe_topic(self):
        host = self.user.host.split('://')[1]
        ws_url = 'ws://%s/ws?topic=%s' % (host, 'jakarta')
        self.user.connect(ws_url, [])


class TweetreamUser(HttpUser, SocketIOUser):
    tasks = [TweetreamTaskSet]
    
    def wait_time(self):
        return poissonDistSample()

    @events.init.add_listener
    def on_locust_init(environment, **_kwargs):
        def checker(environment):
            while environment.runner.state not in [STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP]:
                time.sleep(1)
                if environment.runner.stats.total.num_requests > 5000:
                    environment.runner.quit()
                    return

        if not isinstance(environment.runner, WorkerRunner):
            gevent.spawn(checker, environment)

    @events.test_start.add_listener
    def on_test_start(environment, **kwargs):
        print('Starting test')

    @events.test_stop.add_listener
    def on_test_stop(environment, **kwargs):
        print('Stopping test')


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
        {"duration": 180, "users": 100, "spawn_rate": 50},
        {"duration": 240, "users": 200, "spawn_rate": 50},
        {"duration": 300, "users": 500, "spawn_rate": 100},
        {"duration": 360, "users": 1000, "spawn_rate": 100},
        {"duration": 420, "users": 3000, "spawn_rate": 100},
        {"duration": 480, "users": 5000, "spawn_rate": 100},
        {"duration": 540, "users": 7500, "spawn_rate": 100},
        {"duration": 600, "users": 10000, "spawn_rate": 100},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None