from os import walk
from shutil import rmtree
from time import time

from clean_db import sort_set
from settings import HTML_DIR, SAVE_PROG
from miner import export
from spider import save_response

if __name__ == '__main__':

    # output = 'mortgage_2015.csv'
    output = 'test_out.csv'

    lower_bound = 0

    upper_bound = 1501
    case_type = 'O'
    case_year = '15'

    with open(SAVE_PROG, 'r') as checkpoint:
        lower_bound = int(checkpoint.read()[-4:]) + 1

    start = time()

    wait = save_response(
        case_type, case_year,
        bounds=xrange(lower_bound, upper_bound), gui=False
    )

    end = time()

    print "Total script runtime: {0:.3f} s".format((end - start))
    print "Total crawling runtime: {0:.3f} s".format(((end - start) - wait))

    file_array = [filenames for (dirpath, dirnames, filenames)
                  in walk(HTML_DIR)][0]

    export(file_array, output)
    sort_set(output)

    with open(SAVE_PROG, 'w') as checkpoint:
        checkpoint.write(sorted(file_array)[-1][:-5])

    # rmtree(HTML_DIR)
