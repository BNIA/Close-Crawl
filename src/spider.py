#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Spider

This module crawls through the pages to download individual responses to be
scraped as a separate process. The modularization of scraping from crawling
ensures minimal loss of responses and minimizes time spent on the court servers

The script works as an internal module for Close Crawl, but can be executed
as a standalone to manually process datasets:

    $ python cleaned_data.py <path/to/old/dataset> <path/of/new/dataset>

TODO:
    Finish docs


"""

from __future__ import absolute_import, print_function, unicode_literals
from json import dumps, load
from os import path, makedirs
from random import uniform
from time import sleep

from tqdm import trange

from local_browser import Session
from settings import CASE_PAT, CHECKPOINT, HTML_DIR, HTML_FILE


class Spider(object):

    def __init__(self, case_type, year, bounds=range(1, 15),
                 anonymize=False, gui=False):

        # initial disclaimer page for terms and agreements
        self.browser = Session()

        if anonymize:
            self.browser.anonymize()

        self.browser.disclaimer_form()

        self.WAITING_TIME = 0
        self.case_type = case_type
        self.year = year
        self.bounds = bounds
        self.gui = gui

        if not path.exists(HTML_DIR):
            makedirs(HTML_DIR)

    def save_response(self):

        case_range = trange(
            self.bounds[-1] - self.bounds[0] + 1, desc='Crawling', leave=True
        ) if not self.gui else self.bounds

        for case_num in case_range:

            case = CASE_PAT.format(
                type=self.case_type,
                year=self.year,
                num=('000' + str(self.bounds[case_num]))[-4:]
            )

            try:

                wait = uniform(0.0, 0.5)
                sleep(wait)

                self.WAITING_TIME += wait

                if not self.gui:
                    case_range.set_description("Crawling {}".format(case))

                stripped_html = self.browser.case_id_form(case)

                with open(
                    HTML_FILE.format(case=case) + '.html', 'w'
                ) as case_file:
                    case_file.write(str(stripped_html))

            # pause process
            except KeyboardInterrupt:
                with open(CHECKPOINT, 'r+') as checkpoint:
                    checkpoint_data = load(checkpoint)
                    checkpoint_data["last_case"] = case
                    checkpoint.seek(0)
                    checkpoint.write(dumps(checkpoint_data))
                    checkpoint.truncate()

                print('Crawling paused at', case)
                break

            # case does not exist
            except IndexError:
                with open(CHECKPOINT, 'r+') as checkpoint:
                    checkpoint_data = load(checkpoint)
                    checkpoint_data["error_case"] = case
                    checkpoint.seek(0)
                    checkpoint.write(dumps(checkpoint_data))
                    checkpoint.truncate()

                print(case, "does not exist")
                break

        # close browser and end session
        self.browser.close()


if __name__ == '__main__':

    Session().anonymize()
    Spider('O', '15').save_response()
