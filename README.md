# Model Asset Exchange Framework
 Python package that contains common code shared across all MAX models.

## Dependencies
* [flask-restplus](https://pypi.org/project/flask-restplus/0.11.0/)
* [flask-cors](https://pypi.org/project/Flask-Cors/)

## Installation
The package can be installed with pip. However, this is not necessary as the
Docker images of all MAX models will include `maxfw` as a package.

If you want to run a MAX model outside of a Docker container then you can install
it with the following command:

    $ pip install -U maxfw

## Usage

For an example of this package being used in a MAX model, we recommend looking at the
[MAX-Skeleton Repository on GitHub](https://github.com/IBM/MAX-Skeleton).
