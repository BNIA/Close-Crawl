from glob import glob
from os import path
from re import compile
from re import IGNORECASE
from string import punctuation
from sys import argv

from pandas import concat, read_csv

from settings import FINAL_DATASET


def load(dataset_name):

    df = read_csv(dataset_name)

    df.drop_duplicates(inplace=True)

    df.sort_values(
        ["Filing Date", "Case Number", "Address"],
        ascending=[True, True, True],
        inplace=True
    )

    df["Zip Code"] = df["Zip Code"].fillna(0.0).astype(int)
    df["Zip Code"] = df["Zip Code"].replace(0, '')

    return df


def download(dataset_name):

    df = load(dataset_name)

    df.to_csv(dataset_name, index=False)


def merge_sets(dataset_name):

    BASE_PATH = path.abspath(
        path.join(path.dirname(__file__), "datasets", "scraped")
    )

    DATASETS = glob(BASE_PATH + "/*.csv")

    all_df = []
    for file_ in DATASETS:
        sub_df = read_csv(file_, index_col=None, header=0)
        all_df.append(sub_df)
    df = concat(all_df)

    df.drop_duplicates(inplace=True)

    df.sort_values(
        ["Filing Date", "Case Number", "Address"],
        ascending=[True, True, True],
        inplace=True
    )

    df["Zip Code"] = df["Zip Code"].fillna(0.0).astype(int)
    df["Zip Code"] = df["Zip Code"].replace(0, '')

    df.to_csv(dataset_name, index=False)


street_address = compile(
    '(\d{1,4} [\w\s]{1,20}'
    '(?:st(reet)?|ln|lane|ave(nue)?|r(?:oa)?d'
    '|highway|hwy|sq(uare)?|tr(?:ai)l|dr(?:ive)?'
    '|c(?:our)?t|parkway|pkwy|cir(cle)?'
    '|boulevard|blvd|pl(?:ace)?|'
    'ter(?:race)?)\W?(?=\s|$))', IGNORECASE)

punctuation.replace('#', '')


def clean_addr(df):

    dirty_addr = []

    def filter_addr(address):

        try:
            return ''.join(
                street_address.search(
                    address.translate(None, punctuation)).group(0)
            )

        except AttributeError:
            return ''

    for i in df["Address"]:
        if not filter_addr(i):
            dirty_addr.append(i)

    print (dirty_addr)


if __name__ == '__main__':

    # sort_set(argv[-1])
    # merge_sets(argv[-1])

    df = load(FINAL_DATASET)
    clean_addr(df)
