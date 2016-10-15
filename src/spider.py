from local_browser import *

print browser.title()

disclaimer_form()


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


# case_id_form('24O14000003')
# return_form()
print browser.response().read()
