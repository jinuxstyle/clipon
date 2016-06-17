#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from setuptools import setup
import clipon
from clipon.defines import CLIPON_VERSION

setup(
    name='clipon',
    version=CLIPON_VERSION,
    license='GPL',
    author='Jin Xu',
    author_email='jinuxstyle@hotmail.com',
    description='Clipon - a lightweight clipboard manager',
    long_description="Clipon is a open source project for managing your clipboard history in a simple and efficient way.",
    url="https://github.com/jinuxstyle/clipon",
    packages=['clipon'],
    platforms='linux',
    zip_safe=False,
    keywords=['clipboard', 'history'],

    install_requires=[
        'docopt'
    ],

    entry_points={
        'console_scripts': [
            'clipon = clipon.clipon:main'
        ]
    },

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ]
)
