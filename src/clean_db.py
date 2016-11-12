from re import compile
from re import IGNORECASE
from string import punctuation
from sys import argv

from pandas import read_csv

STREET_ADDR_PAT = u'\d{1,4} [\w\s]{1,20}(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|driveway|dr|court|ct|parkway|pkwy|circle|cir|boulevard|blvd|pl|terrace)\W?(?=\s|$)'
street_address = compile(STREET_ADDR_PAT, IGNORECASE)
punctuation.replace('#', '')


def clean_addr(address):

    return ''.join(
        street_address.findall(address.translate(None, punctuation))
    )


def sort_set(dataset_name):

    df = read_csv(dataset_name)

    df.drop_duplicates(inplace=True)

    df.sort_values(
        ["Filing Date", "Case Number", "Address"],
        ascending=[True, True, True],
        inplace=True
    )

    df["Zip Code"] = df["Zip Code"].fillna(0.0).astype(int)
    df["Zip Code"] = df["Zip Code"].replace(0, '')

    # df["Address"] = df["Address"].apply(
    #     lambda i: clean_addr(i) if clean_addr(i) else i
    # )

    df.to_csv(dataset_name, index=False)


if __name__ == '__main__':

    dataset_name = argv[-1]
    sort_set(dataset_name)
