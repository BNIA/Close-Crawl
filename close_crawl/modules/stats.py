#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""cli

"""

import argparse
from textwrap import dedent
from re import compile as re_compile

from pandas import DataFrame, read_csv, to_datetime
import seaborn as sns
import matplotlib.pyplot as plt

# from _version import __version__

space_pat = re_compile("\s{2,}")

DOC_TEMP = dedent("""\documentclass[paper=letter, fontsize=11pt]{{article}}

\\begin{{document}}

{content}

\\end{{document}}
""")


def latexify(table):

    latex_format = dedent("""
        \\begin{{tabular}}
        \\toprule
        {table}
        \\bottomrule
        \end{{tabular}}""")

    return latex_format.format(
        table=space_pat.sub(" & ", str(table)).replace('\n', "\\\\\n"))


def generate_stats(dataset):

    sns.set(style="whitegrid", font_scale=1.5)

    df = read_csv(dataset)
    df["Filing Date"] = to_datetime(df["Filing Date"])

    df_head = df.head().to_latex()
    df_count = latexify(df.count())
    df_nulls = latexify(df.isnull().sum())

    # print(latex_tablify(df_nulls))

    new_df = DataFrame(
        df.groupby(df["Filing Date"].dt.week)["Case Number"].count()
    )
    new_df.columns = ["Case Count"]
    new_df["Week"] = new_df.index

    df_describe = new_df["Case Count"].describe()

    # print(df_count)

    sns_plot = sns.factorplot(
        x="Week", y="Case Count", kind="bar", data=new_df, size=12
    )
    sns_plot.set_xticklabels(rotation=90, horizontalalignment="right")
    sns_plot.savefig("output.png")

    output_content = DOC_TEMP.format(
        content=str(df_count + df_nulls)
    ).replace("\\toprule", '').replace("\\midrule", '').replace("\\bottomrule", '')

    with open("test.tex", 'w') as test_file:
        test_file.write(output_content)


if __name__ == "__main__":

    generate_stats("output.csv")
