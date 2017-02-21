#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# does a simple statistic analysis for this thing - general

import json
import pandas as pd
import numpy as np
import datetime
import re

list_files = ['abcnews_go_com_20170215-17.json',
              'breitbart_com_20170215-17.json',
              'cnn_com_20170215-17.json',
              'dailymail_co_uk_20170215-17.json',
              'nationalenquirer_com_20170215-17.json',
              'news_bbc_co_uk_20170215-17.json',
              'rt_com_20170215-17.json',
              'telegraph_co_uk_20170215-17.json',
              'theguardian_com_20170215-17.json',
              'thesun_co_uk_20170215-17.json',
              'washingtonpost_com_20170215-17.json']

# open and read bot-list
df_bots = pd.read_csv('_scripts/_bot_list.csv')
list_bots = list(df_bots['name'])

# loop through the files
for each_file in list_files:

    file_name = re.sub('_20170215-17.json','',each_file)

    # open the file
    with open('merged/%s' % each_file) as fr:
        json_data = json.loads(fr.read())

    list_out_tup = []

    for json_entry in json_data:

        # make date human readable
        form_date = datetime.date.fromtimestamp(json_entry['data']['created'])
        str_date = form_date.strftime('%Y-%m-%d')

        # create output date
        tup_data = (
                    str_date,
                    json_entry['data']['score'],
                    json_entry['data']['title'],
                    json_entry['data']['subreddit'],
                    json_entry['data']['subreddit_id'],
                    json_entry['data']['author'],
                    json_entry['data']['url'],
                    json_entry['data']['id'],
                    )

        # check if its in the list of bots
        if json_entry['data']['subreddit'] not in list_bots:
            list_out_tup.append(tup_data)
        else:
            pass

    # the column names
    list_cols = [
                 'date',
                 'score',
                 'title',
                 'sub',
                 'sub_id',
                 'author',
                 'url',
                 'url_id',
                 ]

    # create output tupple
    df_out = pd.DataFrame(list_out_tup)

    df_out.columns = list_cols

    df_out.to_csv('analysis/csv/%s.csv' % file_name, index=None)
