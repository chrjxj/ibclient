import os
import codecs
from setuptools import setup, find_packages
import ibclient


def parse_requirements(filename):
    with open(filename) as f:
        required = f.read().splitlines()
        return required


long_desc = """
IBClient
===============
A Python SDK to access market data through Interactive Brokers TWS

"""

setup(
    name='ibclient',
    version=ibclient.__version__,
    description='A Python SDK to access market data through Interactive Brokers TWS',
    long_description=long_desc,
    author='Jin Xu',
    author_email='jin_xu1@qq.com',
    license='BSD',
    keywords=['Interactive Brokers', 'TWS', 'IB', 'Stock', 'finance'],
    classifiers=[
        'Development Status :: 1 - Alpha',
        'License :: OSI Approved :: BSD License'
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    tests_require=parse_requirements('requirements.txt'),

)
