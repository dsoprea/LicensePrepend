from setuptools import setup, find_packages
import os

description = "Make sure all source files have your standard licensing stub "\
              "at the top."

long_description = ""

setup(name='prepend_license',
      version='0.2.0',
      description=description,
      long_description=long_description,
      classifiers=[],
      keywords='license',
      author='Dustin Oprea',
      author_email='myselfasunder@gmail.com',
      url='https://github.com/dsoprea/LicensePrepend',
      license='GPL 2',
      packages=find_packages(exclude=[]),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
            'nose'
      ],
      scripts=['scripts/plicense'],
)
