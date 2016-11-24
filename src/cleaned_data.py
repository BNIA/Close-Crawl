#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""CleanedData

This module implements post-scraping cleaning processes on the raw initial
dataset. Processes include stripping excess strings off Address values,
removing Zip Code and Partial Cost values mislabeled as Address, and merging
rows containing blank values in alternating features.

The script works as an internal module for Close Crawl, but can be executed
as a standalone to manually process datasets:

    $ python cleaned_data.py <path/to/old/dataset> <path/of/new/dataset>

"""

from __future__ import absolute_import, unicode_literals

from pandas import DataFrame, concat, read_csv, to_datetime

from patterns import NULL_ADDR, STRIP_ADDR, filter_addr, punctuation


class CleanedData:

    def __init__(self, path):
        """Constructor for CleanedData

        Args:
            path (`str`): path to input CSV dataset

        Attributes:
            df (`pandas.core.frame.DataFrame`): initial DataFrame
            columns (`list` of `str`): columns of the DataFrame
            clean_df (`pandas.core.frame.DataFrame`): final DataFrame to be
                outputted
        """

        self.df = self.__prettify(read_csv(path))

        self.columns = list(self.df)
        self.clean_df = []

    def __prettify(self, df, internal=True):
        """Drops duplicates, sorts and fills missing values in the DataFrame
        to make it manageable.

        Args:
            df (`pandas.core.frame.DataFrame`): DataFrame to be managed
            internal (`bool`, optional): flag for determining state of
                DataFrame

        Returns:
            df (`pandas.core.frame.DataFrame`): organized DataFrame
        """

        df.drop_duplicates(inplace=True, keep=False)
        df["Filing Date"] = to_datetime(df["Filing Date"])

        df.sort_values(
            ["Filing Date", "Case Number", "Address"],
            ascending=[True] * 3,
            inplace=True
        )

        if internal:
            df["Zip Code"] = df["Zip Code"].fillna(0.0).astype(int)
            df["Zip Code"] = df["Zip Code"].replace(0, '')

        return df

    def clean_addr(self):

        def clean_string(addr):

            if not filter_addr(addr):

                if NULL_ADDR.sub('', addr):
                    return unicode(
                        STRIP_ADDR.sub('', addr)
                    ).translate(
                        {ord(c): None for c in punctuation}
                    ).strip()

            return addr

        self.df["Address"] = self.df["Address"].apply(
            lambda x: clean_string(x)
        )
        self.df["Address"] = self.df["Address"].apply(
            lambda x: NULL_ADDR.sub('', x)
        )

        self.df["Zip Code"] = self.df["Zip Code"].replace('', float('nan'))
        self.df["Address"] = self.df["Address"].replace('', float('nan'))

    def __combine_rows(self, row):

        def __filter_tuple(col):

            for value in set(col):
                if value == value:  # equivalent to value != nan
                    return value

        return [__filter_tuple(x) for x in zip(*row)]

    def __mergeable(self, bool_vec):

        def __sum_col():
            return [sum(x) for x in zip(*bool_vec)]

        def __bool_pat(row):
            return set(row[-3:]) == set([1]) and set(row[:-3]) != set([1])

        return True if __bool_pat(__sum_col()) else False

    def merge_nulls(self):

        origin_df = self.df.dropna()
        null_df = self.df[self.df.isnull().any(axis=1)]
        bool_df = null_df.notnull()

        new_df = []

        for i in null_df["Case Number"].unique():
            yo = bool_df[null_df["Case Number"] == i]
            new_row = null_df[null_df["Case Number"] == i]

            if self.__mergeable(yo.values):
                new_row = self.__combine_rows(new_row.values.tolist())
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

        self.clean_df = self.__prettify(
            self.clean_df[self.columns], internal=False
        )

    def init_clean(self):

        self.clean_addr()
        self.merge_nulls()

    def download(self, output_name):

        self.clean_df.to_csv(output_name, index=False)


if __name__ == '__main__':

    from sys import argv

    df_obj = CleanedData(argv[1])
    df_obj.init_clean()
    df_obj.download(argv[2])
