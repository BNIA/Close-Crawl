from pandas import concat, DataFrame, read_csv, to_datetime
from numpy import NaN

from patterns import filter_addr
from patterns import NULL_ADDR, STRIP_ADDR, punctuation
from settings import FINAL_DATASET


class CleanedData():

    def __init__(self, dataset):

        self.df = self.prettify(read_csv(dataset))

        self.columns = list(self.df)

        self.clean_df = []

    def prettify(self, df, internal=True):

        df.drop_duplicates(inplace=True, keep=False)
        df["Filing Date"] = to_datetime(df["Filing Date"])

        df.sort_values(
            ["Filing Date", "Case Number", "Address"],
            ascending=[True, True, True],
            inplace=True
        )

        if internal:
            df["Zip Code"] = df["Zip Code"].fillna(0.0).astype(int)
            df["Zip Code"] = df["Zip Code"].replace(0, '')

        return df

    def download(self, output_name):

        self.clean_df.to_csv(output_name, index=False)

    def clean_addr(self):

        def clean_string(addr):

            if not filter_addr(addr):
                full_str = NULL_ADDR.sub('', addr)
                if full_str:
                    return STRIP_ADDR.sub(
                        '', addr).translate(None, punctuation).strip()

            return addr

        self.df["Address"] = self.df["Address"].apply(
            lambda x: clean_string(x)
        )
        self.df["Address"] = self.df["Address"].apply(
            lambda x: NULL_ADDR.sub('', x)
        )

        self.df["Zip Code"] = self.df["Zip Code"].replace('', NaN)
        self.df["Address"] = self.df["Address"].replace('', NaN)

    def mergeable(self, bool_vec):

        def sum_col():
            return [sum(x) for x in zip(*bool_vec)]

        def bool_pat(row):
            return set(row[-3:]) == set([1]) and set(row[:-3]) != set([1])

        flat_list = sum_col()
        return True if bool_pat(flat_list) else False

    def combine_rows(self, row):

        def filter_tuple(col):

            def isNaN(num):
                return num != num

            for i in set(col):
                if not isNaN(i):
                    return i

        return [filter_tuple(x) for x in zip(*row)]

    def merge_nulls(self):

        origin_df = self.df.dropna()
        null_df = self.df[self.df.isnull().any(axis=1)]
        bool_df = null_df.notnull()

        new_df = []

        for i in null_df["Case Number"].unique():
            yo = bool_df[null_df["Case Number"] == i]
            new_row = null_df[null_df["Case Number"] == i]

            if self.mergeable(yo.values):
                new_row = self.combine_rows(new_row.values.tolist())
            else:
                new_row = new_row.values.tolist()[0]

            new_df.append(
                {
                    feature: value
                    for feature, value in zip(self.columns, new_row)
                }
            )

        self.clean_df = concat(
            [origin_df, DataFrame(new_df)]
        ).reset_index(drop=True)

        self.clean_df = self.prettify(
            self.clean_df[self.columns], internal=False
        )


if __name__ == '__main__':

    df_obj = CleanedData(
        FINAL_DATASET.format(dir="2015", year="2015")
    )

    df_obj.clean_addr()
    df_obj.merge_nulls()
    df_obj.download("2015_clean.csv")
