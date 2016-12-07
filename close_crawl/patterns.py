#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Patterns

This module implements post-scraping cleaning processes on the raw initial
dataset. Processes include stripping excess strings off Address values,
removing Zip Code and Partial Cost values mislabeled as Address, and merging
rows containing blank values in alternating features.

The script works as an internal module for Close Crawl, but can be executed
as a standalone to manually process datasets:

    $ python cleaned_data.py <path/to/old/dataset> <path/of/new/dataset>

TODO:
    Finish docs

"""


from re import IGNORECASE, compile
from string import punctuation

street_address = compile(
    '(\d{1,4} [\w\s]{1,20}'
    '(?:st(reet)?|ln|lane|ave(nue)?|r(?:oa)?d'
    '|highway|hwy|sq(uare)?|tr(?:ai)l|dr(?:ive)?'
    '|c(?:our)?t|parkway|pkwy|cir(cle)?'
    '|boulevard|blvd|pl(?:ace)?|(apt|unit).[A-Z]{1}|'
    'ter(?:race)?)\W?(?=\s|$))', IGNORECASE)

punctuation = punctuation.replace('#', '')

# case insensitive delimiter for Titles
TITLE_SPLIT_PAT = compile(" vs ", IGNORECASE)

# pattern for Baltimore zip codes
ZIP_PAT = compile("2\d{4}")

# regex pattern to capture monetary values between $0.00 and $999,999,999.99
# punctuation insensitive
MONEY_PAT = compile('\$\d{,3},?\d{,3},?\d{,3}\.?\d{2}')

MONEY_STR = '\$\d{,3},?\d{,3},?\d{,3}\.?\d{2}'

NULL_ADDR = compile(
    '^('
    '(' + MONEY_STR + ')|'
    '(2\d{4})|'
    '(\d+)|'
    '(2\d{4}.*' + MONEY_STR + ')'
    ')$', IGNORECASE)

STRIP_ADDR = compile('(balto|2\d{4}|md|' + MONEY_STR + ').*', IGNORECASE)


def filter_addr(address):

    try:
        return ''.join(
            street_address.search(
                address.translate(None, punctuation)).group(0)
        )

    except AttributeError:
        return ''
