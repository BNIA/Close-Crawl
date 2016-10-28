#!/usr/bin/env python

"""venv.py
Makefile helper script to determine if virtualenv is activated"""

if __name__ == '__main__':

    import sys

    if hasattr(sys, 'real_prefix'):
        sys.stdout.write('1')
    else:
        sys.stdout.write('0')
