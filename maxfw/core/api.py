from .app import MAX_API
from flask import abort
from flask_restplus import Resource, fields

from utils.image_utils import ImageProcessor

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


def redirect_errors_to_flask(func):
    """
    This decorator function will capture all Pythonic errors and return them as flask errors.

    If you are looking to disable this functionality, please remove this decorator from the `apply_transforms()` module
    under the ImageProcessor class.
    """

    def inner(*args, **kwargs):
        try:
            # run the function
            return func(*args, **kwargs)
        except ValueError as ve:
            if 'specific_message' in str(ve):
                raise NotImplementedError
            else:
                raise NotImplementedError
        except TypeError as te:
            raise te
            # TODO
        except Exception as e:
            # on error, return a 400 using the `abort` module in flask
            if len(str(e)) > 0:
                # if there is a specific error message, return it
                abort(400, str(e))
            else:
                # otherwise, return a generic message
                abort(400, "Something went wrong in the image processing pipeline. Please verify your image.")

    return inner


class MAXImageProcessor(ImageProcessor):
    """Composes several transforms together.

    Args:
        transforms (list of ``Transform`` objects): list of transforms to compose.

    Example:
        >>> pipeline = ImageProcessor([
        >>>     Rotate(150),
        >>>     Resize([100,100])
        >>> ])
        >>> pipeline.apply_transforms(img)
    """

    @redirect_errors_to_flask
    def apply_transforms(self, img):
        for t in self.transforms:
            img = t(img)
        return img

# class FileRequestParser(object):
#     def __init__(self):
#         self.parser = reqparse.RequestParser()
#         self.parser.add_argument('file', type=FileStorage, location='files', required=True)
