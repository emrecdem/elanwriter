import setuptools

def readme():
    with open('README.md') as f:
        return f.read()


setuptools.setup(name='elanwriter',
      version='0.0.0.dev2',
      description='A tool to write out Elan (.eaf) files using python.',
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
      author='B.L. de Vries',
      author_email='b.devries@esciencecenter.nl',
      packages=setuptools.find_packages(),
      install_requires=[],
      )