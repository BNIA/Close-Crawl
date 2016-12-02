#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""main

The main executible script for Close Crawl. This file manages types, flags
and constraints for the case type, year and output data file.

    $ python main.py <case_type> <case_year> <path/of/new/dataset>
      <opt: anonymize_flag> <opt: debug>

TODO:
    Finish docs

"""

from __future__ import absolute_import, print_function, unicode_literals
from json import dumps, load
from os import remove, walk
from shutil import rmtree
from time import time

from cleaned_data import CleanedData
from local_browser import Session
from miner import export
from settings import HTML_DIR, CHECKPOINT
from spider import Spider


def main(case_type, case_year, output, anonymize_flag=True, debug=True):
    """Main function for Close Crawl.

    Usage:
        $ python main.py <case_type> <case_year> <path/of/new/dataset>
          <opt: anonymize_flag> <opt: debug>

    Example usage:
        $ python main.py O 2015 test_set.csv 0 1

    Args:
        case_type (`str`): type of foreclosure case, options are 'O' and 'C'
        case_year (`str`): year of foreclosure cases
        output (`str`): path of the output CSV file, along with the valid
            extension (.csv)
        anonymize_flag (`bool`, optional): option to spoof IP address for
            scraping. Default -> True.
            WARNING: THIS OPTION IS HIGHLY DEPENDANT ON TYPE OF MACHINE AND
            SEVERAL SYSTEM DEPENDANCIES AND REQUIREMENTS, POSSIBLY REQUIRES
            THIRD PARTY SECURED BROWSERS SUCH AS TOR. THIS OPTION HAS ONLY BEEN
            TESTED ON LINUX DISTROS. WINDOWS MACHINES HAVE NOT BEEN TESTED.
        debug (`bool`, optional): option for switching between debug mode.
            Default -> True

    Returns:
        None
    """

    start = time()

    if anonymize_flag:
        Session().anonymize()

    lower_bound = 1
    temp_output = "temp_data.csv"

    with open(CHECKPOINT) as checkpoint:
        prev_bound = load(checkpoint)
        if prev_bound:
            lower_bound = int(prev_bound["last_case"][-4:]) + 1

    upper_bound = lower_bound + 499

    start_crawl = time()

    spider = Spider(
        case_type, case_year,
        bounds=range(lower_bound, upper_bound + 1), gui=False
    )

    spider.save_response()

    wait = spider.WAITING_TIME

    end_crawl = time()

    file_array = [filenames for (dirpath, dirnames, filenames)
                  in walk(HTML_DIR)][0]

    start_mine = time()
    export(file_array, temp_output)
    end_mine = time()

    df_obj = CleanedData(temp_output)

    df_obj.init_clean()
    df_obj.download(output)

    with open(CHECKPOINT, 'r+') as checkpoint:
        checkpoint_data = load(checkpoint)
        checkpoint_data["last_case"] = sorted(file_array)[-1][:-5]
        checkpoint.seek(0)
        checkpoint.write(dumps(checkpoint_data))
        checkpoint.truncate()

    if not debug:
        remove(temp_output)
        rmtree(HTML_DIR)

    end = time()

    print("Crawling runtime: {0:.3f} s".format((end_crawl - start_crawl)))
    print(
        "Downloading runtime: {0:.3f} s".format(
            ((end_crawl - start_crawl) - wait))
    )
    print("Mining runtime: {0:.3f} s".format((end_mine - start_mine)))
    print("Program runtime: {0:.3f} s".format((end - start)))


if __name__ == '__main__':

    from sys import argv

    if len(argv) > 3 and len(argv) < 7:
        case_type = argv[1]
        case_year = argv[2][-2:]
        output = argv[3]
        anonymize_flag = 1
        debug = 1

        if len(argv) > 4:
            anonymize_flag = bool(argv[4])

            if len(argv) == 6:
                debug = bool(argv[5])

        main(case_type, case_year, output, anonymize_flag, debug)

    else:
        print("Invalid usage of script.\n")
        print(main.__doc__)
