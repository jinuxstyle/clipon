#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from setuptools import setup
import clipon
from clipon.defines import CLIPON_VERSION

long_desc="""Clipon is a open source project for managing your
clipboard history in a simple and efficient way.

It's useful if you want to take notes more efficiently when reading
documents or web pages. It trackes whatever you copied so that you
don't have to switch to another app to do paste whenever you copied
something useful. The paste operation is kind of a distraction when
you want to focus on reading. With Clipon, you just copy things when
reading, and do paste in batch after reading.

It also helps remember what you have copied and you might later want to
revisit some of them.

It's simple to use, start the daemon

    $ clipon start

Then you can view the clipboard history with following command

    $ clipon list

To see more subcommands, use

    $ clipon -h | --help
"""

setup(
    name='clipon',
    version=CLIPON_VERSION,
    license='GPL',
    author='Jin Xu',
    author_email='jinuxstyle@hotmail.com',
    description='Clipon - a lightweight clipboard manager',
    long_description=long_desc,
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
