# pyfoliage/__init__.py
""" `PyFoliage`
"""

# GEt version from setup.py
from pathlib import Path
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"

# Import all functions from crnpy

from .pyfoliage import *