"""Example app to login to GitHub"""
import http.cookiejar

import mechanicalsoup

from settings import URL

browser = mechanicalsoup.Browser()


# def case_id_form(case):

#     for form in browser.forms():
#         if form.attrs['name'] == 'inquiryFormByCaseNum':
#             browser.form = form
#             break

#     browser.form['caseId'] = case
#     browser.submit()
#     response = browser.response().read()
#     browser.back()

#     return response

browser = mechanicalsoup.Browser()
login_page = browser.get(URL)
login_form = mechanicalsoup.Form(login_page.soup.form)
login_form.check({"disclaimer": ['Y']})

response = browser.submit(login_form, URL)
print(response.soup)
