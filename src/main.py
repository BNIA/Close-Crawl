#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""main

The main executible script for Close Crawl. This file manages types, flags
and constraints for the case type, year and output data file.

    $ python main.py <case_type> <case_year> <path/of/new/dataset>
      <opt: anonymize> <opt: debug>

TODO:
    Finish docs

"""

from __future__ import absolute_import, print_function, unicode_literals
from json import dump, dumps, load
from os import path, remove, walk
from shutil import rmtree
from time import time

from cleaned_data import CleanedData
from miner import export
from settings import CASE_PAT, CHECKPOINT, HTML_DIR
from spider import Spider


def main(case_type, case_year, output, lower_bound=1, upper_bound=500,
         anonymize=True, debug=True):
    """Main function for Close Crawl.

    Usage:
        $ python main.py <case_type> <case_year> <path/of/new/dataset>
          <opt: lower_bound> <opt: upper_bound>
          <opt: anonymize> <opt: debug>

    Example usage:
        $ python main.py O 2015 test_set.csv 300 600 0 1

    Args:
        case_type (`str`): type of foreclosure case, options are 'O' and 'C'
        case_year (`str`): year of foreclosure cases
        output (`str`): path of the output CSV file, along with the valid
            extension (.csv)
        anonymize (`bool`, optional): option to spoof IP address for
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

    temp_output = "temp_data.csv"

    if not path.isfile(CHECKPOINT):
        with open(CHECKPOINT, 'w') as checkpoint:
            data = {
                'last_case': CASE_PAT.format(
                    type=case_type, year=case_year,
                    num=('000' + str(lower_bound))[-4:]
                ),
                'error_case': ''
            }
            dump(data, checkpoint)

    with open(CHECKPOINT) as checkpoint:
        prev_bound = load(checkpoint)
        if prev_bound:
            lower_bound = int(prev_bound["last_case"][-4:])

    start_crawl = time()

    spider = Spider(
        case_type, case_year,
        bounds=range(lower_bound, upper_bound + 1),
        anonymize=anonymize, gui=False
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

    from sys import argv, exit

    if len(argv) > 3 and len(argv) < 9:
        case_type = argv[1]
        case_year = argv[2][-2:]
        output = argv[3]
        lower_bound = 1
        upper_bound = 500
        anonymize = 1
        debug = 1

        try:
            if len(argv) > 4:
                lower_bound = int(argv[4])

                if len(argv) > 5:
                    upper_bound = int(argv[5])

                    if len(argv) > 6:
                        anonymize = bool(argv[6])

                        if len(argv) == 8:
                            upper_bound = bool(argv[7])

            main(case_type, case_year, output, lower_bound, upper_bound,
                 anonymize, debug)

        except ValueError:
            exit("Please provide valid command line input.")

    else:
        exit("Invalid usage of script.\n" + main.__doc__)
