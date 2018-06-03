import sys


try:
    from setuptools import setup
    have_setuptools = True
except ImportError:
    from distutils.core import setup
    have_setuptools = False
setup_kwargs = {
        'name': 'bigfan',
        'version': '0.1.2',
        'description': 'Wind Farm Analysis and Optimization',
        'author': 'Annalise Miller',
        'author_email': 'millanna@oregonstate.edu',
        'url': 'https://github.com/annalisemckenzie/BigFan',
        'classifiers': [
            'License :: OSI Approved',
            'Intended Audience :: Wind Farm Developers',
            'Programming Language :: Python :: 3.6',
            ],
        'zip_safe': False,
        'packages': ['bigfan', 'bigfan.tests'],
        'package_dir': {
            'bigfan': 'bigfan',
            },
        # not confident about this line
        'data_files': [('bigfan', ['bigfan/inputs.csv'])],
        }
if __name__ == '__main__':
    setup(**setup_kwargs)
