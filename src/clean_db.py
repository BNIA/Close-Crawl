from sys import argv

from pandas import read_csv


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

    sort_set(argv[-1])
