# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fcc4d',
    version='0.0.1',
    description='Client library for FreeConferenceCall For Developers (FCC4D) API.',
    long_description=long_description,
    url='https://github.com/mkching/fcc4d-python',
    author='Michael Ching',
    author_email='mching@widevoice.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Telephony',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='freeconferencecall fcc4d',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['requests'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)
