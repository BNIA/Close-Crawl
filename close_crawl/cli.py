#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""close_crawl_cli

The main executible script for Close Crawl. This file manages types, flags
and constraints for the case type, year and output data file.

Usage:
    $ python main.py <case_type> <case_year> <path/of/new/dataset>
      <opt: lower_bound> <opt: upper_bound> <opt: debug>

Example usage:
    $ python main.py O 2015 test_set.csv -l=300 -u=600 -d=1

"""

from __future__ import absolute_import, print_function, unicode_literals
import argparse

from modules import main
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

    # positional arguments
    parser.add_argument("type", help=menu_pad + "| Type of foreclosure cases")
    parser.add_argument("year", help=menu_pad + "| Year of foreclosure cases")
    parser.add_argument("output", help=menu_pad + "| Path of output file")

    # optional arguments

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
        "-c", "--cases", metavar="\b", help="| Path of JSON array of cases"
    )

    # debug mode
    parser.add_argument(
        "-d", "--debug", type=int, default=1, metavar="\b", help="| Debug mode"
    )

    # processing options
    parser.add_argument(
        "--scrape", action="store_false", help=menu_pad + "| Scrape only"
    )
    parser.add_argument(
        "--mine", action="store_false", help=menu_pad + "| Mine only"
    )
    parser.add_argument(
        "--clean", action="store_false", help=menu_pad + "| Clean only"
    )

    # parse arguments to pass into function
    args = parser.parse_args()

    main.close_crawl(
        case_type=args.type, case_year=args.year, output=args.output,
        cases=args.cases, lower_bound=args.lower, upper_bound=args.upper,
        debug=bool(args.debug), scrape=not(args.scrape), mine=not(args.mine),
        clean=not(args.clean)
    )
