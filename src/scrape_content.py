# from csv import writer
from re import compile

from bs4 import BeautifulSoup

FEATURES = [
    'Case Number:',
    'Title:',
    'Filing Date:',
    'Address:',
    'Zip Code:',
    'Business or Organization Name:'
]

white_space_pat = compile('\s+')
address_pat = compile('\w+.*\d{5}')


# def strip_html(html_data):


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

    def strip_address(pair):

        # return pair[0] == 'Business or Organization Name:' and
        # address_pat.findall(pair[-1])
        return pair[0] == 'Business or Organization Name:' and pair[-1].startswith()

    soup = BeautifulSoup(html_data, 'html.parser')
    td_list = soup.find_all('tr')

    test = []
    for tag in td_list:
        try:
            tag = tuple([strip_white_space(j) for j in tag.findAll('span')])
            if set(tag) & set(FEATURES):
                test.append(tag)

        except IndexError:
            continue

    # flatten multidimensional array into single dimensional
    li = [item for sublist in test for item in sublist]

    li = [
        tuple(li[i:i + 2]) for i in xrange(0, len(li), 2)
        if li[i:i + 2][0] in FEATURES
    ]

    address = []
    business = []

    for i in li:
        if i[0] == 'Address:':
            address.append(i)
        elif i[0] == 'Business or Organization Name:':
            business.append(i)

    return address, business
    # return {
    #     li[i:i + 2][0]: li[i:i + 2][-1] for i in xrange(0, len(li), 2)
    #     if li[i:i + 2][0] in FEATURES
    #     # if li[i:i + 2][0] in FEATURES or strip_address(li[i:i + 2])
    # }


if __name__ == '__main__':

    from pprint import pprint

    with open('test_pages/test1.html', 'r') as dummy_html:
        pprint(scrape(dummy_html))
