import os
import redis
from werkzeug.urls import url_parse
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader

home_path = "/home/lensee-1/"

class LowLevel(object):
    def __init__(self, config):
        self.redis = redis.Redis(
            config['redis_host'], config['redis_port'], decode_responses=True
        )
        # This is our routing for the lowlevel api
        self.url_map = Map(
            [
                Rule("/<read_simulator>", endpoint="read_simulator"),
                Rule("/<write_simulator>", endpoint="write_simulator"),
            ]
        )

    # Reads from the simulator file
    def on_read_simulator(self, request):
        f = open(home_path + "/.simulator_save", 'r')
        val = f.read().split('\n')[-2]
        return Response(val)

    # Writes to the simulator config file 
    def on_write_simulator(self, request):
        time = request.args.get('time')
        f = open(home_path + "/.simulator_conf", 'w')
        f.write(str(time))
        f.close()
        return Response(200)

    # This makes sure the routing calls the correct method
    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, 'on_' + values['read_simulator'])(request)
        except HTTPException as e:
            return e

    # This is the process that constantly runs
    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

# This can be localhost and a random port since this will only be called here
def create_app(redis_host='localhost', redis_port=6379, with_static=True):
    app = LowLevel({
        'redis_host': redis_host,
        'redis_port': redis_port
    })
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static': os.path.join(os.path.dirname(__file__), 'static')
        })
    return app

# Starts the process
if __name__ == '__main__':
    from werkzeug.serving import run_simple

    app = create_app()
    run_simple('172.30.103.27', 5000, app, use_debugger=True, use_reloader=True)
