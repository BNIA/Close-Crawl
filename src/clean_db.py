from glob import glob
from os import path
from sys import argv

from pandas import concat, read_csv

from patterns import filter_addr
from patterns import NULL_ADDR, STRIP_ADDR, punctuation
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


def clean_addr(df):

    def cleen(addr):

        if not filter_addr(addr):
            full_str = NULL_ADDR.sub('', addr)
            if full_str:
                return STRIP_ADDR.sub(
                    '', addr).translate(None, punctuation).strip()

        return addr

    df["Address"] = df["Address"].apply(lambda x: cleen(x))
    df["Address"] = df["Address"].apply(lambda x: NULL_ADDR.sub('', x))

    # print df.groupby("Case Number")["Partial Cost"].apply(
    #     lambda x: x.notnull()).head()[260:280]
    print df['Partial Cost'].head(280)
    print df['Partial Cost'].where(df['Partial Cost'].notnull(),
                                   df['Address'])[260:280]

    df.to_csv('testtest.csv', index=False)


if __name__ == '__main__':

    # download(argv[-1])

    df = load(FINAL_DATASET.format(dir="2014", year="2014"))
    clean_addr(df)
