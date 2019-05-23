#!/usr/bin/env python

from setuptools import setup

setup(
    name='igl-website-fixpaths',
    version='0.1.0',
    description='Extension for Python-Markdown to replace paths in urls.',
    long_description='',
    long_description_content_type="text/markdown",
    py_modules=['urlprocessor'],
    install_requires=['Markdown>=3.0'],
    classifiers=[
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Text Processing :: Markup',
        'Topic :: Utilities'
    ]
)
