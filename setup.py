from re import search
from setuptools import setup, find_packages

with open('README.md') as f:
    README = f.read()

with open('starkcore/__init__.py') as f:
    version = search(r'version = \"(.*)\"', f.read()).group(1)

setup(
    name="starkcore",
    packages=find_packages(),
    include_package_data=True,
    description="Basic SDK functionalities for the starkbank and starkinfra SDKs",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT License",
    url="https://github.com/starkinfra/core-python",
    author="Stark Infra",
    author_email="developers@starkbank.com",
    keywords=[],
    version=version,
    install_requires=[
        "requests>=2.23.0",
        "starkbank-ecdsa>=2.0.3",
    ],
)
