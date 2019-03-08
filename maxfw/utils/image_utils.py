# standard lib
import io

# other dependencies
from flask import abort
from PIL import Image
import numpy as np


class ImagePreprocessor:
    '''A Pillow-based image preprocessing tool adapted for MAX APIs.'''

    def __init__(self, remove_alpha_channel=False, grayscale=False, normalize=False, standardize=False, rotate_angle=None, resize_shape=None):
        '''
        :param grayscale:   Boolean - Convert an RGB image to grayscale. This reduces the number of channels to one.
        :param normalize:   Boolean - Scale the pixel values to interval [0, 1].
        :param standardize: Boolean -  Scale the pixel values to interval [-1, 1].
        :param remove_alpha_channel: Boolean - Removes the alpha channel and converts image to RGB.
        :param rotate_angle: float - Degrees counterclockwise to rotate.
        :param resize_shape: tuple - The requested size in pixels, as a 2-tuple: (width, height).
        '''
        self.grayscale = grayscale
        self.normalize = normalize
        self.standardize = standardize
        self.remove_alpha_channel = remove_alpha_channel
        self.rotate_angle = rotate_angle
        self.resize_shape = resize_shape

        # Param sanity check
        assert self.standardize in [True, False]
        assert self.normalize in [True, False]
        assert self.remove_alpha_channel in [True, False]
        assert int(normalize) + int(standardize) < 2, "Setting both normalize and stardize to True is not possible."
        
        # Configure image mode, mapping user params to PIL modes.
        self._image_mode = None
        if self.grayscale:
            self._image_mode = 'L'
        elif self.remove_alpha_channel:
            self._image_mode = 'RGB'

    def preprocess_imagedata(self, image_data):
        '''
        Read the image from a bytestream, and apply all necessary transofrmations.
        If the PIL.Image module is unable to process the stream, a Flask error with status code 400 will be raised.

        Input: Image bytes.
        Returns: Numpy array.
        '''
        try:
            im = Image.open(io.BytesIO(image_data)).convert(self._image_mode)
            
        except:
            abort(400, "The provided input is not a valid image. Make sure that the bytestream of an image is passed as input.")

        if self.rotate_angle:
            im = im.rotate(self.rotate_angle)
        
        if self.resize_shape:
            im = im.resize(self.resize_shape)
        
        im = np.array(im)
        if self.normalize:
            im = im / np.linalg.norm(im)
        # return numpy array
        return im

class ImagePostprocessor:
    '''A Pillow-based image postprocessing tool adapted for MAX APIs.'''

    def __init__(self, denormalize):
        self.denormalize = denormalize

    def image_to_bytestream(self, image):
        '''
        input: the output image produced by the model
        :return:
        '''
        stream = io.BytesIO()
        image.save(stream)
        return stream.seek(0)
