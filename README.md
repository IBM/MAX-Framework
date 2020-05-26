[![Build Status](https://travis-ci.com/IBM/MAX-Framework.svg?branch=master)](https://travis-ci.com/IBM/MAX-Framework) [![PyPy release](https://img.shields.io/pypi/v/maxfw.svg)](https://pypi.org/project/maxfw/) 

# Model Asset Exchange Framework
 Python package that contains common code shared across all MAX models.

## Dependencies
* [flask-restx](https://pypi.org/project/flask-restx/0.1.1/)
* [flask-cors](https://pypi.org/project/Flask-Cors/)

## Installation

The package can be installed with pip. However, this is not necessary as each MAX
model will get the `maxfw` package via the `MAX-Base` image.

If you want to run a MAX model outside of a Docker container then you can install
it with the following command:

    $ pip install -U maxfw

## Usage

For an example of this package being used in a MAX model, we recommend looking at the
[MAX-Skeleton Repository on GitHub](https://github.com/IBM/MAX-Skeleton).
