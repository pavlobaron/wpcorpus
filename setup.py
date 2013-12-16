#!/usr/bin/env python


from setuptools import setup

setup(name='wpcorpus',
      version='1.0',
      description='NLP corpus based on Wikipedia\'s full article dump',
      author='Pavlo Baron',
      author_email='pb@pbit.org',
      url='https://github.com/pavlobaron/wpcorpus',
      packages=['lib/wpcorpus/'],
      install_requires=[
          'argparse',
          'lxml',
          'pika',
          'tables',
          'SimpleConfigParser',
          'nltk'
      ],
     )

