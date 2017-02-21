#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# 

import pandas as pd
import numpy as np
import re


list_files = ['abcnews_go_com.csv',
              'breitbart_com.csv',
              'cnn_com.csv',
              'dailymail_co_uk.csv',
              'nationalenquirer_com.csv',
              'news_bbc_co_uk.csv',
              'rt_com.csv',
              'telegraph_co_uk.csv',
              'theguardian_com.csv',
              'thesun_co_uk.csv',
              'washingtonpost_com.csv']


list_t1_out = []

# loop through the files
for each_file in list_files:

    # get the domain name
    domain_name = re.sub('\.csv','',each_file)

    # read the dataframe
    df_data = pd.read_csv('analysis/csv/%s' % each_file)

    int_aut = len(set(list(df_data['author'])))
    int_all = len(df_data)
    int_sub = len(set(list(df_data['sub'])))
    int_url = len(set(list(df_data['url'])))

    list_t1_out.append((domain_name, int_all, int_aut, int_sub, int_url))

    list_each_sub = []

    # move on to the second table
    for each_sub in list(set(df_data['sub'])):

        # each sub
        df_sub = df_data[df_data['sub']==each_sub]

        num_total = len(df_sub)
        num_unique = len(set(df_sub['url']))
        av_score = sum(df_sub['score'])/len(df_sub)
        min_score = min(df_sub['score'])
        max_score = max(df_sub['score'])
        std_score = np.std(df_sub['score'])

        # create the data tup and append
        tup_dom_out = (each_sub,
                       num_total,
                       num_unique,
                       av_score,
                       min_score,
                       max_score,
                       std_score)
        
        list_each_sub.append(tup_dom_out)

    df_t2 = pd.DataFrame(list_each_sub)
    
    df_t2.columns = ['sub','posts','unique','av','min','max','std']

    df_t2 = df_t2.sort_values(['posts','unique'], ascending=False)

    df_t2.to_csv('analysis/t2/%s_t2.csv' % each_file, index=None)

df_t1 = pd.DataFrame(list_t1_out)
df_t1.columns = ['dom', 'total','auth', 'sub', 'url']

# save the dataframe
df_t1.to_csv('analysis/overview.csv', index=None)

