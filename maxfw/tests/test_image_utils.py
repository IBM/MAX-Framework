# Standard libs
import io

# Dependencies
import pytest
import numpy as np
from PIL import Image

# The module to test
from maxfw.utils.image_utils import ImageProcessor, ToPILImage, Resize, Grayscale, Normalize, Standardize, Rotate

# Initialize a test input file
stream = io.BytesIO()
Image.open('maxfw/tests/test_image.jpg').convert('RGBA').save(stream, 'PNG')
test_input = stream.getvalue()


def test_imageprocessor_read():
    """Test the Imageprocessor."""

    # Test with 4 channels
    transform_sequence = [ToPILImage('RGBA')]
    p = ImageProcessor(transform_sequence)
    img_out = p.apply_transforms(test_input)
    assert np.array(img_out).shape == (678, 1024, 4)

    # Test with 3 channels
    transform_sequence = [ToPILImage('RGB')]
    p = ImageProcessor(transform_sequence)
    img_out = p.apply_transforms(test_input)
    assert np.array(img_out).shape == (678, 1024, 3)


def test_imageprocessor_resize():
    """Test the Imageprocessor's resize function."""

    # Resize to 200x200
    transform_sequence = [ToPILImage('RGBA'), Resize(size=(200, 200))]
    p = ImageProcessor(transform_sequence)
    img_out = p.apply_transforms(test_input)
    assert np.array(img_out).shape == (200, 200, 4)

    # Resize to 2000x2000
    transform_sequence = [ToPILImage('RGBA'), Resize(size=(2000, 2000))]
    p = ImageProcessor(transform_sequence)
    img_out = p.apply_transforms(test_input)
    assert np.array(img_out).shape == (2000, 2000, 4)


def test_imageprocessor_grayscale():
    """Test the Imageprocessor's grayscale function."""

    # Using the standard 1 output channel
    transform_sequence = [ToPILImage('RGBA'), Resize(size=(200, 200)), Grayscale()]
    p = ImageProcessor(transform_sequence)
    img_out = p.apply_transforms(test_input)
    assert np.array(img_out).shape == (200, 200)

    # Using 3 output channels
    transform_sequence = [ToPILImage('RGBA'), Resize(size=(200, 200)), Grayscale(num_output_channels=3)]
    p = ImageProcessor(transform_sequence)
    img_out = p.apply_transforms(test_input)
    assert np.array(img_out).shape == (200, 200, 3)

    # Using 4 output channels
    transform_sequence = [ToPILImage('RGBA'), Resize(size=(200, 200)), Grayscale(num_output_channels=4)]
    p = ImageProcessor(transform_sequence)
    img_out = p.apply_transforms(test_input)
    assert np.array(img_out).shape == (200, 200, 4)


def test_imageprocessor_normalize():
    """Test the Imageprocessor's normalize function."""

    # Test normalize
    transform_sequence = [ToPILImage('RGBA'), Normalize()]
    p = ImageProcessor(transform_sequence)
    img_out = p.apply_transforms(test_input)
    assert np.max(img_out) <= 1 and np.min(img_out) >= 0

    # Test normalize
    transform_sequence = [ToPILImage('RGB'), Normalize(), Normalize()]
    p = ImageProcessor(transform_sequence)
    img_out = p.apply_transforms(test_input)
    assert np.max(img_out) <= 1 and np.min(img_out) >= 0

    # Test normalize
    transform_sequence = [ToPILImage('L'), Normalize()]
    p = ImageProcessor(transform_sequence)
    img_out = p.apply_transforms(test_input)
    assert np.max(img_out) <= 1 and np.min(img_out) >= 0


def test_imageprocessor_standardize():
    """Test the Imageprocessor's standardize function."""

    # Test standardize
    transform_sequence = [ToPILImage('RGBA'), Standardize()]
    p = ImageProcessor(transform_sequence)
    img_out = p.apply_transforms(test_input)
    assert round(np.std(img_out)) == 1

    # Test standardize
    transform_sequence = [ToPILImage('RGB'), Standardize(), Standardize()]
    p = ImageProcessor(transform_sequence)
    img_out = p.apply_transforms(test_input)
    assert round(np.std(img_out)) == 1

    # Test standardize
    transform_sequence = [ToPILImage('L'), Standardize()]
    p = ImageProcessor(transform_sequence)
    img_out = p.apply_transforms(test_input)
    assert round(np.std(img_out)) == 1


def test_imageprocessor_rotate():
    """Test the Imageprocessor's rotate function."""

    # Test rotate (int)
    transform_sequence = [ToPILImage('RGBA'), Resize((200, 200)), Rotate(5)]
    p = ImageProcessor(transform_sequence)
    img_out = p.apply_transforms(test_input)
    assert np.array(img_out).shape == (200, 200, 4)

    # Test rotate (negative int)
    transform_sequence = [ToPILImage('RGBA'), Resize((200, 200)), Rotate(-5)]
    p = ImageProcessor(transform_sequence)
    img_out = p.apply_transforms(test_input)
    assert np.array(img_out).shape == (200, 200, 4)

    # Test rotate (float)
    transform_sequence = [ToPILImage('RGBA'), Resize((200, 200)), Rotate(499.99)]
    p = ImageProcessor(transform_sequence)
    img_out = p.apply_transforms(test_input)
    assert np.array(img_out).shape == (200, 200, 4)


def test_imageprocessor_combinations():
    """Test various combinations of the Imageprocessor's functionality."""

    # Combination 1
    transform_sequence = [
        ToPILImage('RGB'),
        Resize((2000, 2000)),
        Normalize(),
        Rotate(5),
        Grayscale(num_output_channels=4),
        Resize((200, 200)),
    ]
    p = ImageProcessor(transform_sequence)
    img_out = p.apply_transforms(test_input)
    assert np.array(img_out).shape == (200, 200, 4)


def test_flask_error():
    # Test for flask exception by using the wrong channel format
    with pytest.raises(Exception, match=r"^400 Bad Request: .*"):
        transform_sequence = [ToPILImage('XXX')]
        p = ImageProcessor(transform_sequence)
        p.apply_transforms(test_input)

    # Test for a specific error message
    with pytest.raises(Exception, match=r"pic should be bytes or ndarray.*"):
        transform_sequence = [ToPILImage('RGB')]
        p = ImageProcessor(transform_sequence)
        p.apply_transforms("")


if __name__ == '__main__':
    # Running Pytest
    pytest.main([__file__])
