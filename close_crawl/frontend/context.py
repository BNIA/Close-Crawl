#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from os.path import abspath, dirname
import sys

MODULE_PATH = dirname(abspath(dirname(__file__)))
sys.path.append(MODULE_PATH)

import _version
import modules
