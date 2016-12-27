#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""settings

Configuration settings and global variables for the entire project. This file
is intended to only be used as a non-executable script.
"""

from os import path

# browser settings
HEADER = ("Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1)"
          " Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1")
URL = "http://casesearch.courts.state.md.us/casesearch//inquiry-index.jsp"
CASE_PAT = "24{type}{year}00{num}"

# temporary directory settings
HTML_DIR = "responses"
HTML_FILE = path.join(HTML_DIR, "{case}")

# log file settings
CHECKPOINT = "checkpoint.json"
NO_CASE = "no_case.json"

# data mining settings
FEATURES = [
    "Filing Date",
    "Case Number",
    "Case Type",
    "Title",
    "Plaintiff",
    "Defendant",
    "Address",
    "Business or Organization Name",
    "Party Type",
]

FIELDS = FEATURES + [
    "Zip Code",
    "Partial Cost",
]

INTERNAL_FIELDS = [
    "Business or Organization Name",
    "Party Type",
]


# front end form settings
CASE_TYPE = [
    ('O', "Mortgage"),
    ('C', "Tax"),
]

CASE_YEAR = [(str(year)[-2:], year) for year in range(2016, 2009, -1)]
