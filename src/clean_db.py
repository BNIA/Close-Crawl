from pandas import read_csv


def sort_set(dataset_name):

    df = read_csv(dataset_name)

    df.sort_values(
        ["Filing Date", "Case Number", "Address"],
        ascending=[True, True, True],
        inplace=True
    )

    # TODO: Handle missing values
    # df.fillna("-", inplace=True)

    df["Zip Code"] = df["Zip Code"].fillna(0.0).astype(int)
    df["Zip Code"] = df["Zip Code"].replace(0, '')
    df.to_csv(dataset_name, index=False)


if __name__ == '__main__':

    dataset_name = "test_out.csv"
    sort_set(dataset_name)
