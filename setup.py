#####################################
#
# Copyright 2018 NXP
#
#####################################

import sys
import os
from setuptools import setup


long_description = 'edgescacle command-line interface library and tool'
if os.path.exists('README.txt'):
    long_description = open('README.txt').read()


def getRequires():
    deps = ['click', 'texttable']
    return deps


base_url = 'https://bitbucket.sw.nxp.com/projects/DCCA/repos/escli'
version = '1.0.0'
setup(
    name='escli',
    version=version,
    author='NXP',
    author_email='edgescale@nxp.com',
    url='{0}escli'.format(base_url),
    download_url='{0}escli/tarball/{1}'.format(base_url, version),
    packages=['escli', 'esclicore'],
    license='NXP EULA',
    description='EdgeScale CLI library and tool, simplified for Python',
    long_description=long_description,
    install_requires=getRequires(),
    entry_points={
        'console_scripts': ['escli=escli.cli:cli'],
    },

    keywords=[
        'edgescale',
        'NXP',
        'cli'],
    classifiers=[
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
