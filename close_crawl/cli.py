#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""cli

The main command line script for Close Crawl. This file manages types, flags
and constraints for the case type, year and output data file as well as the
processing options.

Parameters:
  {O,C}        | Type of foreclosure cases
  year         | Year of foreclosure cases
  output       | Path of output file

Optional parameters:
  -h, --help   | Show this help message and exit
  -v, --version| Show program's version number and exit
  -l, --lower  | Lower bound of range of cases
  -u, --upper  | Upper bound of range of cases
  -f, --file   | Path of JSON array of cases
  -d, --debug  | Debug mode
  -s, --scrape | Scrape only
  -m, --mine   | Mine only
  -c, --clean  | Clean only

Usage:
    $ python cli.py [-h] [-v] [-l] [-u] [-f] [-d] [-s] [-m] [-c]
                  {O,C} year output

Example usages:
    $ python cli.py -l=50 -u=3500 -d -s -m C 2016 output.csv
    $ python cli.py -c="cases_to_scrape.json" -d O 2014 output01.csv
"""

from __future__ import absolute_import, print_function, unicode_literals
import argparse
import sys

from modules import main
from modules.settings import CASE_TYPES
from _version import __version__

if __name__ == "__main__":

    # manually backspace for formatting help menu
    menu_pad = '\b' * 4

    parser = argparse.ArgumentParser(
        description="The command line interface for Close Crawl",
        add_help=False
    )

    # arguments for details on program
    parser._positionals.title = "Parameters"
    parser._optionals.title = "Optional parameters"
    parser.add_argument(
        "-h", "--help", action="help",
        default=argparse.SUPPRESS,
        help=menu_pad + "| Show this help message and exit"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="Close Crawl {}".format(__version__),
        help=menu_pad + "| Show program's version number and exit"
    )

    # ----- positional arguments -----
    parser.add_argument("type", choices=CASE_TYPES,
                        help=menu_pad + "| Type of foreclosure cases")
    parser.add_argument("year", help=menu_pad + "| Year of foreclosure cases")
    parser.add_argument("output", help=menu_pad + "| Path of output file")

    # ----- optional arguments -----
    # crawling parameters
    parser.add_argument(
        "-l", "--lower", type=int, default=0, metavar="\b",
        help="| Lower bound of range of cases"
    )
    parser.add_argument(
        "-u", "--upper", type=int, default=0, metavar="\b",
        help="| Upper bound of range of cases"
    )
    parser.add_argument(
        "-f", "--file", metavar="\b", help="| Path of JSON array of cases"
    )

    # debug mode
    parser.add_argument(
        "-d", "--debug", action="store_true", help=menu_pad + "| Debug mode"
    )

    # processing options
    parser.add_argument(
        "-s", "--scrape", action="store_false", help=menu_pad + "| Scrape only"
    )
    parser.add_argument(
        "-m", "--mine", action="store_false", help=menu_pad + "| Mine only"
    )
    parser.add_argument(
        "-c", "--clean", action="store_false", help=menu_pad + "| Clean only"
    )

    # parse arguments to pass into function
    args = parser.parse_args()

    # processing options are in inverted logic
    if args.scrape and args.mine and args.clean:
        args.scrape = args.mine = args.clean = False

    # exit script if both range and file of cases or none are selected
    # if case_file xnor (lower_bound and upper_bound)
    if (bool(args.file) == bool(args.lower and args.upper)):
        parser.print_help()
        sys.exit("\nSelect a range or a file of cases (but not both).")

    # exit script if all but the mining step is disabled
    elif (not(args.scrape) and args.mine and not(args.clean)):
        parser.print_help()
        sys.exit("\nData cannot be cleaned without being mined first.")

    main.close_crawl(
        case_type=args.type, case_year=args.year, output=args.output,
        cases=args.file, lower_bound=args.lower, upper_bound=args.upper,
        debug=bool(args.debug), scrape=not(args.scrape), mine=not(args.mine),
        clean=not(args.clean)
    )
