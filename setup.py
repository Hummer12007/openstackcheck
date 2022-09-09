import os
from setuptools import setup

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
    packages=['openstackcheck'],
    install_requires=['openstacksdk', 'paramiko', 'environs'],
    #long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)

