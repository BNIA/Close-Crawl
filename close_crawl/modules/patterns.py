#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Patterns

Regular expression patterns and string filtering functions implemented in the
project. This file is intended to only be used as a non-executable script.

TODO:
    Finish docs
"""

from re import compile as re_compile
from re import I as IGNORECASE
from string import punctuation

PUNCTUATION = punctuation.replace('#', '')  # all punctuations except '#'

street_address = re_compile(
    "("  # begin regex group
    "\d{1,4}\s"  # house number
    "[\w\s]{1,20}"  # street name
    "("  # start street type group
    "(?:st(reet)?|ln|lane|ave(nue)?"  # (st)reet, lane, ln, (ave)nue
    "|r(?:oa)?d|highway|hwy|dr(?:ive)?"  # rd, road, hwy, highway, (dr)ive
    "|sq(uare)?|tr(?:ai)l|c(?:our)?t"  # (sq)uare, (tr)ail, ct, court
    "|parkway|pkwy|cir(cle)?|ter(?:race)?"  # parkway, pkwy, (cir)cle, (ter)race
    "|boulevard|blvd|pl(?:ace)?"  # boulevard, bvld, (pl)ace
    "\W?(?=\s|$))"  # look ahead for whitespace or end of string
    ")"  # end street type group
    "(\s(apt|block|unit)(\W|#)?([\d|\D|#-|\W])+)?"  # apt, block, unit number
    ")",  # end regex group
    IGNORECASE  # case insensitive flag
)

# case insensitive delimiter for Titles
TITLE_SPLIT_PAT = re_compile(" vs ", IGNORECASE)

# pattern for Baltimore zip codes
ZIP_STR = "2\d{4}"
ZIP_PAT = re_compile(ZIP_STR)

# regex pattern to capture monetary values between $0.00 and $999,999,999.99
# punctuation insensitive
MONEY_STR = "\$\d{,3},?\d{,3},?\d{,3}\.?\d{2}"
MONEY_PAT = re_compile(MONEY_STR)

NULL_ADDR = re_compile(
    "^("
    "(" + MONEY_STR + ")"
    "|(" + ZIP_STR + ")"
    "|(\d+)"
    "|(" + ZIP_STR + ".*" + MONEY_STR + ")"
    ")$",
    IGNORECASE
)

STRIP_ADDR = re_compile(
    "(balto|" + ZIP_STR + "|md|" + MONEY_STR + ").*",
    IGNORECASE
)


def filter_addr(address):

    try:
        return ''.join(
            street_address.search(
                address.translate(None, PUNCTUATION)).group(0)
        )

    except AttributeError:
        return ''


"""
(\d{1,4}\s[\w\s]{1,20}((?:st(reet)?|ln|lane|ave(nue)?|r(?:oa)?d|highway|hwy|
dr(?:ive)?|sq(uare)?|tr(?:ai)l|c(?:our)?t|parkway|pkwy|cir(cle)?|ter(?:race)?|
boulevard|blvd|pl(?:ace)?)\W?(?=\s|$))(\s(apt|block|unit)\W?([A-Z]|\d+))?)
"""
