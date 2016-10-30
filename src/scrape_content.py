"""scrape_content.py


"""

from csv import DictWriter
from os import path, walk
from re import compile, IGNORECASE

from bs4 import BeautifulSoup

from settings import FEATURES, HTML_DIR, HTML_FILE

features = [i + ':' for i in FEATURES]
TITLE_SPLIT_PAT = compile(" vs ", IGNORECASE)


def scrape(case_type, html_data):
    """Scrapes the desired features

    input:
      html_data: <str>, source HTML

    output:
      <dict>, features scraped and mapped from content
    """

    soup = BeautifulSoup(html_data, "html.parser")
    td_list = soup.find_all("tr")

    if any(x in str(soup.h5).upper()
           for x in ["CASE INFORMATION", "DEFENDANT"]):

        feature_list = []
        for tag in td_list:
            try:
                tag = tuple([j.string for j in tag.findAll("span")])
                if set(tag) & set(features):
                    feature_list.append(tag)

            except IndexError:
                continue

        # flatten multidimensional list
        feature_list = [item.replace(':', '')
                        for sublist in feature_list for item in sublist]

        # break up elements with n-tuples greater than 2
        # then convert list of tuples to dict for faster lookup
        feature_list = dict([
            tuple(feature_list[i:i + 2])
            for i in xrange(0, len(feature_list), 2)
            if feature_list[i:i + 2][0] in FEATURES
        ])

        # break up Title feature into Plaintiff and Defendant
        feature_list["Plaintiff"], feature_list["Defendant"] = \
            TITLE_SPLIT_PAT.split(feature_list["Title"])

        feature_list["Case Type"] = \
            "Mortgage" if 'O' in case_type else "Tax sale"

        return feature_list


def export(file_array, out_db):

    dataset = []
    file_exists = path.isfile(out_db)

    for file_name in file_array:
        with open(HTML_FILE.format(case=file_name), 'r') as html_src:
            row = scrape(file_name, html_src.read())
            dataset.append(row)

    with open(out_db, 'a') as csv_file:
        writer = DictWriter(csv_file, fieldnames=FEATURES)

        if not file_exists:
            writer.writeheader()

        for row in dataset:
            writer.writerow(row)


if __name__ == '__main__':

    file_array = [filenames for (dirpath, dirnames, filenames)
                  in walk(HTML_DIR)][0]

    out_db = 'test_out.csv'
    export(file_array, out_db)
