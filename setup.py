# -*- coding: utf-8 -*-
"""
Created on Thu May 10 11:22:08 2018

@author: Annalise
setup.py
"""

import sys


try:
    from setuptools import setup
    have_setuptools = True
except ImportError:
    from distutils.core import setup
    have_setuptools = False
setup_kwargs = {
        'name': 'BigFan',
        'version': '0.1.0',
        'description': 'Wind Farm Analysis and Optimization',
        'author': 'Annnalise Miller',
        'author_email': 'millanna@oregonstate.edu',
        'url': 'http://www.oreilly.com/',
        'classifiers': [
            'License :: OSI Approved',
            'Intended Audience :: Wind Farm Developers',
            'Programming Language :: Python :: 3.6',
            ],
        'zip_safe': False,
        'packages': ['BigFan'],
        'package_dir': {
            'BigFan': 'BigFam',
            },
        # not confident about this lin
        'data_files': [('BigFan', ['inputs.csv'])],
        }
if __name__ == '__main__':
    setup(**setup_kwargs)