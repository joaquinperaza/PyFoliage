---
layout: default
title: PyFoliage
description: A Python library for calculating the green canopy cover of plants in images
---

# Welcome to PyFoliage's Documentation

PyFoliage is a Python library designed to calculate the green canopy cover of plants in images. It is a spin-off from the Canopeo application and uses the same algorithm to classify green canopy cover.

## Features

- Calculate the green canopy cover in a single image or a list of images.
- Apply a mask to classify the green canopy cover in an image.
- Extract EXIF metadata from images, including date/time and geolocation data.
- Save the generated mask as a binary image.

## Getting Started

First, install the library using pip:

```bash
pip install pyfoliage
```

Then, you can import PyFoliage in your Python scripts:

```python
import pyfoliage
```
See the [Getting Started Guide](#) for more detailed usage examples.

## Documentation

For more detailed descriptions of how to use PyFoliage, see the [examples](#). The [API Reference](#) contains detailed information about the functions and classes in PyFoliage.

## Feedback

For making feature requests and reporting errors, please open an issue in the Github repository.

## Privacy and image metadata

PyFoliage retrieves metadata such as image name, image dimensions, timestamp, and geographic coordinates already present in the images. If the images don't contain geographic coordinates, PyFoliage outputs null values. PyFoliage does not collect any private user or image information.

## License

PyFoliage is an open-source project under the MIT license. We only request that you acknowledge and properly cite our work.

## Green canopy cover methodology

Details of the image processing routine are described in:
        Patrignani, A. and Ochsner, T.E. (2015), Canopeo: A Powerful New Tool for Measuring Fractional Green Canopy Cover. Agronomy Journal, 107: 2312-2320. https://doi.org/10.2134/agronj15.0150


## External packages

This tool wouldn't be possible without the following projects:

- [Pillow](https://pillow.readthedocs.io/en/stable/)
- [NumPy](https://numpy.org/)
- [pandas](https://pandas.pydata.org/)
