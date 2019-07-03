from flask import abort
from maxfw.utils.image_utils import ImageProcessor


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
            if 'pic should be 2 or 3 dimensional' in str(ve):
                abort(400, "Invalid input dimensions, please ensure the input is a grayscale,", 
                    "RGB or RGBA image or a corresponding numpy array of 2 or 3 dimensions.")
        except TypeError as te:
            if 'bytes or ndarray' in str(te):
                abort(400, "Invalid input format, please make sure the input is an image or numpy array")
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @redirect_errors_to_flask
    def apply_transforms(self, img):
        return super().apply_transforms(img)
