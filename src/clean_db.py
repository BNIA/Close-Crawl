from glob import glob
from os import path
from sys import argv

from pandas import concat, read_csv


def sort_set(dataset_name, merge=False):

    df = read_csv(dataset_name)

    df.drop_duplicates(inplace=True)

    df.sort_values(
        ["Filing Date", "Case Number", "Address"],
        ascending=[True, True, True],
        inplace=True
    )

    df["Zip Code"] = df["Zip Code"].fillna(0.0).astype(int)
    df["Zip Code"] = df["Zip Code"].replace(0, '')

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


if __name__ == '__main__':

    # sort_set(argv[-1])
    merge_sets(argv[-1])
