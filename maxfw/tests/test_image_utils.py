# Standard libs
import io
import os

# Dependencies
import pytest
from PIL import Image

# The module to test
from maxfw.utils.image_utils import ImagePreprocessor, ImagePostprocessor

# Initialize a test input file
stream = io.BytesIO()
Image.open('maxfw/tests/test_image.jpg').convert('RGBA').save(stream, 'PNG')
test_input = stream.getvalue()

def test_imagepreprocessor_read():
    '''
    Test the ImagePreprocessor.
    '''
    # Test reshape
    preprocessor = ImagePreprocessor(verbose=True)
    assert preprocessor.preprocess_imagedata(test_input).shape == (678, 1024, 3)


def test_imagepreprocessor_rotate():
    '''
    Test the ImagePreprocessor image read.
    '''
    # Test reshape
    preprocessor = ImagePreprocessor(rotate_angle=180, verbose=True)
    preprocessor_no_rotate = ImagePreprocessor(rotate_angle=0, verbose=True)
    x = preprocessor.preprocess_imagedata(test_input)
    y = preprocessor_no_rotate.preprocess_imagedata(test_input)
    assert x[-1,:,:].all() == y[0,:,:].all()

def test_imagepreprocessor_resize():
    '''
    Test the ImagePreprocessor resize function.
    '''
    # Test reshape
    preprocessor = ImagePreprocessor(resize_shape=(100,100), verbose=True)
    assert preprocessor.preprocess_imagedata(test_input).shape == (100, 100, 3)

def test_imagepreprocessor_grayscale():
    '''
    Test the ImagePreprocessor grayscale function.
    '''
    preprocessor = ImagePreprocessor(grayscale=True, verbose=True)
    assert preprocessor.preprocess_imagedata(test_input).shape == (678, 1024)

def test_imagepreprocessor_output():
    '''
    Test the ImagePreprocessor file output function.
    '''
    # test file output
    preprocessor = ImagePreprocessor(verbose=True)
    preprocessor.preprocess_imagedata(test_input, png_file_path='test_output.png')
    # test if the output image is a valid image
    Image.open('test_output.png')
    # remove the test output
    os.remove('test_output.png')

def test_imagepostprocessor():
    '''
    Test the ImagePostProcessor.
    '''

    postprocessor = ImagePostprocessor()


if __name__ == '__main__':
    pytest.main([__file__])