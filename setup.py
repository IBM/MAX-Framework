from setuptools import setup

setup(name='maxfw',
      version='1.1.0',
      description='A package to simplify the creation of MAX models',
      url='https://github.com/IBM/MAX-Framework',
      author='CODAIT',
      author_email='djalova@us.ibm.com, nickp@za.ibm.com, brendan.dwyer@ibm.com',
      license='Apache',
      packages=['maxfw', 'maxfw.core', 'maxfw.model'],
      zip_safe=True,
      install_requires=[
        'flask-restplus==0.11.0',
        'flask-cors',
        ],
    )
