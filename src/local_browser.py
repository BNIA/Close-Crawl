import cookielib

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


def anonymize():

    import socks
    import socket

    for i in xrange(5):
        socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5,
                              addr="127.0.0.1", port=9050)

        socket.socket = socks.socksocket

        print browser.open("http://icanhazip.com").read()


# Follows refresh 0 but not hangs on refresh > 0
browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# # Want debugging messages?
# browser.set_debug_http(True)
# browser.set_debug_redirects(True)
# browser.set_debug_responses(True)

# User-Agent
browser.addheaders = [('User-agent', HEADER)]

# visit the site
browser.open(URL)


def disclaimer_form():

    # Select the first (index zero) form
    browser.select_form(nr=0)

    # Let's search
    browser.form['disclaimer'] = ['Y']
    browser.submit()
