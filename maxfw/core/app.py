import os
from flask import Flask
from flask_restplus import Api, Namespace
from flask_cors import CORS
from .default_config import API_TITLE, API_DESC, API_VERSION

MAX_API = Namespace('model', description='Model information and inference operations')


class MAXApp(object):

    def __init__(self, title=API_TITLE, desc=API_DESC, version=API_VERSION):
        self.app = Flask(title, static_url_path='')

        # load config
        if os.path.exists("config.py"):
            self.app.config.from_object("config")

        self.api = Api(
            self.app,
            title=title,
            description=desc,
            version=version)

        self.api.namespaces.clear()
        self.api.add_namespace(MAX_API)

        # enable cors if flag is set
        if os.getenv('CORS_ENABLE') == 'true' and (os.environ.get('WERKZEUG_RUN_MAIN') == 'true'):
            CORS(self.app, origins='*')
            self.app.logger.info('NOTE: MAX Model Server is currently allowing cross-origin requests - (CORS ENABLED)')

    def add_api(self, api, route):
        MAX_API.add_resource(api, route)

    def mount_static(self, route):
        @self.app.route(route)
        def index():
            return self.app.send_static_file('index.html')

    def run(self, host='0.0.0.0'):
        self.app.run(host)
