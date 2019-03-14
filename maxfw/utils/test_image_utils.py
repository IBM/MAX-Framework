# Standard libs
import io
import os

# Dependencies
import pytest
from PIL import Image

# The module to test
from image_utils import ImagePreprocessor, ImagePostprocessor

# Initialize a test input file
stream = io.BytesIO()
Image.open('test_image.jpg').convert('RGBA').save(stream, 'PNG')
test_input = stream.getvalue()

def test_imagepreprocessor():
    '''
    Test the ImagePreprocessor.
    '''

    # Test reshape
    preprocessor = ImagePreprocessor(rotate_angle=180,resize_shape=(100,100), verbose=True, normalize=False)
    assert preprocessor.preprocess_imagedata(test_input).shape == (100, 100, 3)

    # Test grayscale
    preprocessor = ImagePreprocessor(resize_shape=(100, 100), grayscale=True, verbose=True)
    assert preprocessor.preprocess_imagedata(test_input).shape == (100, 100)

    # test file output
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
    #pytest.main([__file__])
    test_imagepreprocessor()
    test_imagepostprocessor()