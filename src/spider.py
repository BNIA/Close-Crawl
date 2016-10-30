"""spider.py

Crawls through the pages to download individual responses to be scraped as
a separate process. The modularization of scraping from crawling ensures
minimal loss of responses and minimizes time spent on the court servers"""

from os import path, makedirs
from random import randrange
from re import compile, IGNORECASE
from time import sleep

from local_browser import *
from settings import CASES, HTML_DIR, HTML_FILE


HR_PAT = compile('<HR>', IGNORECASE)


def case_id_form(case):

    for form in browser.forms():
        if form.attrs['name'] == 'inquiryFormByCaseNum':
            browser.form = form
            break

    browser.form['caseId'] = case
    browser.submit()
    response = HR_PAT.split(str(browser.response().read()))
    browser.back()

    return response


def partial_cost(html):

    return all(x in html for x in ['Business or Organization Name:', '$'])


def save_response(case_array):

    # initial page for terms and agreements upon disclaimer
    disclaimer_form()

    if not path.exists(HTML_DIR):
        makedirs(HTML_DIR)

    for case in case_array:

        sleep(randrange(0, 1))

        try:
            print "Crawling", case
            html = case_id_form(case)
            stripped_html = html[0] + html[2]

            business = [
                s for s in html if partial_cost(s)
            ]

            print business

            # TODO: determine category for case types
            if '' in stripped_html.upper():
                with open(
                    HTML_FILE.format(case=case) + '.html', 'w'
                ) as case_file:
                    case_file.write(str(stripped_html))

        except IndexError:
            with open('stop.txt', 'w') as failed_case:
                failed_case.write(case)
            exit("Case number does not exist")


if __name__ == '__main__':

    save_response(CASES)
