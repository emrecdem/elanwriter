#from setuptools import setup
import setuptools

def readme():
    with open('README.rst') as f:
        return f.read()


setuptools.setup(name='elanwriter',
      version='0.0.0.dev1',
      description='',
      long_description=readme(),
      long_description_content_type='text/markdown',
      url='https://github.com/emrecdem/elanwriter',
    classifiers=(
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ),
      keywords='',
      #url='https://github.com/bldevries/opacity_calculator',
      author='B.L. de Vries',
      author_email='b.devries@esciencecenter.nl',
      packages=setuptools.find_packages(),
#      zip_safe=True)
      )