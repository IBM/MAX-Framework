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
            if 'channel' in str(ve):
                abort(400, "Invalid input, please ensure the input has right number of channels.")
            elif 'mode' in str(ve):
                abort(400, "Invalid input, please ensure the right mode is used with the given channels.")
            else:
                abort(400, str(ve))
        except TypeError as te:
            abort(400, "Invalid input." + str(te))
        except Exception as e:
            # on error, return a 400 using the `abort` module in flask
            if len(str(e)) > 0:
                # if there is a specific error message, return it
                abort(400, str(e))
            else:
                # otherwise, return a generic message
                abort(400, "Undocumented input error, please verify inputs.")

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
