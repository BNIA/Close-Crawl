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

    disclaimer_form()

    if not path.exists(HTML_DIR):
        makedirs(HTML_DIR)

    for case in case_array:
        sleep(randrange(0, 3))
        html = case_id_form(case)
        stripped_html = html[0] + html[2]
        with open(HTML_FILE.format(case=case), 'w') as case_file:
            case_file.write(str(stripped_html))


save_response(CASES)
