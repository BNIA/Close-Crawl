"""spider.py

Crawls through the pages to download individual responses to be scraped as
a separate process. The modularization of scraping from crawling ensures
minimal loss of responses and minimizes time spent on the court servers"""

from os import path, makedirs
from random import uniform
from re import compile, IGNORECASE
from time import sleep

from local_browser import *
from settings import HTML_DIR, HTML_FILE


HR_PAT = compile('<HR>', IGNORECASE)

# regex pattern to capture monetary values between $0.00 and $999,999,999.99
# punctuation insensitive
MONEY_PAT = compile('\$\d{,3},?\d{,3},?\d{,3}\.?\d{2}')


CASE_PAT = '24{type}{year}00{num}'


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


def defendant_section(html):

    return all(x in html for x in ['Business or Organization Name:', '$'])


def save_response(case_type, year, bounds=xrange(1, 10)):

    # initial page for terms and agreements upon disclaimer
    disclaimer_form()

    if not path.exists(HTML_DIR):
        makedirs(HTML_DIR)

    for case in bounds:

        case_num = str(('000' + str(case)))[-4:]
        case = CASE_PAT.format(type=case_type, year=year, num=case_num)
        sleep(uniform(0.0, 1.1))

        try:
            print "Crawling", case
            html = case_id_form(case)
            stripped_html = html[0] + html[2]

            business = [s for s in html if defendant_section(s)]

            partial_cost = MONEY_PAT.findall(' '.join(business))

            with open(HTML_FILE.format(case=case) + '.html', 'w') as case_file:
                case_file.write(str(stripped_html))
                if len(partial_cost):
                    case_file.write(partial_cost[0])

        except IndexError:
            with open('stop.txt', 'w') as failed_case:
                failed_case.write(case)
            exit("Case number does not exist")


if __name__ == '__main__':

    save_response('C', '14')
