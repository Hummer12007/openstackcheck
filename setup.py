import os
from setuptools import find_packages, setup

def readfile(fname):
	with open(os.path.join(os.path.dirname(__file__), fname)) as f: return f.read()

setup(
    name = "openstackcheck",
    version = "0.1",
    author = "Mykyta Holubakha",
    author_email = "hilobakho@gmail.com",
    description = "Smoke tests for OpenStack deployments",
    license = "MIT",
    keywords = "openstack",
    packages=find_packages(),
    install_requires=['openstacksdk', 'paramiko', 'environs', 'requests'],
    long_description=readfile('README'),
    entry_points={
        'console_scripts': ['openstackcheck = openstackcheck.main:main'],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)

