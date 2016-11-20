from os import walk
from shutil import rmtree
from time import time

from clean_db import load, download
from settings import HTML_DIR, SAVE_PROG
from miner import export
from spider import save_response

if __name__ == '__main__':

    output = '2014.csv'

    lower_bound = 1

    case_type = 'O'
    case_year = '14'

    with open(SAVE_PROG, 'r') as checkpoint:
        prev_bound = checkpoint.read()
        if prev_bound:
            lower_bound = int(prev_bound[-4:]) + 1

    upper_bound = lower_bound + 499

    start = time()

    wait = save_response(
        case_type, case_year,
        bounds=xrange(lower_bound, upper_bound + 1), gui=False
    )

    end = time()

    print "Total crawling script runtime: {0:.3f} s".format((end - start))
    print "Total downloading runtime: {0:.3f} s".format(((end - start) - wait))

    file_array = [filenames for (dirpath, dirnames, filenames)
                  in walk(HTML_DIR)][0]

    start = time()
    export(file_array, output)
    end = time()

    print "Total mining runtime: {0:.3f} s".format((end - start))

    download(output)

    with open(SAVE_PROG, 'w') as checkpoint:
        checkpoint.write(sorted(file_array)[-1][:-5])

    # rmtree(HTML_DIR)
