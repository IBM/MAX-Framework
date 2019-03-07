from image_utils import ImagePreprocessor

from PIL import Image
import io
stream = io.BytesIO()
Image.open('test_image.jpg').convert('RGBA').save(stream, 'PNG')

# Set up ImagePreprocessor
preprocessor = ImagePreprocessor(grayscale=True, rotate=0, resize=(100,100))
print(preprocessor.preprocess_imagedata(stream.getvalue()))
