#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""main

The main executable script for Close Crawl. This file manages types, flags
and constraints for the case type, year and output data file.

Usage:
    $ python main.py <case_type> <case_year> <path/of/new/dataset>
      <opt: lower_bound> <opt: upper_bound> <opt: debug>

Example usage:
    $ python main.py O 2015 test_set.csv -l=300 -u=600 -d=1

"""

from __future__ import absolute_import, print_function, unicode_literals
from json import dump, dumps, load
from os import path, remove, walk
from shutil import rmtree
from time import time

from .cleaner import Cleaner
from .miner import Miner
from .settings import CHECKPOINT, HTML_DIR
from .spider import Spider


def close_crawl(case_type, case_year, output, cases='', lower_bound=0,
                upper_bound=0, debug=False, scrape=True, mine=True,
                clean=True):
    """Main function for Close Crawl.

    Args:
        case_type (`str`): type of foreclosure case, options are 'O' and 'C'
        case_year (`str`): year of foreclosure cases
        output (`str`): path of the output CSV file, along with the valid
            extension (.csv)
        lower_bound (`int`, optional): lower bound of range of cases
        upper_bound (`int`, optional): upper bound of range of cases
        debug (`bool`, optional): option for switching between debug mode.
            Default -> True

    Returns:
        None
    """

    start = time()

    temp_output = "temp_data.csv"
    case_list = []

    if not path.isfile(CHECKPOINT):
        print("Initializing project...")
        with open(CHECKPOINT, "w") as checkpoint:
            dump(
                {
                    "last_case": "{:04d}".format(int(str(lower_bound)[-4:])),
                    "type": case_type,
                    "year": case_year[-2:],
                    "error_case": '',
                },
                checkpoint
            )

    if not cases:

        with open(CHECKPOINT) as checkpoint:
            prev_bound = int(load(checkpoint)["last_case"])
            if not lower_bound:
                lower_bound = prev_bound
            upper_bound = upper_bound if int(upper_bound) > int(lower_bound) \
                else str(lower_bound + 5)

        case_list = range(int(lower_bound), int(upper_bound) + 1)

    else:

        with open(cases) as manual_cases:
            case_list = list(load(manual_cases))

    start_crawl = time()

    if scrape:
        spider = Spider(
            case_type=case_type, year=case_year[-2:],
            bounds=case_list, gui=False
        )

        spider.save_response()

    wait = spider.WAITING_TIME

    end_crawl = time()

    file_array = [filenames for (dirpath, dirnames, filenames)
                  in walk(HTML_DIR)][0]

    start_mine = time()

    if mine:
        miner = Miner(file_array, temp_output)
        miner.scan_files()
        miner.export()

    end_mine = time()

    if clean:
        df_obj = Cleaner(temp_output)

        df_obj.init_clean()
        df_obj.download(output)

    with open(CHECKPOINT, "r+") as checkpoint:
        checkpoint_data = load(checkpoint)
        checkpoint_data["last_case"] = sorted(file_array)[-1].split('.')[0][-4:]
        checkpoint.seek(0)
        checkpoint.write(dumps(checkpoint_data))
        checkpoint.truncate()

    if not debug:
        remove(temp_output)
        rmtree(HTML_DIR)

    end = time()

    print("Crawling runtime: {0:.2f} s".format((end_crawl - start_crawl)))
    print(
        "Downloading runtime: {0:.2f} s".format(
            ((end_crawl - start_crawl) - wait))
    )
    print("Mining runtime: {0:.2f} s".format((end_mine - start_mine)))
    print("Program runtime: {0:.2f} s".format((end - start)))
    print("------------ SCRAPING COMPLETED ------------")
