from setuptools import setup, find_packages

setup(
    name='PyFoliage',
    version='0.0.1',
    url='https://github.com/joaquinperaza/PyFoliage.git',
    author='Joaquin Peraza',
    author_email='jperaza@ksu.edu',
    description='A Python package for the batch processing of green canopy cover images.',
    packages=find_packages(),
    install_requires=['numpy >= 1.11.1', 'matplotlib >= 1.5.1'],
)
