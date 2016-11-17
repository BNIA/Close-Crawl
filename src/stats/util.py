from os import path

from pandas import read_csv, to_datetime


def generate_stats():

    BASE_PATH = path.join(
        path.dirname(path.abspath(path.dirname(__file__))),
        "datasets", "final.csv"
    )

    df = read_csv(BASE_PATH)

    print BASE_PATH

    df["Filing Date"] = to_datetime(df["Filing Date"])
    print df.groupby(df["Filing Date"])["Case Number"].count().to_dict()


if __name__ == '__main__':

    generate_stats()
