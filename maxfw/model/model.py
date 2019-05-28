from abc import ABC, abstractmethod


class MAXModelWrapper(ABC):
    def __init__(self, path=None):
        """Implement code to load model here"""
        pass

    def _pre_process(self, x):
        """Implement code to process raw input into format required for model inference here"""
        return x

    def _post_process(self, x):
        """Implement any code to post-process model inference response here"""
        return x

    @abstractmethod
    def _predict(self, x):
        """Implement core model inference code here"""
        return x

    def predict(self, x):
        pre_x = self._pre_process(x)
        prediction = self._predict(pre_x)
        result = self._post_process(prediction)
        return result
