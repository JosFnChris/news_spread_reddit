# Hi Fred, you can add your stuff here, and we can work on it together.
# this works to create stats -such as mean, stdev for files in specific folder... let me know what you think - worked for me
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 13:21:17 2017

@author: Fred
"""
#Libraries needed
import json
import csv
import pandas as pd
import numpy as np

#files in folder -needed with extension as bbc is different
list_of_files =['breitbart_com',
               'cnn_com',
               'news_bbc_co_uk',
               'rt_com',
               'washingtonpost_com']


# load the bot file and turn into list
df_bots = pd.read_csv('_scripts/_bot_list.csv')
list_bots = list(df_bots['name'])


for item in list_of_files:
    
    print('%s Hello' % item)


    # open file
    with open('merged/%s_20170215-17.json' % item)as anything:
        json_data = json.loads(anything.read())
        
    list_of_tuples = []

    # the json is a list of json entries
    for item3 in json_data:
        var_author = item3['data']['author']
        var_score = item3['data']['score']
        var_title = item3['data']['title']
        var_sub = item3['data']['subreddit']
    
        tuple_data1 = (var_author,
              var_score,
              var_title,
              var_sub)
        
        # get rid of the bots
        if var_sub not in list_bots:
            list_of_tuples.append(tuple_data1)
        else:
            pass
    
    df_data= pd.DataFrame(list_of_tuples)
    
    # add column titles
    df_data.columns= ['author','score','title','subt']
    
    #statistics - looking at authors occurences
    sub_distrib = df_data.subt.value_counts()
    sub_distrib.to_csv('data/_tables/%s_sub_distrib.csv' % item)
    
    list_of_data = []
    
    #calculate table with mean and std deviation and n
    for item2 in sub_distrib.index:
        var_1=df_data.loc[df_data['subt'] == item2 ].subt.count()
        var_3=np.std(df_data.loc[df_data['subt'] == item2 ].score)
        var_2=np.average(df_data.loc[df_data['subt'] == item2].score)
    
        tuple_data = (item2,
              var_1,
              var_2,
              var_3)
        
        list_of_data.append(tuple_data)
    
    df_stats = pd.DataFrame(list_of_data)
    # add column titles
    df_stats.columns = ['Subreddit','n','mean','std']
    df_stats.to_csv('data/_tables/%s_stats.csv' % item)
    
print('all done')
