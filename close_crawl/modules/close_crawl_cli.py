#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""close_crawl_cli

The main executible script for Close Crawl. This file manages types, flags
and constraints for the case type, year and output data file.

Usage:
    $ python main.py <case_type> <case_year> <path/of/new/dataset>
      <opt: lower_bound> <opt: upper_bound>
      <opt: anon> <opt: debug>

Example usage:
    $ python main.py O 2015 test_set.csv -l=300 -u=600 -a=0 -d=1

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


def main(case_type, case_year, output, cases='',
         lower_bound=0, upper_bound=0, anon=False, debug=False):
    """Main function for Close Crawl.

    Args:
        case_type (`str`): type of foreclosure case, options are 'O' and 'C'
        case_year (`str`): year of foreclosure cases
        output (`str`): path of the output CSV file, along with the valid
            extension (.csv)
        lower_bound (`int`, optional): lower bound of range of cases
        upper_bound (`int`, optional): upper bound of range of cases
        anon (`bool`, optional): option to spoof IP address for
            scraping. Default -> True
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
    case_list = []

    if not path.isfile(CHECKPOINT):
        print("Initializing project...")
        with open(CHECKPOINT, 'w') as checkpoint:
            dump(
                {
                    'last_case': '{:04d}'.format(int(str(lower_bound)[-4:])),
                    'type': case_type,
                    'year': case_year,
                    'error_case': '',
                },
                checkpoint
            )

    if not cases:

        with open(CHECKPOINT) as checkpoint:
            prev_bound = int(load(checkpoint)['last_case'])
            if not lower_bound:
                lower_bound = prev_bound
            upper_bound = upper_bound if upper_bound > lower_bound \
                else str(int(lower_bound) + 500)

        case_list = range(int(lower_bound), int(upper_bound) + 1)

    else:

        with open(cases) as manual_cases:
            case_list = list(load(manual_cases))

    start_crawl = time()

    spider = Spider(
        case_type=case_type, year=case_year,
        bounds=case_list, anonymize=anon, gui=False
    )

    spider.save_response()

    wait = spider.WAITING_TIME

    end_crawl = time()

    file_array = [filenames for (dirpath, dirnames, filenames)
                  in walk(HTML_DIR)][0]

    start_mine = time()
    miner = Miner(file_array, temp_output)
    miner.scan_files()
    miner.export()
    end_mine = time()

    df_obj = Cleaner(temp_output)

    df_obj.init_clean()
    df_obj.download(output)

    with open(CHECKPOINT, 'r+') as checkpoint:
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


if __name__ == '__main__':

    from _version import __version__

    import argparse

    # manually backspace for formatting help menu
    menu_pad = '\b' * 4

    parser = argparse.ArgumentParser(
        description="The main executible script for Close Crawl",
        add_help=False
    )

    # arguments for details on program
    parser._positionals.title = 'Parameters'
    parser._optionals.title = 'Optional parameters'
    parser.add_argument(
        '-h', '--help', action='help',
        default=argparse.SUPPRESS,
        help=menu_pad + '| Show this help message and exit'
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='Close Crawl {}'.format(__version__),
        help=menu_pad + "| Show program's version number and exit"
    )

    # positional arguments
    parser.add_argument('type', help=menu_pad + '| Type of foreclosure cases')
    parser.add_argument('year', help=menu_pad + '| Year of foreclosure cases')
    parser.add_argument('output', help=menu_pad + '| Path of output file')

    # optional arguments
    parser.add_argument(
        '-l', '--lower', type=int, default=0, metavar='\b',
        help='| Lower bound of range of cases'
    )
    parser.add_argument(
        '-u', '--upper', type=int, default=0, metavar='\b',
        help='| Upper bound of range of cases'
    )
    parser.add_argument(
        '-c', '--cases', metavar='\b', help='| Path of JSON array of cases'
    )
    parser.add_argument(
        '-a', '--anon', type=int, default=1, metavar='\b',
        help='| Spoof IP address during crawling'
    )
    parser.add_argument(
        '-d', '--debug', type=int, default=1, metavar='\b', help='| Debug mode'
    )

    # parse arguments to pass into function
    args = parser.parse_args()
    main(args.type, args.year, args.output, args.cases,
         args.lower, args.upper, bool(args.anon), bool(args.debug))
