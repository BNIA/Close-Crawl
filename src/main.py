from os import walk
from shutil import rmtree

from settings import CASE_PAT
from settings import HTML_DIR, SAVE_PROG
from scrape_content import export
from spider import save_response

if __name__ == '__main__':

    output = 'mortgage_2015.csv'

    lower_bound = 0

    with open(SAVE_PROG, 'r') as checkpoint:
        lower_bound = int(checkpoint.read()[-4:])

    upper_bound = 551
    case_type = 'O'
    case_year = '15'

    save_response(case_type, case_year, xrange(lower_bound, upper_bound))

    file_array = [filenames for (dirpath, dirnames, filenames)
                  in walk(HTML_DIR)][0]

    export(file_array, output)

    with open(SAVE_PROG, 'w') as checkpoint:
        checkpoint.write(
            CASE_PAT.format(type=case_type, year=case_year, num=upper_bound)
        )

    rmtree(HTML_DIR)
