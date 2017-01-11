#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=unused-import

from __future__ import absolute_import, print_function, unicode_literals

from os import path

from .context import modules
from modules import spider
from modules.settings import CASE_PAT, HTML_FILE


def test_crawl():
    """Download responses"""

    case_type = 'O'
    year = "15"
    bounds = range(1, 6)
    spider_obj = spider.Spider(
        case_type=case_type, year=year, bounds=bounds
    )

    spider_obj.save_response()

    case_files = [
        HTML_FILE.format(
            case=CASE_PAT.format(
                type=case_type,
                year=year,
                num='{:04d}'.format(int(str(bounds[case_num])[-4:]))
            ) + ".html")
        for case_num, _ in enumerate(bounds)
    ]

    def files_created():

        for case_file in case_files:
            if not path.exists(case_file):
                return False

        return True

    assert(files_created())
