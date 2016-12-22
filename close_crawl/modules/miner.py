#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Miner


TODO:
    Finish docs

"""

from __future__ import absolute_import, print_function, unicode_literals

from csv import DictWriter
from json import dump, dumps, load
from os import path, walk

from bs4 import BeautifulSoup
from tqdm import trange

from .patterns import MONEY_PAT, TITLE_SPLIT_PAT, ZIP_PAT, filter_addr
from .settings import HTML_FILE, NO_CASE
from .settings import FEATURES, FIELDS, INTERNAL_FIELDS

features = [i + ':' for i in FEATURES]


def scrape(case_num, html_data):
    """Scrapes the desired features

    Args:
        html_data: <str>, source HTML

    Returns:
        scraped_features: <dict>, features scraped and mapped from content
    """

    soup = BeautifulSoup(html_data, "html.parser")
    td_list = soup.find_all("tr")

    feature_list = []
    for tag in td_list:
        try:
            tag = [j.string for j in tag.findAll("span")]
            if set(tuple(tag)) & set(features):
                try:
                    tag = [i for i in tag if "(each" not in i.lower()]
                except AttributeError:
                    continue
                feature_list.append(tag)

        except IndexError:
            continue

    try:
        # flatten multidimensional list
        feature_list = [item.replace(':', '')
                        for sublist in feature_list for item in sublist]

    except Exception as e:
        print(e, feature_list)

    return distribute(case_num, feature_list)


def distribute(case_num, feature_list):

    # break up elements with n-tuples greater than 2
    # then convert list of tuples to dict for faster lookup
    business = [
        tuple(feature_list[i:i + 2])
        for i in range(0, len(feature_list), 2)
        if any(x in feature_list[i:i + 2][0] for x in INTERNAL_FIELDS)
    ]

    feature_list = dict([
        tuple(feature_list[i:i + 2])
        for i in range(0, len(feature_list), 2)
        if feature_list[i:i + 2][0] in FEATURES
    ])

    filt = []

    for ii in range(len(business)):
        try:
            if business[ii][1].upper() == "PROPERTY ADDRESS" and \
                    business[ii + 1][0].upper() == \
                    "BUSINESS OR ORGANIZATION NAME":
                filt.append(business[ii + 1])

        except IndexError:
            print("Party Type issue at Case", feature_list["Case Number"])

    business = filt
    scraped_features = []
    temp_features = {}

    for address in business:

        str_address = filter_addr(str(address[-1]))

        temp_features["Title"] = feature_list["Title"]
        temp_features["Case Type"] = feature_list["Case Type"]
        temp_features["Case Number"] = feature_list["Case Number"]
        temp_features["Filing Date"] = feature_list["Filing Date"]

        # break up Title feature into Plaintiff and Defendant
        try:
            temp_features["Plaintiff"], temp_features["Defendant"] = \
                TITLE_SPLIT_PAT.split(temp_features["Title"])

        except ValueError:
            temp_features["Plaintiff"], temp_features["Defendant"] = \
                ('', '')

        if temp_features["Case Type"].upper() == "FORECLOSURE":
            temp_features["Case Type"] = "Mortgage"

        temp_features["Address"] = str_address if str_address else address[-1]

        temp_features["Zip Code"] = ''.join(
            ZIP_PAT.findall(address[-1])
        )

        temp_features["Partial Cost"] = ''.join(
            MONEY_PAT.findall(address[-1])
        )

        scraped_features.append(temp_features)
        temp_features = {}

    if not scraped_features:

        if not path.isfile(NO_CASE):
            with open(NO_CASE, 'w') as no_case_file:
                dump([], no_case_file)

        with open(NO_CASE, 'r+') as no_case_file:
            no_case_data = load(no_case_file)
            no_case_data.append(str(case_num[:-5]))
            no_case_file.seek(0)
            no_case_file.write(dumps(sorted(list(set(no_case_data)))))
            no_case_file.truncate()

    return scraped_features


def export(file_array, out_db, gui=False):

    dataset = []
    file_exists = path.isfile(out_db)

    case_range = trange(len(file_array), desc='Mining', leave=True) \
        if not gui else range(len(file_array))

    for file_name in case_range:
        with open(
            HTML_FILE.format(case=file_array[file_name]), 'r'
        ) as html_src:

            row = scrape(file_array[file_name], html_src.read())

            if not gui:
                case_range.set_description(
                    "Mining {}".format(file_array[file_name])
                )

            dataset.extend(row)

    with open(out_db, 'a') as csv_file:
        writer = DictWriter(
            csv_file,
            fieldnames=[col for col in FIELDS if col not in [
                'Business or Organization Name',
                'Party Type',
            ]]
        )

        if not file_exists:
            writer.writeheader()

        for row in dataset:
            writer.writerow(row)


if __name__ == '__main__':

    from sys import argv

    export(sorted(
        [filenames for (dirpath, dirnames, filenames)
         in walk(argv[1])][0]), argv[2]
    )
