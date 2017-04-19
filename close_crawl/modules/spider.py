#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Spider

This module crawls through the pages to download individual responses to be
scraped as a separate process. The modularization of scraping from crawling
ensures minimal loss of responses and minimizes time spent on the court servers


TODO:
    Finish docs


"""

from __future__ import absolute_import, print_function, unicode_literals
from json import dumps, load
from os import path, makedirs
from random import uniform
from sys import stdout
from time import sleep

from tqdm import trange

from .local_browser import Session
from .settings import CASE_PAT, CHECKPOINT, HTML_DIR, HTML_FILE


class Spider(object):

    def __init__(self, case_type, year, bounds=range(1, 6), gui=False):

        # initial disclaimer page for terms and agreements
        self.browser = Session()

        self.browser.disclaimer_form()

        self.WAITING_TIME = 0
        self.case_type = case_type
        self.year = year
        self.bounds = bounds

        if not path.exists(HTML_DIR):
            makedirs(HTML_DIR)

    def save_response(self):

        case_range = trange(
            len(self.bounds), desc='Crawling', leave=True
        )

        for case_num in case_range:

            if case_num and not case_num % 500:
                print("500 CASES SCRAPED. SCRIPT WILL WAIT 5 MINUTES TO RESUME")

                for i in range(300, 0, -1):
                    sleep(1)
                    stdout.write('\r' + "%02d:%02d" % divmod(i, 60))
                    stdout.flush()

            case = CASE_PAT.format(
                type=self.case_type,
                year=self.year,
                num='{:04d}'.format(int(str(self.bounds[case_num])[-4:]))
            )

            try:

                wait = uniform(0.0, 0.5)
                sleep(wait)

                self.WAITING_TIME += wait

                case_range.set_description("Crawling {}".format(case))

                stripped_html = self.browser.case_id_form(case)

                if stripped_html:
                    with open(
                        HTML_FILE.format(case=case) + '.html', 'w'
                    ) as case_file:
                        case_file.write(str(stripped_html))

            # pause process
            except KeyboardInterrupt:

                self.dump_json({
                    "error_case":
                        '{:04d}'.format(int(str(self.bounds[case_num])[-4:])),
                        "year": self.year,
                        "type": self.type
                })
                print('Crawling paused at', case)
                break

            # case does not exist
            except IndexError:

                self.dump_json({"error_case": case})
                print(case, "does not exist")
                break

        # close browser and end session
        self.close_sesh()

    @staticmethod
    def dump_json(data):

        with open(CHECKPOINT, 'r+') as checkpoint:
            checkpoint_data = load(checkpoint)

            for key, val in data.items():
                checkpoint_data[key] = val

            checkpoint_data[key] = data
            checkpoint.seek(0)
            checkpoint.write(dumps(checkpoint_data))
            checkpoint.truncate()

    def close_sesh(self):

        self.browser.close()
