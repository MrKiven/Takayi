# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

data = []

install_requires = []
with open('requirements.txt') as f:
    for r in f:
        install_requires.append(r)

setup(
    name="takayi",
    version="0.3.3",
    description="Type hints for python 2.x",
    long_description=open('README.md').read(),
    author="Kiven",
    author_email="kiven.mr@gmail.com",
    url="https://github.com/MrKiven/Takayi",
    packages=find_packages(),
    package_data={"": ["LICENSE"], "veskit": data},
    tests_require=[
        'pytest==2.5.2',
        'pytest-cov==1.8.1',
        'pytest-xdist==1.13.1',
        'mock==1.0.1',
    ],
    install_requires=[],
)
