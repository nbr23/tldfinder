#!/usr/bin/env python3

from setuptools import setup

setup(name='tldfinder',
      version='1.0',
      description='List TLDs available for registration for a specific name and their pricing at ovh.com',
      author='Maxence Ardouin',
      author_email='max@23.tf',
      url='https://github.com/nbr23/tldfinder',
      license='MIT',
      packages=['tldfinder'],
      zip_safe=True,
      install_requires=[
          'requests',
          ],
      entry_points={
          'console_scripts': [
              "tldfinder = tldfinder.__main__:main",
              ],
          },
      )

