#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""local_browser

This module implements post-scraping cleaning processes on the raw initial
dataset. Processes include stripping excess strings off Address values,
removing Zip Code and Partial Cost values mislabeled as Address, and merging
rows containing blank values in alternating features.

The script works as an internal module for Close Crawl, but can be executed
as a standalone to manually process datasets:

    $ python cleaned_data.py <path/to/old/dataset> <path/of/new/dataset>

TODO:
    Finish docs

"""

from __future__ import absolute_import, print_function, unicode_literals
import cookielib
from socket import socket

from mechanize import Browser, _http
from socks import PROXY_TYPE_SOCKS5, setdefaultproxy, socksocket

from settings import HEADER, URL


class Session(object):

    def __init__(self):

        self.browser = Browser()

        # cookie Jar
        cj = cookielib.LWPCookieJar()
        self.browser.set_cookiejar(cj)

        # browser options
        self.browser.set_handle_equiv(True)
        self.browser.set_handle_gzip(True)
        self.browser.set_handle_redirect(True)
        self.browser.set_handle_referer(True)
        self.browser.set_handle_robots(False)

        # follows refresh 0 but not hangs on refresh > 0
        self.browser.set_handle_refresh(
            _http.HTTPRefreshProcessor(), max_time=1
        )

        # user-Agent
        self.browser.addheaders = [('User-agent', HEADER)]

    def anonymize(self):

        setdefaultproxy(proxy_type=PROXY_TYPE_SOCKS5,
                        addr="127.0.0.1", port=9050)

        socket = socksocket

        print("Current spoofed IP:", self.browser.open(
            "http://icanhazip.com").read())

    def case_id_form(self, case):

        for form in self.browser.forms():
            if form.attrs['name'] == 'inquiryFormByCaseNum':
                self.browser.form = form
                break

        self.browser.form['caseId'] = case
        self.browser.submit()
        response = self.browser.response().read()
        self.browser.back()

        return response

    def disclaimer_form(self):

        # visit the site
        self.browser.open(URL)

        # select the only form on the page
        self.browser.select_form(nr=0)

        # select the checkbox
        self.browser.form['disclaimer'] = ['Y']

        # submit the form
        self.browser.submit()
