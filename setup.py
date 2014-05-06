from setuptools import setup, find_packages
import os

long_description = ""

setup(name='prepend_licenses',
      version='0.2.0',
      description="Make sure all source files have ayour standard licensing stub at the top.",
      long_description=long_description,
      classifiers=[],
      keywords='license',
      author='Dustin Oprea',
      author_email='myselfasunder@gmail.com',
      url='',
      license='GPL 2',
      packages=find_packages(exclude=[]),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
      ],
      scripts=['scripts/pl'],
)
