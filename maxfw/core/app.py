import os
import logging
from flask import Flask, Response
from flask_restplus import Api, Namespace, Resource, fields
from flask_cors import CORS
from .default_config import API_TITLE, API_DESC, API_VERSION

MAX_API = Namespace('model', description='Model information and inference operations')

class MAXApp(object):

    def __init__(self, title=API_TITLE, desc=API_DESC, version=API_VERSION):
        self.app = Flask(title)

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
        if os.getenv('CORS_ENABLE') == 'true' and \
        os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            CORS(self.app, origins='*')
            self.app.logger.info(
            'NOTE: MAX Model Server is currently allowing ' + \
            'cross-origin requests - (CORS ENABLED)')

    def add_api(self, api, route):
        MAX_API.add_resource(api, route)

    def run(self, host='0.0.0.0'):
        self.app.run(host)
