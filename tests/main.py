import gevent, math, random, time

from locust import HttpUser, task, events
from locust.runners import STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP, WorkerRunner


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


class TweetreamUser(HttpUser):
    
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

    @task
    def landing_page(self):
        self.client.get('/')
