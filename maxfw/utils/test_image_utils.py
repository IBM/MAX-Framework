# Standard libs
import io

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

    preprocessor = ImagePreprocessor(grayscale=True, rotate_angle=None, resize_shape=(100, 100), verbose=True)
    preprocessor.preprocess_imagedata(test_input)

def test_imagepostprocessor():
    '''
    Test the ImagePostProcessor.
    '''

    postprocessor = ImagePostprocessor()


if __name__ == '__main__':
    pytest.main([__file__])
    #test_imagepreprocessor()
    #test_imagepostprocessor()