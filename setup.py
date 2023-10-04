from setuptools import find_packages
from setuptools import setup
import os

base_dir = os.path.dirname(__file__)

setup(
    name="gfrancodev-glogger",
    version="0.2",
    description="Log Aggregator",
    author="Gustavo Franco",
    author_email="conctact@gfrancodev.com",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'boto3==1.18.2',
        'configparser==5.0.2',
        'google-cloud==0.34.0',
        'websockets==11.0.3',
        'google-cloud-logging==3.7.0',
        'google-cloud-storage==2.11.0',
        'azure-storage-blob==12.18.2',
        'appinsights==0.13.0',
        'colorama==0.4.6',
    ],
    entry_points={
        "console_scripts": [
            "glogger=glogger.main:main"
        ]
    },
    packages=find_packages(exclude=["exemplo", ".idea"]),
    setup_requires="setuptools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)

