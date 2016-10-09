from csv import writer
from re import compile

from bs4 import BeautifulSoup

FEATURES = [
    'Case Number:',
    'Title:',
    'Appearance Date:',
    # 'Address:',
    # 'Zip Code:'
    'Business or Organization Name:'
]

white_space_pat = compile('\s+')


def scrape(html_data):
    """Scrapes the desired FEATURES

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

    soup = BeautifulSoup(html_data, 'html.parser')
    td_list = soup.findAll('tr')
    scraped_features = {key: None for key in FEATURES}

    test = []
    for tag in td_list:
        try:
            tag = tuple([strip_white_space(j) for j in tag.findAll('span')])
            if set(tag) & set(FEATURES):
                # test.append(tag)

                scraped_features[tag[0]] = tag
                test.append(tag)
        except IndexError:
            continue

    return list((test))


if __name__ == '__main__':

    from pprint import pprint

    with open('test2.html', 'r') as dummy_html:
        pprint(scrape(dummy_html))
