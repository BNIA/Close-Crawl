#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""local_browser

This module contains the configurations and settings for the browser used for
crawling and scraping through the pages in Close Crawl. The script contains the
implementation of the Session class which inherits attributes from the classobj
mechanize.Browser()

The script works as an internal module for Close Crawl, but can be imported
as a module for testing purposes.

TODO:
    Finish docs
    Replace deprecated Mechanize with MechanicalSoup

"""

from __future__ import absolute_import, print_function, unicode_literals
import cookielib  # import http.cookiejar for Python3
import socket

from mechanize import Browser, _http
import socks

from .settings import HEADER, URL


class Session(object):

    def __init__(self):
        """Constructor for Session

        Args:
            None

        Attributes:
            browser (`mechanize._mechanize.Browser`): browser object in session
        """

        self.browser = Browser()

        # set error and debug handlers for the browser

        # cookie jar
        self.browser.set_cookiejar(cookielib.LWPCookieJar())

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

    def close(self):
        """Destructor for Session. Closes current browser session

        Args:
            None

        Returns:
            None
        """
        self.browser.close()

    def anonymize(self):
        """Anonymizes IP address of the hosting machine

        WARNING: THIS OPTION IS HIGHLY DEPENDANT ON TYPE OF MACHINE AND
        SEVERAL SYSTEM DEPENDANCIES AND REQUIREMENTS, POSSIBLY REQUIRES
        THIRD PARTY SECURED BROWSERS SUCH AS TOR. THIS OPTION HAS ONLY BEEN
        TESTED ON LINUX DISTROS. WINDOWS MACHINES HAVE NOT BEEN TESTED.

        Args:
            None

        Returns:
            None
        """

        socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5,
                              addr="127.0.0.1", port=9050)

        socket.socket = socks.socksocket

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
