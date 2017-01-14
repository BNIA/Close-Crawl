"""Example app to login to GitHub"""
from __future__ import absolute_import, print_function, unicode_literals
from sys import version_info
if version_info >= (3, 0):
    print("ayyyy")
    from http import cookiejar

else:
    import cookielib

import mechanicalsoup
import requests
from settings import URL


# def case_id_form(case):

#     for form in browser.forms():
#         if form.attrs['name'] == 'inquiryFormByCaseNum':
#             browser.form = form
#             break

#     browser.form['caseId'] = case
#     browser.submit()
#     response = browser.response().read()
#     browser.back()

#     return response


class Session(object):

    def __init__(self):
        """Constructor

        Args:
            None

        Attributes:
            browser (`mechanize._mechanize.Browser`): browser object in session
        """

        # you can chooise another cookie store like a LWPCookieJar
        s = requests.Session()
        s.cookies = cookiejar.CookieJar()
        self.browser = mechanicalsoup.Browser(session=s)
        self.response = None

        # set error and debug handlers for the browser

        # # browser options
        # self.browser.set_handle_equiv(True)
        # self.browser.set_handle_gzip(True)
        # self.browser.set_handle_redirect(True)
        # self.browser.set_handle_referer(True)
        # self.browser.set_handle_robots(False)

        # # follows refresh 0 but doesn't hang on refresh > 0
        # self.browser.set_handle_refresh(
        #     _http.HTTPRefreshProcessor(), max_time=1
        # )

        # # user-Agent
        # self.browser.addheaders = [('User-agent', HEADER)]

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

        # # iterate through the forms to find the correct one
        # for form in self.browser.forms():
        #     if form.attrs['name'] == 'inquiryFormByCaseNum':
        #         self.browser.form = form
        #         break

        # # submit case ID and return the response
        # self.browser.form['caseId'] = case
        # self.browser.submit()
        # response = self.browser.response().read()
        # self.browser.back()

        # return response

        case_form = self.response.soup.find_all("form")[-1]
        case_form = mechanicalsoup.Form(case_form)
        case_form.input({"caseId": case})
        self.response = self.browser.submit(case_form, self.response.url).soup
        print(self.response)

    def disclaimer_form(self):
        """Navigates to the URL to proceed to the case searching page

        Args:
            None

        Returns:
            None
        """

        login_page = self.browser.get(URL)
        login_form = mechanicalsoup.Form(login_page.soup.form)
        login_form.check({"disclaimer": ['Y']})

        self.response = self.browser.submit(login_form, URL)


response = Session()
response.disclaimer_form()

response.case_id_form("24O15000001")
