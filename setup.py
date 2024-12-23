import io
import setuptools
from zlai import __version__

__title__ = "wisecon"
__license__ = "MIT"
__description__ = "Quant/Data API"
__author_email__ = "chensy.cao@foxmail.com"
__url__ = "https://caochensy.github.io/wisecon/"


with open("requirements.txt", "r") as f:
    requires = f.readlines()
__requires__ = requires


with io.open("README.md", "r+", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name=__title__,
    version=__version__,
    author="chensy",
    author_email=__author_email__,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=__url__,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=__requires__,
    package_data={
        '': ['*.csv', '*.xlsx', '*.pickle'],
    },
)


# python setup.py sdist bdist_wheel

