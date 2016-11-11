"""spider.py

Crawls through the pages to download individual responses to be scraped as
a separate process. The modularization of scraping from crawling ensures
minimal loss of responses and minimizes time spent on the court servers"""

from os import path, makedirs
from random import uniform
from re import compile, IGNORECASE
from time import sleep

from tqdm import trange

from local_browser import *
from settings import CASE_PAT
from settings import CASE_ERR, HTML_DIR, HTML_FILE, SAVE_PROG

HR_PAT = compile('<HR>', IGNORECASE)
H6_PAT = compile('<H6>', IGNORECASE)


def mine_filter(response):

    # TODO: FIX DUPLICATE ADDRESS ISSUE
    filtered_response = H6_PAT.split(response)
    split_response = ' '.join(HR_PAT.split(filtered_response[1])[1:])

    return filtered_response[0] + split_response


def case_id_form(case):

    for form in browser.forms():
        if form.attrs['name'] == 'inquiryFormByCaseNum':
            browser.form = form
            break

    browser.form['caseId'] = case
    browser.submit()
    response = mine_filter(browser.response().read())
    browser.back()

    return response


def defendant_section(html):

    return all(x in html for x in ['Business or Organization Name:', '$'])


def save_response(case_type, year, bounds=xrange(1, 15), gui=False):

    # initial page for terms and agreements upon disclaimer
    disclaimer_form()
    WAITING_TIME = 0

    if not path.exists(HTML_DIR):
        makedirs(HTML_DIR)

    case_range = trange(bounds[-1] - bounds[0], desc='Crawling', leave=True
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

            stripped_html = case_id_form(case)

            with open(HTML_FILE.format(case=case) + '.html', 'w') as case_file:
                case_file.write(str(stripped_html))

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

    save_response('O', '15')
