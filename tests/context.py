#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from os.path import abspath, dirname, join
import sys

MODULE_PATH = join(dirname(abspath(dirname(__file__))), "close_crawl")
sys.path.append(MODULE_PATH)

import modules
