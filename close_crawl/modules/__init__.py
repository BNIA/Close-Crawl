#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""modules
"""


import __builtin__

del __builtin__.range
__builtin__.range = xrange

del __builtin__.input
__builtin__.input = raw_input
