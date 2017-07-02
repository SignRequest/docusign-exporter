# -*- coding: utf-8 -*-
__author__ = "Michaël Krens"
__copyright__ = "Copyright 2017, SignRequest B.V."

import os
from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# helpfull: https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
# distribute using: python setup.py sdist bdist_wheel upload

setup(
    name="docusign_exporter",
    version='1.0.3',
    author="Michaël Krens",
    author_email="michael@signrequest.com",
    description="A simple tool to bulk export / download all documents from your DocuSign account using the API.",
    keywords="DocuSign bulk download SignRequest",
    url="https://github.com/SignRequest/docusign-exporter",
    packages=['docusign_exporter'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
    install_requires=required,
    entry_points={
        'console_scripts': [
            'docusign_exporter=docusign_exporter.docusign_exporter:main',
        ],
    },
)
