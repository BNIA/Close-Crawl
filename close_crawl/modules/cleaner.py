#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Cleaner

This module implements post-scraping cleaning processes on the raw initial
dataset. Processes include stripping excess strings off Address values,
removing Zip Code and Partial Cost values mislabeled as Address, and merging
rows containing blank values in alternating features.

The script works as an internal module for Close Crawl, but can be executed
as a standalone to manually process datasets:

    $ python cleaner.py <path/to/old/dataset> <path/of/new/dataset>

"""

from __future__ import absolute_import, print_function, unicode_literals

from pandas import DataFrame, concat, read_csv, to_datetime

from .patterns import NULL_ADDR, STRIP_ADDR, filter_addr, punctuation


class Cleaner(object):
    """Class object for cleaning the raw dataset extracted after the initial
    scraping
    """

    def __init__(self, path):
        """Constructor for Cleaner

        Args:
            path (`str`): path to input CSV dataset

        Attributes:
            df (`pandas.core.frame.DataFrame`): initial DataFrame
            columns (`list` of `str`): columns of the DataFrame
            clean_df (`pandas.core.frame.DataFrame`): final DataFrame to be
                outputted
        """

        self.df = self.prettify(read_csv(path))

        self.columns = list(self.df)
        self.clean_df = []

    @staticmethod
    def prettify(df, internal=True):
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
        """Cleans excess strings off Address values and removes Zip Code and
        Partial Cost values mislabeled as Address.

        Args:
            None

        Returns:
            None
        """

        def clean_string(addr):
            """Appplies regular expressions and other filters on Address
            values

            Args:
                addr (`str`): Address value to be filtered

            Returns:
                addr (`str`): filtered Address value
            """

            # if value does not match the street_address pattern
            if not filter_addr(addr):  # patterns.filter_addr

                if NULL_ADDR.sub('', addr):  # value may contain valid Address
                    return unicode(
                        STRIP_ADDR.sub(
                            '', addr)  # strip off Zip Code and Partial Cost
                    ).translate(
                        {ord(c): None for c in punctuation}
                    ).strip()  # strip off punctuations

            return addr

        print("Cleaning addresses...")

        self.df["Address"] = self.df["Address"].apply(
            lambda x: clean_string(x)
        )
        self.df["Address"] = self.df["Address"].apply(
            lambda x: NULL_ADDR.sub('', x)
        )

        # replace empty string values with NULL
        self.df["Zip Code"] = self.df["Zip Code"].replace('', float('nan'))
        self.df["Address"] = self.df["Address"].replace('', float('nan'))

    @staticmethod
    def combine_rows(row):
        """Merges rows after filtering out common values

        Args:
            row (`list` of `list` of `str`): groupby("Case Number") rows

        Returns:
            (`list` of `str`): merged row
        """

        def __filter_tuple(col):
            """Filters common values from rows

            Args:
                col (`tuple` of `str`): values per column

            Returns:
                value (`str`): common value found per mergeable rows
            """

            for value in set(col):
                if value == value:  # equivalent to value != NaN
                    return value

        return [__filter_tuple(x) for x in zip(*row)]

    @staticmethod
    def mergeable(bool_vec):
        """Determines if groupby("Case Number") rows are mergeable

        Example:
            bool_vec = [
                [True, True, True, True, True, True, False, True, True],
                [True, True, True, True, True, True, True, False, False],
                [True, True, True, True, True, True, False, False, False]
            ]

            __sum_col(bool_vec) -> [3, 3, 3, 3, 3, 3, 1, 1, 1]

            __bool_pat(__sum_col(bool_vec)) -> True

        Args:
            bool_vec (`list` of `bool`): represents non-NULL values

        Returns:
            (`bool`): True if rows are mergeable
        """

        def __sum_col():
            """Sums columns

            Args:
                None

            Returns:
                (`list` of `int`): sum of columns
            """
            return [sum(x) for x in zip(*bool_vec)]

        def __bool_pat(row):
            """Determines mergeability

            Args:
                None

            Returns:
                (`bool`): True if rows are mergeable
            """
            return set(row[-3:]) == set([1]) and set(row[:-3]) != set([1])

        return True if __bool_pat(__sum_col()) else False

    def merge_nulls(self):
        """Splits DataFrames into those with NULL values to be merged, and then
        later merged with the original DataFrame

        Args:
            None

        Returns:
            None
        """

        print("Merging rows...")

        # filter out rows with any NULL values
        origin_df = self.df.dropna()

        # filter out rows only with NULL values
        null_df = self.df[self.df.isnull().any(axis=1)]

        # boolean representation of the DataFrame with NULL values
        bool_df = null_df.notnull()

        # (`list` of `dict` of `str` : `str`) to be converted to a DataFrame
        new_df = []

        for i in null_df["Case Number"].unique():
            bool_row = bool_df[null_df["Case Number"] == i]
            new_row = null_df[null_df["Case Number"] == i]

            # if the rows are mergeable, combine them
            if self.mergeable(bool_row.values):
                new_row = self.combine_rows(new_row.values.tolist())

                new_df.append(
                    {
                        feature: value
                        for feature, value in zip(self.columns, new_row)
                    }
                )

            # else, treat them individually
            else:
                new_row = new_row.values.tolist()

                for row in new_row:
                    new_df.append(
                        {
                            feature: value
                            for feature, value in zip(self.columns, row)
                        }
                    )

        # merge the DataFrames back
        self.clean_df = concat(
            [origin_df, DataFrame(new_df)]
        ).reset_index(drop=True)

        # prettify the new DataFrame
        self.clean_df = self.prettify(
            self.clean_df[self.columns], internal=False
        )

    def init_clean(self):
        """Initializes cleaning process

        Args:
            None

        Returns:
            None
        """

        self.clean_addr()
        self.merge_nulls()

    def download(self, output_name):
        """Downloads the cleaned and manipulated DataFrame into a CSV file

        Args:
            output_name (`str`): path of the new output file

        Returns:
            None
        """
        self.clean_df.to_csv(output_name, index=False)


if __name__ == '__main__':

    df_obj = Cleaner("output.csv")

    df_obj.init_clean()
    df_obj.download("../meh/clean.csv")
