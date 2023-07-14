from setuptools import setup, find_packages

setup(
    name='pyfoliage',
    version='0.0.2',
    url='https://github.com/joaquinperaza/PyFoliage.git',
    author='Joaquin Peraza',
    include_package_data=True,
    author_email='jperaza@ksu.edu',
    description='A Python package for the batch processing of green canopy cover images.',
    packages=['pyfoliage'],
    package_dir={"": "src"},
    install_requires=['tqdm', 'pandas', 'numpy', 'Pillow'],
)
