#
# Copyright 2018-2021 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='maxfw',
      version='1.1.6',
      description='A package to simplify the creation of MAX models',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/IBM/MAX-Framework',
      author='CODAIT',
      author_email='djalova@us.ibm.com, nickp@za.ibm.com, brendan.dwyer@ibm.com',
      license='Apache',
      packages=['maxfw', 'maxfw.core', 'maxfw.model', 'maxfw.utils'],
      zip_safe=True,
      install_requires=[
        'flask-restx>=0.3',
        'flask-cors>=3.0.9',
        'Pillow>=8.1.1',
        'numpy>=1.18.4',
        ],
      test_suite='nose.collector',
      tests_require=['nose']
      )
