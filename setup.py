# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="type-doctor",
    version='0.0.1',
    long_description=open('README.md').read(),
    author="Kiven",
    author_email="kiven.mr@gmail.com",
    url="https://github.com/MrKiven/type-doctor",
    packages=find_packages(),
    tests_require=[
        'pytest==2.5.2',
        'pytest-cov==1.8.1',
        'pytest-xdist==1.13.1',
        'mock==1.0.1',
    ],
    install_requires=[],
    classifiers=[
        'Private :: Do Not Upload',
    ]
)
