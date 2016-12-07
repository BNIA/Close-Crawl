#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""settings

Configuration settings and variables for the project
"""

HEADER = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
URL = 'http://casesearch.courts.state.md.us/casesearch//inquiry-index.jsp'
CASE_PAT = '24{type}{year}00{num}'

HTML_DIR = 'responses/'
HTML_FILE = HTML_DIR + '{case}'

LOG_DIR = 'logs/{}.txt'
CASE_ERR = LOG_DIR.format('invalid_case')
SAVE_PROG = LOG_DIR.format('checkpoint')
CHECKPOINT = "checkpoint.json"
NO_CASE = "no_case.json"

FEATURES = [
    'Filing Date',
    'Case Number',
    'Case Type',
    'Title',
    'Plaintiff',
    'Defendant',
    'Address',
    'Business or Organization Name',
    'Party Type',
]

FIELDS = FEATURES + [
    'Zip Code',
    'Partial Cost',
]

INTERNAL_FIELDS = [
    'Business or Organization Name',
    'Party Type',
]
