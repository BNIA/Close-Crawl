"""spider

Crawls through the pages to download individual responses to be scraped as
a separate process. The modularization of scraping from crawling ensures
minimal loss of responses and minimizes time spent on the court servers"""

from os import path, makedirs
from random import randrange
from time import sleep

from local_browser import *
from settings import CASES, HTML_DIR, HTML_FILE


def case_id_form(case):

    for form in browser.forms():
        if form.attrs['name'] == 'inquiryFormByCaseNum':
            browser.form = form
            break

    browser.form['caseId'] = case
    browser.submit()
    response = str(browser.response().read()).upper().split('<HR>')
    browser.back()

    return response


def save_response(case_array):

    # initial page for terms and agreements upon disclaimer
    disclaimer_form()

    if not path.exists(HTML_DIR):
        makedirs(HTML_DIR)

    for case in case_array:
        sleep(randrange(0, 3))
        html = case_id_form(case)
        stripped_html = html[0] + html[2]

        if 'FORECLOSURE' in stripped_html:
            with open(HTML_FILE.format(case=case) + '.html', 'w') as case_file:
                case_file.write(str(stripped_html))


if __name__ == '__main__':

    save_response(CASES)
