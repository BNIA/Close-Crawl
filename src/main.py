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
from os import walk
from shutil import rmtree
from time import time

from cleaned_data import CleanedData
from local_browser import anonymize
from miner import export
from settings import HTML_DIR, SAVE_PROG, CHECKPOINT
from spider import save_response


def main(case_type, case_year, output, anonymize_flag=True, debug=True):

    if anonymize_flag:
        anonymize()

    lower_bound = 1

    with open(CHECKPOINT) as checkpoint:
        prev_bound = load(checkpoint)
        if prev_bound:
            lower_bound = int(prev_bound["last_case"][-4:]) + 1

    upper_bound = lower_bound + 499

    start = time()

    wait = save_response(
        case_type, case_year,
        bounds=range(lower_bound, upper_bound + 1), gui=False
    )

    end = time()

    print("Total crawling script runtime: {0:.3f} s".format((end - start)))
    print("Total downloading runtime: {0:.3f} s".format(((end - start) - wait)))

    file_array = [filenames for (dirpath, dirnames, filenames)
                  in walk(HTML_DIR)][0]

    start = time()
    export(file_array, output)
    end = time()

    print("Total mining runtime: {0:.3f} s".format((end - start)))

    df_obj = CleanedData(output)

    df_obj.init_clean()
    df_obj.download("2015_clean.csv")

    with open(CHECKPOINT, 'r+') as checkpoint:
        checkpoint_data = load(checkpoint)
        checkpoint_data["last_case"] = sorted(file_array)[-1][:-5]
        checkpoint.seek(0)
        checkpoint.write(dumps(checkpoint_data))
        checkpoint.truncate()

    if not debug:
        rmtree(HTML_DIR)


if __name__ == '__main__':

    from sys import argv

    case_type = argv[1]
    case_year = argv[2][-2:]
    output = argv[3]

    main(case_type, case_year, output)
