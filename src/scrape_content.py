from csv import DictWriter
from os.path import isfile
from re import compile

from bs4 import BeautifulSoup

FEATURES = [
    'Case Number',
    'Title',
    'Filing Date:',
    'Address',
    'Zip Code',
    # 'Business or Organization Name:'
]

FEATURES = [i.upper() + ':' for i in FEATURES]

white_space_pat = compile('\s+')


def strip_html(html_data):

    return html_data.upper().split('<HR>')


def scrape(html_data):
    """Scrapes the desired features

    input:
      html_data: <str>, source HTML

    output:
      scraped_features: <dict>, features scraped and mapped from content
    """

    def strip_white_space(element):
        """Strips out excess whitespace

        input:
          element: <bs4.element.Tag>, element tag from HTML

        output:
          <str>, stripped elements
        """
        return white_space_pat.sub(' ', str(element.string))

    stripped_html = strip_html(html_data)
    html_data = stripped_html[0] + stripped_html[2]

    soup = BeautifulSoup(html_data, 'html.parser')
    td_list = soup.find_all('tr')

    if any(x in str(soup.h5).upper()
           for x in ['CASE INFORMATION', 'DEFENDANT']):

        feature_list = []
        for tag in td_list:
            try:
                tag = tuple([strip_white_space(j)
                             for j in tag.findAll('span')])
                if set(tag) & set(FEATURES):
                    feature_list.append(tag)

            except IndexError:
                continue

        # flatten multidimensional list
        feature_list = [item for sublist in feature_list for item in sublist]

        # break up elements with n-tuples greater than 2
        feature_list = [
            tuple(feature_list[i:i + 2])
            for i in xrange(0, len(feature_list), 2)
            if feature_list[i:i + 2][0] in FEATURES
        ]

        return dict(feature_list)


if __name__ == '__main__':

    test = 'test_out.csv'

    file_exists = isfile(test)

    with open('test_pages/test3.html', 'r') as dummy_html:
        row = scrape(dummy_html.read())

        with open(test, 'a') as csvfile:
            fieldnames = row.keys()
            writer = DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow(row)
