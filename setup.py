# from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='example-package-rrmhearts',
    version='0.1',
    packages=find_packages('src', exclude=['test']),
    license='MIT',
    long_description=open('README.md').read(),
)