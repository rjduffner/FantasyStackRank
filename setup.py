import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires=['yql',
          'pyyaml']

setup(name='FantasyStackRank',
      version='0.0.1',
      description='FantasyStackRank',
      author='',
      author_email='',
      url='',
      keywords='yql yahoo',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires
      )
