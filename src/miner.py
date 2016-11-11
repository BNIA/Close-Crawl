"""scrape_content.py


"""

from csv import DictWriter
from os import path, walk
from re import compile, IGNORECASE

from bs4 import BeautifulSoup

from settings import HTML_DIR, HTML_FILE
from settings import FEATURES, FIELDS

features = [i + ':' for i in FEATURES]
TITLE_SPLIT_PAT = compile(" vs ", IGNORECASE)
ADDR_PAT = compile("\sBalto.md\s", IGNORECASE)
ZIP_PAT = compile("\d{5}")
# regex pattern to capture monetary values between $0.00 and $999,999,999.99
# punctuation insensitive
MONEY_PAT = compile('\$\d{,3},?\d{,3},?\d{,3}\.?\d{2}')


def scrape(case_type, html_data):
    """Scrapes the desired features

    input:
      html_data: <str>, source HTML

    output:
      scraped_features: <dict>, features scraped and mapped from content
    """

    soup = BeautifulSoup(html_data, "html.parser")
    td_list = soup.find_all("tr")

    if any(x in str(soup.h5).upper()
           for x in ["CASE INFORMATION", "DEFENDANT"]):

        feature_list = []
        for tag in td_list:
            try:
                tag = [j.string for j in tag.findAll("span")]
                if set(tuple(tag)) & set(features):
                    tag = [i for i in tag if "(each" not in i.lower()]
                    feature_list.append(tag)

            except IndexError:
                continue

        try:
            # flatten multidimensional list
            feature_list = [item.replace(':', '')
                            for sublist in feature_list for item in sublist]

        except Exception as e:
            print e, feature_list

        # print feature_list

        # break up elements with n-tuples greater than 2
        # then convert list of tuples to dict for faster lookup
        businesses = [
            tuple(feature_list[i:i + 2])
            for i in xrange(0, len(feature_list), 2)
            if any(
                x in feature_list[i:i + 2][0]
                for x in ['Business or Organization Name', 'Party Type']
            )
        ]

        filt = []

        for ii in xrange(len(businesses)):
            if businesses[ii][1].upper() == "PROPERTY ADDRESS" \
                    and businesses[ii + 1][0].upper() == "BUSINESS OR ORGANIZATION NAME":
                filt.append((businesses[ii], businesses[ii + 1]))

        print filt

        feature_list = dict([
            tuple(feature_list[i:i + 2])
            for i in xrange(0, len(feature_list), 2)
            if feature_list[i:i + 2][0] in FEATURES
        ])

        scraped_features = []
        temp_features = {}

        for address in businesses:

            address = ADDR_PAT.split(address[-1])

            # filters addresses not considered 'valid'
            if len(address) > 1:

                temp_features["Title"] = feature_list["Title"]
                temp_features["Case Type"] = feature_list["Case Type"]
                temp_features["Case Number"] = feature_list["Case Number"]
                temp_features["Filing Date"] = feature_list["Filing Date"]

                # break up Title feature into Plaintiff and Defendant
                try:
                    temp_features["Plaintiff"], temp_features["Defendant"] = \
                        TITLE_SPLIT_PAT.split(temp_features["Title"])

                except ValueError:
                    temp_features["Plaintiff"], temp_features["Defendant"] = \
                        ('', '')

                if temp_features["Case Type"].upper() == "FORECLOSURE":
                    temp_features["Case Type"] = "Mortgage"

                temp_features["Address"] = address[0]

                temp_features["Zip Code"] = ''.join(
                    ZIP_PAT.findall(address[-1])
                )

                temp_features["Partial Cost"] = ''.join(
                    MONEY_PAT.findall(address[-1])
                )

                scraped_features.append(temp_features)
                temp_features = {}

        return scraped_features


def export(file_array, out_db):

    dataset = []
    file_exists = path.isfile(out_db)

    for file_name in file_array:
        with open(HTML_FILE.format(case=file_name), 'r') as html_src:
            row = scrape(file_name, html_src.read())
            dataset.extend(row)

    with open(out_db, 'a') as csv_file:
        writer = DictWriter(csv_file, fieldnames=FIELDS)

        if not file_exists:
            writer.writeheader()

        for row in dataset:
            writer.writerow(row)


if __name__ == '__main__':

    file_array = [filenames for (dirpath, dirnames, filenames)
                  in walk(HTML_DIR)][0]

    out_db = 'test_out.csv'
    export(file_array, out_db)
