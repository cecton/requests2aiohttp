#!/usr/bin/env python3

import os

from setuptools import setup, find_packages


ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)


version = None
exec(open('requests2aiohttp/__init__.py').read())


with open('./requirements.txt') as reqs_txt:
    requirements = list(iter(reqs_txt))


setup(
    name="requests2aiohttp",
    version=version,
    description="A compatibility layer to transform requests.Session classes "
                "to aiohttp.ClientSession",
    url='https://github.com/cecton/requests2aiohttp',
    packages=find_packages(exclude=["tests.*", "tests"]),
    install_requires=requirements,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
    ],
    maintainer='Cecile Tonglet',
    maintainer_email='cecile.tonglet@gmail.com',
)
