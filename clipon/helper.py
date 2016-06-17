#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import sys
import os
import re
import logging
import logging.handlers
from logging import Logger
from xml.dom import minidom
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

INT_MAX = sys.maxsize

#create or get a logger with given name
LOGGER_NAME = 'clipon'
logger = logging.getLogger(LOGGER_NAME)

def init_log(logfile):
    global logger
    logger.setLevel(logging.DEBUG)

    # create a rotating file handler
    h = logging.handlers.RotatingFileHandler(logfile, maxBytes=1024*1024)
    h.setLevel(logging.INFO)
    fmt = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    formatter = logging.Formatter(fmt, datefmt='%Y/%m/%d %H:%M:%S')
    h.setFormatter(formatter)

    logger.addHandler(h)
    logger.info("Initialized logger")

def open_file(dir_path, file_path, mode):
    fd = None
    if not os.path.isfile(file_path):
        try:
            if not os.path.exists(dir_path):
                os.mkdir(dir_path, 0o700)
            if not os.path.exists(file_path):
                open(file_path, 'x')
        except IOError:
            logger.error("Failed to create file %s" % file_path)
            return None

    try:
        fd = open(file_path, mode)
    except IOError:
        logger.error("Failed to open file %s" % file_path)
        return None

    return fd

def format_pretty(elem):
    """
    Return a pretty-printed XML string for the given element.
    """
    raw_string = ET.tostring(elem, encoding='utf-8')
    s = raw_string.decode()
    s = re.sub(' *\n *', '', s) # remove any newline and its surrounding white space
    raw_string = s.encode(encoding="utf-8")
    dom_string = minidom.parseString(raw_string)
    return dom_string.toprettyxml(indent="  ")
