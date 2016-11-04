"""spider.py

Crawls through the pages to download individual responses to be scraped as
a separate process. The modularization of scraping from crawling ensures
minimal loss of responses and minimizes time spent on the court servers"""

from os import path, makedirs
from random import uniform
from re import compile, IGNORECASE
from time import sleep, time

from tqdm import trange

from local_browser import *
from settings import CASE_PAT
from settings import CASE_ERR, HTML_DIR, HTML_FILE, SAVE_PROG

HR_PAT = compile('<HR>', IGNORECASE)

# regex pattern to capture monetary values between $0.00 and $999,999,999.99
# punctuation insensitive
MONEY_PAT = compile('\$\d{,3},?\d{,3},?\d{,3}\.?\d{2}')


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


def get_duration():

    return WAITING_TIME


def save_response(case_type, year, bounds=xrange(1, 10), gui=False):

    # initial page for terms and agreements upon disclaimer
    disclaimer_form()
    WAITING_TIME = 0

    if not path.exists(HTML_DIR):
        makedirs(HTML_DIR)

    case_range = trange(max(bounds), desc='Crawling', leave=True
                        ) if not gui else bounds

    for case_num in case_range:

        case = CASE_PAT.format(
            type=case_type, year=year, num=('000' + str(bounds[case_num]))[-4:]
        )

        try:

            wait = uniform(0.0, 0.5)
            sleep(wait)

            WAITING_TIME += wait

            if not gui:
                case_range.set_description("Crawling {}".format(case))

            html = case_id_form(case)
            stripped_html = html[0] + html[2]

            business = [s for s in html if defendant_section(s)]

            partial_cost = MONEY_PAT.findall(' '.join(business))

            with open(HTML_FILE.format(case=case) + '.html', 'w') as case_file:
                case_file.write(str(stripped_html))
                if len(partial_cost):
                    case_file.write(partial_cost[0])

        except KeyboardInterrupt:
            with open(SAVE_PROG, 'w') as save_file:
                save_file.write(case)
            print 'Crawling paused at', case
            break

        except IndexError:
            with open(CASE_ERR, 'w') as failed_case:
                failed_case.write(case)
            exit("Case number does not exist")

    return WAITING_TIME


if __name__ == '__main__':

    start = time()
    save_response('O', '15')
    end = time()

    print (end - start)
