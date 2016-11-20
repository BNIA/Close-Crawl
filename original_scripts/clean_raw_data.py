from collections import deque
from string import punctuation
from re import compile, IGNORECASE

file_name = "fwdforeclosuredatafiles/2015_Raw_Data_Court_FF.txt"

street_address = compile(
    '(\d{1,4} [\w\s]{1,20}'
    '(?:st(reet)?|ln|lane|ave(nue)?|r(?:oa)?d'
    '|highway|hwy|sq(uare)?|tr(?:ai)l|dr(?:ive)?'
    '|c(?:our)?t|parkway|pkwy|cir(cle)?'
    '|boulevard|blvd|pl(?:ace)?|'
    'ter(?:race)?)\W?(?=\s|$))', IGNORECASE)

punctuation = punctuation.replace('#', '')

ZIP_PAT = compile("2\d{4}")
# regex pattern to capture monetary values between $0.00 and $999,999,999.99
# punctuation insensitive
MONEY_PAT = compile('\$\d{,3},?\d{,3},?\d{,3}\.?\d{2}')


def clean_addr(address):

    try:
        return ''.join(
            street_address.search(
                address.translate(None, punctuation)).group(0)
        )

    except AttributeError:
        return address


if __name__ == '__main__':

    dataset = {}

    dates = []
    case_nums = []
    titles = []
    addresses = []
    zips = []
    costs = []

    works = 0

    with open(file_name, 'r') as input_file:
        for j in input_file:
            row = deque(j.split())

            dates.append(row.popleft())

            case_nums.append(row.popleft().replace('-', ''))

            curtail = 1

            zip_code = ZIP_PAT.findall(row[-1])
            if zip_code:
                zips.append(zip_code)
                curtail += 1

            cost = MONEY_PAT.findall(row[-1])
            if cost:
                costs.append(cost)
                curtail += 1

            row = ' '.join(list(row)[:-curtail]).replace('  ', '')

            address = clean_addr(row)
            addresses.append(address)

            # titles.append(row.replace(address, ''))
            titles.append(row.split(address))

        dataset['date'] = dates
        dataset['case_nums'] = case_nums
        dataset['zip'] = zips
        dataset['cost'] = costs
        dataset['address'] = addresses
        dataset['title'] = titles

    print len(dataset['date'])
    print len(dataset['case_nums'])
    print len(dataset['zip'])
    print len(dataset['cost'])
    print len(dataset['address'])
    print (dataset['title'])
