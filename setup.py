import re
from os import path

from setuptools import find_packages, setup

# Get the long description from README.md
PATH = path.abspath(path.dirname(__file__))
with open(path.join(PATH, "README.md"), encoding="utf-8") as file:
    long_description = file.read()

# Get version
with open(path.join(PATH, "sampling/__init__.py"), encoding="utf-8") as file:
    version = re.search(r"__version__ = \"(.*?)\"", file.read()).group(1)

setup(
    name="sampling",
    version=version,
    description="Pure Python sampling utilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tommyod/sampling",
    author="tommyod",
    author_email="tommy.odland@gmail.com",
    maintainer="tommyod, smu095, glemvik",
    license="MIT",
    packages=find_packages(exclude=["*tests*"]),
    python_requires=">=3.6",
    install_requires=[],
    # https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords=["sampling, statistics"],
)
