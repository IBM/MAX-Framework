# standard lib
import io

# other dependencies
from flask import abort
from PIL import Image
import numpy as np


class ImageProcessor:
    '''Parent / base class for the common functions in the processors.'''

    # The supported dtypes as a class variable
    dtype_map = {'single': np.float32, 'int': np.int, 'double': np.float64, 'half': np.float16,
                 'uint8': np.uint8}
    verbose = True

    def _verbose_message(self, message):
        '''
        Print message if verbose=True.
        '''
        if self.verbose:
            print(message)

    def _to_png(self, im, png_file_path):
        '''If applicable, save the numpy array to a PNG image.'''
        if png_file_path:
            self._verbose_message(f"Saving the image to PNG file '{png_file_path}'")
            # Verify the object type
            if type(im) is np.ndarray:
                Image.fromarray(im.astype(np.uint8)).save(png_file_path, 'PNG')
            elif type(im) is Image.Image:
                im.save(png_file_path, 'PNG')
            else:
                # Sanity check
                raise Exception('The image to be saved should be a numpy.ndarray or a Pillow.Image object.')

    def _to_dtype(self, im, to_dtype):
        '''If applicable, change the dtype.'''
        if to_dtype:
            im = im.astype(self.dtype_map[to_dtype])
        return im

    def _resize(self, im, resize_shape):
        '''If applicable, resize the image.'''
        # skip if resize_shape is None
        if resize_shape is None:
            return im
        # otherwise, resize to the target shape
        if type(im) is np.ndarray:
            im = Image.fromarray(im)
        self._verbose_message(f"Resizing the image from {im.size} to {resize_shape}.")
        return im.resize(resize_shape)

    def _rotate(self, im, rotate_angle):
        '''If applicable, rotate the image'''
        if rotate_angle:
            # convert np.ndarray to Pillow.Image if required
            if type(im) is np.ndarray:
                im = Image.fromarray(im)
            # rotate
            self._verbose_message(f"Rotating the image with an angle of {rotate_angle} degrees counterclockwise.")
            im = im.rotate(rotate_angle)
        return im
    
    def _normalize(self, im, normalize):
        '''If applicable, normalize the image array'''
        if type(im) is not np.ndarray:
                im = np.array(im)
        self._verbose_message(f"Normalizing the image to a [0,1] scale.")
        im = im / (np.max(im) - np.min(im))
        return im
    
    def _standardize(self, im, normalize):
        '''If applicable, normalize the image array'''
        if type(im) is not np.ndarray:
                im = np.array(im)
        self._verbose_message(f"Standardizing the image to a [-1,1] scale.")
        mean = np.mean(im)
        std = np.std(im)
        im = (im - mean) / std
        return im
    
    def _load_image_from_model_output(self, image_data):
        '''Guess the input type, and convert it to a Pillow.Image object.'''
        # load the image from the variable in the memory
        if type(image_data) is np.ndarray:
            # if the image is a np.ndarray
            im = Image.fromarray(image_data)
            self._verbose_message("Loading image from numpy.ndarray format")
        elif type(image_data) is Image.Image:
            # if the image is a Pillow image
            im = image_data
            self._verbose_message("Loading image from Pillow.Image format")
        else:
            # if the image is neither a numpy array or a Pillow image,
            # we can attempt to convert it to a numpy array or from bytes and load this with Pillow
            # otherwise, throw an error
            try:
                im = Image.fromarray(np.array(image_data))
                self._verbose_message("Loading image")
            except:
                # if it's not convertable to a numpy array, it might be bytes
                try:
                    im = Image.open(io.BytesIO(image_data))
                    self._verbose_message("Loading image from bytes")
                except:
                    raise Exception('Please supply a valid input image. Ideally, this is a numpy.ndarray.')
        return im

class ImagePreprocessor(ImageProcessor):
    '''A Pillow-based image preprocessing tool adapted for MAX APIs.'''

    def __init__(self, keep_alpha_channel=False, grayscale=False, normalize=False, standardize=False,
                 rotate_angle=None, resize_shape=None, verbose=False, to_dtype=None,
                 error_max_size=(np.Inf, np.Inf),
                 error_min_size=(0, 0), resize_max_size=(np.Inf, np.Inf), resize_min_size=(0, 0)):
        '''
        :param grayscale:   Boolean - Convert an RGB image to grayscale. This reduces the number of dimensions to 2 (H,W) instead of 3 (H,W,C).
        :param normalize:   Boolean - Scale the pixel values to interval [0, 1].
        :param standardize: Boolean -  Scale the pixel values to interval [-1, 1].
        :param keep_alpha_channel: Boolean - Removes the alpha channel and converts image to RGB.
        :param rotate_angle: float - Degrees counterclockwise to rotate.
        :param resize_shape: tuple - The requested size in pixels, as a 2-tuple: (width, height).
        :param verbose: Boolean -  set verbosity on/off.
        :param to_dtype: String - convert image to 'full', 'half', 'double', 'int' or 'uint8'.
        :param: error_max_size: Tuple(int, int) - Throw an error when the image dimensions exceed these dimensions
        :param: error_min_size: Tuple(int, int) - Throw an error when the image dimensions are lower than these dimensions
        :param: resize_max_size: Tuple(int, int) - Resize when the image dimensions are higher than these dimensions
        :param: resize_min_size: Tuple(int, int) - Resize when the image dimensions are lower than these dimensions
        '''
        self.grayscale = grayscale
        self.normalize = normalize
        self.standardize = standardize
        self.keep_alpha_channel = keep_alpha_channel
        self.rotate_angle = rotate_angle
        self.resize_shape = resize_shape
        self.verbose = verbose
        self.to_dtype = to_dtype
        self.error_max_size = error_max_size
        self.error_min_size = error_min_size
        self.resize_max_size = resize_max_size
        self.resize_min_size = resize_min_size

        # Param sanity check
        assert self.standardize in [True, False]
        assert self.normalize in [True, False]
        assert self.keep_alpha_channel in [True, False]
        assert self.verbose in [True, False]
        assert int(normalize) + int(standardize) < 2, "Setting both normalize and stardize to True is not possible."
        assert self.to_dtype in self.dtype_map or self.to_dtype is None, "The dtype should be either 'full', 'half', 'double', 'int' or 'uint8'."
        assert type(self.error_max_size) == tuple, "Please supply a tuple (int, int) for error_max_size."
        assert type(self.error_max_size[1]) == int or self.error_max_size[
            1] == np.Inf, "Please supply a tuple (int, int) for error_max_size."
        assert type(self.error_min_size) == tuple and type(
            self.error_min_size[1]) == int, "Please supply a tuple (int, int) for error_min_size."
        assert type(self.resize_max_size) == tuple, "Please supply a tuple (int, int) for resize_max_size."
        assert type(self.resize_max_size[1]) == int or self.resize_max_size[
            1] == np.Inf, "Please supply a tuple (int, int) for resize_max_size."
        assert type(self.resize_min_size) == tuple and type(
            self.resize_min_size[1]) == int, "Please supply a tuple (int, int) for resize_min_size."

        # Configure image mode, mapping user params to PIL modes.
        # The image is converted to 'RGB' unless 'grayscale' or 'keep_alpha_channel' is specified.
        self._image_mode = 'RGB'
        if self.grayscale:
            # reduces the dimensions to 2 (HW) instead of 3 (HWC)
            self._image_mode = 'L'
        elif self.keep_alpha_channel:
            self._image_mode = 'RGBA'

    def preprocess_imagedata(self, image_data, png_file_path=None):
        '''
        Read the image from a byte stream, and apply all necessary transformations.
        If the PIL.Image module is unable to process the stream, a Flask error with status code 400 will be raised.

        Input: Image bytes.
        Returns: Numpy array.
        '''
        assert type(png_file_path) in [type(None), str], "The 'to_file' argument must be set to a valid filepath."

        # Load the image into a Pillow.Image object
        try:
            self._verbose_message(f"Loading image from bytestream.")
            im = Image.open(io.BytesIO(image_data)).convert(self._image_mode)

        except:
            abort(400,
                  "The provided input is not a valid image. Make sure that the bytestream of an image is passed as input.")

        # Verify that the input image is between the dimension boundaries, otherwise throw an ERROR.
        if im.size[0] > self.error_max_size[0] or im.size[1] > self.error_max_size[1]:
            abort(400,
                  f"The dimensions of the provided image ({im.size}) are bigger than the maximum allowed dimensions ({self.error_max_size}).")

        if im.size[0] < self.error_min_size[0] or im.size[1] < self.error_min_size[1]:
            abort(400,
                  f"The dimensions of the provided image ({im.size}) are smaller than the minimum allowed dimensions ({self.error_min_size}).")

        # Verify that the input image is between the dimension boundaries, otherwise RESIZE.
        if im.size[0] > self.resize_max_size[0] or im.size[1] > self.resize_max_size[1]:
            self._verbose_message(
                f"Image exceeds maximum allowed dimensions. Resizing the image from {im.size} to {self.resize_max_size}.")
            im = im.resize(self.resize_max_size)

        if im.size[0] < self.resize_min_size[0] or im.size[1] < self.resize_min_size[1]:
            self._verbose_message(
                f"Image is smaller than the minimum allowed dimensions. Resizing the image from {im.size} to {self.resize_min_size}.")
            im = im.resize(self.resize_min_size)

        # if applicable, rotate the image
        if self.rotate_angle:
            im = self._rotate(im, self.rotate_angle)

        # if applicable, resize the image
        if self.resize_shape:
            im = self._resize(im, self.resize_shape)

        # Convert the Pillow.Image object into a np.ndarray
        im = np.array(im)
        
        # normalize
        if self.normalize:
            im = self._normalize(im, self.normalize)

        # standardize
        if self.standardize: 
            im = self._standardize(im, self.standardize)

        # if applicable, write out to png
        if png_file_path:
            self._to_png(im, png_file_path)

        # if applicable, change dtype
        if self.to_dtype:
            im = self._to_dtype(im, to_dtype=self.to_dtype)

        # return the image (numpy.ndarray)
        self._verbose_message(f"Returning the image ({type(im)})")
        return im


class ImagePostprocessor(ImageProcessor):
    '''A Pillow-based image postprocessing tool adapted for MAX APIs.'''

    def __init__(self, denormalize=False, verbose=False, to_dtype=None, resize_shape=None,
                 rotate_angle=None):
        self.denormalize = denormalize
        self.verbose = verbose
        self.to_dtype = to_dtype
        self.resize_shape = resize_shape
        self.rotate_angle = rotate_angle

    def postprocess_imagedata(self, image_data=None, from_file=None, png_file_path=None):
        '''
        :param image_data: A numpy array, or a Pillow object.
        :param from_file:
        :param png_file_path:
        :return: the image as np.ndarray format
        '''

        # Sanity checks
        assert image_data or from_file, "Specify either the 'from_file' argument or the 'image_data' argument."

        # Load the image returned by the model as a Pillow.Image
        if image_data:
            im = self._load_image_from_model_output(image_data)
        elif from_file:
            self._verbose_message(f"Loading image from '{from_file}'")
            im = Image.open(from_file)

        # if applicable, rotate the image
        if self.rotate_angle:
            im = self._rotate(im, self.rotate_angle)

        # if applicable, resize the image
        if self.resize_shape:
            im = self._resize(im, self.resize_shape)

        # Convert the Pillow.Image object into a np.ndarray
        im = np.array(im)

        if self.denormalize:
            self._verbose_message(f"Denormalizing the image to a [0, 255] scale. NOTE: Results might be spurious.")
            im = (im + 0) * 255

        # write out to png or skip
        if png_file_path:
            self._to_png(im, png_file_path)

        # change dtype or skip
        if self.to_dtype:
            im = self._to_dtype(im, to_dtype=self.to_dtype)

        # return the image (numpy.ndarray)
        self._verbose_message(f"Returning the image ({type(im)})")
        return im

    def image_to_bytestream(self, image):
        '''
        input: the output image produced by the model
        :return: a bytestream
        '''
        # Return the image as a bytestream
        stream = io.BytesIO()
        image.save(stream)
        self._verbose_message(f"Returning the image ({type(stream)})")
        return stream.seek(0)
