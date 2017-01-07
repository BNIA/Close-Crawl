#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from .context import modules
from modules import local_browser


def test_anon():
    """Anonymize the session"""

    browser = local_browser.Session()

    origin_ip = browser.open("http://icanhazip.com").read()
    browser.anonymize()
    anon_ip = browser.open("http://icanhazip.com").read()

    assert(origin_ip != anon_ip)
