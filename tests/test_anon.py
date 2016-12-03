import cookielib

import mechanize

# Browser
browser = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
browser.set_cookiejar(cj)
HEADER = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'

# Browser options
browser.set_handle_equiv(True)
browser.set_handle_gzip(True)
browser.set_handle_redirect(True)
browser.set_handle_referer(True)
browser.set_handle_robots(False)


def anonymize():

    import socks
    import socket

    socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5,
                          addr="127.0.0.1", port=9050)

    socket.socket = socks.socksocket

    print browser.open("http://icanhazip.com").read()
    # browser.close()


# Follows refresh 0 but not hangs on refresh > 0
browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent
browser.addheaders = [('User-agent', HEADER)]


anonymize()

# visit the site
print browser.open("http://www.google.com").read()
print browser.open("http://icanhazip.com").read()
