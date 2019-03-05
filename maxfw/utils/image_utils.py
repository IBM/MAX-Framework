# standard lib
import io

# other dependencies
from flask import abort
from PIL import Image


class ImagePreprocessor:
    '''A Pillow-based image preprocessing tool adapted for MAX APIs.'''

    def __init__(self, keep_alpha_channel, grayscale=False, normalize=False, standardize=False):
        '''
        :param grayscale: Convert the image to grayscale. This reduces the number of channels to one.
        :param normalize: Scale the pixel values to interval [0, 1].
        :param standardize: Scale the pixel values to interval [-1, 1].
        :param keep_alpha_channel:
        '''
        self.grayscale = grayscale
        self.normalize = normalize
        self.standardize = standardize
        assert self.standardize in [True, False]
        assert self.normalize in [True, False]
        assert int(normalize) + int(standardize) < 2, "Setting both normalize and stardize to True is not possible."
        self.keep_alpha_channel = keep_alpha_channel

    def preprocess_imagedata(self, image_data):
        '''
        Read the image from a bytestream.
        If the PIL.Image module is unable to process the stream, a Flask error with status code 400 will be raised.

        Input: Image bytes.
        Returns: Numpy array.
        '''
        try:
            im = Image.open(io.BytesIO(image_data))
        except:
            abort(400, "The provided input is not a valid image. Make sure that the bytestream of an image is passed as input.")

        # send the image through the pipeline
        if self.grayscale:
            pass

        # return numpy array
        return im


class ImagePostprocessor:
    '''A Pillow-based image postprocessing tool adapted for MAX APIs.'''

    def __init__(self, denormalize):
        self.denormalize = denormalize

    def image_to_bytestream(self):
        '''
        input: the output image produced by the model
        :return:
        '''
        return
