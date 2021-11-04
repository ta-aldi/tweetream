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
    time_limit = 600
    spawn_rate = 10

    def tick(self):
        run_time = self.get_run_time()

        if run_time < self.time_limit:
            # User count rounded to nearest hundred.
            user_count = round(run_time, -2)
            return (user_count, self.spawn_rate)

        return None