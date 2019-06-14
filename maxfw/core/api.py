from .app import MAX_API
from flask_restplus import Resource, fields

METADATA_SCHEMA = MAX_API.model('ModelMetadata', {
        'id': fields.String(required=True, description='Model identifier'),
        'name': fields.String(required=True, description='Model name'),
        'description': fields.String(required=True, description='Model description'),
        'type': fields.String(required=True, description='Model type'),
        'source': fields.String(required=True, description='Model source'),
        'license': fields.String(required=False, description='Model license')
    })


class MAXAPI(Resource):
    pass


class MetadataAPI(MAXAPI):

    def get(self):
        """To be implemented"""
        raise NotImplementedError()


class PredictAPI(MAXAPI):

    def post(self):
        """To be implemented"""
        raise NotImplementedError()


class CustomMAXAPI(MAXAPI):
    pass

# class FileRequestParser(object):
#     def __init__(self):
#         self.parser = reqparse.RequestParser()
#         self.parser.add_argument('file', type=FileStorage, location='files', required=True)
