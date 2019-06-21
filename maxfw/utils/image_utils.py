from __future__ import division
import sys
from PIL import Image
import collections

from . import image_functions as F

if sys.version_info < (3, 3):
    Sequence = collections.Sequence
    Iterable = collections.Iterable
else:
    Sequence = collections.abc.Sequence
    Iterable = collections.abc.Iterable


_pil_interpolation_to_str = {
    Image.NEAREST: 'PIL.Image.NEAREST',
    Image.BILINEAR: 'PIL.Image.BILINEAR',
    Image.BICUBIC: 'PIL.Image.BICUBIC',
    Image.LANCZOS: 'PIL.Image.LANCZOS',
    Image.HAMMING: 'PIL.Image.HAMMING',
    Image.BOX: 'PIL.Image.BOX',
}


class ImageProcessor(object):
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

    def __init__(self, transforms=[]):
        assert isinstance(transforms, Iterable)
        self.transforms = transforms

    def apply_transforms(self, img):
        # verify whether the Normalize or Standardize transformations are positioned at the end
        encoding = [(isinstance(t, Normalize) or isinstance(t, Standardize)) for t in self.transforms]
        assert sum(encoding[:-1]) == 0, \
            'A Standardize or Normalize transformation must be positioned at the end of the pipeline.'

        # apply the transformations
        for t in self.transforms:
            img = t(img)
        return img


class ToPILImage(object):
    """Convert a byte stream or an ndarray to PIL Image.

    Converts a byte stream or a numpy ndarray of shape
    H x W x C to a PIL Image while preserving the value range.

    Args:
        mode (`PIL.Image mode`_): color space and pixel depth of input data (optional).
            If ``mode`` is ``None`` (default) there are some assumptions made about the input data:
             - If the input has 4 channels, the ``mode`` is assumed to be ``RGBA``.
             - If the input has 3 channels, the ``mode`` is assumed to be ``RGB``.
             - If the input has 2 channels, the ``mode`` is assumed to be ``LA``.
             - If the input has 1 channel, the ``mode`` is determined by the data type (i.e ``int``, ``float``,
              ``short``).

    .. _PIL.Image mode: https://pillow.readthedocs.io/en/latest/handbook/concepts.html#concept-modes
    """
    def __init__(self, target_mode, mode=None):
        self.mode = mode
        self.target_mode = target_mode

    def __call__(self, pic):
        """
        Args:
            pic (bytestream or numpy.ndarray): Image to be converted to PIL Image.

        Returns:
            PIL Image: Image converted to PIL Image.

        """
        return F.to_pil_image(pic, self.target_mode, self.mode)


class PILtoarray(object):
    """
    onvert a PIL Image object to a numpy ndarray.
    """

    def __call__(self, pic):
        """
        Args:
            pic (PIL Image): Image to be converted to a numpy ndarray.

        Returns:
            numpy ndarray

        """
        return F.pil_to_array(pic)


class Normalize(object):
    """
    Normalize the image to a range between [0, 1].
    """

    def __call__(self, img):
        """
        Args:
        img (PIL image or numpy.ndarray): Image to be normalized.

        Returns:
        numpy.ndarray: Normalized image.
        """
        return F.normalize(img)


class Standardize(object):
    """
    Standardize the image (mean-centering and STD of 1).
    """

    def __call__(self, img):
        """
        Args:
        img (PIL image or numpy.ndarray): Image to be standardized.

        Returns:
        numpy.ndarray: Standardized image.
        """
        return F.standardize(img)


class Resize(object):
    """Resize the input PIL Image to the given size.

    Args:
        size (sequence or int): Desired output size. If size is a sequence like
            (h, w), output size will be matched to this. If size is an int,
            smaller edge of the image will be matched to this number.
            i.e, if height > width, then image will be rescaled to
            (size * height / width, size)
        interpolation (int, optional): Desired interpolation. Default is
            ``PIL.Image.BILINEAR``
    """

    def __init__(self, size, interpolation=Image.BILINEAR):
        assert isinstance(size, int) or (isinstance(size, Iterable) and len(size) == 2)
        self.size = size
        self.interpolation = interpolation

    def __call__(self, img):
        """
        Args:
            img (PIL Image): Image to be scaled.

        Returns:
            PIL Image: Rescaled image.
        """
        return F.resize(img, self.size, self.interpolation)


class Rotate(object):
    """
    Rotate the input PIL Image by a given angle (counter clockwise).

    Args:
        angle (int or float): Counter clockwise angle to rotate the image by.
    """

    def __init__(self, angle):
        self.angle = angle

    def __call__(self, img):
        """
        Args:
            img (PIL Image): Image to be rotated.

        Returns:
            PIL Image: Rotated image.
        """
        return F.rotate(img, self.angle)


class Grayscale(object):
    """Convert image to grayscale.

    Args:
        num_output_channels (int): (1 or 3) number of channels desired for output image

    Returns:
        PIL Image: Grayscale version of the input.
        - If num_output_channels == 1 : returned image is single channel
        - If num_output_channels == 3 : returned image is 3 channel with r == g == b

    """

    def __init__(self, num_output_channels=1):
        self.num_output_channels = num_output_channels

    def __call__(self, img):
        """
        Args:
            img (PIL Image): Image to be converted to grayscale.

        Returns:
            PIL Image: Randomly grayscaled image.
        """
        return F.to_grayscale(img, num_output_channels=self.num_output_channels)
