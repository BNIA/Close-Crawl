#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""cli

The main command line script for Close Crawl. This file manages types, flags
and constraints for the case type, year and output data file as well as the
processing options.

Usage:
    $ python cli.py
"""

from __future__ import absolute_import, print_function, unicode_literals
import sys
from textwrap import dedent

from modules import main

if __name__ == "__main__":

    args = {}

    args["type"] = input("Enter type of case (1 char: {C, O}): ")
    args["year"] = input("Enter year of case (4 digit int): ")
    args["output"] = input("Enter name of output file (CSV file path): ")

    opt = int(input("Enter 0 for manual parameters or 1 for automatic: "))
    if bool(opt):
        args["file"] = input("Enter name of cases file (JSON file path): ")
        args["lower"] = args["upper"] = 0

    else:
        args["file"] = ""
        args["lower"] = input("Enter lower bound of cases (1-4 digit int): ")
        args["upper"] = input("Enter upper bound of cases (1-4 digit int): ")

    args["debug"] = input(
        "Enter 0 for default mode, 1 for debug (1 digit int): "
    )

    print(
        dedent(
            """Processing options:\n\n"""
            """For the following options, enter 0 to disable or 1 to enable."""
            """\nNOTE: The script will exit if all but the mining step is """
            """enabled - data cannot be cleaned without being mined first."""
        )
    )

    args["scrape"] = bool(input("Scrape: {0, 1}: "))
    args["mine"] = bool(input("Mine: {0, 1}: "))
    args["clean"] = bool(input("Clean: {0, 1}: "))

    # exit script if all but the mining step is enabled
    if (args["scrape"] and not(args["mine"]) and args["clean"]):
        sys.exit("\nData cannot be cleaned without being mined first.")

    main.close_crawl(
        case_type=args["type"], case_year=args["year"], output=args["output"],
        cases=args["file"], lower_bound=args["lower"],
        upper_bound=args["upper"], debug=args["debug"],
        scrape=args["scrape"], mine=args["mine"],
        clean=args["clean"]
    )
