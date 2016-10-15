import cookielib

from bs4 import BeautifulSoup
import mechanize

from settings import HEADER, URL

# Browser
browser = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
browser.set_cookiejar(cj)

# Browser options
browser.set_handle_equiv(True)
browser.set_handle_gzip(True)
browser.set_handle_redirect(True)
browser.set_handle_referer(True)
browser.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
# browser.set_debug_http(True)
# browser.set_debug_redirects(True)
# browser.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
browser.addheaders = [('User-agent', HEADER)]

# visit the site
browser.open(URL)


def disclaimer_form():

    # Select the first (index zero) form
    browser.select_form(nr=0)

    # Let's search
    browser.form['disclaimer'] = ['Y']
    browser.submit()


def case_id_form(case):

    for form in browser.forms():
        if form.attrs['name'] == 'inquiryFormByCaseNum':
            browser.form = form
            break

    browser.form['caseId'] = case
    browser.submit()


def return_form():

    browser.back()
    case_id_form('24O14000013')


disclaimer_form()
case_id_form('24O14000003')
return_form()

print browser.response().read()
