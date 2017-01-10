#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""local_browser

NOTICE: Close Crawl runs its browser form submissions through Mechanize.
The module, however, is deprecated and does not support Python 3. The more
stable and maintained Mechanize and BeautifulSoup wrapper, MechanicalSoup,
will be replacing the Mechanize methods to support Python 3.

This module contains the configurations and settings for the browser used for
crawling and scraping through the pages in Close Crawl. The script contains the
implementation of the Session class which inherits attributes from the classobj
mechanize.Browser()

The script works as an internal module for Close Crawl, but can be imported
as a module for testing purposes.

TODO:
    Replace deprecated Mechanize with MechanicalSoup

"""

from __future__ import absolute_import, print_function, unicode_literals
import cookielib  # import http.cookiejar for Python3
import warnings

from mechanize import Browser, _http

from .settings import HEADER, URL

warnings.filterwarnings('ignore', category=UserWarning)


class Session(object):

    def __init__(self):
        """Constructor

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

        # follows refresh 0 but doesn't hang on refresh > 0
        self.browser.set_handle_refresh(
            _http.HTTPRefreshProcessor(), max_time=1
        )

        # user-Agent
        self.browser.addheaders = [('User-agent', HEADER)]

    def open(self, url):
        return self.browser.open(url)

    def close(self):
        """Destructor for Session. Closes current browser session

        Args:
            None

        Returns:
            None
        """
        self.browser.close()

    def case_id_form(self, case):
        """Grabs the form in the case searching page, and inputs the
        case number to return the response.

        Args:
            case (`str`): case ID to be scraped

        Returns:
            response (`str`): HTML response
        """

        # iterate through the forms to find the correct one
        for form in self.browser.forms():
            if form.attrs['name'] == 'inquiryFormByCaseNum':
                self.browser.form = form
                break

        # submit case ID and return the response
        self.browser.form['caseId'] = case
        self.browser.submit()
        response = self.browser.response().read()
        self.browser.back()

        return response

    def disclaimer_form(self):
        """Navigates to the URL to proceed to the case searching page

        Args:
            None

        Returns:
            None
        """

        # visit the site
        self.browser.open(URL)

        # select the only form on the page
        self.browser.select_form(nr=0)

        # select the checkbox
        self.browser.form['disclaimer'] = ['Y']

        # submit the form
        self.browser.submit()
